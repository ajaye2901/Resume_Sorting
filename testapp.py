import cv2
import pytesseract
import re
import numpy as np
import streamlit as st
import io
import fitz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr(file):
    img_text = ''
    doc = fitz.open(stream=file.read(), filetype="pdf")    # create a document object 'doc' using fitz package by reading the bytes of the file and specifying the file type as 'pdf'
    for page_num in range(doc.page_count):   
        img = doc.load_page(page_num).get_pixmap()   # get the pixmap object of the current page 
        img = np.frombuffer(img.samples, dtype=np.uint8).reshape(img.height, img.width, 3)  # convert it to a numpy array
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (thresh, binary) = cv2.threshold(grey, 225, 255, cv2.THRESH_BINARY)
        data = pytesseract.image_to_string(binary)  # perform OCR on the binary image to get text
        img_text += data
    return img_text


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
    resume = st.file_uploader("Upload a Resume", type=["pdf"])
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
