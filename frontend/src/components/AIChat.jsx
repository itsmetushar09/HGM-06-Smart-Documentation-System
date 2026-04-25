import { useState } from "react";
import { motion } from "framer-motion";
import { API_BASE } from "../config";

export default function AIChat({ repo }) {

  const [messages, setMessages] = useState([
    { type: "bot", text: "Hi 👋 Ask me anything about the docs!" },
  ]);

  const [input, setInput] = useState("");

  const sendMessage = async () => {

    if (!input.trim()) return;

    const userMsg = {
      type: "user",
      text: input
    };

    setMessages(prev => [...prev, userMsg]);

    try {

      const response = await fetch(
        `${API_BASE}/ask-ai`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question: input,
            repo: repo   // repo context ready for teammate's backend
          })
        }
      );

      const data = await response.json();

      setMessages(prev => [
        ...prev,
        {
          type: "bot",
          text: data.answer || "No response received."
        }
      ]);

    } catch (error) {

      setMessages(prev => [
        ...prev,
        {
          type: "bot",
          text: "Error contacting AI server."
        }
      ]);

    }

    setInput("");

  };


  return (

    <div className="flex flex-col h-full p-4">

      {/* Title */}
      <div className="font-semibold mb-3">
        AI Assistant ({repo})
      </div>


      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-3">

        {messages.map((msg, i) => (

          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-2 rounded-lg max-w-[80%] ${
              msg.type === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "bg-gray-200 text-black"
            }`}
          >
            {msg.text}
          </motion.div>

        ))}

      </div>


      {/* Input */}
      <div className="flex gap-2">

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) =>
            e.key === "Enter" && sendMessage()
          }
          placeholder="Ask something..."
          className="flex-1 border rounded-lg px-3 py-2 text-sm outline-none"
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-4 rounded-lg hover:bg-blue-500"
        >
          Send
        </button>

      </div>

    </div>

  );

}
