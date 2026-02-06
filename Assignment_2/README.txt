 Overview
This project implements a Prompt Quality Scoring Agent using LangChain and OpenAI models.
Given any text prompt, the agent evaluates it across five criteria:
- Clarity
- Specificity / Details
- Context
- Output Format & Constraints
- Persona Definition
The agent returns:
- Individual scores (0–10)
- A final averaged score
- A short explanation
- 2–3 improvement suggestions
All results are validated using a Pydantic model for reliability.