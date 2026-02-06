from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END

from models import EmailInput, Classification, WorkflowOutput, AgentDecision, FollowUp
from classifier import classification_chain
from agent import agent_executor
import json


class State(TypedDict):
    email: EmailInput
    classification: Classification
    agent_raw_output: Dict
    workflow_output: WorkflowOutput

def classify_node(state: State) -> State:
    print("****In Classify Node method*****")
    email = state["email"]
    classification = classification_chain.invoke({
        "subject": email.subject,
        "body": email.body
    })
    state["classification"] = classification
    return state

def agent_node(state: State) -> State:
    print("*****In Agent Node method*****")
    email = state["email"]
    cls = state["classification"]
    result = agent_executor.invoke({
        "subject": email.subject,
        "body": email.body,
        "urgency": cls.urgency,
        "topic": cls.topic
    })
    result1 = result["output"]
    result2 = json.loads(result1)
    state["agent_raw_output"] = result2
    print(state["agent_raw_output"])
    return state
    

def finalize_node(state: State) -> State:
    print("*****In Finalize Node method*****")
    cls = state["classification"]
    try:
        raw = state["agent_raw_output"]
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Invalid LLM output: {e}\nRaw output: {raw}")
    print(raw)
    #raw1 = json.loads(raw)
    #response_draft = raw["message"]

    print("<<<<<>>>>>>>")

    wf = WorkflowOutput(
        classification=cls,
        #response_draft=raw["response_draft"],
        response_draft=raw["response_draft"],
        decision=raw["decision"],
        #decision=AgentDecision(action = raw["decision"]),
        follow_up=raw["follow_up"]
        #follow_up=FollowUp(needed = raw["follow_up"])
    )
    state["workflow_output"] = wf
    print("####*****####")
    print(wf)
    print("####*****####")
    return state

graph = StateGraph(State)
graph.add_node("classify", classify_node)
graph.add_node("agentic", agent_node)
graph.add_node("finalize", finalize_node)

graph.set_entry_point("classify")
graph.add_edge("classify", "agentic")
graph.add_edge("agentic", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()