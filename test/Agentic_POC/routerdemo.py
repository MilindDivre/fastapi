from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langgraph.checkpoint.memory import InMemorySaver

class ChatState(TypedDict):
    user_input: str
    intent: Literal["greeting", "question", "complaint", "other"]
    response: str

def identify_intent(state: ChatState):
    text = state["user_input"].lower()
    if "hello" in text or "hi" in text:
        return {"intent": "greeting"}
    elif "?" in text:
        return {"intent": "question"}
    elif "problem" in text or "not working" in text:
        return {"intent": "complaint"}
    else:
        return {"intent": "other"}

def handle_greeting(state: ChatState):
    return {"response": "Hello! How can I help you today?"}

def handle_question(state: ChatState):
    return {"response": "That's a great question! Let me find the answer."}

def handle_complaint(state: ChatState):
    return {"response": "I'm sorry to hear that. Can you provide more details?"}

def handle_other(state: ChatState):
    return {"response": "Can you please clarify your request?"}

def route_intent(state: ChatState):
    return state["intent"]

graph = StateGraph(ChatState)
graph.add_node("identify_intent", identify_intent)
graph.add_node("handle_greeting", handle_greeting)
graph.add_node("handle_question", handle_question)
graph.add_node("handle_complaint", handle_complaint)
graph.add_node("handle_other", handle_other)

graph.add_edge(START, "identify_intent")
graph.add_conditional_edges("identify_intent", route_intent, {
    "greeting": "handle_greeting",
    "question": "handle_question",
    "complaint": "handle_complaint",
    "other": "handle_other"
})
graph.add_edge("handle_greeting", END)
graph.add_edge("handle_question", END)
graph.add_edge("handle_complaint", END)
graph.add_edge("handle_other", END)
checkpoint_saver = InMemorySaver()
workflow = graph.compile(checkpointer=checkpoint_saver)
config1 = {"configurable":{"thread_id":"1"}}
workflow.invoke({
    "user_input": "what is python?"
},config=config1)

workflow.get_state(config1) # This will return final state of the workflow