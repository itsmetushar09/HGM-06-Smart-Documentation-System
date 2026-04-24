export default function Sidebar({ docs, setActiveDoc }) {
  return (
    <div className="h-full w-64 bg-[#0b1b2b] border-r overflow-y-auto">

      <div className="p-4 font-semibold">
        Docs
      </div>

      {docs.map(doc => (
        <div
          key={doc.doc_id}
          onClick={() => setActiveDoc(doc.doc_id)}
          className="cursor-pointer hover:bg-gray-700 p-2"
        >
          {doc.title}
        </div>
      ))}

    </div>
  );
}
