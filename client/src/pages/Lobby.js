import React, { useEffect, useState } from 'react';
import { fetchCodeBlocks } from '../api/api';
import { useNavigate } from 'react-router-dom';

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
    </div>
  );
};

export default Lobby;
