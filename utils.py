import re
from typing import Dict, List, Any

def validate_input(data: Dict[str, Any]) -> bool:
    """Validate input data for portfolio generation"""
    
    # Check if data is a dictionary
    if not isinstance(data, dict):
        return False
    
    # Check required fields
    required_fields = ['name', 'profession']
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    
    # Validate name (should be non-empty string)
    if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
        return False
    
    # Validate profession (should be non-empty string)
    if not isinstance(data['profession'], str) or len(data['profession'].strip()) == 0:
        return False
    
    # Validate experience if provided
    if 'experience' in data and data['experience']:
        if not isinstance(data['experience'], str):
            return False
    
    # Validate skills if provided
    if 'skills' in data and data['skills']:
        if not isinstance(data['skills'], list):
            return False
        # Check if all skills are strings
        for skill in data['skills']:
            if not isinstance(skill, str):
                return False
    
    # Validate projects if provided
    if 'projects' in data and data['projects']:
        if not isinstance(data['projects'], list):
            return False
        # Check if all projects are strings
        for project in data['projects']:
            if not isinstance(project, str):
                return False

    # Validate education if provided
    if 'education' in data and data['education']:
        # Accept either a string (legacy) or a list of dicts (advanced)
        if isinstance(data['education'], str):
            pass  # ok
        elif isinstance(data['education'], list):
            for edu in data['education']:
                if not isinstance(edu, dict):
                    return False
                # school and degree are recommended but not strictly required
                allowed_keys = {'school', 'degree', 'field', 'start_date', 'end_date'}
                # Must not contain unexpected keys
                if any(k not in allowed_keys for k in edu.keys()):
                    return False
                # If dates provided, ensure strings
                for k in ['school', 'degree', 'field', 'start_date', 'end_date']:
                    if k in edu and edu[k] is not None and not isinstance(edu[k], str):
                        return False
        else:
            return False
    
    return True

def format_response(content: str) -> Dict[str, str]:
    """Format the AI-generated content into structured sections"""
    
    # Split content into sections based on common patterns
    sections = {
        'summary': '',
        'skills': '',
        'experience': '',
        'projects': '',
        'conclusion': ''
    }
    
    # Try to extract sections using regex patterns
    content_lower = content.lower()
    
    # Extract summary (usually at the beginning)
    summary_match = re.search(r'(?:summary|about|overview)[:\s]*(.*?)(?=\n\n|\n(?:skills|experience|projects|conclusion)|$)', 
                             content, re.DOTALL | re.IGNORECASE)
    if summary_match:
        sections['summary'] = summary_match.group(1).strip()
    
    # Extract skills section
    skills_match = re.search(r'(?:skills|technical skills|core competencies)[:\s]*(.*?)(?=\n\n|\n(?:experience|projects|conclusion)|$)', 
                            content, re.DOTALL | re.IGNORECASE)
    if skills_match:
        sections['skills'] = skills_match.group(1).strip()
    
    # Extract experience section
    experience_match = re.search(r'(?:experience|work experience|professional experience)[:\s]*(.*?)(?=\n\n|\n(?:projects|conclusion)|$)', 
                                content, re.DOTALL | re.IGNORECASE)
    if experience_match:
        sections['experience'] = experience_match.group(1).strip()
    
    # Extract projects section
    projects_match = re.search(r'(?:projects|portfolio|key projects)[:\s]*(.*?)(?=\n\n|\n(?:conclusion|contact)|$)', 
                              content, re.DOTALL | re.IGNORECASE)
    if projects_match:
        sections['projects'] = projects_match.group(1).strip()
    
    # Extract conclusion section
    conclusion_match = re.search(r'(?:conclusion|summary|closing)[:\s]*(.*?)$', 
                                content, re.DOTALL | re.IGNORECASE)
    if conclusion_match:
        sections['conclusion'] = conclusion_match.group(1).strip()
    
    # If no sections were found, put all content in summary
    if not any(sections.values()):
        sections['summary'] = content
    
    return sections

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS and other security issues"""
    if not isinstance(text, str):
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    
    # Limit length
    if len(text) > 1000:
        text = text[:1000]
    
    return text.strip()

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text for better portfolio optimization"""
    if not text:
        return []
    
    # Simple keyword extraction (can be enhanced with NLP libraries)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall'}
    
    keywords = [word for word in words if word not in stop_words]
    
    # Return unique keywords, limited to 20
    return list(set(keywords))[:20]
