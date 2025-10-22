#!/usr/bin/env python3
"""
ForgeFolio Startup Script
Run this to start the ForgeFolio application
"""
import os
import sys

def main():
    """Start the ForgeFolio application"""
    print("Starting ForgeFolio...")
    
    # Set demo mode if no API key is provided
    if not os.getenv('GROQ_API_KEY'):
        print("No GROQ_API_KEY found. Running in demo mode.")
        os.environ['DEMO_MODE'] = 'true'
    
    # Import and run the app
    from app import app
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"ForgeFolio is running on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
