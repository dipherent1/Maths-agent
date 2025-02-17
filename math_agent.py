import google.generativeai as genai
from PIL import Image
import os

class MathAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.variables = {}
        
    def process_input(self, input_source):
        # Prepare prompt for Gemini
        prompt = f"""
        Given this mathematical input and existing variables {self.variables}:
        1. Extract new variable assignments
        2. Solve equations using existing variables
        3. Return ONLY results in format: var=value (one per line)
        
        Input:"""
        
        if isinstance(input_source, Image.Image):
            # For image inputs
            response = self.model.generate_content([prompt, input_source])
        else:
            # For text inputs
            response = self.model.generate_content(prompt + input_source)
            
        self._update_variables(response.text)
        return self.variables
    
    def _update_variables(self, response):
        for line in response.split('\n'):
            line = line.strip()
            if '=' in line:
                var, value = line.split('=', 1)
                try:
                    self.variables[var.strip()] = float(value.strip())
                except ValueError:
                    pass

# Usage
#get api key form .env file

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
agent = MathAgent(API_KEY)

# Process text input
agent.process_input("a = 2")        # {'a': 2}
agent.process_input("b = 3")        # {'a': 2, 'b': 3}
# Process image input (snapshot of "a + b = c")
agent.process_input(Image.open('equation.jpg'))  # {'a': 2, 'b': 3, 'c': 5}

while True:
    user_input = input("Enter equation or image path: ")
    if user_input.lower() == "exit":
        break
    if user_input.endswith(".jpg") or user_input.endswith(".png"):
        agent.process_input(Image.open(user_input))
    else:
        agent.process_input(user_input)
    print("Current variables:", agent.variables)

print("Final variables:", agent.variables)