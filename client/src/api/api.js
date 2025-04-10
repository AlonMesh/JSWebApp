import axios from 'axios';
import { API_BASE } from './config';

// const API_BASE = "http://localhost:8000"

// Fetches code blocks from the API.
export const fetchCodeBlocks = async () => {
  console.log("Fetching code blocks from API...", API_BASE);
  const res = await axios.get(`${API_BASE}/code-blocks`);
  return res.data;
};

// Fetches a specific code block by its ID from the API.
export const fetchCodeBlock = async (id) => {
  const res = await axios.get(`${API_BASE}/code-blocks/${id}`);
  return res.data;
};

// Creates a new code block in the API.
export const createCodeBlock = async ({title, initial_code, solution_code}) => {
  const res = await axios.post(`${API_BASE}/code-blocks`, {
    title,
    initial_code,
    solution_code,
  });
  return res.data;
}