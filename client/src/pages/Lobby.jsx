import React, { useEffect, useState } from 'react';
import { fetchCodeBlocks } from '../api/api';
import { useNavigate } from 'react-router-dom';
import AddCodeBlockForm from '../components/AddCodeBlockForm';

const Lobby = () => {
  const [blocks, setBlocks] = useState([]);
  const navigate = useNavigate();  // useNavigate hook to programmatically navigate

  useEffect(() => {
    fetchCodeBlocks().then(setBlocks);
  }, []);

  return (
    <div>
      <h1>Choose code block</h1>
      <ul>
        {blocks.map((block) => (
          <li key={block.id}>
            <button onClick={() => navigate(`/code/${block.id}`)}> {/* Navigate to the code block page */}
              {block.title}
            </button>
          </li>
        ))}
      </ul>
      <AddCodeBlockForm onAdd={(newBlock) => setBlocks((prev) => [...prev, newBlock])} /> {/* Add new block to the list */}
    </div>
  );
};

export default Lobby;
