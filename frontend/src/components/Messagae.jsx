import React from 'react';

const Message = ({ message }) => {
  // The `message` object should have `role` ('user' or 'ai') and `content`
  const messageClass = message.role;
  return (
    <div className={`message ${messageClass}`}>
      {message.content}
    </div>
  );
};

export default Message;