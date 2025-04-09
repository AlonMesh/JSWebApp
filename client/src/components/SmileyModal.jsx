import React from 'react';
import '../css/SmileyModal.css';

const SmileyModal = ({ onClose }) => {
  return (
    <div className="smiley-overlay">
      <div className="smiley-modal">
        <button className="close-btn" onClick={onClose}>×</button>
        <div className="smiley-content">
          <div className="smiley-icon">😄</div>
          <h2>Great job!</h2>
          <p>The students solved the code block successfully.</p>
        </div>
      </div>
    </div>
  );
};

export default SmileyModal;
