import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def split_sentences(text):
    t = re.sub(r"\s+", " ", text.strip())
    if not t:
        return []
    parts = re.split(r"(?<=[\.!?])\s+(?=[A-Z0-9\(\[\"])|(?<=:)\s+(?=[A-Z0-9])", t)
    out = [p.strip() for p in parts if p.strip()]
    if not out:
        out = [t]
    return out

def textrank_like(sentences, k):
    if len(sentences) <= k:
        return sentences
    vec = TfidfVectorizer(min_df=1, ngram_range=(1,2), stop_words="english")
    X = vec.fit_transform(sentences)
    S = (X * X.T)
    try:
        S.setdiag(0)
    except Exception:
        pass
    scores = np.array(S.sum(axis=1)).ravel()
    idx = np.argsort(-scores)[:k]
    idx = sorted(idx.tolist())
    return [sentences[i] for i in idx]

def summarize_document(text, top_n=10, openai_key=None):
    sents = split_sentences(text)
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            prompt = "Summarize the document in concise bullet points. Keep it focused and faithful to the text."
            content = prompt + "\n\n" + "\n".join(sents[:800])
            resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":content}], temperature=0.2, max_tokens=600)
            return resp.choices[0].message.content.strip()
        except Exception:
            pass
    return " ".join(textrank_like(sents, top_n))

def summarize_topic(text, topic, top_n=8, openai_key=None):
    sents = split_sentences(text)
    if not sents:
        return ""
    vec = TfidfVectorizer(min_df=1, ngram_range=(1,2), stop_words="english")
    X = vec.fit_transform(sents + [topic])
    qv = X[-1]
    S = X[:-1]
    scores = (S * qv.T).toarray().ravel()
    order = np.argsort(-scores)[:max(3, top_n)]
    picks = [sents[i] for i in order if scores[i] > 0]
    picks = picks if picks else textrank_like(sents, top_n)
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            ctx = "\n".join(picks[:50])
            prompt = f"Write a focused summary about '{topic}'. Use only the context. Add brief justification from related parts."
            content = prompt + "\n\nContext:\n" + ctx
            resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":content}], temperature=0.2, max_tokens=600)
            return resp.choices[0].message.content.strip()
        except Exception:
            pass
    return " ".join(picks)

def lines_view(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines
