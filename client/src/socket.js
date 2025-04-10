import { WS_BASE } from './api/config';

export const connectToRoom = (roomID, onMessage) => {
    const socket = new WebSocket(`${WS_BASE}/ws/${roomID}`);
  
    socket.onopen = () => {
        console.log('WebSocket connected to the room:', roomID);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        onMessage(data);
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed for room:', roomID);
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    return socket;
};