import React, { useEffect, useState } from 'react'; 
import { fetchCodeBlocks } from '../api/api';
import AddCodeBlockForm from '../components/AddCodeBlockForm';
import LobbyHeader from '../components/LobbyHeader';
import FeaturedTopicsSection from '../components/FeaturedTopicsSection';
import SecondaryTopicsSection from '../components/SecondaryTopicsSection';
import '../css/Lobby.css';

/**
 * Lobby component renders the main lobby page of the application.
 * It fetches code blocks from the API and displays them in sections.
 * Users can also add new code blocks through a form.
 */
const Lobby = () => {
  const [blocks, setBlocks] = useState([]);

  useEffect(() => {
    fetchCodeBlocks().then(setBlocks);
  }, []);

  return (
    <div>
      <LobbyHeader />
      <FeaturedTopicsSection blocks={blocks.slice(0, 4)} />
      <SecondaryTopicsSection blocks={blocks.slice(4)} />
      <AddCodeBlockForm onAdd={(newBlock) => setBlocks((prev) => [...prev, newBlock])} /> {/* Add new block to the list */}
    </div>
  );
};

export default Lobby;
