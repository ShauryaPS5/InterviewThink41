import React from 'react';

// Mock data - in a real app, you'd fetch this from your backend
const mockHistory = [
  { id: 101, title: 'Order Status #ORD123' },
  { id: 102, title: 'Stock for Classic T-Shirt' },
  { id: 103, title: 'Top selling products' },
];

const HistoryPanel = ({ onSelectConversation }) => {
  return (
    <div className="history-panel">
      <h3>Conversation History</h3>
      <ul>
        {mockHistory.map((convo) => (
          <li key={convo.id} onClick={() => onSelectConversation(convo.id)}>
            {convo.title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryPanel;