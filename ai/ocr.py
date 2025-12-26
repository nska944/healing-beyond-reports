from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path, max_pages=2):
    """
    Extract text safely with limits to avoid worker timeout
    """
    text = ""

    try:
        images = convert_from_path(
            pdf_path,
            dpi=150,
            first_page=1,
            last_page=max_pages
        )

        for img in images:
            try:
                text += pytesseract.image_to_string(
                    img,
                    timeout=5   # ⏱ HARD OCR TIMEOUT
                )
            except RuntimeError:
                text += "\n[OCR timeout on page]\n"

    except Exception as e:
        print("OCR failed:", e)
        return ""

    return text.strip()
