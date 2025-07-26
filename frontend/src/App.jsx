import React from 'react';
import ChatWindow from './components/chatWindow';
import HistoryPanel from './components/HistoryPanel';

function App() {
  const handleSelectConversation = (id) => {
    // In a real app, this would trigger an action in your context
    // to fetch and load the messages for the selected conversation ID.
    console.log("Load conversation:", id);
    alert(`You clicked conversation ${id}. Implement the logic in ChatContext to load its messages!`);
  }

  return (
    <div className="app-container">
      <HistoryPanel onSelectConversation={handleSelectConversation} />
      <ChatWindow />
    </div>
  );
}

export default App;