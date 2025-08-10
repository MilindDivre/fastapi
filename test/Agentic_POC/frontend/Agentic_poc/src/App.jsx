import React, { useState, useRef, useEffect } from "react";
import { render } from "react-dom";
// import "./styles.css";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [intent, setIntent] = useState("");
  const [loading, setLoading] = useState(false);
  const [threads, setThreads] = useState([]);
  const [selectedThreadId, setSelectedThreadId] = useState(null);
  const threadIdRef = useRef(null);

  // Generate a thread_id if not present
  if (!threadIdRef.current) {
    threadIdRef.current = crypto.randomUUID();
  }

  // Fetch all threads on mount
  useEffect(() => {
    fetch("http://localhost:8000/threads")
      .then((res) => res.json())
      .then((data) => {
        setThreads(data.threads || []);
      });
  }, [response, intent]); // Refresh threads after each response

  const handleSend = () => {
    setLoading(true);
    setResponse("");
    setIntent("");
    const thread_id = threadIdRef.current;
    const eventSource = new EventSource(
      `http://localhost:8000/chat-sse?user_input=${encodeURIComponent(input)}&thread_id=${encodeURIComponent(
        thread_id
      )}`
    );
    let responseText = "";
    eventSource.onmessage = (event) => {
      console.log("SSE message:", event.data);
      // Ignore empty tokens
      if (!event.data.trim()) return;
      // If the event is the intent, set intent and close
      if (
        event.data === "greeting" ||
        event.data === "question" ||
        event.data === "complaint" ||
        event.data === "other"
      ) {
        setIntent(event.data);
        eventSource.close();
        setLoading(false);
      } else {
        // Otherwise, it's a token, so append to response
        responseText += event.data;
        setResponse(responseText);
      }
    };
    eventSource.onerror = (err) => {
      console.log("SSE error:", err);
      // Only show error if no response was received
      if (!responseText) {
        setResponse("Error receiving stream.");
        setIntent("");
      }
      eventSource.close();
      setLoading(false);
    };
  };

  // Select a thread from sidebar
  const handleSelectThread = (thread_id) => {
    setSelectedThreadId(thread_id);
    threadIdRef.current = thread_id;
    // Find last message in thread to show response
    const thread = threads.find((t) => t.thread_id === thread_id);
    if (thread && thread.messages.length > 0) {
      const lastMsg = thread.messages[thread.messages.length - 1];
      setResponse(lastMsg.response);
      setIntent(lastMsg.intent);
      setInput("");
    }
  };

  // Get current thread's messages
  const currentThread = threads.find((t) => t.thread_id === threadIdRef.current);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <div
        style={{
          width: 220,
          background: "#f7f7f7",
          borderRight: "1px solid #eee",
          padding: 16,
          overflowY: "auto",
        }}
      >
        <h3 style={{ marginTop: 0 }}>Your Chats</h3>
        <button
          style={{
            marginBottom: 12,
            width: "100%",
            padding: 8,
            borderRadius: 4,
            border: "none",
            background: "#007bff",
            color: "#fff",
          }}
          onClick={() => {
            // Start new thread
            const newId = crypto.randomUUID();
            threadIdRef.current = newId;
            setSelectedThreadId(newId);
            setResponse("");
            setIntent("");
            setInput("");
          }}
        >
          + New Chat
        </button>
        {threads.length === 0 && <div>No chats yet.</div>}
        {threads.map((thread) => (
          <div
            key={thread.thread_id}
            style={{
              padding: "8px 6px",
              marginBottom: 6,
              background: selectedThreadId === thread.thread_id ? "#e3eafc" : "#fff",
              borderRadius: 4,
              cursor: "pointer",
              border: selectedThreadId === thread.thread_id ? "1px solid #007bff" : "1px solid #eee",
            }}
            onClick={() => handleSelectThread(thread.thread_id)}
          >
            <strong>Chat {thread.thread_id.slice(0, 8)}</strong>
            <br />
            <span style={{ fontSize: 12, color: "#555" }}>
              {thread.messages.length > 0 ? thread.messages[0].user_input : "(empty)"}
            </span>
          </div>
        ))}
      </div>
      {/* Main Chat Area */}
      <div
        style={{
          flex: 1,
          maxWidth: 500,
          margin: "40px auto",
          padding: 20,
          border: "1px solid #eee",
          borderRadius: 8,
          background: "#fff",
        }}
      >
        <h2>LangGraph Chat Demo</h2>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{
            width: "100%",
            padding: 8,
            marginBottom: 10,
            borderRadius: 4,
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input}
          style={{
            padding: "8px 16px",
            borderRadius: 4,
            border: "none",
            backgroundColor: "#007bff",
            color: "#fff",
            cursor: loading || !input ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Sending..." : "Send"}
        </button>
        {/* Always show latest response and intent at the top of main area */}
        {response && (
          <div style={{ marginTop: 20 }}>
            <strong>Response:</strong> {response}
            <br />
            <strong>Intent:</strong> {intent}
          </div>
        )}
        {/* Collapsible chat history below response/intent */}
        {currentThread && currentThread.messages.length > 0 && (
          <details style={{ marginTop: 24 }}>
            <summary style={{ cursor: "pointer", fontWeight: "bold" }}>Show Chat History</summary>
            <div
              style={{
                maxHeight: 220,
                overflowY: "auto",
                background: "#f9f9f9",
                padding: 10,
                borderRadius: 6,
              }}
            >
              {currentThread.messages.map((msg, idx) => (
                <div key={idx} style={{ marginBottom: 12 }}>
                  <div style={{ fontWeight: "bold" }}>You:</div>
                  <div style={{ marginBottom: 4 }}>{msg.user_input}</div>
                  <div style={{ fontWeight: "bold" }}>Assistant:</div>
                  <div>{msg.response}</div>
                  <div style={{ fontSize: 12, color: "#888" }}>Intent: {msg.intent}</div>
                  <hr style={{ margin: "8px 0" }} />
                </div>
              ))}
            </div>
          </details>
        )}
      </div>
    </div>
  );
}

export default App;
