import json
from utils.conversation import LLMHandler
from utils.templates import get_template

class Developer:
    def __init__(self):
        self.llm = LLMHandler()
    
    def generate_code(self, user_stories, design_doc):
        """
        Generate code based on user stories and design document
        """
        # Get the code template
        template = get_template("code_template.py")
        
        # Prepare user stories for the prompt
        stories_text = ""
        for i, story in enumerate(user_stories):
            stories_text += f"User Story #{i+1}: {story['title']}\n"
            stories_text += f"As a {story['role']}, I want {story['want']} so that {story['so_that']}\n"
            stories_text += "Acceptance Criteria:\n"
            for criterion in story['acceptance_criteria']:
                stories_text += f"- {criterion}\n"
            stories_text += "\n"
        
        # Create the prompt for the LLM to identify required files
        files_prompt = f"""
You are a senior Software Developer working on implementing a system based on the following design document and user stories.

THE DESIGN DOCUMENT:
{design_doc}

THE USER STORIES:
{stories_text}

First, identify all the Python files that need to be created for this project. 
Your task is to list all the necessary files based on the design document and user stories.

Format your response as a JSON array of filenames, for example:
```json
["main.py", "database.py", "api.py", "models.py", "utils.py"]
```

Focus only on the core files needed for the application, considering the architecture described in the design document.
"""
        
        # Get response from LLM for file list
        files_response = self.llm.get_response(files_prompt)
        
        # Extract the JSON array from the response
        try:
            # Try to find JSON in the response
            json_start = files_response.find("[")
            json_end = files_response.rfind("]") + 1
            
            if json_start >= 0 and json_end > json_start:
                files_json = files_response[json_start:json_end]
                files_list = json.loads(files_json)
            else:
                # Fallback to a default list if JSON parsing fails
                files_list = ["main.py", "database.py", "api.py", "models.py", "utils.py"]
        except Exception as e:
            print(f"Error parsing file list: {str(e)}")
            # Fallback to a default list
            files_list = ["main.py", "database.py", "api.py", "models.py", "utils.py"]
        
        # Generate code for each file
        code_files = {}
        
        for filename in files_list:
            # Create the prompt for the LLM to generate code for this file
            code_prompt = f"""
You are a senior Software Developer working on implementing a system based on the following design document and user stories.

THE DESIGN DOCUMENT:
{design_doc}

THE USER STORIES:
{stories_text}

You need to implement the file: {filename}

Based on the design document and user stories, create the complete code for this file.
Make sure your code is well-documented, follows best practices, and implements the functionality described in the design.

Here's a template to help you get started, but feel free to modify it:

{template}

DO NOT use placeholder comments like "// Implementation goes here". Provide the COMPLETE and WORKING implementation.
"""
            
            # Get response from LLM for code
            code = self.llm.get_response(code_prompt)
            
            # Add the code to the dictionary
            code_files[filename] = code
        
        return code_files