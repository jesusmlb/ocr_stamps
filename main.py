import PIL.Image
from PIL import Image
import cv2
import easyocr as ocr
import numpy as np
import pandas as pd
import re
import streamlit as st
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    nparr = np.frombuffer(bytes_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    reader = ocr.Reader(['en'])
    kernel = np.ones((7,7), np.uint8)
    blur = cv2.GaussianBlur(img,(5,5),0)
    dilation = cv2.dilate(blur, kernel, iterations = 1)
    results = reader.readtext(dilation)

    text = ""
    for _ in range(len(results)):
        text += results[_][1] + " " 

    pattern = r'(.+?)(?=(?:\d{3} \w\d{2}|Nos\.|\d{4}|$))(?:\.20|20)?'

    matches = re.findall(pattern, text)

    grouped_items = {}
    current_year = None

    for item in matches:
        if re.match(r'^\d{4}', item):
            current_year = item
            grouped_items[current_year] = []
        elif current_year is not None:
            grouped_items[current_year].append(item)

    # Now let's iterate between the items and extract the information to create a dataframe
    data = []
    for year, items in grouped_items.items():
        for _ in items:
            pattern = r'(\d+) (\w+) (\d+ \|) (.*?)(?=\s*\d+\s+\d+) (\d+) (\d+)'
            # let's add another pattern to check
            pattern1 = r'(\d+) (\w+) ([\d.]+) (.*?) ([\d.]+) ([\d.]+)'
            # let's add another pattern to check
            pattern2 = r'(\d+) (\w+) (.*?) ([\d.]+) ([\d.]+)'
            # let's add another pattern to check
            pattern3 = r'(\d+) (\w+) ([\w.]+) (.*?)(?:(?:on (\d+))|([\d.]+)) ([\d.]+)'
            # let's add another pattern to check
            pattern4 = r'(\d+) (\w+) (\S+) (.*?) (\d+) (\d+)'

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

    df = pd.DataFrame(data, columns=['Stock #', 'Year', 'Illustration #', 'Denomination', 'Description', 'New or Unused Value', 'Used Value', 'Notes'])
    st.write(df)
