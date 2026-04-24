import { lazy, Suspense, useEffect, useState } from "react";
import RepoSelector from "../components/RepoSelector";
import Sidebar from "../components/Sidebar";
import { API_BASE } from "../config";

const DocContent = lazy(() => import("../components/DocContent"));
const AIChat = lazy(() => import("../components/AIChat"));

export default function Docs() {
  const [repo, setRepo] = useState(null);
  const [docs, setDocs] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);

  const [showSidebar, setShowSidebar] = useState(true);
  const [showChat, setShowChat] = useState(false);
  const [loadError, setLoadError] = useState("");


  useEffect(() => {
    if (!repo?.name) return;

    fetch(`${API_BASE}/docs?repo=${encodeURIComponent(repo.name)}&owner=${encodeURIComponent(repo.owner)}`)
      .then(async (res) => {
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || "Failed to load docs");
        }

        return data;
      })
      .then((data) => {
        setLoadError("");
        setDocs(data);

        if (data.length > 0) {
          setActiveDoc(data[0].doc_id);
        } else {
          setActiveDoc(null);
        }
      })
      .catch((error) => {
        setDocs([]);
        setActiveDoc(null);
        setLoadError(error.message || "Failed to load docs for this repository.");
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
            Current Repo: {repo?.fullName || "None"}
          </div>

          <div className="flex gap-4 text-blue-400">

            <button onClick={() => setShowSidebar(!showSidebar)}>
              {showSidebar ? "Hide Sidebar" : "Show Sidebar"}
            </button>

            <button onClick={() => setShowChat(!showChat)}>
              {showChat ? "Hide Chat" : "Show Chat"}
            </button>

            <button
              onClick={() => {
                setShowChat(false);
                setRepo(null);
                setDocs([]);
                setActiveDoc(null);
                setLoadError("");
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
              <Suspense fallback={<div>Loading document viewer...</div>}>
                {loadError ? (
                  <div className="text-red-500">{loadError}</div>
                ) : (
                  <DocContent
                    key={`${repo.owner}/${repo.name}:${activeDoc || ""}`}
                    activeDoc={activeDoc}
                    repo={repo.name}
                    owner={repo.owner}
                  />
                )}
              </Suspense>
            )}

          </div>

          {/* Chat panel */}
          {showChat && (
            <div className="w-80 border-l bg-[#0b1b2b]">
              {repo ? (
                <Suspense fallback={<div className="p-4">Loading chat...</div>}>
                  <AIChat key={`${repo.owner}/${repo.name}`} repo={repo.name} owner={repo.owner} />
                </Suspense>
              ) : (
                <div className="flex h-full items-center justify-center p-6 text-center text-sm text-slate-300">
                  Load a repository first, then the AI chat will answer questions about its markdown docs.
                </div>
              )}
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
