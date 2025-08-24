import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_text_pdf(content, out_dir, filename):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    parts = []
    for block in str(content).split("\n"):
        parts.append(Paragraph(block, styles["Normal"]))
        parts.append(Spacer(1, 8))
    doc.build(parts)
    return path
