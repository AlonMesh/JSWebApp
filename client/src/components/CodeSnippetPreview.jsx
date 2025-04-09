import React from 'react';

/**
 * A small, read-only code preview box.
 * Typically used within a code block card on the lobby page.
*/
const CodeSnippetPreview = ({ code }) => {
  return (
    <div
      style={{
        backgroundColor: '#1e1e1e',
        color: '#d4d4d4',
        padding: '0.75rem',
        borderRadius: '8px',
        fontFamily: 'monospace',
        fontSize: '0.9rem',
        overflowX: 'auto',
        maxHeight: '6rem',
        whiteSpace: 'pre',
        boxShadow: 'inset 0 0 0 1px #333',
      }}
    >
      {code || '// Code preview not available'}
    </div>
  );
};

export default CodeSnippetPreview;
