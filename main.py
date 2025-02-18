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
        Given this mathematical input and existing variables {self.variables}:
        1. Extract new variable assignments
        2. Solve equations using existing variables
        3. Return ONLY results in format: var=value (one per line)
        
        Input:"""
        
        if isinstance(input_source, Image.Image):
            response = self.model.generate_content([prompt, input_source])
        else:
            response = self.model.generate_content(prompt + input_source)
        
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
