import os,sys
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import subprocess

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Initialize OpenAI
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4", temperature=0)

# Prompt for Playwright script generation
prompt = PromptTemplate(
    input_variables=["instruction"],
    template="""
You are a coding assistant. Write a complete Python Playwright script for this instruction do not use headless mode:
{instruction}

Include:
1. Importing Playwright and use browser = playwright.chromium.launch(headless=False).
2. Navigation, form filling, clicking, or waiting actions as needed.
3. Proper error handling.
4. A function named 'run()' that executes the script.
5. write only python code in generated_script.py
6. Do not include any plain text just add code
"""
)

# Prompt for refinement
refinement_prompt = PromptTemplate(
    input_variables=["instruction", "error"],
    template="""
You wrote a Playwright script for this instruction:
{instruction}

However, it encountered the following error:
{error}

Please refine the script to fix this issue.

write only python code in generated_script.py
"""
)

# Function to generate Playwright script
def generate_script(instruction):
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(instruction)

# Function to refine Playwright script
def refine_script(instruction, error):
    chain = LLMChain(llm=llm, prompt=refinement_prompt)
    return chain.run({"instruction": instruction, "error": error})

# Function to execute a script
def execute_script(script_code, script_name="generated_script.py"):
    # Save the script to a file
    python_code = script_code.split("```python")[1].split("```")[0].strip()
    with open(script_name, "w") as f:
        f.write(python_code)

    # Execute the saved script using Python
    try:
        # subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        
        # # Install Playwright browsers
        # subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print(sys.executable)
        # Execute the saved Python script
        subprocess.run([sys.executable, script_name], check=True)
        return "Execution successful!"
    except subprocess.CalledProcessError as e:
        return f"Execution failed with error: {str(e)}"

# Function to load instructions from a JSON file
def load_instructions_from_json(json_file):
    with open(json_file, "r") as f:
        tasks = json.load(f)
    return [task["task"] for task in tasks]


if __name__ == "__main__":
    execute_script("")