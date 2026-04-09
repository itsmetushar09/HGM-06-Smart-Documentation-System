import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import DocContent from "../components/DocContent";
import { docs } from "../data/docs";
import { motion } from "framer-motion";
import AIChat from "../components/AIChat";

export default function Docs() {
  const [activeDoc, setActiveDoc] = useState("introduction");

  return (
    <div className="h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <div className="w-1/5 hidden md:block">
          <Sidebar setActiveDoc={setActiveDoc} activeDoc={activeDoc} />
        </div>

        {/* Content */}
        <div className="flex-1 p-6 overflow-y-auto">
  <motion.div
    key={activeDoc}
    initial={{ opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0 }}
    transition={{ duration: 0.3 }}
  >
    <DocContent content={docs[activeDoc]} />
  </motion.div>
</div>

        {/* AI Chat */}
        <div className="w-1/5 hidden lg:block bg-gray-100 p-4">
  <AIChat />
</div>
      </div>
    </div>
  );
}