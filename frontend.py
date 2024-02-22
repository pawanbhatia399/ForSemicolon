import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
import subprocess
import base64
from fpdf import FPDF


def extract_text_from_pdf(file):
    with BytesIO(file.read()) as file_buffer:
        pdf_reader = PdfReader(file_buffer)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def execute_backend_script(text_data):
    # Call the backend script with the text data
    result = subprocess.run(["python", "backend.py", text_data], capture_output=True, text=True)
    return result.stdout.strip()

def save_as_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

def main():
    st.title("PDF Text Extractor and Text Display")

    # PDF upload section
    st.header("PDF File Upload")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        st.success("PDF file uploaded successfully!")

        # Display extracted text from PDF on submit
        if st.button("Extract Text from PDF"):
            pdf_text = extract_text_from_pdf(pdf_file)
            st.subheader("Text Extracted from PDF:")
            st.write(pdf_text)

            # Execute backend script with PDF text and display result
            backend_result = execute_backend_script(pdf_text)
            st.subheader("Backend Result:")
            st.write(backend_result)

            # Option to download PDF
            if st.button("Download PDF"):
                pdf_filename = generate_pdf(backend_result)
                st.subheader("Download Link:")
                st.markdown(f"[Download PDF]({pdf_filename})", unsafe_allow_html=True)

    # Text input section
    st.header("Text Input")
    user_text = st.text_area("Enter your text here")

    # Display entered text on submit
    if st.button("Display Text"):
        st.subheader("Text Entered:")
        st.write(user_text)

        # Execute backend script with user text and display result
        backend_result = execute_backend_script(user_text)
        st.subheader("Backend Result:")
        st.write(backend_result)

        # Option to download PDF
        if backend_result:
            if st.button("Download PDF"):
                st.success("Downloading PDF...")
                save_as_pdf(backend_result, "output.pdf")

        with open("output.pdf", "rb") as f:
            pdf_data = f.read()
            b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="output.pdf">Click here to download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
 

if __name__ == "__main__":
    main()
