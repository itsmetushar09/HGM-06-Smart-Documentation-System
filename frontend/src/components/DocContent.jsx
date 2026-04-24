import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useEffect, useState } from "react";
import { API_BASE } from "../config";

export default function DocContent({ activeDoc, repo, owner }) {

  const [content, setContent] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {

    if (!activeDoc) return;

    const encodedDocId = activeDoc
      .split("/")
      .map((segment) => encodeURIComponent(segment))
      .join("/");

    fetch(
      `${API_BASE}/docs/${encodedDocId}?repo=${encodeURIComponent(repo)}&owner=${encodeURIComponent(owner)}`
    )
      .then(async (res) => {
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || "Failed to load document");
        }

        return data;
      })
      .then(data => {
        setError("");
        setContent(data.content);
      })
      .catch((fetchError) => {
        setContent("");
        setError(fetchError.message || "Failed to load document");
      });

  }, [activeDoc, owner, repo]);


  return (

    <div className="max-w-4xl mx-auto">

      {error ? (
        <p className="mb-4 text-sm text-red-500">{error}</p>
      ) : null}
  
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
  
        {content}
  
      </ReactMarkdown>
  
    </div>
  
  );

}
