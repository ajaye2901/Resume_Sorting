import cv2
import pytesseract
import re
import numpy as np
import streamlit as st

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr(file):
    img = np.frombuffer(file.read(), np.uint8) #converts the stream of bytes to a numpy array of 8-bit unsigned integers.
    img = cv2.imdecode(img, cv2.IMREAD_COLOR) #reads the numpy array as an image, using OpenCV's IMREAD_COLOR flag to read the image as a color image.
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, binary) = cv2.threshold(grey, 225, 255, cv2.THRESH_BINARY)
    data = pytesseract.image_to_string(binary)
    return data

def check(resume, keywords):
    text = ocr(resume)
    text = text.lower()
    l = []
    for i in keywords:
        matches = re.findall(r'(?i)' + i, text)
        l.extend(matches)
    l = list(set(l))
    st.write(l)
    if len(l) >= 3:
        return True
    else:
        return False

def app():
    st.title("Resume Keyword Check")
    resume = st.file_uploader("Upload a Resume", type=["jpeg", "jpg", "png"])
    keywords = st.text_input("Enter keywords (separated by comma)")
    if st.button("Search"):
        keywords = [keyword.strip() for keyword in keywords.split(",")]
        if resume is not None:
            if check(resume, keywords):
                st.write("Resume qualified")
            else:
                st.write("The resume does not contain enough keywords.")
        else:
            st.write("Please upload a resume.")
if __name__ == '__main__':
    app()
