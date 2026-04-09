import { useState } from "react";
import { motion } from "framer-motion";

export default function AIChat() {
  const [messages, setMessages] = useState([
    { type: "bot", text: "Hi 👋 Ask me anything about the docs!" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;

    const newMessages = [
      ...messages,
      { type: "user", text: input },
      { type: "bot", text: "Thinking..." },
    ];

    setMessages(newMessages);
    setInput("");

    // Simulate AI response (later backend)
    setTimeout(() => {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { type: "bot", text: "This is a demo AI response 🤖" },
      ]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat Messages */}
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
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
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