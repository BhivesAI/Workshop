# Career Path Advisor 🎯

An AI-powered career planning system that creates personalized learning roadmaps using Microsoft Learn resources. Powered by Azure OpenAI GPT-4o and designed to help aspiring tech professionals navigate their learning journey.

## Overview

This system uses **3 specialized AI agents** working together to understand your career goals and create a structured learning path:

1. **Profile Agent** - Learns about your background, goals, and time commitment
2. **Research Agent** - Searches Microsoft Learn for courses, certifications, and labs
3. **Advisor Agent** - Creates a personalized, phased learning roadmap

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                              │
│      "I want to become a cloud developer"                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PROFILE AGENT                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Gathers via conversation:                                │  │
│  │  • Career goal (cloud dev, data scientist, etc.)          │  │
│  │  • Current level (beginner/intermediate/advanced)         │  │
│  │  • Existing skills (languages/tools)                      │  │
│  │  • Time commitment (hours per week)                       │  │
│  │  • Target timeline (3 months, 6 months, 1 year)          │  │
│  │                                                           │  │
│  │  Outputs: PROFILE_COMPLETE with structured data          │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH AGENT                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Searches Microsoft Learn via MCP for:                    │  │
│  │  • Foundational courses (beginner level)                  │  │
│  │  • Intermediate modules (skill building)                  │  │
│  │  • Advanced topics (specialization)                       │  │
│  │  • Certifications (career milestones)                     │  │
│  │  • Hands-on labs (practical experience)                   │  │
│  │                                                           │  │
│  │  Returns 5-7 resources with:                             │  │
│  │  - Title, Type, Level, Duration, URL                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ADVISOR AGENT                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Creates personalized roadmap with:                       │  │
│  │                                                           │  │
│  │  PHASE 1: FOUNDATION (Months 1-2)                        │  │
│  │  • Beginner courses and fundamentals                     │  │
│  │  • Estimated time commitment                             │  │
│  │                                                           │  │
│  │  PHASE 2: SKILL BUILDING (Months 3-4)                    │  │
│  │  • Intermediate modules and practical labs               │  │
│  │  • Real-world project practice                           │  │
│  │                                                           │  │
│  │  PHASE 3: SPECIALIZATION (Months 5-6)                    │  │
│  │  • Advanced topics and deep dives                        │  │
│  │  • Certification preparation                             │  │
│  │                                                           │  │
│  │  CERTIFICATION TARGET                                     │  │
│  │  • Recommended certification with exam link              │  │
│  │                                                           │  │
│  │  WEEKLY COMMITMENT & NEXT STEPS                          │  │
│  │  • Realistic timeline based on availability              │  │
│  │  • Immediate actionable steps                            │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              PERSONALIZED LEARNING ROADMAP                      │
│         Ready to start your career journey! 🚀                  │
└─────────────────────────────────────────────────────────────────┘
```

## Features

✅ **Conversational Profile Building** - Natural Q&A to understand your background  
✅ **Microsoft Learn Integration** - Real-time search of courses, certifications, and labs  
✅ **Phased Learning Plans** - Structured progression from beginner to advanced  
✅ **Realistic Time Estimates** - Based on your weekly time commitment  
✅ **Certification Guidance** - Clear certification targets for career advancement  
✅ **Personalized Recommendations** - Tailored to your existing skills and goals  

## Prerequisites

- Python 3.8+
- Azure OpenAI account with GPT-4o deployment
- Internet connection for Microsoft Learn API access

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd career-path-advisor
```

### 2. Create virtual environment
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install python-dotenv
pip install agent-framework --pre
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Azure OpenAI Credentials
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

⚠️ **Security Note**: Always add `.env` to your `.gitignore` file!



## Usage

Run the career advisor:

```bash
python career_path_advisor.py
```

### Example Session

```
======================================================================
🎯 CAREER PATH ADVISOR - Powered by Microsoft Learn
======================================================================

Let's plan your tech career journey!

What tech career are you interested in? I want to become a cloud developer

[1/3] UNDERSTANDING YOUR GOALS...

What's your current experience level? (beginner/intermediate/advanced)

> beginner

[1/3] UNDERSTANDING YOUR GOALS...

What programming languages or tools do you already know?

> I know Python and a bit of JavaScript

[1/3] UNDERSTANDING YOUR GOALS...

How many hours per week can you dedicate to learning?

> 10 hours

[1/3] UNDERSTANDING YOUR GOALS...

What's your target timeline? (3 months, 6 months, 1 year)

> 6 months

[1/3] UNDERSTANDING YOUR GOALS...

PROFILE_COMPLETE
- Goal: cloud developer
- Level: beginner
- Skills: Python, JavaScript
- Time: 10 hours per week
- Timeline: 6 months

[2/3] FINDING LEARNING RESOURCES...

RESOURCE: Microsoft Azure Fundamentals
TYPE: course
LEVEL: beginner
DURATION: 8 hours
DOCS: https://learn.microsoft.com/training/paths/azure-fundamentals/
---
RESOURCE: Build cloud-native apps with Azure
TYPE: module
LEVEL: intermediate
DURATION: 12 hours
DOCS: https://learn.microsoft.com/training/paths/build-cloud-native/
---
RESOURCE: Azure Developer Associate Certification
TYPE: certification
LEVEL: intermediate
DURATION: 40 hours prep
DOCS: https://learn.microsoft.com/certifications/azure-developer/
---
...

[3/3] CREATING YOUR PERSONALIZED ROADMAP...

**YOUR CAREER PATH: Cloud Developer**

**PHASE 1: FOUNDATION (Months 1-2)**
- Azure Fundamentals: Learn cloud concepts and Azure basics
- Python for Cloud: Apply existing Python skills to cloud
- Estimated time: 80 hours

**PHASE 2: SKILL BUILDING (Months 3-4)**
- Build Cloud-Native Apps: Hands-on Azure development experience
- Azure DevOps Basics: CI/CD and deployment automation
- Estimated time: 80 hours

**PHASE 3: SPECIALIZATION (Months 5-6)**
- Advanced Azure Services: Deep dive into Azure capabilities
- Certification Prep: Azure Developer Associate exam preparation
- Estimated time: 80 hours

**CERTIFICATION TARGET**
- Azure Developer Associate (AZ-204): Industry-recognized cloud developer credential
- Exam link: https://learn.microsoft.com/certifications/azure-developer/

**WEEKLY COMMITMENT**
Based on 10 hours/week: 6-month timeline is realistic and achievable

**NEXT STEPS**
1. Start with Azure Fundamentals course this week
2. Set up free Azure account for practice
3. Track progress using Microsoft Learn profile

======================================================================
✅ YOUR PERSONALIZED LEARNING PATH IS READY!
======================================================================

💡 Tip: Bookmark the resource links and start with Phase 1!
```

## Career Paths Supported

The advisor can create learning paths for various tech careers:

- **Cloud Developer** - Azure, AWS, cloud-native applications
- **Data Scientist** - Machine learning, data analysis, AI
- **DevOps Engineer** - CI/CD, automation, infrastructure
- **Full Stack Developer** - Web development, frontend + backend
- **Cybersecurity Specialist** - Security, compliance, threat detection
- **AI/ML Engineer** - Artificial intelligence, machine learning models
- **Mobile Developer** - iOS, Android, cross-platform apps
- **Game Developer** - Game engines, graphics, gameplay programming

## How It Works

### 1. Profile Agent
The Profile Agent asks targeted questions to understand:
- **Career Goal**: What role you're aiming for
- **Experience Level**: Beginner, intermediate, or advanced
- **Existing Skills**: Languages and tools you already know
- **Time Commitment**: How many hours per week you can dedicate
- **Timeline**: When you want to achieve your goal

This information is used to personalize the entire learning path.

### 2. Research Agent
Uses the **Microsoft Learn MCP (Model Context Protocol)** to search for:
- **Courses**: Structured learning modules
- **Certifications**: Industry-recognized credentials
- **Labs**: Hands-on practice environments
- **Documentation**: In-depth technical references

The agent prioritizes resources that match your experience level and career goal.

### 3. Advisor Agent
Creates a **phased learning roadmap** with:
- **3 Phases**: Foundation → Skill Building → Specialization
- **Time Estimates**: Based on your weekly commitment
- **Certification Goals**: Clear credential targets
- **Next Steps**: Immediate actionable items

The roadmap is realistic and accounts for your time availability.


## Configuration

### Agent Settings

- **Temperature**: 0.0 (deterministic, consistent responses)
- **Max Tokens**: Varies by agent (Profile: 150, Research: 300, Advisor: 500)
- **Model**: Azure OpenAI GPT-4o (best instruction-following)

### Microsoft Learn MCP
- **Timeout**: 30 seconds
- **Request Timeout**: 30 seconds
- **Auto-cleanup**: Handled automatically after session

## Troubleshooting

### "Azure OpenAI credentials not found"
**Solution**: 
- Ensure `.env` file exists in project root
- Verify all required variables are set
- Check for typos in variable names
- Make sure there are no extra spaces in values


## Best Practices

### For Best Results:
1. **Be specific** about your career goal
2. **Be honest** about your current skill level
3. **Be realistic** about time commitment
4. **Follow the phases** in order - don't skip ahead
5. **Track your progress** using Microsoft Learn profiles
6. **Practice consistently** - even 1 hour daily is better than 10 hours once a week

### Time Commitment Guidelines:
- **Beginner to Job-Ready**: 6-12 months (10-15 hours/week)
- **Career Pivot**: 12-18 months (10-15 hours/week)
- **Skill Enhancement**: 3-6 months (5-10 hours/week)
- **Certification Prep**: 1-3 months (10-20 hours/week)

## Example Use Cases

### Use Case 1: Complete Beginner
```
Goal: "I want to become a web developer"
Level: Beginner
Skills: None
Time: 15 hours/week
Timeline: 1 year

→ Advisor creates path starting from HTML/CSS basics
→ Progresses through JavaScript, frameworks, backend
→ Targets industry certification
```

### Use Case 2: Career Pivot
```
Goal: "I want to move from software dev to cloud engineering"
Level: Intermediate
Skills: Java, SQL
Time: 10 hours/week
Timeline: 6 months

→ Advisor leverages existing programming skills
→ Focuses on cloud-specific knowledge gaps
→ Accelerated path to Azure certifications
```

### Use Case 3: Skill Enhancement
```
Goal: "I want to add machine learning to my skillset"
Level: Advanced programmer
Skills: Python, statistics
Time: 8 hours/week
Timeline: 4 months

→ Advisor skips programming fundamentals
→ Focuses directly on ML concepts and frameworks
→ Emphasizes hands-on projects and certifications
```

## Technologies Used

- **Azure OpenAI GPT-4o** - AI agents for profile analysis and recommendations
- **Microsoft Agent Framework** - Multi-agent orchestration system
- **MCP (Model Context Protocol)** - Integration with Microsoft Learn API
- **Python asyncio** - Asynchronous execution for performance
- **python-dotenv** - Secure environment variable management

