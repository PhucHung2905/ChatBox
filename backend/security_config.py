# CORS Configuration for Production
# This file helps configure CORS settings for different deployment environments

from flask import Flask
from flask_cors import CORS
import os

def setup_cors_production(app: Flask):
    """
    Configure CORS for production environment
    """
    # Get allowed origins from environment variable or use defaults
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    cors_origins = [origin.strip() for origin in cors_origins]
    
    CORS(app, 
         origins=cors_origins,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         max_age=3600
    )
    
    return app

def add_security_headers(app: Flask):
    """
    Add security headers to all responses
    """
    @app.after_request
    def set_security_headers(response):
        # Prevent clickjacking attacks
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Prevent MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Strict Transport Security (HTTPS only)
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline';"
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
    
    return app
