from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from PIL import Image
import io
import uvicorn
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

# Initialize FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class MathAgent:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is missing")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.variables = {}
        
    def process_input(self, input_source):
        prompt = f"""
        You are a math-solving assistant. Follow these rules in order:

        1. Determine if the input is a math problem (any numerical expressions, shape references, variable assignments, or solvable phrases).
        - Examples of valid math inputs:
            - a = 6
            - y = area of 5 by 5 rectangle
            - 2 + 2
            - factors of 9
            - solve for x in x + 3 = 10
        - If it is NOT a math problem, return exactly this text: "ERROR: This is not a Valid math problem."

        2. If it IS a math problem:
        - You have access to existing variables {self.variables}.
        - Interpret shape references (e.g., "area of 5 by 5 rectangle" → 25).
        - Extract or update variables from the input (e.g., "a = 6", "x = area of ...").
        - If no variable name is specified, store the result in a variable named "result".
        - Solve the expression or equation using existing and newly assigned variables.

        3. Return ONLY the final results in the format:
        var=value
        (one result per line).

        Input:
        """

        if isinstance(input_source, Image.Image):
            response = self.model.generate_content([prompt, input_source])
        else:
            response = self.model.generate_content(prompt + input_source)
        
        
        print(response.text)
        if "ERROR" in response.text:
            raise ValueError(response.text)
        self._update_variables(response.text)
        return self.variables
    
    def _update_variables(self, response):
        for line in response.split("\n"):
            line = line.strip()
            if "=" in line:
                var, value = line.split("=", 1)
                try:
                    self.variables[var.strip()] = float(value.strip())
                except ValueError:
                    pass

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GOOGLE_API_KEY")
agent = MathAgent(API_KEY)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "variables": agent.variables})

@app.post("/compute")
async def compute(expression: str = Form(...)):
    try:
        variables = agent.process_input(expression)
        return {"status": "success", "variables": variables}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/compute-image")
async def compute_image(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        variables = agent.process_input(image)
        return {"status": "success", "variables": variables}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/variables")
async def get_variables():
    return {"variables": agent.variables}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
