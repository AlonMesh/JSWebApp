import React from "react";
import { useNavigate } from 'react-router-dom';
import '../css/SecondaryTopicsSection.css';

/**
 * A section that displays the secondary code blocks (not the main 4) in the lobby page.
 * A list of code block buttons that redirect to the code block page.
 */
const SecondaryTopicsSection = ({ blocks }) => {
  const navigate = useNavigate();

  return (
    <section className="secondary-topics-section">
      <h2 className="section-title">Other Topics</h2>
      <div className="code-block-buttons-container">
        {blocks.map((block) => (
          <button
            key={block.id}
            className="secondary-topic-button"
            onClick={() => navigate(`/code/${block.id}`)}
          >
            {block.title}
          </button>
        ))}
      </div>
    </section>
  );
};

export default SecondaryTopicsSection;
