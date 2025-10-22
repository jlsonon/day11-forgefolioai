import os
import json
from groq import Groq
from typing import Dict, List, Any, Optional
from portfolio_templates import PortfolioTemplates, SampleData, PortfolioEnhancer

class GroqClient:
    """Client for interacting with Groq API"""
    client: Optional[Groq]
    model: str
    api_key: Optional[str]
    demo_mode: bool
    
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

        # Prefer a stronger default model if available
        self.model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    def generate_portfolio(self, user_data: Dict[str, Any], template_id: Optional[str] = None) -> Dict[str, Any]:
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
            # Safety: client must be available here (demo handled earlier)
            if self.client is None:
                raise RuntimeError("Groq client is not initialized")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional portfolio generator creating a {template['name']} portfolio. Create compelling, well-structured content that showcases the user's skills and experience effectively. Use the {template['style']} style with a {template['tone']} tone. Focus on {template['focus']}. Format content using {template['format']}. Make this portfolio UNIQUE and different from other templates."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Increased for more creative variations
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            structured_content = self._structure_portfolio_content(content, template)
            
            # Add enhanced features to the structured content
            structured_content['achievements'] = PortfolioEnhancer.add_achievements(user_data)
            structured_content['testimonials'] = PortfolioEnhancer.add_testimonials(user_data)
            structured_content['contact'] = PortfolioEnhancer.add_contact_info(user_data)
            structured_content['template_specific'] = PortfolioEnhancer.generate_template_specific_content(template_id, user_data)
            
            # Format education if provided
            if 'education' in user_data and user_data['education']:
                structured_content['education'] = PortfolioEnhancer.format_education(user_data['education'])
            
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
    
    def _generate_enhanced_demo_portfolio(self, user_data: Dict[str, Any], template_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate an enhanced demo portfolio with templates and additional features"""
        if not template_id:
            template_id = PortfolioTemplates.get_template_for_profession(user_data.get('profession', ''))
        
        template = PortfolioTemplates.get_template(template_id)
        
        # Generate template-specific content
        template_content = PortfolioEnhancer.generate_template_specific_content(template_id, user_data)
        
        # Generate base content with template-specific variations
        base_content = self._generate_template_specific_demo(user_data, template, template_content)
        
        # Format education if provided
        education_formatted = ""
        if 'education' in user_data and user_data['education']:
            education_formatted = PortfolioEnhancer.format_education(user_data['education'])
        
        # Add enhanced features
        enhanced_content = {
            'template': template,
            'tagline': template_content.get('tagline', ''),
            'summary': self._extract_section(base_content, 'Professional Summary'),
            'skills': self._extract_section(base_content, 'Technical Skills') or self._extract_section(base_content, 'Skills'),
            'experience': self._extract_section(base_content, 'Professional Experience'),
            'education': education_formatted or user_data.get('education', ''),
            'projects': self._extract_section(base_content, 'Key Projects'),
            'conclusion': self._extract_section(base_content, 'Conclusion'),
            'achievements': PortfolioEnhancer.add_achievements(user_data),
            'testimonials': PortfolioEnhancer.add_testimonials(user_data),
            'contact': self._get_contact_info(user_data),
            'template_specific': template_content,
            'raw_content': base_content
        }
        
        return enhanced_content
    
    def _generate_template_specific_demo(self, user_data: Dict[str, Any], template: Dict[str, Any], template_content: Dict[str, Any]) -> str:
        """Generate demo content tailored to specific template type"""
        name = user_data.get('name', 'John Doe')
        profession = user_data.get('profession', 'Software Developer')
        experience = user_data.get('experience', '5 years of experience')
        skills = user_data.get('skills', ['Python', 'JavaScript', 'React'])
        projects = user_data.get('projects', ['E-commerce Platform', 'Task Management App'])
        
        # Template-specific content generation
        if template['style'] == 'modern':
            return f"""
**Professional Summary**
{name} is a forward-thinking {profession} with {experience}. Passionate about leveraging cutting-edge technologies to build scalable, performant applications. Known for writing clean, maintainable code and driving technical innovation.

**Technical Skills**
• Programming: {', '.join(skills[:3]) if len(skills) >= 3 else ', '.join(skills)}
• Frameworks & Tools: Modern development stack with cloud deployment expertise
• Best Practices: TDD, CI/CD, Agile methodologies, Code reviews
• Problem-solving: Complex algorithmic challenges, System design
• Collaboration: Cross-functional team leadership, Technical mentorship

**Professional Experience**
{experience} specializing in full-stack development and architecture design. Led development of high-impact applications serving thousands of users. Implemented automated testing strategies that reduced bugs by 60%. Optimized database queries resulting in 3x performance improvement.

**Key Projects**
{chr(10).join([f"• {project} - Architected and developed scalable solution with modern tech stack" for project in projects])}
• Performance Optimization Initiative - Reduced load time by 70% through code splitting and caching
• Microservices Migration - Transformed monolithic app to microservices architecture

**Conclusion**
{name} combines technical expertise with innovative problem-solving to deliver exceptional results. Ready to tackle challenging projects and contribute to cutting-edge technology initiatives.
            """
        
        elif template['style'] == 'creative':
            return f"""
**Professional Summary**
{name} is a visionary {profession} who transforms ideas into captivating experiences. With {experience} of pushing creative boundaries, {name} brings artistry and innovation to every project. Believes in design that not only looks beautiful but tells a story and creates emotional connections.

**Skills & Expertise**
• Creative Tools: {', '.join(skills[:3]) if len(skills) >= 3 else ', '.join(skills)}
• Design Philosophy: User-centered, emotionally engaging, purposefully bold
• Artistic Vision: Blending modern aesthetics with timeless principles
• Collaboration: Working closely with clients to bring their vision to life
• Innovation: Staying ahead of design trends while maintaining authenticity

**Professional Experience**
{experience} crafting memorable brand experiences and digital products. Worked with diverse clients from startups to Fortune 500 companies. Specialized in creating designs that resonate with target audiences and drive engagement. Award-winning portfolio showcasing range and versatility.

**Portfolio Highlights**
{chr(10).join([f"• {project} - Created stunning visual identity that increased brand recognition by 40%" for project in projects])}
• Brand Reimagining Campaign - Complete visual overhaul that modernized company image
• Interactive Experience Design - Immersive digital experience with 95% positive feedback

**Conclusion**
{name} is passionate about creating design that matters. Every project is an opportunity to push creative boundaries and deliver work that exceeds expectations. Let's create something extraordinary together.
            """
        
        elif template['style'] == 'corporate':
            return f"""
**Executive Summary**
{name} is a results-driven {profession} with {experience} delivering strategic leadership and measurable business outcomes. Proven track record of scaling operations, driving revenue growth, and building high-performing teams. Expert in transforming organizational challenges into competitive advantages.

**Core Competencies**
• Leadership: {', '.join(skills[:3]) if len(skills) >= 3 else ', '.join(skills)}
• Strategic Planning: Long-term vision with actionable execution plans
• Financial Acumen: P&L management, budget optimization, ROI maximization
• Team Development: Building and mentoring world-class teams
• Change Management: Leading organizational transformations

**Professional Experience**
{experience} in executive leadership roles across diverse industries. Successfully led multiple business units to achieve record-breaking performance. Implemented strategic initiatives resulting in $5M+ revenue increase. Spearheaded digital transformation that improved operational efficiency by 45%.

**Key Achievements**
{chr(10).join([f"• {project} - Strategic initiative that delivered 150% ROI within 18 months" for project in projects])}
• Market Expansion - Entered 3 new markets, establishing strong competitive position
• Operational Excellence - Reduced costs by $2M while improving quality metrics

**Conclusion**
{name} brings strategic vision, operational excellence, and proven leadership to drive organizational success. Ready to lead your company to new heights of achievement.
            """
        
        elif template['style'] == 'academic':
            return f"""
**Professional Summary**
{name} is a distinguished {profession} with {experience} advancing knowledge through rigorous research and scholarly contributions. Research focuses on innovative methodologies and interdisciplinary approaches. Committed to academic excellence and mentoring the next generation of scholars.

**Research Expertise**
• Research Areas: {', '.join(skills[:3]) if len(skills) >= 3 else ', '.join(skills)}
• Methodologies: Quantitative and qualitative research, Statistical analysis
• Publications: Peer-reviewed journals, Conference proceedings
• Grants: Successful track record securing research funding
• Collaboration: International research networks and partnerships

**Academic Experience**
{experience} in research and teaching at leading institutions. Principal investigator on multiple funded research projects. Published extensively in top-tier journals with significant citation impact. Presented research at international conferences and symposia.

**Key Research Projects**
{chr(10).join([f"• {project} - Groundbreaking research published in leading journal" for project in projects])}
• Interdisciplinary Research Initiative - Collaborative study with $500K funding
• Innovation in Methodology - Developed novel research framework adopted by peers

**Conclusion**
{name} is dedicated to advancing knowledge and contributing to academic discourse. Seeking opportunities for impactful research collaboration and scholarly exchange.
            """
        
        else:  # freelance
            return f"""
**Professional Summary**
{name} is an independent {profession} with {experience} delivering exceptional results for clients worldwide. Specializes in providing personalized, high-quality services tailored to each client's unique needs. Committed to excellence, timely delivery, and building long-term partnerships.

**Services & Skills**
• Expertise: {', '.join(skills[:3]) if len(skills) >= 3 else ', '.join(skills)}
• Client-Focused: Clear communication, transparent processes
• Flexible: Adaptable to project requirements and timelines
• Quality-Driven: Meticulous attention to detail, unlimited revisions
• Reliable: On-time delivery, responsive communication

**Professional Experience**
{experience} working with diverse clients from startups to established businesses. Successfully completed 50+ projects with 98% client satisfaction rate. Known for exceeding expectations and delivering work that drives real business results. Available for both short-term and long-term collaborations.

**Featured Projects**
{chr(10).join([f"• {project} - Delivered ahead of schedule with client praising 'exceptional quality'" for project in projects])}
• Client Success Story - Project that increased client revenue by 200%
• Long-term Partnership - 2-year engagement with Fortune 500 company

**Conclusion**
{name} is ready to bring your vision to life with expertise, dedication, and personalized service. Let's discuss how we can work together to achieve your goals. Available for new projects starting immediately.
            """
    
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
        education_data = user_data.get('education', [])
        
        # Format education information for the prompt
        education_text = ""
        if education_data:
            education_parts = []
            for edu in education_data:
                degree = edu.get('degree', '')
                school = edu.get('school', '')
                field = edu.get('field', '')
                start_date = edu.get('start_date', '')
                end_date = edu.get('end_date', '')
                
                edu_str = f"{degree}"
                if field:
                    edu_str += f" in {field}"
                if school:
                    edu_str += f" from {school}"
                if start_date and end_date:
                    edu_str += f" ({start_date} - {end_date})"
                education_parts.append(edu_str)
            
            education_text = "\n".join(education_parts)
        
        prompt = f"""
        Create a UNIQUE and DISTINCT {template['name']} portfolio for the following person:
        
        Name: {name}
        Profession: {profession}
        Experience: {experience}
        Skills: {', '.join(skills) if skills else 'Not specified'}
        Projects: {', '.join(projects) if projects else 'Not specified'}
        Education: {education_text if education_text else 'Not specified'}
        
        Template Style: {template['style']}
        Tone: {template['tone']}
        Focus Areas: {template['focus']}
        Format Style: {template['format']}
        Required Sections: {', '.join(template['sections'])}
        
        IMPORTANT: Make this portfolio COMPLETELY DIFFERENT from other templates:
        - For {template['style']} style: Use {template['tone']} language
        - Focus specifically on: {template['focus']}
        - Format using: {template['format']}
        - Include unique insights and perspectives relevant to this template type
        
        Please generate a comprehensive portfolio that includes:
        1. A compelling professional summary that matches the {template['tone']} tone
        2. Detailed skills section with both technical and soft skills
        3. Professional experience with quantifiable achievements and specific metrics
        4. Key projects with detailed impact descriptions and outcomes
        5. Professional achievements and recognitions
        6. Educational background with full details
        7. Additional sections relevant to {template['style']} style
        8. A strong professional conclusion
        
        Make the content engaging, professional, and specifically tailored to the {template['style']} style.
        Use proper formatting with clear sections, bullet points, and professional language.
        Include specific metrics, achievements, and measurable outcomes wherever possible.
        Ensure this portfolio feels UNIQUE and matches the specific template type.
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
            if self.client is None:
                return False
            _ = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False
