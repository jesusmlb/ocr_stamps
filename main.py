# Import necessary libraries
import PIL.Image
from PIL import Image
import cv2
import easyocr as ocr
import numpy as np
import pandas as pd
import re
import streamlit as st
from io import StringIO

# Streamlit file uploader to choose an image file
uploaded_file = st.file_uploader("Choose a file")

with st.spinner('Wait for it... We are working very hard on your file...'):
    
    # Check if a file is uploaded
    if uploaded_file is not None:
        # Read file as bytes
        bytes_data = uploaded_file.getvalue()
        nparr = np.frombuffer(bytes_data, np.uint8)
        
        # Decode image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Initialize OCR reader for English language
        reader = ocr.Reader(['en'])
        
        # Image processing steps
        kernel = np.ones((7,7), np.uint8)
        blur = cv2.GaussianBlur(img,(5,5),0)
        dilation = cv2.dilate(blur, kernel, iterations=1)
        
        # Perform OCR on the processed image
        results = reader.readtext(dilation)
    
        # Extract text from OCR results
        text = ""
        for _ in range(len(results)):
            text += results[_][1] + " " 
    
        # Define a regex pattern for extracting relevant information
        pattern = r'(.+?)(?=(?:\d{3} \w\d{2}|Nos\.|\d{4}|$))(?:\.20|20)?'
        
        # Use regex to match the pattern and extract information
        matches = re.findall(pattern, text)
    
        # Group extracted items by year
        grouped_items = {}
        current_year = None
    
        # Iterate through the matches and group by year
        for item in matches:
            if re.match(r'^\d{4}', item):
                current_year = item
                grouped_items[current_year] = []
            elif current_year is not None:
                grouped_items[current_year].append(item)
    
        # Initialize data list for creating a DataFrame
        data = []
    
        # Iterate through grouped items and apply different regex patterns
        for year, items in grouped_items.items():
            for _ in items:
                # Define regex patterns for different cases
                pattern = r'(\d+) (\w+) (\d+ \|) (.*?)(?=\s*\d+\s+\d+) (\d+) (\d+)'
                pattern1 = r'(\d+) (\w+) ([\d.]+) (.*?) ([\d.]+) ([\d.]+)'
                pattern2 = r'(\d+) (\w+) (.*?) ([\d.]+) ([\d.]+)'
                pattern3 = r'(\d+) (\w+) ([\w.]+) (.*?)(?:(?:on (\d+))|([\d.]+)) ([\d.]+)'
                pattern4 = r'(\d+) (\w+) (\S+) (.*?) (\d+) (\d+)'
    
                # Apply regex patterns and append data to the list
                if re.match(pattern, _, re.DOTALL):
                    match = re.match(pattern, _, re.DOTALL)
                    data.append([match.group(1), year[0:4], match.group(2), match.group(3), match.group(4), match.group(5), match.group(6), year[-9:-1]])
                elif re.match(pattern1, _, re.DOTALL):
                    match = re.match(pattern1, _, re.DOTALL)
                    data.append([match.group(1), year[0:4], match.group(2), match.group(4), match.group(5), match.group(6), year[-14:-1]])
                elif re.match(pattern4, _, re.DOTALL):
                    match = re.match(pattern4, _, re.DOTALL)
                    data.append([match.group(1), year[0:4], match.group(2), match.group(3), match.group(4), match.group(5), match.group(6), year[-9:-1]])       
                elif re.match(pattern2, _, re.DOTALL):
                    match = re.match(pattern2, _, re.DOTALL)
                    data.append([match.group(1), year[0:4], match.group(2), match.group(3), match.group(4), match.group(5), year[-9:-1]])
                elif re.match(pattern3, _, re.DOTALL):
                    match = re.match(pattern3, _, re.DOTALL)
                    data.append([match.group(1), year[0:4], match.group(2), match.group(3), match.group(4), match.group(5), year[-9:-1]])
                else:
                    data.append([_, '', '', '', '', ''])        
    
        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=['Stock #', 'Year', 'Illustration #', 'Denomination', 'Description', 'New or Unused Value', 'Used Value', 'Notes'])
        
        # Display the DataFrame using Streamlit
        st.write(df)
        st.success('There you go! We have successfully extracted the information from the file!')
