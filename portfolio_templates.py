"""
Portfolio Templates for ForgeFolio
Multiple professional templates for different industries and styles
"""
from typing import Dict, List, Any
import random

class PortfolioTemplates:
    """Collection of professional portfolio templates"""
    
    TEMPLATES = {
        'tech_modern': {
            'name': 'Modern Tech Professional',
            'description': 'Clean, modern design perfect for software developers and tech professionals',
            'style': 'modern',
            'sections': ['summary', 'skills', 'experience', 'projects', 'achievements', 'education', 'contact'],
            'tone': 'professional and technical',
            'focus': 'technical skills, projects, and measurable achievements',
            'format': 'structured with bullet points and metrics'
        },
        'creative_artist': {
            'name': 'Creative Artist',
            'description': 'Bold, creative design for artists, designers, and creative professionals',
            'style': 'creative',
            'sections': ['summary', 'portfolio', 'skills', 'experience', 'testimonials', 'education', 'contact'],
            'tone': 'expressive and artistic',
            'focus': 'creative vision, portfolio pieces, and artistic philosophy',
            'format': 'narrative style with vivid descriptions'
        },
        'business_executive': {
            'name': 'Business Executive',
            'description': 'Professional, corporate design for executives and business leaders',
            'style': 'corporate',
            'sections': ['summary', 'experience', 'leadership', 'achievements', 'education', 'contact'],
            'tone': 'authoritative and strategic',
            'focus': 'leadership experience, business impact, and strategic vision',
            'format': 'executive summary style with ROI metrics'
        },
        'academic_researcher': {
            'name': 'Academic Researcher',
            'description': 'Scholarly design for researchers, academics, and PhD candidates',
            'style': 'academic',
            'sections': ['summary', 'research', 'publications', 'education', 'awards', 'teaching', 'contact'],
            'tone': 'scholarly and analytical',
            'focus': 'research contributions, publications, and academic achievements',
            'format': 'academic CV style with citations and research areas'
        },
        'freelancer_creative': {
            'name': 'Freelancer Creative',
            'description': 'Dynamic design for freelancers and independent contractors',
            'style': 'freelance',
            'sections': ['summary', 'services', 'portfolio', 'testimonials', 'skills', 'education', 'contact'],
            'tone': 'personable and client-focused',
            'focus': 'services offered, client satisfaction, and versatility',
            'format': 'benefit-driven with client testimonials'
        }
    }
    
    @classmethod
    def get_template(cls, template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID"""
        return cls.TEMPLATES.get(template_id, cls.TEMPLATES['tech_modern'])
    
    @classmethod
    def get_all_templates(cls) -> Dict[str, Dict[str, Any]]:
        """Get all available templates"""
        return cls.TEMPLATES
    
    @classmethod
    def get_random_template(cls) -> str:
        """Get a random template ID"""
        return random.choice(list(cls.TEMPLATES.keys()))
    
    @classmethod
    def get_template_for_profession(cls, profession: str) -> str:
        """Get the best template for a given profession"""
        profession_lower = profession.lower()
        
        if any(word in profession_lower for word in ['artist', 'designer', 'creative', 'graphic', 'ui', 'ux']):
            return 'creative_artist'
        elif any(word in profession_lower for word in ['executive', 'manager', 'director', 'ceo', 'cfo', 'business']):
            return 'business_executive'
        elif any(word in profession_lower for word in ['researcher', 'scientist', 'professor', 'academic', 'phd']):
            return 'academic_researcher'
        elif any(word in profession_lower for word in ['freelancer', 'consultant', 'contractor', 'independent']):
            return 'freelancer_creative'
        else:
            return 'tech_modern'

class SampleData:
    """Pre-filled sample data for quick demos"""
    
    SAMPLE_PROFILES = {
        'software_developer': {
            'name': 'Alex Chen',
            'profession': 'Senior Software Developer',
            'experience': '5+ years of experience in full-stack development with expertise in modern web technologies. Led development of scalable applications serving 100K+ users.',
            'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker', 'PostgreSQL', 'MongoDB'],
            'projects': [
                'E-commerce Platform - Built scalable online marketplace with microservices architecture',
                'Real-time Chat Application - Developed using WebSockets and React',
                'Machine Learning API - Created ML pipeline for predictive analytics'
            ]
        },
        'data_scientist': {
            'name': 'Dr. Sarah Johnson',
            'profession': 'Data Scientist',
            'experience': '6+ years in machine learning and data analysis. PhD in Statistics with focus on predictive modeling and big data analytics.',
            'skills': ['Python', 'R', 'Machine Learning', 'TensorFlow', 'PyTorch', 'SQL', 'Tableau', 'Statistics'],
            'projects': [
                'Customer Segmentation Model - Improved marketing ROI by 40%',
                'Predictive Analytics Dashboard - Real-time business intelligence solution',
                'NLP Text Classification - Automated document processing system'
            ]
        },
        'ui_designer': {
            'name': 'Maria Rodriguez',
            'profession': 'UI/UX Designer',
            'experience': '4+ years creating user-centered designs for web and mobile applications. Expert in design thinking and user research methodologies.',
            'skills': ['Figma', 'Adobe Creative Suite', 'Sketch', 'User Research', 'Prototyping', 'HTML/CSS', 'JavaScript'],
            'projects': [
                'Mobile Banking App - Redesigned user experience for 500K+ users',
                'E-learning Platform - Created intuitive learning management system',
                'Healthcare Dashboard - Designed data visualization for medical professionals'
            ]
        },
        'marketing_manager': {
            'name': 'David Kim',
            'profession': 'Marketing Manager',
            'experience': '7+ years in digital marketing and brand management. Led campaigns that generated $2M+ in revenue and increased brand awareness by 150%.',
            'skills': ['Digital Marketing', 'SEO/SEM', 'Google Analytics', 'Social Media', 'Content Strategy', 'Email Marketing', 'A/B Testing'],
            'projects': [
                'Brand Rebranding Campaign - Increased market share by 25%',
                'Digital Marketing Automation - Implemented lead nurturing system',
                'Social Media Strategy - Grew followers from 10K to 100K+'
            ]
        }
    }
    
    @classmethod
    def get_sample_profile(cls, profile_id: str) -> Dict[str, Any]:
        """Get a specific sample profile"""
        return cls.SAMPLE_PROFILES.get(profile_id, cls.SAMPLE_PROFILES['software_developer'])
    
    @classmethod
    def get_all_sample_profiles(cls) -> Dict[str, Dict[str, Any]]:
        """Get all available sample profiles"""
        return cls.SAMPLE_PROFILES
    
    @classmethod
    def get_random_profile(cls) -> str:
        """Get a random sample profile ID"""
        return random.choice(list(cls.SAMPLE_PROFILES.keys()))

class PortfolioEnhancer:
    """Advanced portfolio enhancement features"""
    
    @staticmethod
    def add_achievements(user_data: Dict[str, Any]) -> List[str]:
        """Generate achievements based on user data"""
        name = user_data.get('name', '')
        profession = user_data.get('profession', '')
        experience = user_data.get('experience', '')
        
        achievements = [
            f"Led cross-functional teams to deliver {random.randint(5, 20)}+ successful projects",
            f"Increased team productivity by {random.randint(15, 40)}% through process optimization",
            f"Reduced project delivery time by {random.randint(20, 50)}% through agile methodologies",
            f"Improved system performance by {random.randint(30, 80)}% through optimization",
            f"Generated ${random.randint(100, 500)}K+ in cost savings through automation",
            f"Received {random.randint(2, 5)} industry awards for excellence",
            f"Published {random.randint(1, 3)} articles in leading industry publications",
            f"Spoke at {random.randint(2, 8)}+ international conferences"
        ]
        
        return random.sample(achievements, random.randint(2, 4))
    
    @staticmethod
    def add_testimonials(user_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate professional testimonials"""
        name = user_data.get('name', '')
        
        testimonials = [
            {
                "quote": f"{name} is an exceptional professional who consistently delivers outstanding results. Their expertise and dedication are unmatched.",
                "author": "Sarah Williams",
                "position": "Senior Manager"
            },
            {
                "quote": f"Working with {name} was a game-changer for our project. Their innovative approach and attention to detail are remarkable.",
                "author": "Michael Chen",
                "position": "Project Director"
            },
            {
                "quote": f"{name} brings incredible value to every project. Their technical skills and leadership qualities are outstanding.",
                "author": "Emily Davis",
                "position": "CTO"
            }
        ]
        
        return random.sample(testimonials, random.randint(1, 2))
    
    @staticmethod
    def add_contact_info(user_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate professional contact information with country-specific phone formats"""
        name = user_data.get('name', 'John Doe')
        first_name = name.split()[0].lower()
        last_name = name.split()[-1].lower() if len(name.split()) > 1 else 'doe'
        
        # Country-specific phone formats with extensions
        phone_formats = [
            # United States/Canada
            f"+1 ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            # United Kingdom
            f"+44 {random.randint(20, 29)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
            # Philippines
            f"+63 {random.randint(900, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            # Australia
            f"+61 {random.randint(400, 499)} {random.randint(100, 999)} {random.randint(100, 999)}",
            # India
            f"+91 {random.randint(70, 99)}{random.randint(100, 999)} {random.randint(10000, 99999)}",
            # Singapore
            f"+65 {random.randint(8000, 9999)} {random.randint(1000, 9999)}",
            # Germany
            f"+49 {random.randint(30, 89)} {random.randint(10000000, 99999999)}",
            # France
            f"+33 {random.randint(1, 9)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
            # Japan
            f"+81 {random.randint(70, 90)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
            # South Korea
            f"+82 10 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
        ]
        
        return {
            "email": f"{first_name}.{last_name}@email.com",
            "phone": random.choice(phone_formats),
            "linkedin": f"linkedin.com/in/{first_name}-{last_name}",
            "github": f"github.com/{first_name}{last_name}",
            "website": f"{first_name}{last_name}.com"
        }
    
    @staticmethod
    def format_education(education_data: List[Dict[str, Any]]) -> str:
        """Format education information with school, dates, and details"""
        if not education_data:
            return ""
        
        def format_date(date_str: str) -> str:
            """Convert YYYY-MM to MMM YYYY format"""
            if not date_str:
                return ""
            try:
                # Handle YYYY-MM format
                if '-' in date_str and len(date_str) == 7:
                    year, month = date_str.split('-')
                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    month_name = months[int(month) - 1]
                    return f"{month_name} {year}"
                # If already in text format or just year, return as is
                return date_str
            except (ValueError, IndexError):
                return date_str
        
        formatted = []
        for edu in education_data:
            degree = edu.get('degree', '')
            school = edu.get('school', '')
            start_date = edu.get('start_date', '')
            end_date = edu.get('end_date', '')
            field = edu.get('field', '')
            gpa = edu.get('gpa', '')
            honors = edu.get('honors', '')
            
            # First line: School, Degree, Field of Study
            parts = []
            if school:
                parts.append(school)
            if degree:
                parts.append(degree)
            if field:
                parts.append(field)
            
            edu_text = ", ".join(parts)
            
            # Second line: Dates
            if start_date and end_date:
                start_formatted = format_date(start_date)
                end_formatted = format_date(end_date)
                edu_text += f"\n*{start_formatted} - {end_formatted}*"
            elif start_date:
                start_formatted = format_date(start_date)
                edu_text += f"\n*{start_formatted} - Present*"
            
            if gpa:
                edu_text += f"\nGPA: {gpa}"
            if honors:
                edu_text += f"\n{honors}"
            
            formatted.append(edu_text)
        
        return "\n\n".join(formatted)
    
    @staticmethod
    def generate_template_specific_content(template_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate unique content based on template type"""
        name = user_data.get('name', '')
        profession = user_data.get('profession', '')
        
        if template_id == 'tech_modern':
            return {
                'tagline': f'Innovative {profession} | Building the Future with Code',
                'summary_style': 'technical',
                'additional_sections': {
                    'technical_stack': 'Full-stack development expertise with modern frameworks and cloud technologies',
                    'code_philosophy': 'Clean code advocate, TDD practitioner, and continuous learner',
                    'open_source': 'Active contributor to open-source projects'
                }
            }
        
        elif template_id == 'creative_artist':
            return {
                'tagline': f'Visionary {profession} | Creating Art That Inspires',
                'summary_style': 'artistic',
                'additional_sections': {
                    'artistic_vision': 'Blending creativity with purpose to craft memorable experiences',
                    'design_philosophy': 'User-centered design with a focus on emotional connection',
                    'influences': 'Inspired by modern minimalism and bold expressionism'
                }
            }
        
        elif template_id == 'business_executive':
            return {
                'tagline': f'Strategic {profession} | Driving Growth & Innovation',
                'summary_style': 'executive',
                'additional_sections': {
                    'leadership_style': 'Transformational leader focused on empowering teams',
                    'business_impact': 'Proven track record of scaling operations and increasing revenue',
                    'strategic_vision': 'Forward-thinking approach to market disruption and innovation'
                }
            }
        
        elif template_id == 'academic_researcher':
            return {
                'tagline': f'Distinguished {profession} | Advancing Knowledge Through Research',
                'summary_style': 'academic',
                'additional_sections': {
                    'research_interests': 'Cutting-edge research in emerging fields',
                    'methodology': 'Rigorous empirical research with interdisciplinary approaches',
                    'academic_impact': 'Cited researcher with contributions to field advancement'
                }
            }
        
        elif template_id == 'freelancer_creative':
            return {
                'tagline': f'Independent {profession} | Your Vision, My Expertise',
                'summary_style': 'freelance',
                'additional_sections': {
                    'client_approach': 'Collaborative process with clear communication',
                    'availability': 'Available for projects starting immediately',
                    'satisfaction_guarantee': '100% client satisfaction with unlimited revisions'
                }
            }
        
        else:
            return {
                'tagline': f'Professional {profession}',
                'summary_style': 'standard',
                'additional_sections': {}
            }

