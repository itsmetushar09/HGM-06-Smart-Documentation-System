# Smart Documentation System with AI

SmartDocs is a two-part app:

- A `Flask` backend that fetches markdown files from a public GitHub repository, stores docs in MongoDB, embeds them into Qdrant, and answers questions with Groq.
- A `React + Vite` frontend that lets you enter a public GitHub repo, browse markdown files, and chat with the AI assistant.

## Architecture

### Frontend

- `frontend/src/pages/Home.jsx`: login entrypoint
- `frontend/src/pages/Docs.jsx`: repo selection, doc viewer, AI chat layout
- `frontend/src/components/RepoSelector.jsx`: loads GitHub repos and triggers indexing
- `frontend/src/components/DocContent.jsx`: renders markdown
- `frontend/src/components/AIChat.jsx`: sends questions to the backend

### Backend

- `backend/app.py`: Flask app, sessions, CORS, route registration
- `backend/routes/auth_routes.py`: legacy OAuth route file, no longer used by the app flow
- `backend/routes/docs_routes.py`: markdown ingestion and doc retrieval
- `backend/routes/ai_routes.py`: AI question endpoint
- `backend/services/rag_service.py`: embedding generation and Qdrant upsert
- `backend/services/rag_query.py`: vector search plus Groq answer generation
- `backend/config.py`: MongoDB and Qdrant clients

## External Services You Need

This project depends on:

1. MongoDB
2. Qdrant
3. Groq API key

You can run MongoDB and Qdrant locally, or use cloud services such as MongoDB Atlas and Qdrant Cloud.

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- npm
- MongoDB running locally or remotely
- Qdrant running locally or remotely

### 1. Start MongoDB and Qdrant

If you want a fully local stack, Docker is the quickest route:

```bash
docker run -d --name smartdocs-mongo -p 27017:27017 mongo:7
docker run -d --name smartdocs-qdrant -p 6333:6333 qdrant/qdrant
```

### 2. Create backend env file

Copy [`backend/.env.example`](backend/.env.example) to `backend/.env` and fill in the secrets:

```env
FLASK_SECRET_KEY=change-me
GROQ_API_KEY=your-groq-api-key
MONGO_URI=mongodb://localhost:27017
MONGO_TLS=false
QDRANT_URL=http://localhost:6333
QDRANT_HTTPS=false
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=false
```

### 3. Create frontend env file

Copy [`frontend/.env.example`](frontend/.env.example) to `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8001
```

### 4. Install and run the backend

On Windows PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The backend runs on `http://localhost:8001`.

### 5. Install and run the frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`.

### 6. Use the app

1. Open `http://localhost:5173`
2. Go to `/docs`
3. Paste a public GitHub repo URL or `owner/repo`
4. Wait for markdown files to be indexed
5. Open a doc or ask the AI assistant a question

## What I Verified In This Repo

- The frontend production build succeeds with `npm run build`
- The backend dependencies were not installed in this workspace yet, so backend startup was not fully verified here

## Deployment

This codebase is now environment-driven, so you can deploy it without editing source files.

### Recommended split

- Frontend: Vercel or Netlify
- Backend: Render, Railway, or another Python host
- Data services: MongoDB Atlas and Qdrant Cloud

### Backend deployment env vars

Set these in your backend host:

```env
FLASK_SECRET_KEY=strong-random-secret
GROQ_API_KEY=your-groq-api-key
MONGO_URI=your-production-mongodb-uri
MONGO_TLS=true
MONGO_TLS_ALLOW_INVALID_CERTIFICATES=false
QDRANT_URL=https://your-qdrant-endpoint
QDRANT_HTTPS=true
QDRANT_API_KEY=your-qdrant-api-key
FRONTEND_URL=https://your-frontend-domain
CORS_ORIGINS=https://your-frontend-domain
SESSION_COOKIE_SAMESITE=None
SESSION_COOKIE_SECURE=true
```

Run command examples:

- Gunicorn: `gunicorn app:app`
- Waitress on Windows: `waitress-serve --host 0.0.0.0 --port 8001 app:app`

### Frontend deployment env vars

Set this in Vercel or Netlify:

```env
VITE_API_BASE_URL=https://your-backend-domain
```

### Important production note

Because the frontend and backend usually live on different domains in production, the backend must use:

- `SESSION_COOKIE_SAMESITE=None`
- `SESSION_COOKIE_SECURE=true`
- `CORS_ORIGINS=https://your-frontend-domain`

Without those settings, repo-selection session state will not be preserved across sites.

## Current Caveats In The Codebase

- `backend/services/rag_service.py` and `backend/services/rag_query.py` load the sentence-transformer at import time, so first startup can be slow
- embeddings are stored as whole-document payloads, not smaller chunks, which can reduce answer quality on large markdown files
- repo loading fetches every markdown file recursively, so large repositories can take time
- there are no automated tests yet
