#!/bin/bash
set -e

# Build frontend
cd frontend
npm install
npm run build

# Move build to backend/static if serving from backend
# Or keep it separate and serve with a static file server
echo "Frontend built successfully"
cd ..

# Install backend dependencies
cd backend
pip install -r requirements.txt
echo "Backend dependencies installed"
