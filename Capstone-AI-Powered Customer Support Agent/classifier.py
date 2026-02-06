from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from models import Classification
from langchain_groq import ChatGroq


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

classification_parser = PydanticOutputParser(pydantic_object=Classification)

classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify urgency and topic for the email."),
    ("human", "Subject: {subject}\n\nBody:\n{body}\n\n"
              "Return JSON: {format_instructions}")
]).partial(format_instructions=classification_parser.get_format_instructions())

classification_chain = classification_prompt | llm | classification_parser