#!/usr/bin/env python3
"""
ChatBox Backend Startup Script
"""
import os
import sys
import subprocess

# Get the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Run the Flask app
if __name__ == '__main__':
    print("🚀 Starting ChatBox Backend...")
    print(f"📁 Working directory: {backend_dir}")
    print("\n" + "="*60)
    
    # Use Python directly to avoid issues
    subprocess.run([sys.executable, 'app.py'])
