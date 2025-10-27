# ForgeFolio 

An AI-powered portfolio generator that creates professional portfolios using the Groq API. Built with Flask and featuring a modern, responsive web interface.

## Features 

- **AI-Powered Generation**: Uses Groq's LLM to generate professional portfolio content
- **Modern UI**: Beautiful, responsive web interface with gradient design
- **Dynamic Skills & Projects**: Add and manage skills and projects dynamically
- **Real-time Generation**: Fast portfolio generation with loading indicators
- **Copy to Clipboard**: Easy copying of generated content
- **Docker Support**: Containerized deployment ready
- **Health Checks**: Built-in health monitoring

## Tech Stack 

- **Backend**: Flask (Python)
- **AI**: Groq API (LLaMA models)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with gradients and animations
- **Icons**: Font Awesome
- **Deployment**: Docker, Gunicorn

## Quick Start 

### Prerequisites

- Python 3.11+
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ForgeFolio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Environment Variables 

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
FLASK_ENV=development
DEBUG=True
PORT=5000
SECRET_KEY=your_secret_key_here
```

## Docker Deployment 

### Build and run with Docker

```bash
# Build the image
docker build -t ForgeFolio .

# Run the container
docker run -p 5000:5000 -e GROQ_API_KEY=your_api_key ForgeFolio
```

### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  ForgeFolio:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL=llama3-8b-8192
    restart: unless-stopped
```

## API Endpoints 

- `GET /` - Main application interface
- `POST /generate` - Generate portfolio content
- `GET /health` - Health check endpoint

### Generate Portfolio Request

```json
{
  "name": "John Doe",
  "profession": "Software Developer",
  "experience": "5 years of experience in full-stack development...",
  "skills": ["Python", "JavaScript", "React", "Node.js"],
  "projects": ["E-commerce Platform", "Task Management App"]
}
```

### Response

```json
{
  "success": true,
  "content": {
    "summary": "Professional summary...",
    "skills": "Technical skills section...",
    "experience": "Work experience details...",
    "projects": "Project descriptions...",
    "conclusion": "Closing statement..."
  }
}
```

## Project Structure 

```
forgefolio/
├── app.py                 # Main Flask application
├── groq_client.py         # Groq API integration
├── utils.py               # Utility functions
├── templates/
│   └── index_template.html # Main HTML template
├── static/
│   └── style.css          # CSS styles
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Development 

### Running in Development Mode

```bash
export FLASK_ENV=development
export DEBUG=True
python app.py
```

### Code Structure

- **`app.py`**: Main Flask application with routes and error handling
- **`groq_client.py`**: Groq API client with portfolio generation logic
- **`utils.py`**: Utility functions for validation and content formatting
- **`templates/`**: HTML templates with embedded JavaScript
- **`static/`**: CSS styles and static assets

## Features in Detail 

### AI Portfolio Generation
- Uses Groq's LLaMA models for content generation
- Structured prompts for consistent output
- Error handling and fallback mechanisms

### User Interface
- Responsive design for all devices
- Dynamic skill and project management
- Real-time form validation
- Loading states and user feedback

### Security
- Input validation and sanitization
- Environment variable protection
- Non-root Docker user

## Contributing 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/jlsonon/forgefolio/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Roadmap 

- [ ] User authentication and saved portfolios
- [ ] Multiple portfolio templates
- [ ] PDF export functionality
- [ ] Portfolio preview and editing
- [ ] Integration with LinkedIn API
- [ ] Advanced customization options
---
## Author

### Jericho Sonon
#### Medium: [medium.com/@jlsonon12](https://medium.com/@jlsonon12)
#### GitHub: [github.com/jlsonon](https://github.com/jlsonon)
#### LinkedIn: [linkedin.com/in/jlsonon](https://www.linkedin.com/in/jlsonon/)
