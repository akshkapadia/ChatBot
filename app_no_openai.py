from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Core system instructions
CORE_INSTRUCTIONS = """
You are Recruity, an intelligent and professional recruitment assistant chatbot.
You ONLY help with job-related and career guidance topics.
"""

# Comprehensive recruitment knowledge base
RECRUITMENT_KNOWLEDGE = {
    "resume": {
        "keywords": ["resume", "cv", "curriculum vitae", "application"],
        "response": """**📄 Resume Building Guide:**

**Structure & Format:**
• Use a clean, professional layout (Arial, Calibri, or Times New Roman)
• Keep it to 1-2 pages maximum
• Use consistent formatting and bullet points
• Include clear section headers

**Essential Sections:**
• **Contact Information** - Name, phone, email, LinkedIn, location
• **Professional Summary** - 2-3 sentences highlighting your value
• **Work Experience** - Reverse chronological order with achievements
• **Education** - Degree, institution, graduation year
• **Skills** - Technical and soft skills relevant to the role

**Content Tips:**
• Use action verbs (achieved, implemented, led, developed)
• Quantify accomplishments with numbers and percentages
• Tailor content to each specific job application
• Include relevant keywords from job descriptions

**Common Mistakes to Avoid:**
• Spelling and grammar errors
• Generic, one-size-fits-all content
• Including irrelevant personal information
• Using outdated or unprofessional email addresses

**ATS Optimization:**
• Use standard section headings
• Avoid complex formatting, tables, or graphics
• Include relevant keywords naturally
• Save as both PDF and Word formats"""
    },
    
    "interview": {
        "keywords": ["interview", "interviewing", "job interview", "interview tips"],
        "response": """**🎯 Interview Mastery Guide:**

**Pre-Interview Preparation:**
• **Research the Company** - Mission, values, recent news, competitors
• **Study the Job Description** - Match your skills to requirements
• **Prepare STAR Examples** - Situation, Task, Action, Result stories
• **Practice Common Questions** - Rehearse out loud or with friends
• **Prepare Questions to Ask** - Show genuine interest and engagement

**During the Interview:**
• **Arrive Early** - 10-15 minutes before scheduled time
• **Professional Appearance** - Dress appropriately for company culture
• **Body Language** - Maintain eye contact, firm handshake, good posture
• **Listen Actively** - Take time to understand questions fully
• **Be Specific** - Use concrete examples and quantifiable results

**Common Interview Questions:**
• "Tell me about yourself" - 2-minute professional summary
• "Why do you want this job?" - Connect your goals to the role
• "What are your strengths/weaknesses?" - Be honest but strategic
• "Describe a challenge you overcame" - Use STAR method
• "Where do you see yourself in 5 years?" - Show ambition and loyalty

**Post-Interview:**
• **Send Thank-You Email** - Within 24 hours to all interviewers
• **Reiterate Interest** - Mention specific discussion points
• **Follow Up Appropriately** - If no response after stated timeline
• **Continue Job Search** - Don't put all eggs in one basket"""
    },
    
    "career_path": {
        "keywords": ["career", "career path", "career change", "professional development"],
        "response": """**🚀 Career Development Strategy:**

**Self-Assessment Phase:**
• **Identify Strengths** - What are you naturally good at?
• **Clarify Values** - What matters most to you in work?
• **Assess Interests** - What activities energize you?
• **Evaluate Skills** - Technical and soft skills inventory
• **Define Goals** - Short-term (1-2 years) and long-term (5-10 years)

**Skill Development:**
• **Identify Gaps** - Compare current skills to target role requirements
• **Create Learning Plan** - Online courses, certifications, workshops
• **Build Portfolio** - Projects that demonstrate your capabilities
• **Seek Mentorship** - Find guides in your target field
• **Practice Continuously** - Apply new skills in current role or side projects

**Career Transition Strategy:**
• **Network Strategically** - Connect with professionals in target field
• **Gain Relevant Experience** - Volunteer, freelance, or side projects
• **Update Your Brand** - LinkedIn, resume, portfolio alignment
• **Consider Gradual Transition** - Part-time or consulting opportunities
• **Financial Planning** - Prepare for potential income changes

**Professional Growth:**
• **Stay Industry Current** - Follow trends, news, and innovations
• **Attend Events** - Conferences, meetups, professional associations
• **Seek Challenging Projects** - Stretch assignments in current role
• **Document Achievements** - Keep record of accomplishments
• **Regular Review** - Assess progress and adjust plans quarterly"""
    },
    
    "data_science": {
        "keywords": ["data science", "data scientist", "machine learning", "ai", "analytics"],
        "response": """**📊 Data Science Career Roadmap:**

**Foundation Skills (3-6 months):**
• **Programming** - Python (pandas, numpy) or R
• **Statistics** - Descriptive stats, probability, hypothesis testing
• **SQL** - Database querying and data manipulation
• **Excel** - Advanced functions, pivot tables, data analysis

**Intermediate Skills (6-12 months):**
• **Machine Learning** - Scikit-learn, supervised/unsupervised learning
• **Data Visualization** - Matplotlib, Seaborn, Tableau, Power BI
• **Data Cleaning** - Handling missing data, outliers, preprocessing
• **Version Control** - Git and GitHub for project management

**Advanced Skills (12+ months):**
• **Deep Learning** - TensorFlow, PyTorch, neural networks
• **Big Data** - Spark, Hadoop, cloud platforms (AWS, Azure, GCP)
• **MLOps** - Model deployment, monitoring, CI/CD pipelines
• **Specialized Areas** - NLP, computer vision, time series analysis

**Portfolio Projects:**
• **Exploratory Data Analysis** - Clean, analyze, and visualize dataset
• **Prediction Model** - Build and evaluate machine learning model
• **End-to-End Project** - Data collection to deployment
• **Domain-Specific Project** - Healthcare, finance, marketing, etc.

**Career Preparation:**
• **Kaggle Competitions** - Practice and showcase skills
• **GitHub Portfolio** - Well-documented projects with README files
• **Technical Blog** - Write about projects and learnings
• **Networking** - Join data science communities and meetups"""
    },
    
    "software_engineering": {
        "keywords": ["software engineer", "developer", "programming", "coding", "web development"],
        "response": """**💻 Software Engineering Career Roadmap:**

**Programming Fundamentals (2-4 months):**
• **Choose a Language** - Python, JavaScript, Java, or C++
• **Basic Concepts** - Variables, functions, loops, conditionals
• **Data Structures** - Arrays, lists, dictionaries, sets
• **Algorithms** - Sorting, searching, basic problem-solving

**Web Development (4-8 months):**
• **Frontend** - HTML, CSS, JavaScript, React/Angular/Vue
• **Backend** - Node.js, Python (Django/Flask), or Java (Spring)
• **Databases** - SQL (PostgreSQL, MySQL) and NoSQL (MongoDB)
• **APIs** - RESTful services, HTTP methods, JSON

**Advanced Concepts (8-12 months):**
• **System Design** - Scalability, load balancing, microservices
• **DevOps** - Docker, CI/CD, cloud deployment (AWS, Azure)
• **Testing** - Unit tests, integration tests, TDD
• **Security** - Authentication, authorization, common vulnerabilities

**Portfolio Development:**
• **Personal Website** - Showcase your skills and projects
• **Full-Stack Application** - Complete web application with database
• **API Project** - Build and document a RESTful API
• **Open Source Contributions** - Contribute to existing projects

**Interview Preparation:**
• **LeetCode/HackerRank** - Practice coding problems daily
• **System Design** - Learn to design scalable systems
• **Behavioral Questions** - Prepare STAR method examples
• **Mock Interviews** - Practice with peers or platforms like Pramp"""
    },
    
    "salary_negotiation": {
        "keywords": ["salary", "negotiation", "compensation", "pay", "benefits"],
        "response": """**💰 Salary Negotiation Mastery:**

**Research Phase:**
• **Market Research** - Use Glassdoor, PayScale, levels.fyi, LinkedIn Salary
• **Location Factors** - Cost of living adjustments for your area
• **Company Size** - Startups vs. corporations have different structures
• **Industry Standards** - Tech, finance, healthcare have different ranges
• **Your Experience Level** - Junior, mid-level, senior compensation bands

**Preparation Strategy:**
• **Document Achievements** - Quantify your impact with numbers
• **Total Compensation** - Base salary, bonus, equity, benefits, PTO
• **Know Your Worth** - Calculate your value based on skills and experience
• **Set Your Range** - Minimum acceptable, target, and stretch goals
• **Practice Your Pitch** - Rehearse your negotiation conversation

**Negotiation Tactics:**
• **Timing Matters** - After job offer, during performance reviews
• **Start High** - Anchor with a number above your target
• **Be Professional** - Collaborative, not confrontational approach
• **Use Data** - Reference market research and your achievements
• **Consider Everything** - Flexible work, professional development, title

**Common Mistakes to Avoid:**
• **Accepting First Offer** - Almost always room for negotiation
• **Only Focusing on Salary** - Benefits can add significant value
• **Being Emotional** - Keep discussions fact-based and professional
• **Not Having Alternatives** - BATNA (Best Alternative to Negotiated Agreement)
• **Negotiating Too Early** - Wait until you have a firm offer

**Follow-Up:**
• **Get Everything in Writing** - Confirm agreed terms via email
• **Express Gratitude** - Thank them for working with you
• **Set Review Timeline** - When will compensation be reviewed again?"""
    }
}

def get_relevant_response(message):
    """Get relevant response based on message content"""
    lower_message = message.lower()
    
    # Check for off-topic questions
    off_topic_keywords = [
        "weather", "sports", "entertainment", "music", "movies", "food", 
        "travel", "politics", "personal life", "dating", "health", "medical",
        "cooking", "recipes", "games", "celebrities"
    ]
    
    if any(keyword in lower_message for keyword in off_topic_keywords):
        return "I'm Recruity, your career advisor. I'm here to assist with recruitment and job-related topics only. Could you please ask something related to careers, interviews, or job search?"
    
    # Check for job-related content
    job_indicators = [
        "job", "career", "work", "interview", "resume", "cv", "salary", 
        "skills", "training", "professional", "employment", "hiring"
    ]
    
    is_job_related = any(indicator in lower_message for indicator in job_indicators)
    
    if is_job_related:
        # Find specific topic match
        for topic, data in RECRUITMENT_KNOWLEDGE.items():
            if any(keyword in lower_message for keyword in data["keywords"]):
                return data["response"]
        
        # General job-related response
        return """**🎯 Welcome to Recruity - Your AI Career Coach!**

I can help you with:

**📄 Resume & CV Building**
• Structure, formatting, and content optimization
• ATS-friendly resume tips
• Industry-specific resume guidance

**🎯 Interview Preparation**
• Common interview questions and answers
• STAR method for behavioral questions
• Company research strategies

**🚀 Career Development**
• Career path planning and transitions
• Skill development roadmaps
• Professional networking strategies

**💰 Salary Negotiation**
• Market research and compensation analysis
• Negotiation tactics and timing
• Total compensation evaluation

**🔧 Technical Career Paths**
• Data Science, Software Engineering, Product Management
• Skill requirements and learning resources
• Portfolio development guidance

What specific area would you like to focus on today?"""
    
    # Redirect if not job-related
    return "I'm here to assist with recruitment and job-related topics. Could you please ask something related to careers, interviews, job search, or professional development?"

def format_response_for_display(response):
    """Format the response with proper HTML for better display"""
    # Replace bullet points with HTML list items
    response = re.sub(r'•\s*([^\n]+)', r'<li>\1</li>', response)
    
    # Wrap consecutive list items in ul tags
    response = re.sub(r'(<li>.*?</li>)(?:\s*<li>.*?</li>)*', 
                     lambda m: '<ul>' + m.group(0) + '</ul>', 
                     response, flags=re.DOTALL)
    
    # Format bold text
    response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
    
    # Convert line breaks to HTML breaks
    response = response.replace('\n\n', '</p><p>')
    response = response.replace('\n', '<br>')
    
    # Wrap in paragraph tags if not already formatted
    if not response.startswith('<'):
        response = '<p>' + response + '</p>'
    
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message or not isinstance(message, str):
            return jsonify({'response': 'Please provide a valid message.'}), 400
        
        # Get response from knowledge base
        response = get_relevant_response(message)
        
        # Format response for better display
        formatted_response = format_response_for_display(response)
        
        return jsonify({
            'response': formatted_response,
            'source': 'knowledge_base'
        })
        
    except Exception as e:
        print(f"Error processing request: {e}")
        fallback_response = "I'm here to help with your career questions! Ask me about resumes, interviews, career paths, or job search strategies."
        formatted_fallback = format_response_for_display(fallback_response)
        
        return jsonify({
            'response': formatted_fallback,
            'source': 'fallback',
            'error': True
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
