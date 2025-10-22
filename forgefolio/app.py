from flask import Flask, render_template, request, jsonify
import os
from groq_client import GroqClient
from utils import validate_input, format_response
from portfolio_templates import PortfolioTemplates, SampleData
from analytics import analytics

app = Flask(__name__)

# Initialize Groq client (will be created when needed)
groq_client = None

@app.route('/')
def index():
    """Main page route"""
    return render_template('enhanced_template.html')

@app.route('/generate', methods=['POST'])
def generate_portfolio():
    """Generate portfolio content using AI"""
    try:
        data = request.get_json()
        
        # Validate input
        if not validate_input(data):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Initialize Groq client if not already done
        global groq_client
        if groq_client is None:
            try:
                groq_client = GroqClient()
            except ValueError as e:
                return jsonify({
                    'error': 'Groq API key not configured. Please set GROQ_API_KEY environment variable.'
                }), 500
        
        # Extract user information
        name = data.get('name', '')
        profession = data.get('profession', '')
        experience = data.get('experience', '')
        education = data.get('education', '')
        skills = data.get('skills', [])
        projects = data.get('projects', [])
        template_id = data.get('template_id', None)
        custom_contact = data.get('contact', {})
        
        # Generate portfolio content using Groq
        portfolio_content = groq_client.generate_portfolio({
            'name': name,
            'profession': profession,
            'experience': experience,
            'education': education,
            'skills': skills,
            'projects': projects,
            'custom_contact': custom_contact
        }, template_id)
        
        # Track analytics
        features_used = []
        if template_id and template_id != 'tech_modern':
            features_used.append('template_selection')
        if len(skills) > 0 or len(projects) > 0:
            features_used.append('custom_content')
        
        analytics.track_generation(template_id or 'tech_modern', profession, features_used)
        
        return jsonify({
            'success': True,
            'content': portfolio_content
        })
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/templates')
def get_templates():
    """Get available portfolio templates"""
    return jsonify({
        'success': True,
        'templates': PortfolioTemplates.get_all_templates()
    })

@app.route('/sample-profiles')
def get_sample_profiles():
    """Get sample profiles for quick demos"""
    # Track feature usage
    analytics.track_generation('sample_profiles', 'demo', ['sample_profiles'])
    
    return jsonify({
        'success': True,
        'profiles': SampleData.get_all_sample_profiles()
    })

@app.route('/analytics')
def get_analytics():
    """Get analytics statistics"""
    return jsonify({
        'success': True,
        'stats': analytics.get_demo_stats()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
