import { motion } from "framer-motion";
import { Search } from "lucide-react";

export default function Navbar() {
  return (
    <motion.div
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="h-14 bg-gray-900 text-white flex items-center justify-between px-6 shadow-md"
    >
      {/* Logo */}
      <h1 className="text-lg font-semibold">📘 SmartDocs</h1>

      {/* Search */}
      <div className="flex items-center bg-gray-800 px-3 py-1 rounded-lg">
        <Search size={18} />
        <input
          type="text"
          placeholder="Search docs..."
          className="bg-transparent outline-none px-2 text-sm"
        />
      </div>

      {/* Right */}
      <div>
        <button className="bg-blue-600 px-3 py-1 rounded-lg hover:bg-blue-500">
          Login
        </button>
      </div>
    </motion.div>
  );
}