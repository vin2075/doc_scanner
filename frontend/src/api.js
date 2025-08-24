import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE; // CRA uses REACT_APP_ prefix

const API = axios.create({
  baseURL: API_BASE, // dynamic URL
});

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getSummary = (path) =>
  API.post("/summary", { path }, { responseType: "blob" });

export const getTopicSummary = (path, topic) =>
  API.post("/topic-summary", { path, topic }, { responseType: "blob" });

export const getFlowchart = (path, topic) =>
  API.post("/flowchart", { path, topic }, { responseType: "blob" });

export const getLines = (path) =>
  API.post("/lines", { path }, { responseType: "blob" });

export const chatWithDoc = (path, query) =>
  API.post("/chat", { path, query });
