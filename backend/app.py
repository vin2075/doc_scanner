from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import io
from utils.pdf_utils import extract_text_from_pdf
from utils.summarizer import summarize_document, summarize_topic, lines_view
from utils.flowchart import generate_flowchart_png
from utils.chatbot import answer_question
from utils.pdf_exporter import export_text_pdf

load_dotenv()

app = Flask(__name__)
CORS(app)

MAX_FILESIZE = 50 * 1024 * 1024
MAX_PAGES = 60
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def ensure_pdf(file):
    if not file or not file.filename.lower().endswith(".pdf"):
        return False
    return True

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not ensure_pdf(f):
        return jsonify({"error": "Only PDF files are allowed"}), 400
    f.seek(0, os.SEEK_END)
    size = f.tell()
    if size > MAX_FILESIZE:
        return jsonify({"error": "File too large"}), 413
    f.seek(0)
    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)
    return jsonify({"message": "ok", "path": save_path})

@app.route("/summary", methods=["POST"])
def summary():
    data = request.get_json(silent=True) or {}
    path = data.get("path")
    if not path or not os.path.isfile(path):
        return jsonify({"error": "Invalid path"}), 400
    text = extract_text_from_pdf(path, max_pages=MAX_PAGES)
    result = summarize_document(text, openai_key=os.getenv("OPENAI_API_KEY"))
    pdf_path = export_text_pdf(result, RESULT_FOLDER, "summary.pdf")
    return send_file(pdf_path, as_attachment=True)

@app.route("/topic-summary", methods=["POST"])
def topic_summary():
    data = request.get_json(silent=True) or {}
    path = data.get("path")
    topic = data.get("topic", "")
    if not path or not os.path.isfile(path) or not topic:
        return jsonify({"error": "Invalid input"}), 400
    text = extract_text_from_pdf(path, max_pages=MAX_PAGES)
    result = summarize_topic(text, topic, openai_key=os.getenv("OPENAI_API_KEY"))
    pdf_path = export_text_pdf(result, RESULT_FOLDER, f"{topic}_summary.pdf")
    return send_file(pdf_path, as_attachment=True)

@app.route("/flowchart", methods=["POST"])
def flowchart():
    data = request.get_json(silent=True) or {}
    path = data.get("path")
    topic = data.get("topic", "")
    if not path or not os.path.isfile(path):
        return jsonify({"error": "Invalid input"}), 400
    text = extract_text_from_pdf(path, max_pages=MAX_PAGES)
    png_path = generate_flowchart_png(text, topic=topic, out_dir=RESULT_FOLDER)
    return send_file(png_path, as_attachment=True)

@app.route("/lines", methods=["POST"])
def lines():
    data = request.get_json(silent=True) or {}
    path = data.get("path")
    if not path or not os.path.isfile(path):
        return jsonify({"error": "Invalid path"}), 400
    text = extract_text_from_pdf(path, max_pages=MAX_PAGES)
    result = lines_view(text)
    pdf_path = export_text_pdf("\n".join(result), RESULT_FOLDER, "lines.pdf")
    return send_file(pdf_path, as_attachment=True)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    path = data.get("path")
    question = data.get("query", "")
    if not path or not os.path.isfile(path) or not question:
        return jsonify({"error": "Invalid input"}), 400
    text = extract_text_from_pdf(path, max_pages=MAX_PAGES)
    answer, snippets = answer_question(text, question, openai_key=os.getenv("OPENAI_API_KEY"))
    return jsonify({"answer": answer, "source": snippets})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
