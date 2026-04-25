# Smart Documentation System

An AI-powered documentation system that reads markdown files from GitHub repositories and provides intelligent answers based on the documentation using RAG (Retrieval-Augmented Generation).

## Features

- 🔐 GitHub OAuth authentication
- 📚 Automatic markdown file extraction from repositories
- 🤖 AI-powered question answering using Groq LLM
- 🔍 Vector embeddings with Qdrant for semantic search
- 💬 Real-time chat interface
- 📱 Responsive Tailwind CSS UI

## Tech Stack

- **Backend**: Flask, Python
- **Frontend**: React, Vite, Tailwind CSS
- **Database**: MongoDB (for documents), Qdrant (for vectors)
- **AI/LLM**: Groq API, Hugging Face embeddings
- **Deployment**: Gunicorn, Render

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB instance
- Qdrant instance
- GitHub OAuth App
- Groq API key
- Hugging Face API token

### Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd HGM-06-Smart-Documentation-System
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Variables**
Copy `.env.example` files and configure:

**Backend (.env)**
```bash
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
MONGO_URI=mongodb://localhost:27017/smartdocs
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-api-key
HF_TOKEN=your-hugging-face-token
GROQ_API_KEY=your-groq-api-key
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173
```

**Frontend (.env)**
```bash
VITE_API_BASE=http://localhost:8001
```

5. **Run Development Servers**

Backend:
```bash
cd backend
python app.py
```

Frontend:
```bash
cd frontend
npm run dev
```

Access the app at `http://localhost:5173`

## Deployment on Render (Free Plan)

### Backend Deployment

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Set Build Command**:
   ```
   cd backend && pip install -r requirements.txt
   ```
4. **Set Start Command**:
   ```
   cd backend && gunicorn -w 2 -b 0.0.0.0:$PORT app:app
   ```
5. **Set Environment Variables** (in Render dashboard):
   - `FLASK_ENV` = `production`
   - `FLASK_SECRET_KEY` = Your secure random key
   - `GITHUB_CLIENT_ID` = Your GitHub OAuth App ID
   - `GITHUB_CLIENT_SECRET` = Your GitHub OAuth App secret
   - `MONGO_URI` = Your MongoDB Atlas connection string
   - `QDRANT_URL` = Your Qdrant cloud URL
   - `QDRANT_API_KEY` = Your Qdrant API key
   - `HF_TOKEN` = Your Hugging Face API token
   - `GROQ_API_KEY` = Your Groq API key
   - `FRONTEND_URL` = Your deployed frontend URL
   - `CORS_ORIGINS` = Your deployed frontend URL

6. **Update GitHub OAuth App**:
   - Authorization callback URL: `https://your-backend-url.onrender.com/auth/github/callback`

### Frontend Deployment

1. **Create a Static Site** on Render
2. **Connect your GitHub repository**
3. **Set Build Command**:
   ```
   cd frontend && npm install && npm run build
   ```
4. **Set Publish Directory**: `frontend/dist`
5. **Set Environment Variables**:
   - `VITE_API_BASE` = Your backend URL on Render

### Alternative: Deploy Both on One Render Service

Use the provided `Procfile` to deploy backend only, then deploy frontend separately as a static site.

## Project Structure

```
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── docs_routes.py
│   │   └── ai_routes.py
│   ├── services/
│   │   ├── github_service.py
│   │   ├── rag_service.py
│   │   ├── rag_query.py
│   │   └── markdown_parser.py
│   ├── models/
│   │   └── user_model.py
│   └── utils/
│       └── helpers.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── config.js
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Docs.jsx
│   │   └── components/
│   │       ├── RepoSelector.jsx
│   │       ├── Sidebar.jsx
│   │       ├── DocContent.jsx
│   │       └── AIChat.jsx
│   ├── package.json
│   └── vite.config.js
├── Procfile
├── render.yaml
├── .env.example
└── README.md
```

## API Endpoints

### Authentication
- `GET /auth/github/login` - Redirect to GitHub OAuth
- `GET /auth/github/callback` - GitHub OAuth callback
- `GET /auth/github/repos` - Get user's GitHub repositories

### Documentation
- `POST /docs/load-repo` - Load markdown files from a GitHub repository
- `GET /docs` - Get list of loaded documents
- `GET /docs/<doc_id>` - Get specific document content

### AI
- `POST /ask-ai` - Ask a question about the documentation

## Environment Variables

See `.env.example` and `frontend/.env.example` for all available environment variables.

## Performance Optimizations

- ✅ Removed debug logging (saves disk space and improves performance)
- ✅ Pinned exact dependency versions in requirements.txt
- ✅ Optimized Flask session configuration for Render
- ✅ Environment-based CORS configuration
- ✅ Lazy loading of components in frontend
- ✅ Efficient vector embeddings with Qdrant

## Troubleshooting

### OAuth Not Working
- Ensure `FRONTEND_URL` and `CORS_ORIGINS` match your deployed frontend URL
- Check GitHub OAuth app callback URL configuration
- Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are correct

### Repositories Not Loading
- Ensure GitHub token has `repo` scope permission
- Check GitHub API rate limits
- Verify MongoDB connection is active

### AI Responses Not Working
- Verify Qdrant connection is active
- Check Hugging Face and Groq API keys are valid
- Ensure embeddings were created for selected repository

## License

MIT

## Support

For issues and questions, please open an issue on the GitHub repository.

