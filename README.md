# OCR Image Data Extractor

This Streamlit web application allows users to upload an image containing tabular data, perform Optical Character Recognition (OCR), and extract relevant information to display in a structured DataFrame. The app utilizes image processing techniques, the EasyOCR library for text recognition, and regex patterns for extracting specific data from the recognized text.

## Features:

- **File Upload:** Users can upload an image file containing tabular data.

- **Image Processing:** The uploaded image undergoes preprocessing steps, including grayscale conversion, Gaussian blur, and dilation, to enhance text visibility.

- **Text Recognition:** EasyOCR is employed to perform Optical Character Recognition on the processed image and extract text data.

- **Regex Pattern Matching:** The extracted text is then matched against predefined regex patterns to identify and parse relevant information.

- **Data Grouping:** Extracted information is grouped by year, facilitating the organization of data.

- **Data Display:** The final structured data is presented in a DataFrame, showcasing details such as stock number, year, illustration number, denomination, description, new or unused value, used value, and notes.

## How to Use:

1. **Upload Image:** Click on the "Choose a file" button to upload an image containing tabular data.

2. **View Extracted Data:** Once the image is uploaded, the app processes the image, performs OCR, and displays the extracted information in a DataFrame below.

3. **Data Interpretation:** Analyze the DataFrame to understand the structured data extracted from the uploaded image.

## Requirements:

- Python 3.x
- Streamlit
- Pillow (PIL)
- OpenCV
- EasyOCR
- NumPy
- pandas
- re (Regular Expression)

## Installation:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/OCR-Image-Data-Extractor.git
