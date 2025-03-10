import os
import json
import chromadb
from chromadb.config import Settings
from datetime import datetime

class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=os.getenv("CHROMA_DB_PATH", "./data")
        )
        
        # Create collections if they don't exist
        self.requirements_collection = self._get_or_create_collection("requirements")
        self.user_stories_collection = self._get_or_create_collection("user_stories")
        self.design_collection = self._get_or_create_collection("design_docs")
        self.code_collection = self._get_or_create_collection("code")
        self.test_collection = self._get_or_create_collection("tests")
        self.chat_collection = self._get_or_create_collection("conversations")
    
    def _get_or_create_collection(self, name):
        try:
            return self.client.get_collection(name=name)
        except:
            return self.client.create_collection(name=name)
    
    def store_requirements(self, project_name, requirements):
        timestamp = datetime.now().isoformat()
        self.requirements_collection.add(
            documents=[requirements],
            metadatas=[{"project": project_name, "timestamp": timestamp}],
            ids=[f"{project_name}_requirements_{timestamp}"]
        )
    
    def store_user_stories(self, project_name, user_stories):
        timestamp = datetime.now().isoformat()
        for i, story in enumerate(user_stories):
            self.user_stories_collection.add(
                documents=[json.dumps(story)],
                metadatas=[{
                    "project": project_name, 
                    "timestamp": timestamp,
                    "story_id": i,
                    "title": story["title"]
                }],
                ids=[f"{project_name}_story_{i}_{timestamp}"]
            )
    
    def store_design_doc(self, project_name, design_doc):
        timestamp = datetime.now().isoformat()
        self.design_collection.add(
            documents=[design_doc],
            metadatas=[{"project": project_name, "timestamp": timestamp}],
            ids=[f"{project_name}_design_{timestamp}"]
        )
    
    def store_code(self, project_name, code_files):
        timestamp = datetime.now().isoformat()
        for filename, code in code_files.items():
            self.code_collection.add(
                documents=[code],
                metadatas=[{
                    "project": project_name, 
                    "timestamp": timestamp,
                    "filename": filename
                }],
                ids=[f"{project_name}_code_{filename}_{timestamp}"]
            )
    
    def store_test_cases(self, project_name, test_cases):
        timestamp = datetime.now().isoformat()
        for i, test in enumerate(test_cases):
            self.test_collection.add(
                documents=[json.dumps(test)],
                metadatas=[{
                    "project": project_name, 
                    "timestamp": timestamp,
                    "test_id": i,
                    "title": test["title"],
                    "type": "test_case"
                }],
                ids=[f"{project_name}_test_case_{i}_{timestamp}"]
            )
    
    def store_test_results(self, project_name, test_results):
        timestamp = datetime.now().isoformat()
        for i, result in enumerate(test_results):
            self.test_collection.add(
                documents=[json.dumps(result)],
                metadatas=[{
                    "project": project_name, 
                    "timestamp": timestamp,
                    "test_id": i,
                    "title": result["title"],
                    "type": "test_result",
                    "status": result["status"]
                }],
                ids=[f"{project_name}_test_result_{i}_{timestamp}"]
            )
    
    def store_conversation(self, project_name, question, answer):
        timestamp = datetime.now().isoformat()
        self.chat_collection.add(
            documents=[question + "\n\n" + answer],
            metadatas=[{
                "project": project_name, 
                "timestamp": timestamp,
                "question": question[:100]  # Store a preview
            }],
            ids=[f"{project_name}_chat_{timestamp}"]
        )
    
    def query_project_data(self, project_name, query, limit=5):
        """Search across all collections for relevant information"""
        results = {}
        
        collections = [
            ("requirements", self.requirements_collection),
            ("user_stories", self.user_stories_collection),
            ("design", self.design_collection),
            ("code", self.code_collection),
            ("tests", self.test_collection)
        ]
        
        for name, collection in collections:
            try:
                result = collection.query(
                    query_texts=[query],
                    n_results=limit,
                    where={"project": project_name}
                )
                
                if result["documents"][0]:
                    results[name] = {
                        "documents": result["documents"][0],
                        "metadatas": result["metadatas"][0]
                    }
            except Exception as e:
                print(f"Error querying {name}: {str(e)}")
        
        return results