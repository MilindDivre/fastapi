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