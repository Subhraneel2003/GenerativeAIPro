import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMHandler:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "mistralai/Mixtral-8x7B-Instruct-v0.1")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2048"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
    
    def get_response(self, prompt, system_prompt=None):
       # Get a response from the language model
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Format the prompt based on whether a system prompt is provided
        if system_prompt:
            formatted_prompt = f"<s>[INST] {system_prompt} [/INST]</s>\n<s>[INST] {prompt} [/INST]"
        else:
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": 0.95,
                "do_sample": True
            }
        }
        
        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract the generated text
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"].strip()
            else:
                return str(result)
                
        except Exception as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            return f"Error: {str(e)}"