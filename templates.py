import os

def get_template(template_name):
    """
    Load a template file from the templates directory.
    If the template does not exist, create default templates and then load the requested template.
    
    Args:
        template_name (str): Name of the template file to load.
    
    Returns:
        str: Content of the template file.
    
    Raises:
        FileNotFoundError: If the template file cannot be found or created.
    """
    template_path = os.path.join("templates", template_name)
    
    if not os.path.exists(template_path):
        if not os.path.exists("templates"):
            # Create default templates if they don't exist
            create_default_templates()
    
    # Attempt to read the file after ensuring it exists
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return f.read()
    else:
        raise FileNotFoundError(f"Template '{template_name}' not found and could not be created.")

def create_default_templates():
    """
    Create default templates in the 'templates' directory if they don't already exist.
    
    Raises:
        RuntimeError: If there is an issue creating the directory or writing the templates.
    """
    try:
        # Create the 'templates' directory if it doesn't exist
        os.makedirs("templates", exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create 'templates' directory: {e}")
    
    # Define default templates
    templates = {
        "user_story.md": """# User Story

## Title
[Title]

## Description
As a [role]
I want [feature/action]
So that [benefit/value]

## Acceptance Criteria
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

## Priority
[Priority]

## Estimation
[Estimation]
""",
        
        "design_doc.md": """# Design Document

## Overview
[Overview of the system]

## Architecture
[Description of the architecture]

## Components
[List of components]

## Data Model
[Description of the data model]

## APIs
[Description of the APIs]

## Non-functional Requirements
[Non-functional requirements]

## Constraints
[Constraints]
""",
        
        "code_template.py": """# [Module Name]
# Description: [Description]
# Author: AI Development Pod
# Created: [Date]

# Imports
import [module]

# Constants
[CONSTANTS]

# Classes
class [ClassName]:
    \"\"\"
    [Class description]
    \"\"\"
    
    def __init__(self):
        \"\"\"
        Initialize the class
        \"\"\"
        pass
    
    def [method_name](self):
        \"\"\"
        [Method description]
        \"\"\"
        pass

# Main function
def main():
    \"\"\"
    Main function
    \"\"\"
    pass

if __name__ == "__main__":
    main()
""",
        
        "test_case.md": """# Test Case

## Title
[Title]

## Description
[Description]

## Prerequisites
[Prerequisites]

## Test Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Result
[Expected result]

## Actual Result
[Actual result]

## Status
[Status]

## Notes
[Notes]
"""
    }
    
    # Write default templates to files
    for filename, content in templates.items():
        path = os.path.join("templates", filename)
        try:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
        except Exception as e:
            raise RuntimeError(f"Failed to create template file '{filename}': {e}")

# Example usage
try:
    user_story_template = get_template("user_story.md")
    print(user_story_template)
except Exception as e:
    print(f"Error: {e}")
