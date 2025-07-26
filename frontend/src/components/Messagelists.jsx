import React, { useEffect, useRef } from 'react';
import Message from './Message';
import { useChat } from '../context/ChatContext';

const MessageList = () => {
  const { state } = useChat();
  const endOfMessagesRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [state.messages]);

  return (
    <div className="message-list">
      {state.messages.map((msg, index) => (
        <Message key={index} message={msg} />
      ))}
      {state.isLoading && <Message message={{ role: 'ai', content: 'Typing...' }} />}
      <div ref={endOfMessagesRef} />
    </div>
  );
};

export default MessageList;