import json
from pydantic import BaseModel, ValidationError
from typing import List
from langchain_groq import ChatGroq


class PromptScore(BaseModel):
    clarity: int
    specificity: int
    context: int
    output_format: int
    persona: int
    final_score: float
    explanation: str
    suggestions: List[str]


SYSTEM_PROMPT = """
You are a Prompt Quality Scoring Agent.

Given a user prompt, evaluate it on the following criteria (0–10 each):

1. Clarity – Is the goal clear and understandable?
2. Specificity – Are details, constraints, and requirements included?
3. Context – Is background, audience, or purpose provided?
4. Output Format – Does the prompt specify structure, tone, or length?
5. Persona – Does the prompt assign a role or perspective?

Return ONLY a JSON object with:
{
  "clarity": <0-10>,
  "specificity": <0-10>,
  "context": <0-10>,
  "output_format": <0-10>,
  "persona": <0-10>,
  "final_score": <average>,
  "explanation": "<short explanation>",
  "suggestions": ["...", "..."]
}
"""


def score_prompt(prompt: str) -> PromptScore:
    """
    Sends the prompt to the LLM, parses the JSON, validates it,
    and returns a PromptScore object.
    """

    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

    response = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.content

    try:
        parsed = json.loads(raw)
        validated = PromptScore(**parsed)
        return validated
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Invalid LLM output: {e}\nRaw output: {raw}")