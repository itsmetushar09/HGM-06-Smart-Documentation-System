import { useState } from "react";
import { motion } from "framer-motion";

import { API_BASE } from "../config";

export default function AIChat({ repo, owner }) {
  const MotionDiv = motion.div;
  const [messages, setMessages] = useState([
    { type: "bot", text: "Hi! Ask me anything about the docs." },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const question = input.trim();
    const userMsg = { type: "user", text: question };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const response = await fetch(`${API_BASE}/ask-ai`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          repo,
          owner,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "AI request failed");
      }

      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: data.answer || "No response received.",
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: error.message || "Error contacting AI server.",
        },
      ]);
    }
  };

  return (
    <div className="flex h-full flex-col p-4">
      <div className="mb-3 font-semibold text-white">AI Assistant ({repo})</div>

      <div className="mb-3 flex-1 space-y-3 overflow-y-auto">
        {messages.map((msg, i) => (
          <MotionDiv
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`max-w-[80%] rounded-lg p-2 ${
              msg.type === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "bg-gray-200 text-black"
            }`}
          >
            {msg.text}
          </MotionDiv>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask something..."
          className="flex-1 rounded-lg border px-3 py-2 text-sm text-black outline-none"
        />

        <button
          onClick={sendMessage}
          className="rounded-lg bg-blue-600 px-4 text-white hover:bg-blue-500"
        >
          Send
        </button>
      </div>
    </div>
  );
}
