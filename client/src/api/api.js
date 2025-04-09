import axios from 'axios';

const API_BASE = 'http://localhost:8000'; 

/**
 * Fetches code blocks from the API.
 *
 * @async
 * @function fetchCodeBlocks
 * @returns {Promise<Object>} A promise that resolves to the data containing code blocks.
 * @throws {Error} Throws an error if the API request fails.
 */
export const fetchCodeBlocks = async () => {
  const res = await axios.get(`${API_BASE}/code-blocks`);
  return res.data;
};

/**
 * Fetches a specific code block by its ID from the API.
*/
export const fetchCodeBlock = async (id) => {
  const res = await axios.get(`${API_BASE}/code-blocks/${id}`);
  return res.data;
};