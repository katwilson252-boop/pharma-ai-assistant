import React, { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addUserChatMessage, sendChatMessage } from "../redux/interactionSlice";

export default function ChatAssistant() {
  const dispatch = useDispatch();
  const { chatMessages } = useSelector((s) => s.interaction);
  const [input, setInput] = useState("");
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [chatMessages]);

  const handleSend = () => {
    if (!input.trim()) return;
    dispatch(addUserChatMessage(input));
    dispatch(sendChatMessage({ message: input }));
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="card chat-panel">
      <h3>🤖 AI Assistant — Log interaction via chat</h3>
      <div className="chat-messages" ref={scrollRef}>
        {chatMessages.map((m, idx) => (
          <div key={idx} className={`chat-bubble ${m.role}`}>
            {m.text}
            {m.toolCalls?.length > 0 && (
              <div>
                {m.toolCalls.map((tc, i) => (
                  <span key={i} className="tool-tag">
                    🔧 {tc}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="chat-input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe interaction..."
        />
        <button className="btn" onClick={handleSend}>
          Log
        </button>
      </div>
    </div>
  );
}
