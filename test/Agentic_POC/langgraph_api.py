from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel
import uvicorn
from sse_starlette.sse import EventSourceResponse
from fastapi import Query
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI, AsyncOpenAI
import os
import sqlite3
from typing import List, Dict, Any
import uuid

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatState(TypedDict):
    user_input: str
    intent: Literal["greeting", "question", "complaint", "other"]
    response: str

class ChatRequest(BaseModel):
    user_input: str
    thread_id: str  # Add this field

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

gpt = ChatOpenAI(model="gpt-3.5-turbo")

def handle_greeting(state: ChatState):
    prompt = f"You are a helpful assistant. Greet the user and offer help. User said: {state['user_input']}"
    response = gpt.invoke(prompt).content
    return {"response": response}

def handle_question(state: ChatState):
    prompt = f"You are a helpful assistant. Answer the user's question: {state['user_input']}"
    response = gpt.invoke(prompt).content
    return {"response": response}

def handle_complaint(state: ChatState):
    prompt = f"You are a helpful assistant. Address the user's complaint: {state['user_input']}"
    response = gpt.invoke(prompt).content
    return {"response": response}

def handle_other(state: ChatState):
    prompt = f"You are a helpful assistant. Respond to the user's message: {state['user_input']}"
    response = gpt.invoke(prompt).content
    return {"response": response}

def route_intent(state: ChatState):
    return state["intent"]

conn = sqlite3.connect(database='chat_state.db',check_same_thread=False)
checkpoint_saver = SqliteSaver(conn)

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
# checkpoint_saver = InMemorySaver()
workflow = graph.compile(checkpointer=checkpoint_saver)

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.user_input
    thread_id = request.thread_id
    config = {"configurable": {"thread_id": thread_id}}
    result = workflow.invoke({"user_input": user_input}, config=config)
    return {"response": result["response"], "intent": result["intent"]}

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/chat-sse")
async def chat_sse(user_input: str = Query(...), thread_id: str = Query(...)):
    config = {"configurable": {"thread_id": thread_id}}
    # Get previous chat history for this thread
    def get_thread_history(thread_id):
        cursor = conn.cursor()
        cursor.execute("SELECT checkpoint FROM checkpoints WHERE thread_id=?", (thread_id,))
        import msgpack
        history = []
        for (checkpoint_blob,) in cursor.fetchall():
            try:
                state = msgpack.unpackb(checkpoint_blob, raw=False)
            except Exception:
                state = {}
            chat = state.get("channel_values", {})
            user = chat.get("user_input", "")
            assistant = chat.get("response", "")
            if user:
                history.append({"role": "user", "content": user})
            if assistant:
                history.append({"role": "assistant", "content": assistant})
        return history

    # Identify intent first
    intent_result = identify_intent({"user_input": user_input, "intent": "", "response": ""})
    intent = intent_result["intent"]

    # Build messages for OpenAI: system prompt + previous history + current user input
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant. Remember user details and context from previous messages in this conversation. Always use prior information to answer follow-up questions."
    }
    messages = [system_prompt] + get_thread_history(thread_id)
    messages.append({"role": "user", "content": user_input})

    async def event_generator():
        response_text = ""
        # Stream tokens from OpenAI
        stream = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        async for chunk in stream:
            token = getattr(chunk.choices[0].delta, "content", None)
            if token is not None:
                response_text += token
                yield f"data: {token}\n\n"  # Stream tokens separately
        # After streaming response, send intent
        yield f"data: intent:{intent}\n\n"  # Prefix intent with 'intent:' for clarity
        # Save the message to the database using the workflow
        workflow.invoke({"user_input": user_input}, config=config)

    return EventSourceResponse(event_generator())

# Function to extract all threads and their messages from the SqliteSaver database
def get_all_threads(conn) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    # Each thread_id is a conversation, each message is a state snapshot
    cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
    threads = []
    for (thread_id,) in cursor.fetchall():
        cursor.execute("SELECT checkpoint FROM checkpoints WHERE thread_id=?", (thread_id,))
        messages = []
        import msgpack
        for (checkpoint_blob,) in cursor.fetchall():
            # checkpoint_blob is a msgpack-encoded dict
            try:
                state = msgpack.unpackb(checkpoint_blob, raw=False)
            except Exception:
                state = {}
            chat = state.get("channel_values", {})
            messages.append({
                "user_input": chat.get("user_input", ""),
                "response": chat.get("response", ""),
                "intent": chat.get("intent", "")
            })
        threads.append({
            "thread_id": thread_id,
            "messages": messages
        })
    return threads

@app.get("/threads")
async def threads():
    all_threads = get_all_threads(conn)
    return {"threads": all_threads}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
