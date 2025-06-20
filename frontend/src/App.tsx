
import React, { useState, useEffect } from "react";
import axios from "axios";

const backend = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function App() {
  const [chats, setChats] = useState<any[]>([]);
  const [currentChat, setCurrentChat] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    axios.get(`${backend}/chats`).then(res => setChats(res.data));
  }, []);

  const loadChat = (chat_id: string) => {
    setCurrentChat(chat_id);
    axios.get(`${backend}/chat/${chat_id}`).then(res => {
      setMessages(res.data.messages || []);
    });
  };

  const send = () => {
    if (!currentChat) return;
    axios.post(`${backend}/chat`, {
      chat_id: currentChat,
      content: input
    }).then(res => {
      setMessages([...messages, { from: "user", text: input }, { from: "bot", text: res.data.response }]);
      setInput("");
    });
  };

  const newChat = () => {
    axios.post(`${backend}/chat/new`).then(res => {
      loadChat(res.data.chat_id);
      setChats([...chats, { chat_id: res.data.chat_id }]);
    });
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ width: 200, borderRight: '1px solid #ccc', padding: 10 }}>
        <button onClick={newChat}>+ New Chat</button>
        <ul>
          {chats.map(chat => (
            <li key={chat.chat_id} onClick={() => loadChat(chat.chat_id)} style={{ cursor: 'pointer' }}>
              {chat.chat_id.slice(0, 8)}
            </li>
          ))}
        </ul>
      </div>
      <div style={{ flex: 1, padding: 10 }}>
        <div style={{ height: '85%', overflowY: 'auto' }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{ textAlign: msg.from === "user" ? "right" : "left" }}>
              <p><strong>{msg.from}:</strong> {msg.text}</p>
            </div>
          ))}
        </div>
        <div style={{ height: '15%' }}>
          <input value={input} onChange={e => setInput(e.target.value)} style={{ width: '80%' }} />
          <button onClick={send}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
