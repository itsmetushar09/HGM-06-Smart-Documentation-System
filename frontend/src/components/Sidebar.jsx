import { motion } from "framer-motion";

const docs = [
  { id: "introduction", title: "Introduction" },
  { id: "gettingStarted", title: "Getting Started" },
];

export default function Sidebar({ setActiveDoc, activeDoc }) {
  return (
    <div className="h-full bg-gray-950 text-white p-4">
      <h2 className="text-lg mb-4 font-semibold">Docs</h2>

      {docs.map((doc) => (
  <motion.div
    key={doc.id}
    whileHover={{ x: 5 }}
    onClick={() => setActiveDoc(doc.id)}
    className={`p-2 rounded-md cursor-pointer ${
      activeDoc === doc.id
        ? "bg-blue-600"
        : "hover:bg-gray-800"
    }`}
  >
    {doc.title}
  </motion.div>
))}
    </div>
  );
}