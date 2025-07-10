import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const chatEndRef = useRef(null);
  const formatTime = (time) => new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  useEffect(() => {
    document.body.className = darkMode ? "dark" : "";
  }, [darkMode]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = { from: "user", text: trimmed, time: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://intuitive-enchantment-production.up.railway.app/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      const data = await res.json();
      const botMsg = { from: "bot", text: data.response, time: new Date() };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "Error: Could not reach backend.", time: new Date() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleDarkMode = () => setDarkMode((prev) => !prev);

  return (
    <div className={darkMode ? "chat-container dark" : "chat-container"}>
      <nav className="navbar">
        <h2>Joana - ChatBot</h2>
        <button onClick={toggleDarkMode}>{darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}</button>
      </nav>

      <div className="instructions">
        <p><strong>Try:</strong></p>
        <ul>
          <li><code>question: Who is the current president of USA?</code></li>
          <li><code>summarize: [paste some long text]</code></li>
        </ul>
      </div>

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`msg ${msg.from}`}>
            <b>{msg.from === "user" ? "You" : "Joana"}</b>
            <div>{msg.text}</div>
            <span className="timestamp">{formatTime(msg.time)}</span>
          </div>
        ))}
        {loading && <div className="msg bot"><em>Joana is typing...</em></div>}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <textarea
          rows="1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message and hit Enter..."
        />
        <button onClick={sendMessage} disabled={loading}>Send</button>
      </div>
    </div>
  );
}

export default App;
