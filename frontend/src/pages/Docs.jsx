import { useEffect, useState } from "react";
import RepoSelector from "../components/RepoSelector";
import Sidebar from "../components/Sidebar";
import DocContent from "../components/DocContent";
import AIChat from "../components/AIChat";
import { API_BASE } from "../config";

export default function Docs() {

  const [repo, setRepo] = useState(null);
  const [docs, setDocs] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);

  const [showSidebar, setShowSidebar] = useState(true);
  const [showChat, setShowChat] = useState(false);


  useEffect(() => {

    if (!repo) return;

    fetch(`${API_BASE}/docs?repo=${repo}`, {
      credentials: "include"
    })
      .then(res => res.json())
      .then(data => {

        setDocs(data);

        if (data.length > 0) {
          setActiveDoc(data[0].doc_id);
        }

      });

  }, [repo]);


  return (
    <div className="flex h-screen w-screen overflow-hidden">

      {/* Sidebar */}
      {showSidebar && (
        <div className="w-64 border-r bg-[#0b1b2b]">
          <Sidebar docs={docs} setActiveDoc={setActiveDoc} />
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col">

        {/* Header */}
        <div className="flex justify-between items-center px-6 py-3 border-b">

          <div>
            Current Repo: {repo}
          </div>

          <div className="flex gap-4 text-blue-400">

            <button onClick={() => setShowSidebar(!showSidebar)}>
              Toggle Sidebar
            </button>

            <button onClick={() => setShowChat(!showChat)}>
              Toggle Chat
            </button>

            <button
              onClick={() => {
                setRepo(null);
                setDocs([]);
                setActiveDoc(null);
              }}
            >
              Change Repo
            </button>

          </div>
        </div>

        {/* Content area */}
        <div className="flex flex-1 overflow-hidden">

          {/* Docs viewer */}
          <div className="flex-1 overflow-y-auto px-10 py-6">

            {!repo ? (
              <RepoSelector setRepo={setRepo} />
            ) : (
              <DocContent activeDoc={activeDoc} />
            )}

          </div>

          {/* Chat panel */}
          {showChat && (
            <div className="w-80 border-l bg-[#0b1b2b]">
              <AIChat repo={repo} />
            </div>
          )}

        </div>

      </div>

    </div>
  );
}