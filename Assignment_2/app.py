from scorer import score_prompt
from dotenv import load_dotenv
load_dotenv()

def evaluate_prompt(prompt: str):
    result = score_prompt(prompt)
    return result.model_dump()

if __name__ == "__main__":
    test_prompt = "Write a blog post about AI."
    output = evaluate_prompt(test_prompt)
    print(output)