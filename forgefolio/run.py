#!/usr/bin/env python3
"""
PortfolioForge Startup Script
Run this to start the PortfolioForge application
"""
import os
import sys

def main():
    """Start the PortfolioForge application"""
    print("Starting PortfolioForge...")
    
    # Set demo mode if no API key is provided
    if not os.getenv('GROQ_API_KEY'):
        print("No GROQ_API_KEY found. Running in demo mode.")
        os.environ['DEMO_MODE'] = 'true'
    
    # Import and run the app
    from app import app
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"PortfolioForge is running on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
