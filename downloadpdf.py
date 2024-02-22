import streamlit as st
from fpdf import FPDF
import base64

def save_as_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

st.title("Streamlit Text to PDF Example")

# Input box for entering text
user_input = st.text_area("Enter Text:")

# Submit button to display the entered text
if st.button("Submit"):
    st.write("Entered Text:")
    st.write(user_input)

# Download button to save entered text as a PDF file
if st.button("Download as PDF"):
    if user_input:
        st.success("Downloading PDF...")
        save_as_pdf(user_input, "output.pdf")

        with open("output.pdf", "rb") as f:
            pdf_data = f.read()
            b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="output.pdf">Click here to download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Please enter some text before downloading.")
