# Example usage code for DetoxioModelDynamicScanner

# Assuming you have already imported the necessary modules and classes

from conocer.scanner import DetoxioModelDynamicScanner

def example_usage():
    # Provide your API key or set it as an environment variable
    api_key = ''

    # Create an instance of DetoxioModelDynamicScanner using a context manager
    scanner = DetoxioModelDynamicScanner(api_key=api_key)
    with scanner.new_session() as session:
        # Generate prompts
        prompt_generator = session.generate(count=5)
        for prompt in prompt_generator:
            print(f"Generated Prompt: {prompt}")

            # Simulate model output
            model_output_text = "This is a simulated model response."

            # Evaluate the model interaction
            evaluation_response = session.evaluate(prompt, model_output_text)

        # Print the evaluation response
        print(f"Evaluation: {session.get_report().as_dict()}")

if __name__ == "__main__":
    example_usage()