import os
import matplotlib
matplotlib.use("Agg")   
import re
import matplotlib.pyplot as plt

def split_sentences(text):
    t = re.sub(r"\s+", " ", text.strip())
    if not t:
        return []
    parts = re.split(r"(?<=[\.!?])\s+(?=[A-Z0-9\(\[\"])|(?<=:)\s+(?=[A-Z0-9])", t)
    out = [p.strip() for p in parts if p.strip()]
    if not out:
        out = [t]
    return out

def generate_flowchart_png(text, topic="", out_dir="results", max_nodes=10):
    sents = split_sentences(text)
    if topic:
        sents = sents[:200]
    nodes = sents[:max_nodes] if sents else []
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_axes([0,0,1,1])
    ax.axis("off")
    y = 0.9
    for i, s in enumerate(nodes, 1):
        label = re.sub(r"\s+", " ", s)[:140]
        ax.text(0.5, y, f"{i}. {label}", ha="center", va="top", fontsize=9, bbox=dict(boxstyle="round", facecolor="#C0C0C0"))
        if i < len(nodes):
            ax.annotate("", xy=(0.5, y-0.06), xytext=(0.5, y-0.02), arrowprops=dict(arrowstyle="->"))
        y -= 0.1
    os.makedirs(out_dir, exist_ok=True)
    fname = "flowchart.png" if not topic else f"{topic}_flowchart.png"
    path = os.path.join(out_dir, fname)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path
