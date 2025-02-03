from utils import generate_script, execute_script, refine_script, load_instructions_from_json

def main():
    print("Welcome to JSON-based Browser Automation!")
    print("Loading instructions from 'instructions.json'...\n")

    # Load instructions from JSON file
    instructions = load_instructions_from_json("instructions.json")

    for idx, instruction in enumerate(instructions, start=1):
        print(f"Processing Task {idx}: {instruction}\n")

        # Generate Playwright script
        print("Generating Playwright script...")
        script_code = generate_script(instruction)
        print("\nGenerated Script:")
        print(script_code)

        # Execute the script
        print("\nExecuting script...")
        execution_result = execute_script(script_code)
        print(execution_result)

        # Check for errors and refine if needed
        if "failed" in execution_result.lower():
            error_message = execution_result.split("error:")[-1].strip()
            print("\nRefining script based on the error...")
            refined_code = refine_script(instruction, error_message)
            print("\nRefined Script:")
            print(refined_code)

            print("\nRe-executing refined script...")
            final_result = execute_script(refined_code)
            print(final_result)

    print("\nAll tasks completed!")

if __name__ == "__main__":
    main()
