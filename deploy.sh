#!/bin/bash

# Configuration
HOST="admin@103.228.168.119"
REMOTE_DIR="~/UNUM_Back_Test"

echo "🚀 Starting Deployment to $HOST..."

# 1. Create Directory
echo "📂 Creating directory $REMOTE_DIR..."
ssh $HOST "mkdir -p $REMOTE_DIR"

# 2. Sync Files
echo "📡 Syncing files..."
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' --exclude '.DS_Store' ./ $HOST:$REMOTE_DIR

# 3. Setup Remote Environment
echo "🐍 Setting up remote Python environment..."
ssh $HOST "cd $REMOTE_DIR && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"

echo "✅ Deployment Complete!"
echo "To run the app, SSH into the server and run:"
echo "  cd $REMOTE_DIR"
echo "  ./venv/bin/streamlit run dashboard.py"
