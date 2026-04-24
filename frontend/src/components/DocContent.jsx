import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useEffect, useState } from "react";
import { API_BASE } from "../config";

export default function DocContent({ activeDoc }) {

  const [content, setContent] = useState("");

  useEffect(() => {

    if (!activeDoc) return;

    fetch(`${API_BASE}/docs/${activeDoc}`, {
      credentials: "include"
    })
      .then(res => res.json())
      .then(data => {

        setContent(data.content);

      });

  }, [activeDoc]);


  return (

    <div className="max-w-4xl mx-auto">
  
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
  
        {content}
  
      </ReactMarkdown>
  
    </div>
  
  );

}
