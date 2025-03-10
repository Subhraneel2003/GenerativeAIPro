import json
from utils.conversation import LLMHandler
from utils.templates import get_template

class BusinessAnalyst:
    def __init__(self):
        self.llm = LLMHandler()
    
    def generate_user_stories(self, requirements):
        """
        Generate user stories from the high-level business requirements
        """
        # Get the user story template
        template = get_template("user_story.md")
        
        # Create the prompt for the LLM
        prompt = f"""
You are a senior Business Analyst responsible for creating detailed user stories from high-level business requirements.
You need to analyze the following business requirements and create comprehensive user stories that follow the standard "As a [role], I want [feature/action], so that [benefit/value]" format.

THE HIGH-LEVEL BUSINESS REQUIREMENTS:
{requirements}

For each identified major feature/functionality, create a detailed user story including:
1. A clear title
2. The user story in proper format (As a... I want... So that...)
3. A list of specific acceptance criteria (at least 3-5 per story)

Format your response as a valid JSON array with the following structure for each story:
```json
[
  {{
    "title": "Story title",
    "role": "user role",
    "want": "what they want to do",
    "so_that": "the benefit they receive",
    "acceptance_criteria": ["criterion 1", "criterion 2", "criterion 3", ...]
  }},
  ...
]
[
  {
    "title": "Initialize Project with Business Requirements",
    "role": "Project Manager",
    "want": "to input high-level business requirements to initialize the development process",
    "so_that": "the virtual development pod can begin creating project artifacts",
    "acceptance_criteria": [
      "A user-friendly input form allows entering project name and business requirements",
      "The system validates that both fields are completed before proceeding",
      "Business requirements are stored in the system database for reference",
      "The system confirms successful initialization and transitions to the next phase",
      "Requirements can be viewed throughout all project phases"
    ]
  },
  {
    "title": "Generate User Stories from Requirements",
    "role": "Business Analyst Agent",
    "want": "to automatically generate comprehensive user stories from the high-level requirements",
    "so_that": "the development team has clear, structured requirements to work from",
    "acceptance_criteria": [
      "User stories follow the standard 'As a, I want, So that' format",
      "Each user story includes at least 3 acceptance criteria",
      "User stories are displayed in an organized, easy-to-read format",
      "The system stores generated user stories in the database",
      "User stories can be referenced in subsequent development phases"
    ]
  },
  {
    "title": "Create System Design Document",
    "role": "Design Agent",
    "want": "to generate a technical design document based on user stories and requirements",
    "so_that": "developers have clear architecture guidance for implementation",
    "acceptance_criteria": [
      "Design document includes system architecture overview",
      "Component relationships and interactions are clearly defined",
      "Data models and structures are specified",
      "Technology stack recommendations are provided",
      "Design is traceable back to specific user stories and requirements",
      "The document is stored for reference throughout the project lifecycle"
    ]
  },
  {
    "title": "Generate Code Implementation",
    "role": "Developer Agent",
    "want": "to write code that implements the user stories according to the design document",
    "so_that": "a functional software solution is created to meet business requirements",
    "acceptance_criteria": [
      "Code is generated for all specified user stories",
      "Code follows best practices and coding standards",
      "Code is organized into appropriate files and modules",
      "Implementation is consistent with the design document",
      "Code is stored in the system and viewable through the interface"
    ]
  },
  {
    "title": "Create and Execute Test Cases",
    "role": "Testing Agent",
    "want": "to automatically generate and run test cases for the implemented code",
    "so_that": "the quality and functionality of the software can be verified",
    "acceptance_criteria": [
      "Test cases cover all user stories and acceptance criteria",
      "Each test case includes clear steps and expected results",
      "Tests are executed against the generated code",
      "Test results show clear pass/fail status",
      "Failed tests include detailed error information",
      "Test metrics (total tests, pass rate) are displayed"
    ]
  },
  {
    "title": "Interact with Project Manager via Chat",
    "role": "Team Member",
    "want": "to communicate with the Project Manager through a conversational interface",
    "so_that": "I can get information about project status and artifacts",
    "acceptance_criteria": [
      "Chat interface allows natural language questions about the project",
      "Project Manager provides relevant information based on project context",
      "Conversation history is maintained throughout the session",
      "Project Manager can reference specific artifacts when answering questions",
      "Conversations are stored in the database for future reference"
    ]
  },
  {
    "title": "View Project Dashboard",
    "role": "Stakeholder",
    "want": "to access a comprehensive project dashboard",
    "so_that": "I can monitor overall project progress and navigate between phases",
    "acceptance_criteria": [
      "Dashboard displays current project name and phase",
      "Navigation controls allow movement between different project phases",
      "Project artifacts can be accessed from the dashboard",
      "Status indicators show completion status for each phase",
      "Project requirements are accessible at any time"
    ]
  },
  {
    "title": "Store and Retrieve Project Artifacts",
    "role": "System Administrator",
    "want": "all project artifacts to be automatically stored in a database",
    "so_that": "information is persistent and retrievable across sessions",
    "acceptance_criteria": [
      "All artifacts (requirements, user stories, design docs, code, tests) are stored in ChromaDB",
      "Artifacts are searchable and retrievable by project name",
      "Metadata is stored with artifacts for organization",
      "Storage operations are performed automatically at appropriate points",
      "Retrieved artifacts maintain their original structure and formatting"
    ]
  }
]"""