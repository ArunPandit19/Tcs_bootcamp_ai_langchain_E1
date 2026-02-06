from langchain_openai import ChatOpenAI
#from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tools import tools
from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from langchain_groq import ChatGroq


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

agent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI support agent."
     "Use the provided tools, if required, to complete the task. "
     "If you need information, you can call a tool. "
     "If you have enough information, respond with a final answer. "
     "Provide output in JSON format only."
     "Do NOT invent tools. Do NOT call tools that are not listed."
     "Return a JSON object with keys: response_draft, decision, follow_up."),
    ("human",
     "Email:\nSubject: {subject}\nBody: {body}\n\n"
     "Classification:\nUrgency: {urgency}\nTopic: {topic}"),
     ("assistant", "{agent_scratchpad}")

])

agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)