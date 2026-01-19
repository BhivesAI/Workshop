"""
career_path_advisor.py
AI-Powered Career Path Advisor for Tech Careers

This is a beginner-friendly multi-agent system that helps users plan their tech career.
It uses 3 AI agents working together:
1. Profile Agent - Asks questions to understand your background and goals
2. Research Agent - Searches Microsoft Learn for courses and certifications
3. Advisor Agent - Creates a personalized learning roadmap

Technology Stack:
- Azure OpenAI GPT-4o (the AI brain)
- Microsoft Learn (knowledge source)
- Python asyncio (for concurrent operations)
"""

# ============================================================================
# IMPORTS - External libraries we need
# ============================================================================

import os          # For reading environment variables
import asyncio     # For asynchronous (non-blocking) operations
from typing import Any, Dict  # For type hints (makes code clearer)
from dotenv import load_dotenv  # For loading .env file securely

# Microsoft Agent Framework - handles AI agent orchestration
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import MCPStreamableHTTPTool


# ============================================================================
# CONFIGURATION - Load credentials from .env file
# ============================================================================

# Load environment variables from .env file (keeps secrets secure)
load_dotenv()

# Read Azure OpenAI credentials from environment variables
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

# Validate that all required credentials are present
# This prevents cryptic errors later if something is missing
if not AZURE_ENDPOINT:
    raise ValueError("AZURE_OPENAI_ENDPOINT not found in .env file")
if not AZURE_API_KEY:
    raise ValueError("AZURE_OPENAI_API_KEY not found in .env file")
if not DEPLOYMENT_NAME:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME not found in .env file")


# ============================================================================
# MAIN CLASS - The Career Path Advisor System
# ============================================================================

class CareerPathAdvisor:
    """
    Main class that orchestrates the 3-agent system.
    
    Think of this as the "manager" that coordinates:
    - Profile Agent (asks questions)
    - Research Agent (searches Microsoft Learn)
    - Advisor Agent (creates roadmap)
    """
    
    def __init__(self):
        """
        Initialize the advisor system.
        Sets up the AI client, Microsoft Learn connection, and 3 agents.
        """
        
        # ===== STEP 1: Create Azure OpenAI client =====
        # This is how we communicate with GPT-4o
        self.chat_client = AzureOpenAIChatClient(
            deployment_name=DEPLOYMENT_NAME,  # Which model to use
            endpoint=AZURE_ENDPOINT,          # Where to send requests
            api_key=AZURE_API_KEY,           # Authentication
            api_version=API_VERSION          # API version
        )
        
        # ===== STEP 2: Create Microsoft Learn MCP tool =====
        # MCP = Model Context Protocol
        # This lets our agents search Microsoft Learn documentation
        self.mslearn_mcp = MCPStreamableHTTPTool(
            name="microsoft_learn",
            url="https://learn.microsoft.com/api/mcp",
            timeout=30,           # Wait max 30 seconds for response
            request_timeout=30,   # Same timeout for requests
        )
        
        # ===== STEP 3: Create the 3 specialized agents =====
        self.profile_agent = self._create_profile_agent()
        self.research_agent = self._create_research_agent()
        self.advisor_agent = self._create_advisor_agent()
        
        # ===== STEP 4: Initialize conversation context =====
        # Stores the conversation history to avoid repeating questions
        self._profile_context = []
        
        # Storage for the final outputs of each agent
        self.context: Dict[str, Any] = {
            "user_profile": {},         # Profile Agent's output
            "learning_resources": [],   # Research Agent's output
            "career_roadmap": ""        # Advisor Agent's output
        }
    
    
    # ========================================================================
    # AGENT 1: PROFILE AGENT
    # Purpose: Understand the user's career goals and background
    # ========================================================================
    
    def _create_profile_agent(self) -> ChatAgent:
        """
        Creates the Profile Agent with specific instructions.
        
        This agent asks questions to understand:
        - What career you want
        - Your current skill level
        - What you already know
        - How much time you have
        - Your target timeline
        """
        return ChatAgent(
            chat_client=self.chat_client,
            name="ProfileAgent",
            
            # Instructions tell the AI how to behave
            # This is called "prompt engineering"
            instructions="""
You gather information about the user's career goals and background.

Extract 5 key items:
1. Career goal (cloud developer, data scientist, DevOps engineer, etc.)
2. Current level (beginner/intermediate/advanced)
3. Current skills (languages/tools they know)
4. Time commitment (hours per week)
5. Target timeline (3 months, 6 months, 1 year, etc.)

If user provided all 5:
PROFILE_COMPLETE
- Goal: [career goal]
- Level: [current level]
- Skills: [current skills]
- Time: [hours per week]
- Timeline: [target timeline]

If missing info, ask ONE relevant question:
- "What tech career are you interested in?"
- "What's your current experience level? (beginner/intermediate/advanced)"
- "What programming languages or tools do you already know?"
- "How many hours per week can you dedicate to learning?"
- "What's your target timeline? (3 months, 6 months, 1 year)"

RULES:
- Ask ONLY ONE question per response
- Be conversational but concise
- Maximum 2 lines per response
- No explanations, just ask what you need
            """,
        )
    
    
    # ========================================================================
    # AGENT 2: RESEARCH AGENT
    # Purpose: Search Microsoft Learn for relevant courses and certifications
    # ========================================================================
    
    def _create_research_agent(self) -> ChatAgent:
        """
        Creates the Research Agent with Microsoft Learn search capability.
        
        This agent:
        - Searches Microsoft Learn documentation
        - Finds courses, certifications, labs
        - Returns structured data about each resource
        """
        return ChatAgent(
            chat_client=self.chat_client,
            name="ResearchAgent",
            
            instructions="""
Search Microsoft Learn for learning resources matching the user's career goal.

Find resources in these categories:
1. Foundational courses (for beginners)
2. Intermediate modules (skill building)
3. Advanced topics (specialization)
4. Certifications (career milestones)
5. Hands-on labs (practical experience)

Output format:

RESOURCE: [title]
TYPE: [course/module/certification/lab]
LEVEL: [beginner/intermediate/advanced]
DURATION: [estimated time]
DOCS: [url]
---

Find 5-7 resources total. NO other text.

RULES:
- Cover different skill levels
- Include at least one certification path
- Include hands-on labs when available
- Keep output structured and clean
            """,
            
            # IMPORTANT: This agent gets the MCP tool to search Microsoft Learn
            tools=[self.mslearn_mcp],
        )
    
    
    # ========================================================================
    # AGENT 3: ADVISOR AGENT
    # Purpose: Create a personalized learning roadmap
    # ========================================================================
    
    def _create_advisor_agent(self) -> ChatAgent:
        """
        Creates the Advisor Agent that builds the final roadmap.
        
        This agent:
        - Takes the user profile (from Agent 1)
        - Takes the learning resources (from Agent 2)
        - Creates a phased learning plan with realistic timelines
        """
        return ChatAgent(
            chat_client=self.chat_client,
            name="AdvisorAgent",
            
            instructions="""
Create a personalized learning roadmap based on user profile and available resources.

Output format:

**YOUR CAREER PATH: [Career Goal]**

**PHASE 1: FOUNDATION (Months 1-2)**
- [Resource 1]: [Why important - 10 words max]
- [Resource 2]: [Why important - 10 words max]
- Estimated time: [X hours]

**PHASE 2: SKILL BUILDING (Months 3-4)**
- [Resource 3]: [Why important - 10 words max]
- [Resource 4]: [Why important - 10 words max]
- Estimated time: [X hours]

**PHASE 3: SPECIALIZATION (Months 5-6)**
- [Resource 5]: [Why important - 10 words max]
- [Resource 6]: [Why important - 10 words max]
- Estimated time: [X hours]

**CERTIFICATION TARGET**
- [Certification name]: [Why valuable - 15 words max]
- Exam link: [url]

**WEEKLY COMMITMENT**
Based on [X] hours/week: [Realistic timeline assessment]

**NEXT STEPS**
1. [Immediate action - 12 words max]
2. [First resource to start - 12 words max]
3. [How to track progress - 12 words max]

RULES:
- Adapt phases to user's timeline
- Be realistic about time commitments
- Prioritize beginner resources if they're new
- Always include certification goal
- Keep each point under word limits
- No fluff, just actionable advice
            """,
        )
    
    
    # ========================================================================
    # WORKFLOW METHODS - How the agents work together
    # ========================================================================
    
    async def gather_profile(self, user_input: str) -> str:
        """
        Step 1: Use Profile Agent to gather user information.
        
        Args:
            user_input: What the user typed
            
        Returns:
            The agent's response (either a question or PROFILE_COMPLETE)
        """
        print("\n[1/3] UNDERSTANDING YOUR GOALS...")
        
        # Add user input to conversation history
        # This helps the agent remember what was already asked
        self._profile_context.append(f"User: {user_input}")
        full_context = "\n".join(self._profile_context)
        
        # Send the full conversation to the agent
        response = await self.profile_agent.run(full_context)
        
        # Add agent's response to history
        self._profile_context.append(f"Agent: {response.text}")
        
        return response.text
    
    async def research_learning_path(self, profile: str) -> str:
        """
        Step 2: Use Research Agent to find learning resources.
        
        Args:
            profile: The complete user profile from Agent 1
            
        Returns:
            Structured list of courses, certifications, and labs
        """
        print("\n[2/3] FINDING LEARNING RESOURCES...")
        
        # Create a search query for the Research Agent
        research_query = f"""
User Profile:
{profile}

Search Microsoft Learn for learning resources, courses, certifications, and labs 
that match this career goal and experience level.
        """
        
        # The Research Agent will use the MCP tool to search Microsoft Learn
        response = await self.research_agent.run(research_query)
        return response.text
    
    async def create_roadmap(self, profile: str, resources: str) -> str:
        """
        Step 3: Use Advisor Agent to create personalized roadmap.
        
        Args:
            profile: User profile from Agent 1
            resources: Learning resources from Agent 2
            
        Returns:
            Personalized learning roadmap with phases and timelines
        """
        print("\n[3/3] CREATING YOUR PERSONALIZED ROADMAP...")
        
        # Combine profile and resources for the Advisor Agent
        roadmap_query = f"""
USER PROFILE:
{profile}

AVAILABLE RESOURCES:
{resources}

Create a personalized learning roadmap with realistic timelines.
        """
        
        # The Advisor Agent synthesizes everything into a roadmap
        response = await self.advisor_agent.run(roadmap_query)
        return response.text
    
    async def _cleanup_mcp(self):
        """
        Clean up Microsoft Learn MCP connection after we're done.
        
        This prevents the annoying async cleanup errors you might see.
        It's good practice to close connections properly.
        """
        try:
            # Wait a moment for any pending operations
            await asyncio.sleep(0.5)
            
            # Try to close the MCP tool gracefully
            if hasattr(self.mslearn_mcp, 'close'):
                await self.mslearn_mcp.close()
            elif hasattr(self.mslearn_mcp, '__aexit__'):
                await self.mslearn_mcp.__aexit__(None, None, None)
        except Exception:
            # If cleanup fails, that's okay - just ignore it
            pass
    
    
    # ========================================================================
    # MAIN INTERACTIVE SESSION - Brings it all together
    # ========================================================================
    
    async def run_interactive_session(self):
        """
        Main workflow that orchestrates all 3 agents.
        
        Flow:
        1. Profile Agent asks questions → gathers user profile
        2. Research Agent searches Microsoft Learn → finds resources
        3. Advisor Agent creates roadmap → personalized learning path
        """
        
        # ===== Welcome message =====
        print("\n" + "="*70)
        print("🎯 CAREER PATH ADVISOR - Powered by Microsoft Learn")
        print("="*70)
        print("\nLet's plan your tech career journey!\n")
        
        # ===== PHASE 1: Gather Profile =====
        # Ask the initial question
        user_input = input("What tech career are you interested in? ")
        
        profile_text = ""
        # Allow up to 5 exchanges (question + answer pairs)
        for i in range(5):
            # Get response from Profile Agent
            profile_response = await self.gather_profile(user_input)
            print(f"\n{profile_response}")
            
            # Check if we have all the info we need
            if "PROFILE_COMPLETE" in profile_response:
                profile_text = profile_response
                break
            
            # Ask for more input
            user_input = input("\n> ")
            if not user_input.strip():
                break
        
        # Fallback: use last response if we didn't get PROFILE_COMPLETE
        if not profile_text:
            profile_text = profile_response
        
        # Store the profile
        self.context["user_profile"] = profile_text
        
        # ===== PHASE 2: Research Learning Resources =====
        # Research Agent searches Microsoft Learn
        learning_resources = await self.research_learning_path(profile_text)
        print(f"\n{learning_resources}")
        self.context["learning_resources"] = learning_resources
        
        # ===== PHASE 3: Create Personalized Roadmap =====
        # Advisor Agent creates the final learning plan
        career_roadmap = await self.create_roadmap(profile_text, learning_resources)
        print(f"\n{career_roadmap}")
        self.context["career_roadmap"] = career_roadmap
        
        # ===== Success message =====
        print("\n" + "="*70)
        print("✅ YOUR PERSONALIZED LEARNING PATH IS READY!")
        print("="*70)
        print("\n💡 Tip: Bookmark the resource links and start with Phase 1!")
        
        # Clean up connections
        await self._cleanup_mcp()


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

async def main():
    """
    Main function that runs the career advisor.
    
    This is the entry point when you run: python career_path_advisor.py
    """
    try:
        # Create the advisor system
        advisor = CareerPathAdvisor()
        
        # Run the interactive session
        await advisor.run_interactive_session()
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n👋 Good luck on your learning journey!")
    except Exception as e:
        # Handle any other errors
        print(f"\n❌ Error: {e}")


# This ensures main() only runs when executing this file directly
# (not when importing it as a module)
if __name__ == "__main__":
    # asyncio.run() is how we run async functions in Python
    asyncio.run(main())
