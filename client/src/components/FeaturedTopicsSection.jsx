import React from 'react';
import CodeBlockCard from './CodeBlockCard';

/**
 * A section that displays the main 4 code blocks in the lobby page.
 * Contains a title and a list of code block cards.
 */

const FeaturedTopicsSection = ({ blocks }) => {
  return (
    <section className="featured-topics-section">
      <h2>Featured Topics</h2>
      <div className="code-block-cards-container">
        {blocks.map((block) => (
          <CodeBlockCard key={block.id} id={block.id} title={block.title} />
        ))}
      </div>
    </section>
  );
}

export default FeaturedTopicsSection;

