import React, { useState } from 'react';
import '../css/AddCodeBlockForm.css';
import { createCodeBlock } from '../api/api';

/**
 * Component for adding a new code block.
 * @param {function} onAdd - Callback function to handle the addition of a new code block.
*/
const AddCodeBlockForm = ({ onAdd }) => {
  const [title, setTitle] = useState('');
  const [initialCode, setInitialCode] = useState('');
  const [solutionCode, setSolutionCode] = useState('');
  const [successMessage, setSuccessMessage] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try { 
      // Send a POST request to add a new code block
      const newBlock = await createCodeBlock({
        title,
        initial_code: initialCode,
        solution_code: solutionCode,  
      });

      // Add the new block and reset the form
        onAdd(newBlock);
        setTitle('');
        setInitialCode('');
        setSolutionCode('');
        setSuccessMessage(true);

        // Automatically hide the success message after 5 seconds
        setTimeout(() => {
          setSuccessMessage(false);
        }, 5000);
      } 
    catch (error) {
      console.error("Error adding code block:", error);
      alert("An error occurred while adding the code block. Please try again.");
    }
  };

  return (
    <form className="add-code-block-form" onSubmit={handleSubmit}>
      <h3>Add a New Code Block</h3>

      <input
        type="text"
        className="title-input"
        placeholder="Enter block title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <div className="code-fields">
        <textarea
          className="code-input"
          placeholder="Initial code"
          value={initialCode}
          onChange={(e) => setInitialCode(e.target.value)}
          required
          rows={6}
        />
        <textarea
          className="code-input"
          placeholder="Solution code"
          value={solutionCode}
          onChange={(e) => setSolutionCode(e.target.value)}
          required
          rows={6}
        />
      </div>

      <button className="submit-button" type="submit">
        Add Block
      </button>

      {successMessage && (
        <div className="success-message">Code block added successfully!</div>
      )}
    </form>
  );
};

export default AddCodeBlockForm;
