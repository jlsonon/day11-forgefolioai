import os
import json
from groq import Groq
from typing import Dict, List, Any
from portfolio_templates import PortfolioTemplates, SampleData, PortfolioEnhancer

class GroqClient:
    """Client for interacting with Groq API"""
    
    def __init__(self):
        """Initialize Groq client with API key"""
        self.api_key = os.getenv('GROQ_API_KEY')
        self.demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
        
        if not self.api_key and not self.demo_mode:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
            
        self.model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    def generate_portfolio(self, user_data: Dict[str, Any], template_id: str = None) -> Dict[str, Any]:
        """Generate portfolio content based on user data with template support"""
        
        # If in demo mode, return an enhanced demo portfolio
        if self.demo_mode:
            return self._generate_enhanced_demo_portfolio(user_data, template_id)
        
        # Determine template
        if not template_id:
            template_id = PortfolioTemplates.get_template_for_profession(user_data.get('profession', ''))
        
        template = PortfolioTemplates.get_template(template_id)
        prompt = self._create_enhanced_prompt(user_data, template)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional portfolio generator creating a {template['name']} portfolio. Create compelling, well-structured content that showcases the user's skills and experience effectively. Use the {template['style']} style."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            structured_content = self._structure_portfolio_content(content, template)
            
            # Add enhanced features to the structured content
            structured_content['achievements'] = PortfolioEnhancer.add_achievements(user_data)
            structured_content['testimonials'] = PortfolioEnhancer.add_testimonials(user_data)
            structured_content['contact'] = PortfolioEnhancer.add_contact_info(user_data)
            
            return structured_content
            
        except Exception as e:
            raise Exception(f"Error generating portfolio: {str(e)}")
    
    def _create_prompt(self, user_data: Dict[str, Any]) -> str:
        """Create a detailed prompt for portfolio generation"""
        
        name = user_data.get('name', '')
        profession = user_data.get('profession', '')
        experience = user_data.get('experience', '')
        skills = user_data.get('skills', [])
        projects = user_data.get('projects', [])
        
        prompt = f"""
        Create a professional portfolio for the following person:
        
        Name: {name}
        Profession: {profession}
        Experience: {experience}
        Skills: {', '.join(skills) if skills else 'Not specified'}
        Projects: {', '.join(projects) if projects else 'Not specified'}
        
        Please generate:
        1. A compelling professional summary
        2. A detailed skills section
        3. Experience highlights
        4. Project descriptions (if provided)
        5. A professional conclusion
        
        Make the content engaging, professional, and tailored to their field.
        Use proper formatting with clear sections and bullet points where appropriate.
        """
        
        return prompt
    
    def _generate_demo_portfolio(self, user_data: Dict[str, Any]) -> str:
        """Generate a demo portfolio for testing purposes"""
        name = user_data.get('name', 'John Doe')
        profession = user_data.get('profession', 'Software Developer')
        experience = user_data.get('experience', '5 years of experience')
        skills = user_data.get('skills', ['Python', 'JavaScript', 'React'])
        projects = user_data.get('projects', ['E-commerce Platform', 'Task Management App'])
        
        demo_content = f"""
**Professional Summary**
{name} is a dedicated {profession} with {experience}. With a passion for creating innovative solutions and a strong foundation in modern technologies, {name} brings expertise and creativity to every project.

**Technical Skills**
• {', '.join(skills) if skills else 'Python, JavaScript, React, Node.js, SQL'}
• Problem-solving and analytical thinking
• Agile development methodologies
• Version control with Git
• Database design and optimization

**Professional Experience**
{experience} in software development with a focus on creating scalable, maintainable applications. Experience includes full-stack development, API design, and database optimization.

**Key Projects**
{chr(10).join([f"• {project}" for project in projects]) if projects else "• E-commerce Platform - Full-stack web application" + chr(10) + "• Task Management App - React-based productivity tool"}

**Conclusion**
{name} is committed to delivering high-quality solutions and continuously learning new technologies to stay at the forefront of the industry.
        """
        
        return demo_content.strip()
    
    def _generate_enhanced_demo_portfolio(self, user_data: Dict[str, Any], template_id: str = None) -> Dict[str, Any]:
        """Generate an enhanced demo portfolio with templates and additional features"""
        if not template_id:
            template_id = PortfolioTemplates.get_template_for_profession(user_data.get('profession', ''))
        
        template = PortfolioTemplates.get_template(template_id)
        
        # Generate base content
        base_content = self._generate_demo_portfolio(user_data)
        
        # Add enhanced features
        enhanced_content = {
            'template': template,
            'summary': self._extract_section(base_content, 'Professional Summary'),
            'skills': self._extract_section(base_content, 'Technical Skills'),
            'experience': self._extract_section(base_content, 'Professional Experience'),
            'education': user_data.get('education', ''),
            'projects': self._extract_section(base_content, 'Key Projects'),
            'conclusion': self._extract_section(base_content, 'Conclusion'),
            'achievements': PortfolioEnhancer.add_achievements(user_data),
            'testimonials': PortfolioEnhancer.add_testimonials(user_data),
            'contact': self._get_contact_info(user_data),
            'raw_content': base_content
        }
        
        return enhanced_content
    
    def _get_contact_info(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Get contact information, using custom contact if provided, otherwise generate"""
        custom_contact = user_data.get('custom_contact', {})
        
        # If custom contact info is provided, use it
        if custom_contact and any(custom_contact.values()):
            # Fill in missing fields with generated ones
            generated_contact = PortfolioEnhancer.add_contact_info(user_data)
            return {
                'email': custom_contact.get('email') or generated_contact.get('email', ''),
                'phone': custom_contact.get('phone') or generated_contact.get('phone', ''),
                'linkedin': custom_contact.get('linkedin') or generated_contact.get('linkedin', ''),
                'github': custom_contact.get('github') or generated_contact.get('github', ''),
                'website': custom_contact.get('website') or generated_contact.get('website', '')
            }
        
        # Otherwise, generate contact info
        return PortfolioEnhancer.add_contact_info(user_data)
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from portfolio content"""
        import re
        pattern = rf'\*\*{re.escape(section_name)}\*\*\s*(.*?)(?=\n\*\*|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _create_enhanced_prompt(self, user_data: Dict[str, Any], template: Dict[str, Any]) -> str:
        """Create an enhanced prompt for portfolio generation"""
        name = user_data.get('name', '')
        profession = user_data.get('profession', '')
        experience = user_data.get('experience', '')
        skills = user_data.get('skills', [])
        projects = user_data.get('projects', [])
        
        prompt = f"""
        Create a professional {template['name']} portfolio for the following person:
        
        Name: {name}
        Profession: {profession}
        Experience: {experience}
        Skills: {', '.join(skills) if skills else 'Not specified'}
        Projects: {', '.join(projects) if projects else 'Not specified'}
        
        Template Style: {template['style']}
        Required Sections: {', '.join(template['sections'])}
        
        Please generate a comprehensive portfolio that includes:
        1. A compelling professional summary
        2. Detailed skills section with technical and soft skills
        3. Professional experience with quantifiable achievements
        4. Key projects with impact descriptions
        5. Professional achievements and awards
        6. Client testimonials (if applicable)
        7. Contact information
        8. A strong professional conclusion
        
        Make the content engaging, professional, and tailored to the {template['style']} style.
        Use proper formatting with clear sections, bullet points, and professional language.
        Include specific metrics and achievements where possible.
        """
        
        return prompt
    
    def _structure_portfolio_content(self, content: str, template: Dict[str, Any]) -> Dict[str, Any]:
        """Structure the AI-generated content into organized sections"""
        import re
        
        sections = {}
        
        # Extract each section based on the template
        for section in template['sections']:
            if section == 'summary':
                sections['summary'] = self._extract_section(content, 'Professional Summary')
            elif section == 'skills':
                sections['skills'] = self._extract_section(content, 'Technical Skills')
            elif section == 'experience':
                sections['experience'] = self._extract_section(content, 'Professional Experience')
            elif section == 'projects':
                sections['projects'] = self._extract_section(content, 'Key Projects')
            elif section == 'achievements':
                sections['achievements'] = self._extract_section(content, 'Achievements')
            elif section == 'contact':
                # For contact, use the enhanced contact info instead of extracting from content
                sections['contact'] = self._extract_section(content, 'Contact')
        
        # Add template info
        sections['template'] = template
        sections['raw_content'] = content
        
        return sections
    
    def test_connection(self) -> bool:
        """Test the connection to Groq API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False
