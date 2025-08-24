from pdfminer.high_level import extract_text

def extract_text_from_pdf(path, max_pages=60):
    return extract_text(path, maxpages=max_pages) or ""
