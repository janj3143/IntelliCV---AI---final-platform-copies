"""
AI Job Title Chat Integration Service
====================================

Provides AI-powered chat functionality for job title descriptions, meanings,
and career insights. Integrates with various AI services and maintains a
knowledge base of job title information.

Author: IntelliCV-AI Team
Date: October 2, 2025
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import logging

# Try to import AI services (can be expanded with OpenAI, Anthropic, etc.)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIJobTitleChat:
    """AI-powered chat service for job title information"""
    
    def __init__(self):
        self.knowledge_base = self._load_job_title_knowledge_base()
        self.chat_history = []
        self.response_cache = {}
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for chat interactions"""
        logger = logging.getLogger("ai_job_chat")
        logger.setLevel(logging.INFO)
        
        # Create file handler if logs directory exists
        log_dir = Path("logs")
        if log_dir.exists():
            handler = logging.FileHandler(log_dir / "ai_job_chat.log")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_job_title_knowledge_base(self) -> Dict:
        """Load comprehensive job title knowledge base"""
        try:
            kb_path = Path("ai_data/job_title_knowledge_base.json")
            if kb_path.exists():
                with open(kb_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._create_default_knowledge_base()
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return self._create_default_knowledge_base()
    
    def _create_default_knowledge_base(self) -> Dict:
        """Create default knowledge base with comprehensive job title information"""
        return {
            "job_titles": {
                "Software Engineer": {
                    "meaning": "A professional who designs, develops, tests, and maintains software applications and systems.",
                    "description": "Software Engineers apply engineering principles to create efficient, scalable, and maintainable software solutions. They work with various programming languages, frameworks, and development methodologies to build applications that solve real-world problems.",
                    "key_responsibilities": [
                        "Design and develop software applications",
                        "Write clean, efficient, and maintainable code",
                        "Perform testing and debugging of software",
                        "Collaborate with cross-functional teams",
                        "Participate in code reviews and technical discussions",
                        "Document software designs and implementations",
                        "Stay updated with latest technologies and best practices"
                    ],
                    "required_skills": [
                        "Programming languages (Python, Java, JavaScript, C++, etc.)",
                        "Software development frameworks and libraries",
                        "Version control systems (Git)",
                        "Database design and management",
                        "Problem-solving and analytical thinking",
                        "Software testing methodologies",
                        "Agile/Scrum development processes"
                    ],
                    "similar_titles": [
                        "Software Developer", "Application Developer", "Systems Developer",
                        "Full Stack Developer", "Backend Developer", "Frontend Developer"
                    ],
                    "career_progression": [
                        "Junior Software Engineer",
                        "Software Engineer",
                        "Senior Software Engineer",
                        "Lead Software Engineer",
                        "Principal Engineer",
                        "Engineering Manager"
                    ],
                    "industry_context": "Technology sector, present in all industries requiring software solutions",
                    "salary_insights": {
                        "entry_level": "$70,000 - $90,000",
                        "mid_level": "$90,000 - $130,000",
                        "senior_level": "$130,000 - $180,000+",
                        "factors": ["Location", "Company size", "Industry", "Specialization"]
                    }
                },
                "Data Scientist": {
                    "meaning": "A professional who extracts insights and knowledge from structured and unstructured data using statistical analysis and machine learning.",
                    "description": "Data Scientists combine domain expertise, programming skills, and statistical knowledge to extract meaningful insights from data. They develop predictive models, perform complex analyses, and communicate findings to stakeholders to drive business decisions.",
                    "key_responsibilities": [
                        "Collect, clean, and preprocess large datasets",
                        "Perform exploratory data analysis",
                        "Develop and validate predictive models",
                        "Create data visualizations and reports",
                        "Communicate findings to technical and non-technical stakeholders",
                        "Design and conduct experiments",
                        "Implement machine learning algorithms"
                    ],
                    "required_skills": [
                        "Python, R, or similar programming languages",
                        "Statistical analysis and hypothesis testing",
                        "Machine learning algorithms and frameworks",
                        "Data visualization tools (Matplotlib, Seaborn, Plotly)",
                        "SQL and database management",
                        "Big data technologies (Spark, Hadoop)",
                        "Domain expertise in relevant field"
                    ],
                    "similar_titles": [
                        "Data Analyst", "Machine Learning Engineer", "Research Scientist",
                        "Quantitative Analyst", "Business Intelligence Analyst", "Statistician"
                    ],
                    "career_progression": [
                        "Junior Data Scientist",
                        "Data Scientist",
                        "Senior Data Scientist",
                        "Principal Data Scientist",
                        "Data Science Manager",
                        "Chief Data Officer"
                    ],
                    "industry_context": "Technology, finance, healthcare, retail, and any data-driven industry",
                    "salary_insights": {
                        "entry_level": "$80,000 - $110,000",
                        "mid_level": "$110,000 - $150,000",
                        "senior_level": "$150,000 - $200,000+",
                        "factors": ["Industry", "Technical expertise", "Business impact", "Location"]
                    }
                },
                "Product Manager": {
                    "meaning": "A professional who guides the development and strategy of products from conception to launch and beyond.",
                    "description": "Product Managers act as the bridge between business strategy, technology, and user experience. They define product vision, prioritize features, and coordinate cross-functional teams to deliver successful products that meet market needs.",
                    "key_responsibilities": [
                        "Define product strategy and roadmap",
                        "Conduct market research and competitive analysis",
                        "Gather and prioritize product requirements",
                        "Coordinate with engineering, design, and marketing teams",
                        "Analyze product metrics and user feedback",
                        "Make data-driven product decisions",
                        "Communicate product vision to stakeholders"
                    ],
                    "required_skills": [
                        "Strategic thinking and planning",
                        "Market research and analysis",
                        "User experience design principles",
                        "Data analysis and interpretation",
                        "Project management",
                        "Communication and presentation skills",
                        "Technical understanding (varies by product)"
                    ],
                    "similar_titles": [
                        "Product Owner", "Program Manager", "Strategy Manager",
                        "Business Development Manager", "Growth Product Manager", "Technical Product Manager"
                    ],
                    "career_progression": [
                        "Associate Product Manager",
                        "Product Manager",
                        "Senior Product Manager",
                        "Principal Product Manager",
                        "Director of Product",
                        "VP of Product"
                    ],
                    "industry_context": "Technology companies, startups, and product-focused organizations",
                    "salary_insights": {
                        "entry_level": "$90,000 - $120,000",
                        "mid_level": "$120,000 - $160,000",
                        "senior_level": "$160,000 - $220,000+",
                        "factors": ["Company stage", "Product complexity", "Market size", "Location"]
                    }
                },
                "Marketing Manager": {
                    "meaning": "A professional responsible for developing and executing marketing strategies to promote products or services.",
                    "description": "Marketing Managers oversee marketing campaigns, analyze market trends, and coordinate marketing activities to achieve business objectives. They combine creative thinking with analytical skills to reach target audiences effectively.",
                    "key_responsibilities": [
                        "Develop marketing strategies and campaigns",
                        "Manage marketing budgets and resources",
                        "Analyze market trends and consumer behavior",
                        "Coordinate with creative teams and agencies",
                        "Measure and report campaign performance",
                        "Manage brand positioning and messaging",
                        "Oversee digital marketing channels"
                    ],
                    "required_skills": [
                        "Digital marketing expertise",
                        "Marketing analytics and measurement",
                        "Content creation and management",
                        "Brand management",
                        "Social media marketing",
                        "Campaign planning and execution",
                        "Budget management and ROI analysis"
                    ],
                    "similar_titles": [
                        "Digital Marketing Manager", "Brand Manager", "Campaign Manager",
                        "Growth Marketing Manager", "Content Marketing Manager", "Performance Marketing Manager"
                    ],
                    "career_progression": [
                        "Marketing Coordinator",
                        "Marketing Specialist",
                        "Marketing Manager",
                        "Senior Marketing Manager",
                        "Marketing Director",
                        "VP of Marketing"
                    ],
                    "industry_context": "All industries with customer-facing products or services",
                    "salary_insights": {
                        "entry_level": "$50,000 - $70,000",
                        "mid_level": "$70,000 - $100,000",
                        "senior_level": "$100,000 - $140,000+",
                        "factors": ["Industry", "Company size", "Marketing channels", "Results achieved"]
                    }
                },
                "Financial Analyst": {
                    "meaning": "A professional who analyzes financial data to help organizations make informed business decisions.",
                    "description": "Financial Analysts evaluate investment opportunities, assess financial performance, and create financial models to support strategic decision-making. They work with various stakeholders to provide insights on financial trends and business performance.",
                    "key_responsibilities": [
                        "Analyze financial statements and performance metrics",
                        "Create financial models and forecasts",
                        "Prepare investment recommendations",
                        "Monitor market trends and economic indicators",
                        "Conduct valuation analysis",
                        "Present findings to management and stakeholders",
                        "Assess financial risks and opportunities"
                    ],
                    "required_skills": [
                        "Financial modeling and analysis",
                        "Excel and financial software proficiency",
                        "Understanding of accounting principles",
                        "Statistical analysis and forecasting",
                        "Investment analysis and valuation",
                        "Financial reporting and presentation",
                        "Risk assessment and management"
                    ],
                    "similar_titles": [
                        "Investment Analyst", "Credit Analyst", "Budget Analyst",
                        "Research Analyst", "Business Analyst", "Portfolio Analyst"
                    ],
                    "career_progression": [
                        "Junior Financial Analyst",
                        "Financial Analyst",
                        "Senior Financial Analyst",
                        "Principal Analyst",
                        "Finance Manager",
                        "Director of Finance"
                    ],
                    "industry_context": "Financial services, corporate finance, investment firms, and consulting",
                    "salary_insights": {
                        "entry_level": "$55,000 - $75,000",
                        "mid_level": "$75,000 - $105,000",
                        "senior_level": "$105,000 - $140,000+",
                        "factors": ["Industry sector", "Geographic location", "Certification level", "Specialization"]
                    }
                }
            },
            "industry_insights": {
                "Technology": {
                    "growth_outlook": "High growth potential with increasing digitalization",
                    "key_trends": ["AI/ML adoption", "Cloud computing", "Cybersecurity", "Remote work tools"],
                    "skill_demands": ["Programming", "Data analysis", "Cloud platforms", "Security"]
                },
                "Finance": {
                    "growth_outlook": "Stable with fintech disruption opportunities",
                    "key_trends": ["Fintech innovation", "Regulatory compliance", "Digital banking", "Cryptocurrency"],
                    "skill_demands": ["Financial analysis", "Risk management", "Regulatory knowledge", "Technology literacy"]
                },
                "Healthcare": {
                    "growth_outlook": "Strong growth driven by aging population and technology",
                    "key_trends": ["Telemedicine", "Health informatics", "Personalized medicine", "AI diagnostics"],
                    "skill_demands": ["Clinical expertise", "Technology proficiency", "Data analysis", "Patient care"]
                }
            }
        }
    
    def get_job_title_description(self, job_title: str) -> Dict:
        """Get comprehensive description of a job title"""
        # Normalize job title
        normalized_title = self._normalize_job_title(job_title)
        
        # Check knowledge base
        if normalized_title in self.knowledge_base["job_titles"]:
            job_info = self.knowledge_base["job_titles"][normalized_title].copy()
            job_info["source"] = "knowledge_base"
            return job_info
        
        # If not found, try fuzzy matching
        best_match = self._find_similar_title(normalized_title)
        if best_match:
            job_info = self.knowledge_base["job_titles"][best_match].copy()
            job_info["source"] = "similar_match"
            job_info["matched_from"] = best_match
            job_info["original_query"] = job_title
            return job_info
        
        # Generate generic response
        return self._generate_generic_response(job_title)
    
    def chat_about_job_title(self, job_title: str, question: str) -> str:
        """Interactive chat about job title with context-aware responses"""
        
        # Log the interaction
        self.logger.info(f"Chat query - Title: {job_title}, Question: {question}")
        
        # Get job title information
        job_info = self.get_job_title_description(job_title)
        
        # Analyze question intent
        intent = self._analyze_question_intent(question)
        
        # Generate contextual response
        response = self._generate_contextual_response(job_info, question, intent)
        
        # Store in chat history
        self.chat_history.append({
            "timestamp": datetime.now().isoformat(),
            "job_title": job_title,
            "question": question,
            "intent": intent,
            "response": response
        })
        
        return response
    
    def _normalize_job_title(self, title: str) -> str:
        """Normalize job title for matching"""
        # Remove extra spaces, convert to title case
        normalized = re.sub(r'\s+', ' ', title.strip()).title()
        
        # Handle common variations
        variations = {
            "Software Dev": "Software Developer",
            "Data Sci": "Data Scientist",
            "PM": "Product Manager",
            "SWE": "Software Engineer",
            "ML Engineer": "Machine Learning Engineer"
        }
        
        return variations.get(normalized, normalized)
    
    def _find_similar_title(self, title: str) -> Optional[str]:
        """Find similar job title using fuzzy matching"""
        from difflib import SequenceMatcher
        
        best_match = None
        best_score = 0.6  # Minimum similarity threshold
        
        for known_title in self.knowledge_base["job_titles"].keys():
            similarity = SequenceMatcher(None, title.lower(), known_title.lower()).ratio()
            if similarity > best_score:
                best_score = similarity
                best_match = known_title
        
        return best_match
    
    def _analyze_question_intent(self, question: str) -> str:
        """Analyze the intent behind the question"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["salary", "pay", "compensation", "money", "earn"]):
            return "salary"
        elif any(word in question_lower for word in ["skills", "requirements", "qualifications", "need"]):
            return "skills"
        elif any(word in question_lower for word in ["career", "path", "progression", "advancement", "growth"]):
            return "career_path"
        elif any(word in question_lower for word in ["responsibilities", "duties", "tasks", "do", "job"]):
            return "responsibilities"
        elif any(word in question_lower for word in ["similar", "related", "like", "alternative"]):
            return "similar_roles"
        elif any(word in question_lower for word in ["industry", "sector", "field", "market"]):
            return "industry"
        elif any(word in question_lower for word in ["education", "degree", "certification", "study"]):
            return "education"
        else:
            return "general"
    
    def _generate_contextual_response(self, job_info: Dict, question: str, intent: str) -> str:
        """Generate contextual response based on intent and job information"""
        
        job_title = job_info.get("original_query", "this role")
        
        if intent == "salary":
            salary_info = job_info.get("salary_insights", {})
            if salary_info:
                response = f"💰 **Salary Information for {job_title}:**\n\n"
                response += f"• **Entry Level:** {salary_info.get('entry_level', 'Varies')}\n"
                response += f"• **Mid Level:** {salary_info.get('mid_level', 'Varies')}\n" 
                response += f"• **Senior Level:** {salary_info.get('senior_level', 'Varies')}\n\n"
                
                factors = salary_info.get("factors", [])
                if factors:
                    response += f"**Factors affecting salary:** {', '.join(factors)}"
                
                return response
            else:
                return f"Salary for {job_title} varies significantly based on location, experience, company size, and industry. Entry-level positions typically start around $50-70k, with senior roles reaching $100k+ or more."
        
        elif intent == "skills":
            skills = job_info.get("required_skills", [])
            if skills:
                response = f"🎯 **Key Skills for {job_title}:**\n\n"
                for skill in skills[:8]:  # Show top 8 skills
                    response += f"• {skill}\n"
                
                if len(skills) > 8:
                    response += f"\n*...and {len(skills) - 8} more skills*"
                
                return response
            else:
                return f"Key skills for {job_title} typically include relevant technical expertise, problem-solving abilities, communication skills, and domain-specific knowledge."
        
        elif intent == "career_path":
            progression = job_info.get("career_progression", [])
            if progression:
                response = f"🚀 **Career Progression for {job_title}:**\n\n"
                for i, role in enumerate(progression):
                    arrow = "→" if i < len(progression) - 1 else ""
                    response += f"{i+1}. {role} {arrow}\n"
                
                return response
            else:
                similar_titles = job_info.get("similar_titles", [])[:3]
                if similar_titles:
                    return f"Career progression for {job_title} often leads to senior versions of the role or related positions like: {', '.join(similar_titles)}."
                else:
                    return f"Career progression for {job_title} typically involves advancing to senior-level positions, team leadership roles, or specialized expertise areas."
        
        elif intent == "responsibilities":
            responsibilities = job_info.get("key_responsibilities", [])
            if responsibilities:
                response = f"📋 **Key Responsibilities for {job_title}:**\n\n"
                for resp in responsibilities:
                    response += f"• {resp}\n"
                
                return response
            else:
                return f"{job_title} involves various responsibilities depending on the specific organization and seniority level. Generally includes core job functions, collaboration with team members, and contributing to organizational goals."
        
        elif intent == "similar_roles":
            similar_titles = job_info.get("similar_titles", [])
            if similar_titles:
                response = f"🔗 **Similar Roles to {job_title}:**\n\n"
                for title in similar_titles:
                    response += f"• {title}\n"
                
                return response
            else:
                return f"Similar roles to {job_title} would include related positions in the same field or industry with overlapping skills and responsibilities."
        
        elif intent == "industry":
            industry_context = job_info.get("industry_context", "")
            if industry_context:
                return f"🏢 **Industry Context for {job_title}:**\n\n{industry_context}"
            else:
                return f"{job_title} can be found across various industries, with specific requirements and opportunities varying by sector."
        
        elif intent == "education":
            return f"📚 **Education for {job_title}:**\n\nEducational requirements vary by employer and experience level. Common paths include relevant bachelor's degree, professional certifications, bootcamps, or equivalent practical experience. Continuous learning and skill development are important for career advancement."
        
        else:  # general intent
            description = job_info.get("description", "")
            meaning = job_info.get("meaning", "")
            
            if description and meaning:
                response = f"ℹ️ **About {job_title}:**\n\n"
                response += f"**Definition:** {meaning}\n\n"
                response += f"**Overview:** {description}"
                return response
            else:
                return f"{job_title} is a professional role that involves specialized responsibilities and requires relevant skills and experience in the field."
    
    def _generate_generic_response(self, job_title: str) -> Dict:
        """Generate generic response for unknown job titles"""
        return {
            "meaning": f"A professional role in the {job_title} field.",
            "description": f"The {job_title} position involves specialized responsibilities and requires relevant skills and experience. Specific duties and requirements vary by organization and industry context.",
            "key_responsibilities": [
                "Perform job-specific tasks and duties",
                "Collaborate with team members and stakeholders", 
                "Meet performance objectives and standards",
                "Maintain professional development and skills",
                "Follow organizational policies and procedures"
            ],
            "required_skills": [
                "Relevant technical or domain expertise",
                "Communication and collaboration skills",
                "Problem-solving and analytical thinking",
                "Time management and organization",
                "Adaptability and continuous learning"
            ],
            "similar_titles": [
                f"Senior {job_title}",
                f"Lead {job_title}",
                f"{job_title} Specialist",
                f"{job_title} Coordinator"
            ],
            "career_progression": [
                f"Junior {job_title}",
                f"{job_title}",
                f"Senior {job_title}",
                f"Lead {job_title}",
                f"{job_title} Manager"
            ],
            "industry_context": "Varies by industry and organizational needs",
            "salary_insights": {
                "entry_level": "$40,000 - $60,000",
                "mid_level": "$60,000 - $85,000", 
                "senior_level": "$85,000 - $120,000+",
                "factors": ["Location", "Experience", "Industry", "Company size"]
            },
            "source": "generated"
        }
    
    def get_chat_analytics(self) -> Dict:
        """Get analytics on chat usage and patterns"""
        if not self.chat_history:
            return {"total_chats": 0, "popular_intents": {}, "popular_titles": {}}
        
        # Analyze chat patterns
        intents = [chat["intent"] for chat in self.chat_history]
        titles = [chat["job_title"] for chat in self.chat_history]
        
        from collections import Counter
        
        return {
            "total_chats": len(self.chat_history),
            "popular_intents": dict(Counter(intents).most_common(5)),
            "popular_titles": dict(Counter(titles).most_common(10)),
            "recent_activity": self.chat_history[-10:] if len(self.chat_history) > 10 else self.chat_history
        }
    
    def export_knowledge_base(self, file_path: str = "ai_data/job_title_knowledge_export.json"):
        """Export the knowledge base to a file"""
        try:
            export_data = {
                "knowledge_base": self.knowledge_base,
                "chat_history": self.chat_history,
                "export_timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return f"Knowledge base exported to {file_path}"
        
        except Exception as e:
            return f"Error exporting knowledge base: {e}"
    
    def add_job_title_to_knowledge_base(self, job_title: str, job_info: Dict):
        """Add new job title information to knowledge base"""
        self.knowledge_base["job_titles"][job_title] = job_info
        self.logger.info(f"Added new job title to knowledge base: {job_title}")
    
    def update_job_title_info(self, job_title: str, updates: Dict):
        """Update existing job title information"""
        if job_title in self.knowledge_base["job_titles"]:
            self.knowledge_base["job_titles"][job_title].update(updates)
            self.logger.info(f"Updated job title information: {job_title}")
        else:
            self.logger.warning(f"Job title not found for update: {job_title}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize the chat service
    chat_service = AIJobTitleChat()
    
    # Test job title description
    print("=== Job Title Description Test ===")
    job_info = chat_service.get_job_title_description("Software Engineer")
    print(f"Job Title: Software Engineer")
    print(f"Meaning: {job_info['meaning']}")
    print(f"Similar Titles: {', '.join(job_info['similar_titles'][:3])}")
    
    # Test interactive chat
    print("\n=== Interactive Chat Test ===")
    response = chat_service.chat_about_job_title("Data Scientist", "What skills do I need?")
    print(f"Question: What skills do I need for Data Scientist?")
    print(f"Response: {response}")
    
    # Test analytics
    print("\n=== Analytics Test ===")
    analytics = chat_service.get_chat_analytics()
    print(f"Total chats: {analytics['total_chats']}")
    print(f"Popular intents: {analytics['popular_intents']}")