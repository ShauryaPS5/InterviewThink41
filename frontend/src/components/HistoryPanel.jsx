import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useChat } from '../context/ChatContext';

const HistoryPanel = () => {
  const [history, setHistory] = useState([]);
  const { loadConversation } = useChat();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        // In a real app with auth, user_id would be dynamic
        const response = await axios.get('/api/users/user123/conversations');
        setHistory(response.data);
      } catch (error) {
        console.error("Failed to fetch conversation history:", error);
      }
    };
    fetchHistory();
  }, [history]); // Refetch when history changes (e.g., new conversation starts)

  return (
    <div className="history-panel">
      <h3>Conversation History</h3>
      <ul>
        {history.map((convo) => (
          <li key={convo.id} onClick={() => loadConversation(convo.id)}>
            Conversation from {new Date(convo.created_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryPanel;