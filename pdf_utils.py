from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file_bytes):
    try:
        stream = io.BytesIO(file_bytes)
        reader = PdfReader(stream)

        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t

        return text

    except Exception as e:
        return f"PDF_ERROR: {str(e)}"
