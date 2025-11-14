## Things to install ##

pip install fastapi [click here for more info ](https://fastapi.tiangolo.com/ )

pip install uvicorn _we need this to serve our endpoints_


Step 1: Design a Test Repository
Create a structured repository to store the validation tests. This repository can be a database, a JSON/YAML file, or even a version-controlled system like Git.

Example JSON Schema for Storing Tests:
```python
{
  "test_id": "login_page_validation_001",
  "description": "Validate the login page UI elements",
  "html_snapshot": "<html>...Login page HTML...</html>",
  "validations": [
    {
      "description": "Check username input field",
      "criteria": "There is an input field with placeholder 'Enter username' and it is required."
    },
    {
      "description": "Check password input field",
      "criteria": "There is an input field with placeholder 'Enter password' and it is required."
    },
    {
      "description": "Check login button",
      "criteria": "There is a button with text 'Login' and it is enabled."
    }
  ]
}

```
Step 2: Store Tests
Use any of the following storage options:

File-Based Storage:

Store the JSON or YAML files locally or in a cloud-based file system.
Use GitHub/GitLab for version control and collaboration.
Database Storage:

Use a database like SQLite, PostgreSQL, or MongoDB to store test data.
Store each test as a record, with fields for HTML, prompts, and validation criteria.
Cloud Storage:

Use cloud platforms like AWS S3, Google Drive, or Azure Blob Storage to store test files.
Step 3: Reuse Tests
Develop a workflow or tool to retrieve and reuse stored tests. Here’s how:

Load Test Data:

Read the HTML and prompts from the repository.
Combine them into a dynamic prompt for OpenAI.
Dynamic Execution:

Fetch the test by its test_id.
Use the associated html_snapshot and validations to construct an OpenAI prompt.
Example Code (Python):
```python
import openai
import json

# Load a stored test
def load_test(test_id, test_repo_path="tests.json"):
    with open(test_repo_path, "r") as file:
        tests = json.load(file)
    return next((test for test in tests if test["test_id"] == test_id), None)

# Run validation using OpenAI
def run_validation(test):
    html_snapshot = test["html_snapshot"]
    validations = test["validations"]
    
    for validation in validations:
        prompt = f"Analyze the following HTML and check:\n{validation['criteria']}\n\nHTML:\n{html_snapshot}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        print(f"Validation: {validation['description']}")
        print(f"Result: {response['choices'][0]['text'].strip()}")

# Example usage
test_id = "login_page_validation_001"
test = load_test(test_id)
if test:
    run_validation(test)
else:
    print("Test not found!")

```
Step 4: Maintain Test Versioning
Track Changes:

Use version control (e.g., Git) to manage changes to test definitions and associated HTML snapshots.
Commit new versions when the UI changes.
Test IDs and Metadata:

Assign unique IDs (test_id) to each test.
Add metadata (e.g., last_updated, owner, priority) to track the test’s lifecycle.
Example Metadata:
{
  "test_id": "login_page_validation_001",
  "description": "Validate the login page UI elements",
  "last_updated": "2025-01-06",
  "created_by": "QA Team",
  "priority": "High"
}
Step 5: Automate Test Execution
Batch Execution:

Write a script or API endpoint to execute all stored tests automatically.
Example: Run all tests marked as "High Priority" or tests updated within the last 7 days.
Integrate with CI/CD Pipelines:

Include these validations as part of CI/CD pipelines.
Automatically run tests after every deployment or code merge.
Step 6: Reporting and Feedback
Store Results:

Save the results of each test run (e.g., passed/failed status, feedback from OpenAI).
Generate Reports:

Use OpenAI to summarize the results of multiple tests into a readable report.
Example Output:
```python
{
  "test_id": "login_page_validation_001",
  "results": [
    {
      "description": "Check username input field",
      "status": "Pass",
      "details": "The input field with placeholder 'Enter username' exists and is required."
    },
    {
      "description": "Check password input field",
      "status": "Pass",
      "details": "The input field with placeholder 'Enter password' exists and is required."
    },
    {
      "description": "Check login button",
      "status": "Fail",
      "details": "The button with text 'Login' is disabled."
    }
  ]
}

```
Advantages of Storing and Reusing Tests
Consistency:

Reuse tests across different builds or environments without re-defining them.
Scalability:

Centralized test storage makes it easier to manage hundreds of tests.
Adaptability:

Update the HTML snapshot or validation prompts without rewriting the entire test.
Automation-Ready:

Easy to integrate into automated workflows and pipelines.


Here’s how to implement a test storage and execution system for OpenAI-based UI validations, step by step. This example will use Python and JSON for simplicity, but it can be adapted for more complex use cases (e.g., using a database or integrating with CI/CD).

2. Define the Test Repository
We'll use a JSON file to store test cases.

Example tests.json File:
```python
[
  {
    "test_id": "login_page_validation_001",
    "description": "Validate the login page UI elements",
    "html_snapshot": "<!DOCTYPE html>...Login Page HTML Here...</html>",
    "validations": [
      {
        "description": "Check username input field",
        "criteria": "There is an input field with placeholder 'Enter username' and it is required."
      },
      {
        "description": "Check password input field",
        "criteria": "There is an input field with placeholder 'Enter password' and it is required."
      },
      {
        "description": "Check login button",
        "criteria": "There is a button with text 'Login' and it is enabled."
      }
    ]
  }
]

```
Write the Python Script
Below is the implementation for loading tests, running validations, and generating a report.

Full Python Script:
```python
import openai
import json
from datetime import datetime

# Initialize OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Load Test Cases from JSON Repository
def load_tests(file_path="tests.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading test repository: {e}")
        return []

# Save Test Results to a Report
def save_report(report, file_path="test_report.json"):
    try:
        with open(file_path, "w") as file:
            json.dump(report, file, indent=4)
        print(f"Test report saved to {file_path}")
    except Exception as e:
        print(f"Error saving report: {e}")

# Run Validation Using OpenAI
def run_validation(test):
    html_snapshot = test["html_snapshot"]
    validations = test["validations"]
    results = []

    for validation in validations:
        prompt = f"Analyze the following HTML and validate:\n{validation['criteria']}\n\nHTML:\n{html_snapshot}"
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200
            )
            result = response["choices"][0]["text"].strip()
            results.append({
                "description": validation["description"],
                "criteria": validation["criteria"],
                "result": result
            })
        except Exception as e:
            results.append({
                "description": validation["description"],
                "criteria": validation["criteria"],
                "result": f"Error: {e}"
            })

    return results

# Run All Tests
def run_all_tests(test_repo_path="tests.json"):
    tests = load_tests(test_repo_path)
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": []
    }

    for test in tests:
        print(f"Running test: {test['description']}")
        results = run_validation(test)
        report["results"].append({
            "test_id": test["test_id"],
            "description": test["description"],
            "results": results
        })

    save_report(report)
    return report

# Main Function
if __name__ == "__main__":
    report = run_all_tests("tests.json")
    print("Test execution completed. Summary:")
    for test_result in report["results"]:
        print(f"- {test_result['description']}:")
        for result in test_result["results"]:
            print(f"  {result['description']}: {result['result']}")

```
4. How It Works
Test Storage:

Test cases are stored in tests.json, including html_snapshot and validation criteria.
Execution:

The script reads the JSON file, sends prompts to OpenAI for each validation, and collects the results.
Report Generation:

Results are saved in a test_report.json file.
5. Example Test Run
Input tests.json:
```python
[
  {
    "test_id": "homepage_navigation_validation",
    "description": "Validate the homepage navigation bar",
    "html_snapshot": "<html>...Homepage HTML Here...</html>",
    "validations": [
      {
        "description": "Check navigation bar",
        "criteria": "There is a navigation bar with at least 3 links."
      },
      {
        "description": "Check logo",
        "criteria": "The navigation bar contains a logo image."
      }
    ]
  }
]

```
Running test: Validate the homepage navigation bar
  Check navigation bar: ✅ There is a navigation bar with at least 3 links.
  Check logo: ❌ The navigation bar does not contain a logo image.

Generated test_report.json:
json
Copy code

```python
{
  "timestamp": "2025-01-06T15:45:23",
  "results": [
    {
      "test_id": "homepage_navigation_validation",
      "description": "Validate the homepage navigation bar",
      "results": [
        {
          "description": "Check navigation bar",
          "criteria": "There is a navigation bar with at least 3 links.",
          "result": "✅ There is a navigation bar with at least 3 links."
        },
        {
          "description": "Check logo",
          "criteria": "The navigation bar contains a logo image.",
          "result": "❌ The navigation bar does not contain a logo image."
        }
      ]
    }
  ]
}

```
. Next Steps
Expand Test Storage:

Add more test cases to tests.json.
Integrate with CI/CD:

Add this script as a step in your CI/CD pipeline for automated validations.
Enhance Reporting:

Generate HTML/PDF reports for better visualization.
UI for Non-Technical Users:

Create a simple frontend where users can define and execute tests interactively.


#############################
You are a highly skilled test engineer specializing in manual testing.  
Generate manual test cases for the following UI element using the information provided:  

Element Details:  
- **Tag**: {element['tag']}  
- **ID**: {element['id']}  
- **Name**: {element['name']}  
- **Text/Label**: {element['text']}  
- **Type**: {element['type']}  
- **Placeholder**: {element['placeholder']}  
- **Disabled**: {element['disabled']}  
- **Required**: {element['required']}  
- **Max Length**: {element['maxlength']}  
- **Href (if applicable)**: {element['href']}  

### **Test Cases Should Include:**  
1️⃣ **Basic functionality** (Verify expected behavior)  
2️⃣ **Validation rules** (Required field, max length, invalid inputs)  
3️⃣ **Edge cases** (Empty input, long text, special characters, SQL injection)  
4️⃣ **UI behavior** (Visibility, responsiveness, disabled/enabled states)  
5️⃣ **Accessibility testing** (Keyboard navigation, screen reader support, ARIA labels)  
6️⃣ **Security testing** (Prevent XSS, SQL injection, CSRF)  
7️⃣ **Error messages** (Ensure correct messages for incorrect inputs)  
8️⃣ **Usability** (Check tooltip, placeholder guidance, field grouping)  

**Format Output in a Structured Table:**  

| **Test ID**  | **Test Scenario** | **Steps** | **Expected Result** |
|-------------|------------------|-----------|----------------------|

Provide at least **10** well-structured test cases.
######################3
You are an expert in **UI validation testing**.  
Generate **detailed** manual test cases for an **input field** based on the following details:  

- **Field Type**: {element['type']}  
- **Label**: {element['text']}  
- **Placeholder**: {element['placeholder']}  
- **Required**: {element['required']}  
- **Max Length**: {element['maxlength']}  
- **Error messages (if extracted from DOM)**: {element.get('error_messages', 'Not available')}  

### **Test Cases Should Cover:**  
✔ **Valid input scenarios** (Expected user input)  
✔ **Invalid input scenarios** (Edge cases, empty input, special characters, numbers in name fields, etc.)  
✔ **Field constraints** (Max length, required field validation)  
✔ **Security tests** (XSS, SQL injection protection)  
✔ **Error handling** (Correct error messages)  
✔ **Accessibility** (Screen reader reads correct label)  

Format test cases as a structured table with the following columns:  

| **Test ID**  | **Test Case Description** | **Test Steps** | **Expected Outcome** |
|-------------|-------------------------|--------------|----------------------|

Provide at least **10** structured test cases.
#####################
You are a UI and functional testing expert.  
Generate **manual test cases** for a **button** using the following details:  

- **Button Text**: {element['text']}  
- **ID**: {element['id']}  
- **Disabled State**: {element['disabled']}  
- **Expected Action**: (e.g., submit form, navigate to another page)  

### **Test Cases Should Cover:**  
✅ **Button Click Functionality** (Enabled/Disabled state)  
✅ **Keyboard Navigation** (Press Enter/Spacebar to activate)  
✅ **Negative Scenarios** (Click when form is incomplete)  
✅ **Usability** (Hover effects, tooltip, proper cursor change)  
✅ **Security** (Check if button triggers any unauthorized action)  

Provide **at least 8 test cases** in a structured table format.
##################
You are an expert in testing website navigation and UI interactions.  
Generate **manual test cases** for a **hyperlink** based on the following details:  

- **Link Text**: {element['text']}  
- **URL (Href)**: {element['href']}  
- **Target Attribute**: (_blank, _self)  

### **Test Cases Should Cover:**  
1️⃣ **Basic Functionality** (Click the link and verify it navigates to the correct URL)  
2️⃣ **Security Tests** (Ensure no redirections to phishing/malicious sites)  
3️⃣ **Link Behavior in Different Browsers**  
4️⃣ **Link Opening Behavior** (New tab vs. same window)  
5️⃣ **Keyboard Accessibility** (TAB navigation, Enter key activation)  

Provide **at least 5 test cases** in a structured format.
##################
You are an expert in **UI validation and accessibility testing**.  
Generate **manual test cases** for a **dropdown/checkbox** using the following details:  

- **Field Label**: {element['text']}  
- **ID**: {element['id']}  
- **Options Available**: {element.get('options', 'Not available')}  
- **Default Selected Option**: {element.get('default_selected', 'None')}  

### **Test Cases Should Cover:**  
✔ **Dropdown Selection Behavior** (Select valid/invalid options)  
✔ **Keyboard Navigation** (Use arrow keys to navigate)  
✔ **Default Value Verification**  
✔ **Multi-Select Behavior (if applicable)**  
✔ **Negative Scenarios** (Leaving the field blank if required)  
✔ **Accessibility Tests** (Screen readers, ARIA labels)  

Provide **at least 8 test cases** in a structured table format.
##########################
import openai
import json

def generate_jira_test_cases(ui_elements):
    """Generate Jira-compatible test cases based on UI elements."""
    jira_test_cases = []

    for element in ui_elements:
        prompt = f"""
        Generate structured manual test cases for Jira for the following UI element:

        **Element Details:**
        - **Tag:** {element['tag']}
        - **ID:** {element['id']}
        - **Name:** {element['name']}
        - **Text/Label:** {element['text']}
        - **Type:** {element['type']}
        - **Placeholder:** {element['placeholder']}
        - **Disabled:** {element['disabled']}
        - **Required:** {element['required']}
        - **Max Length:** {element['maxlength']}
        - **Href (if applicable):** {element['href']}

        **Test Cases Should Cover:**
        ✅ Functional testing  
        ✅ Edge cases & validation rules  
        ✅ Accessibility testing  
        ✅ Security testing (XSS, SQL Injection)  

        **Format Output as a JSON Object with these fields:**
        - `summary` (Test case title)
        - `test_id` (Unique ID, e.g., WEALTH-TEST-001)
        - `component` (e.g., Login Page)
        - `priority` (High/Medium/Low)
        - `labels` (e.g., UI, Validation)
        - `steps` (Step-by-step instructions)
        - `expected_result` (What should happen)
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert QA engineer."},
                      {"role": "user", "content": prompt}]
        )

        jira_test_case = json.loads(response["choices"][0]["message"]["content"])
        jira_test_cases.append(jira_test_case)

    return jira_test_cases

# Example usage
ui_elements = [
    {"tag": "input", "id": "email", "name": "email", "text": "Email", "type": "text",
     "placeholder": "Enter your email", "disabled": False, "required": True, "maxlength": 50, "href": None}
]

jira_cases = generate_jira_test_cases(ui_elements)
print(json.dumps(jira_cases, indent=2))


##########################################


### **Role:**  
You are an expert QA engineer specializing in manual testing. Your goal is to analyze the given **UI element** and generate well-structured test cases that cover all possible scenarios.  

---

### **UI Element Details:**  
- **Tag**: {element['tag']}  
- **ID**: {element['id']}  
- **Name**: {element['name']}  
- **Text/Label**: {element['text']}  
- **Type**: {element['type']}  
- **Placeholder**: {element['placeholder']}  
- **Disabled**: {element['disabled']}  
- **Required**: {element['required']}  
- **Max Length**: {element['maxlength']}  
- **Href (if applicable)**: {element['href']}  

---

### **Thought Process Before Generating Test Cases:**  
🔹 **Step 1: Understand the Purpose of the Element**  
   - What is its role on the page?  
   - How does a user interact with it?  
   - Is it mandatory or optional?  

🔹 **Step 2: Identify Functional Scenarios**  
   - What are the expected behaviors?  
   - How should it respond to valid/invalid inputs?  
   - Are there any **dependencies** on other fields?  

🔹 **Step 3: Explore Edge Cases & Validations**  
   - What are the input constraints (min/max length, special characters, formats)?  
   - How does the system handle unexpected inputs?  

🔹 **Step 4: Consider UI/UX Aspects**  
   - Is the element **properly aligned and readable**?  
   - Are tooltips, placeholders, and labels **clear and informative**?  

🔹 **Step 5: Ensure Accessibility & Security**  
   - Does it support **keyboard navigation**?  
   - Does it prevent **SQL Injection/XSS attacks**?  

---

### **Test Case Format:**  
- **Test Case Title:** (Concise description)  
- **Preconditions:** (If any)  
- **Test Steps:** (Step-by-step execution steps)  
- **Expected Result:** (What should happen if the test passes)  

---

### **Example Test Cases with Thought Process Applied:**  
**1️⃣ Test Case Title:** Validate Email Field with Invalid Input  
   - **Thought Process:**  
     - Email fields should only accept valid formats.  
     - Some common invalid formats: `test@`, `@test.com`, `test@com`, `test@.com`.  
   - **Preconditions:** User is on the login page.  
   - **Test Steps:**  
     1. Enter `invalid-email` in the email field.  
     2. Click the **Submit** button.  
   - **Expected Result:** The system should display an error message: `"Please enter a valid email address"`.  

---

**2️⃣ Test Case Title:** Verify Required Field Behavior  
   - **Thought Process:**  
     - The field is marked **required**, meaning submission should fail if left empty.  
   - **Preconditions:** User is on the login page.  
   - **Test Steps:**  
     1. Leave the email field blank.  
     2. Click the **Submit** button.  
   - **Expected Result:** The system should display an error message: `"This field is required"`.  

---

**3️⃣ Test Case Title:** Validate Email Field with Maximum Length  
   - **Thought Process:**  
     - If the email field has a **maxlength limit**, the system should prevent excessive input.  
     - If no limit is set, a very long email might break UI or cause unexpected behavior.  
   - **Preconditions:** User is on the login page.  
   - **Test Steps:**  
     1. Enter a long email exceeding 255 characters.  
     2. Click the **Submit** button.  
   - **Expected Result:** The system should either **restrict further input** beyond the max limit or show an **error message**.  

---

💡 **Now, generate at least 10 test cases using this structured approach!**  

# client_probe.py
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as c:
        tools = await c.list_tools()
        print(f"Tools available: {[t.name for t in tools]}")
        res = await c.call_tool("add", {"a": 2, "b": 3})
        print(f"Result of add tool: {res.content[0].text}")

asyncio.run(main())

# OpenAI client with MCP tool integration
import asyncio
import json
from openai import OpenAI
from fastmcp import Client as MCPClient

# load openai api key from environment variable
import os
import dotenv
dotenv.load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


openai sample###################################################
# MCP server URL
MCP_SERVER_URL = "http://localhost:8000/mcp"

async def get_mcp_tools():
    """Fetch available tools from MCP server"""
    try:
        async with MCPClient(MCP_SERVER_URL) as mcp_client:
            tools = await mcp_client.list_tools()
            return tools
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        return []

def convert_mcp_tools_to_openai_format(mcp_tools):
    """Convert MCP tools to OpenAI function calling format"""
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": tool.inputSchema.get("properties", {}),
                    "required": tool.inputSchema.get("required", [])
                }
            }
        })
    return openai_tools

async def call_mcp_tool(tool_name: str, tool_input: dict):
    """Call a tool from the MCP server"""
    try:
        async with MCPClient(MCP_SERVER_URL) as mcp_client:
            result = await mcp_client.call_tool(tool_name, tool_input)
            return result.content[0].text if result.content else "No result"
    except Exception as e:
        return f"Error calling MCP tool: {e}"

async def chat_with_mcp_tools(user_message: str):
    """Send a message to OpenAI and handle tool calls"""
    # Get MCP tools
    mcp_tools = await get_mcp_tools()
    if not mcp_tools:
        print("Warning: No MCP tools available")
        openai_tools = []
    else:
        openai_tools = convert_mcp_tools_to_openai_format(mcp_tools)
    
    messages = [{"role": "user", "content": user_message}]
    
    # Initial request to OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_tools if openai_tools else None,
        tool_choice="auto" if openai_tools else None
    )
    
    # Handle tool calls in a loop
    while response.choices[0].finish_reason == "tool_calls":
        # Process each tool call
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            
            print(f"\n[Tool Call] {tool_name} with input: {tool_input}")
            
            # Call the MCP tool
            tool_result = await call_mcp_tool(tool_name, tool_input)
            print(f"[Tool Result] {tool_result}")
            
            # Add assistant response and tool result to messages
            messages.append({"role": "assistant", "content": response.choices[0].message.content or ""})
            messages.append({
                "role": "user",
                "content": f"Tool {tool_name} returned: {tool_result}"
            })
        
        # Get next response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=openai_tools if openai_tools else None,
            tool_choice="auto" if openai_tools else None
        )
    
    # Return the final response
    return response.choices[0].message.content

async def main():
    # Test with different questions
    questions = [
        "What is Python?",
        "Can you add 5 and 3?",
        "Echo the word 'hello'",
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print('='*60)
        try:
            answer = await chat_with_mcp_tools(question)
            print(f"\nFinal Answer: {answer}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())


##############################
server
##################################
# server.py
from fastmcp import FastMCP

mcp = FastMCP("Example Remote MCP")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.tool
def echo(message: str, uppercase: bool = False) -> str:
    """Echo a message, optionally uppercased."""
    return message.upper() if uppercase else message

# Optional: a simple read-only resource
@mcp.resource("config://version")
def version():
    """Server version string."""
    return "1.0.0"

if __name__ == "__main__":
    # Expose as a REMOTE HTTP MCP endpoint:
    # Your endpoint will be http://localhost:8000/mcp
    mcp.run(transport="http", host="0.0.0.0", port=8000)

