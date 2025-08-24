import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def split_sentences(text):
    t = re.sub(r"\s+", " ", text.strip())
    if not t:
        return []
    parts = re.split(r"(?<=[\.!?])\s+(?=[A-Z0-9\(\[\"])|(?<=:)\s+(?=[A-Z0-9])", t)
    out = [p.strip() for p in parts if p.strip()]
    if not out:
        out = [t]
    return out

def retrieve(text, query, k=8):
    sents = split_sentences(text)
    if not sents:
        return [], []
    vec = TfidfVectorizer(min_df=1, ngram_range=(1,2), stop_words="english")
    X = vec.fit_transform(sents + [query])
    qv = X[-1]
    S = X[:-1]
    scores = (S * qv.T).toarray().ravel()
    idx = np.argsort(-scores)[:k]
    snippets = [sents[i] for i in idx if scores[i] > 0]
    return snippets, scores[idx].tolist()

def answer_question(text, question, openai_key=None):
    ctx, _ = retrieve(text, question, k=8)
    if openai_key and ctx:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            prompt = "Answer using only the provided excerpts. If unknown, say you don't know. Cite brief quotes."
            content = prompt + "\n\nExcerpts:\n" + "\n".join(f"- {c}" for c in ctx[:50]) + f"\n\nQuestion: {question}\nAnswer:"
            resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":content}], temperature=0, max_tokens=500)
            return resp.choices[0].message.content.strip(), ctx
        except Exception:
            pass
    return " ".join(ctx[:5]) if ctx else "I don't know.", ctx
