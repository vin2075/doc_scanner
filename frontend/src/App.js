import React, { useState } from "react";
import {
  uploadFile,
  getSummary,
  getTopicSummary,
  getFlowchart,
  getLines,
  chatWithDoc,
} from "./api";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [path, setPath] = useState("");
  const [topic, setTopic] = useState("");
  const [question, setQuestion] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  const handleUpload = async () => {
    try {
      const res = await uploadFile(file);
      setPath(res.data.path);
      alert("File uploaded successfully!");
    } catch (err) {
      alert("Upload failed!");
    }
  };

  const downloadFile = (blob, filename) => {
    const url = window.URL.createObjectURL(new Blob([blob]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleSummary = async () => {
    const res = await getSummary(path);
    downloadFile(res.data, "summary.pdf");
  };

  const handleTopicSummary = async () => {
    const res = await getTopicSummary(path, topic);
    downloadFile(res.data, `${topic}_summary.pdf`);
  };

  const handleFlowchart = async () => {
    const res = await getFlowchart(path, topic);
    downloadFile(res.data, `${topic || "flowchart"}.png`);
  };

  const handleLines = async () => {
    const res = await getLines(path);
    downloadFile(res.data, "lines.pdf");
  };

  const handleChat = async () => {
    const res = await chatWithDoc(path, question);
    setChatResponse(res.data.answer);
  };

  return (
    <div className="container">
      <h1>📄 DocScanner</h1>

      <div className="section">
        <h2>1. Upload PDF</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload</button>
      </div>

      {path && (
        <>
          <div className="section">
            <h2>2. Summaries</h2>
            <button onClick={handleSummary}>Generate Summary</button>
            <input
              type="text"
              placeholder="Enter topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
            <button onClick={handleTopicSummary}>Topic Summary</button>
          </div>

          <div className="section">
            <h2>3. Flowchart</h2>
            <button onClick={handleFlowchart}>Generate Flowchart</button>
          </div>

          <div className="section">
            <h2>4. Lines View</h2>
            <button onClick={handleLines}>Get Lines</button>
          </div>

          <div className="section">
            <h2>5. Chat with Document</h2>
            <input
              type="text"
              placeholder="Ask a question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <button onClick={handleChat}>Ask</button>
            {chatResponse && (
              <div className="chat-response">
                <b>Answer:</b> {chatResponse}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
