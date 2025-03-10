import json
from utils.conversation import LLMHandler
from utils.templates import get_template

class DesignAgent:
    def __init__(self):
        self.llm = LLMHandler()
    
    def create_design(self, requirements, user_stories):
        """
        Create a system design document based on requirements and user stories
        """
        # Get the design document template
        template = get_template("design_doc.md")
        
        # Prepare user stories for the prompt
        stories_text = ""
        for i, story in enumerate(user_stories):
            stories_text += f"User Story #{i+1}: {story['title']}\n"
            stories_text += f"As a {story['role']}, I want {story['want']} so that {story['so_that']}\n"
            stories_text += "Acceptance Criteria:\n"
            for criterion in story['acceptance_criteria']:
                stories_text += f"- {criterion}\n"
            stories_text += "\n"
        
        # Create the prompt for the LLM
        prompt = f"""
You are a senior Software Architect responsible for creating a comprehensive system design document based on business requirements and user stories.

THE HIGH-LEVEL BUSINESS REQUIREMENTS:
{requirements}

THE USER STORIES:
{stories_text}

Based on this information, create a detailed design document that includes:

1. Overview of the system
2. Architecture diagram (described in text)
3. Key components and their responsibilities
4. Data model and database design
5. API definitions and endpoints
6. Technology stack recommendations
7. Non-functional requirements (performance, security, scalability)
8. Implementation considerations

Format your response as a well-structured Markdown document.
Be specific in your design choices and explain the rationale behind key architectural decisions.

Here's a template to help you get started, but feel free to modify it to best represent the system design:

{template}
"""
        
        # Get response from LLM
        design_doc = self.llm.get_response(prompt)
        
        return design_doc