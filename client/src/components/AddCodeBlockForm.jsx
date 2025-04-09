import React, { useState } from 'react';

const AddCodeBlockForm = ({ onAdd }) => {
  const [title, setTitle] = useState('');
  const [initialCode, setInitialCode] = useState('');
  const [solutionCode, setSolutionCode] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:8000/code-blocks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        initial_code: initialCode,
        solution_code: solutionCode,
      }),
    });

    if (response.ok) {
      const newBlock = await response.json();
      onAdd(newBlock);
      setTitle('');
      setInitialCode('');
      setSolutionCode('');
    } else {
      alert('Failed to add code block');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '2rem' }}>
      <h3>Add a New Code Block</h3>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
        style={{ display: 'block', marginBottom: '0.5rem', width: '100%' }}
      />
      <textarea
        placeholder="Initial code"
        value={initialCode}
        onChange={(e) => setInitialCode(e.target.value)}
        required
        rows={4}
        style={{ display: 'block', marginBottom: '0.5rem', width: '100%' }}
      />
      <textarea
        placeholder="Solution code"
        value={solutionCode}
        onChange={(e) => setSolutionCode(e.target.value)}
        required
        rows={4}
        style={{ display: 'block', marginBottom: '0.5rem', width: '100%' }}
      />
      <button type="submit">Add Block</button>
    </form>
  );
};

export default AddCodeBlockForm;
