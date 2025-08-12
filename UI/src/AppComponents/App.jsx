import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! How can I help you today?' },
  ]);
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages(prev => [
      ...prev,
      { sender: 'user', text: input },
      { sender: 'bot', text: `You said: "${input}"` }, // Dummy bot response
    ]);
    setInput('');
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="bg-white shadow p-4 text-xl font-semibold text-center">
        ChatBot
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-xs ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-300 text-black'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="p-4 bg-white border-t flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          className="flex-1 border rounded-full px-4 py-2 focus:outline-none"
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default App;
