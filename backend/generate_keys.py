#!/usr/bin/env python3
"""
Generate secure secret keys for production
Run this to generate strong keys for JWT and SECRET_KEY
"""

import secrets
import string

def generate_secret_key(length=32):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_secure_keys():
    """Generate all required secure keys"""
    
    print("🔐 Generating Secure Keys for Production\n")
    
    jwt_secret = generate_secret_key(64)
    secret_key = generate_secret_key(64)
    
    print("Copy these into your .env file:\n")
    print("=" * 70)
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print("=" * 70)
    print(f"SECRET_KEY={secret_key}")
    print("=" * 70)
    
    print("\n⚠️  Keep these values SECRET! Do not commit to GitHub!")
    print("💾 Save to .env file and keep backup in safe place")

if __name__ == '__main__':
    generate_secure_keys()
