from utils.conversation import LLMHandler
from utils.database import ChromaManager

class ProjectLead:
    def __init__(self):
        self.llm = LLMHandler()
        self.db = ChromaManager()
    
    def respond(self, question, project_name, requirements, artifacts):
        """
        Respond to a question about the project
        """
        # Create context from project artifacts
        context = self._prepare_context(project_name, requirements, artifacts, question)  # Pass 'question' here
        
        # Create the prompt for the LLM
        prompt = f"""
You are the Project Lead of an AI development pod working on the project "{project_name}".
You have access to the following project information:

HIGH-LEVEL REQUIREMENTS:
{requirements}

PROJECT ARTIFACTS SUMMARY:
{context}

A team member has asked you the following question:
"{question}"

Please respond to this question as the Project Lead. Be concise, informative, and accurate.
If the information is not available in the context, politely explain what information you have 
and what might be needed to better answer the question.
"""
        
        # Get response from LLM
        response = self.llm.get_response(prompt)
        
        # Store the conversation in the database
        self.db.store_conversation(project_name, question, response)
        
        return response
    
    def _prepare_context(self, project_name, requirements, artifacts, question):
        """
        Prepare context from project artifacts
        """
        context = []
        
        # Add user stories summary
        if artifacts["user_stories"]:
            stories_summary = "\nUSER STORIES SUMMARY:\n"
            for i, story in enumerate(artifacts["user_stories"]):
                stories_summary += f"- User Story #{i+1}: {story['title']} (As a {story['role']}, I want {story['want'][:50]}...)\n"
            context.append(stories_summary)
        
        # Add design document summary
        if artifacts["design_doc"]:
            design_preview = artifacts["design_doc"][:500] + "..." if len(artifacts["design_doc"]) > 500 else artifacts["design_doc"]
            context.append(f"\nDESIGN DOCUMENT PREVIEW:\n{design_preview}")
        
        # Add code summary
        if artifacts["code"]:
            code_summary = "\nCODE FILES:\n"
            for filename in artifacts["code"].keys():
                code_summary += f"- {filename}\n"
            context.append(code_summary)
        
        # Add test summary
        if artifacts["test_cases"]:
            test_summary = "\nTEST CASES SUMMARY:\n"
            for i, test in enumerate(artifacts["test_cases"]):
                test_summary += f"- Test #{i+1}: {test['title']}\n"
            context.append(test_summary)
        
        # Add test results if available
        if artifacts["test_results"]:
            passed = sum(1 for result in artifacts["test_results"] if result["status"] == "PASS")
            total = len(artifacts["test_results"])
            pass_rate = (passed / total) * 100 if total > 0 else 0
            
            results_summary = f"\nTEST RESULTS SUMMARY:\n"
            results_summary += f"- Total Tests: {total}\n"
            results_summary += f"- Tests Passed: {passed}\n"
            results_summary += f"- Pass Rate: {pass_rate:.1f}%\n"
            
            # Add failed tests
            failed_tests = [r for r in artifacts["test_results"] if r["status"] == "FAIL"]
            if failed_tests:
                results_summary += "- Failed Tests:\n"
                for test in failed_tests:
                    results_summary += f"  - {test['title']}\n"
            
            context.append(results_summary)
        
        # Query the database for relevant information
        db_results = self.db.query_project_data(project_name, question)
        if db_results:
            relevant_info = "\nRELEVANT INFORMATION FROM DATABASE:\n"
            for category, data in db_results.items():
                if data["documents"]:
                    relevant_info += f"- From {category.upper()}:\n"
                    for i, doc in enumerate(data["documents"]):
                        preview = doc[:200] + "..." if len(doc) > 200 else doc
                        relevant_info += f"  Document {i+1}: {preview}\n"
            context.append(relevant_info)
        
        return "\n".join(context)
