import { useEffect, useRef, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { connectToRoom } from '../socket';
import { MESSAGE_TYPES, ROLES } from '../constants';

/**
 * Custom hook that manages all logic for a collaborative code block room.
 * Handles socket connection, role assignment, real-time code syncing,
 * participant tracking, and solution detection.
 */
export const useCodeBlock = () => {
  // Extract room ID from URL
  const { id: roomId } = useParams();

  // Used for navigation
  const navigate = useNavigate();

  // State hooks
  const [userRole, setUserRole] = useState(null); 
  const [code, setCode] = useState(''); 
  const [studentsCount, setStudentsCount] = useState(0); 
  const [isSolved, setIsSolved] = useState(false); 
  const [initialCode, setInitialCode] = useState('');


  // WebSocket connection reference
  const socketRef = useRef(null);

  // Handles incoming WebSocket messages and updates state accordingly
  const handleSocketMessage = useCallback((data) => {
    switch (data.type) {
      case MESSAGE_TYPES.ROLE:
        setUserRole(data.role);
        break;
      case MESSAGE_TYPES.PARTICIPANTS:
        setStudentsCount(data.students_count);
        break;
      case MESSAGE_TYPES.REDIRECT:
        alert('Mentor has left the room. Redirecting to lobby.');
        navigate('/');
        break;
      case MESSAGE_TYPES.CODE_UPDATE:
        setCode(data.code);
        if (!initialCode) {
          setInitialCode(data.code);
        }
        break;
      case MESSAGE_TYPES.CODE_RESET:
        setCode(data.code);
        break;
      case MESSAGE_TYPES.SOLVED:
        setIsSolved(true);
        break;
      default:
        break;
    }
  }, [navigate, initialCode]);

  // Establishes WebSocket connection when the component mounts 
  useEffect(() => {
    if (socketRef.current) return; // Prevents multiple connections

    socketRef.current = connectToRoom(roomId, handleSocketMessage);

    return () => {
      if (
        socketRef.current &&
        (socketRef.current.readyState === WebSocket.OPEN ||
          socketRef.current.readyState === WebSocket.CONNECTING)
      ) {
        socketRef.current.close();
      }
      socketRef.current = null;
    };
  }, [roomId, handleSocketMessage]);

  // Handles code changes made by the user
  const handleCodeChange = (newValue) => {
    setCode(newValue);
    if (userRole === ROLES.STUDENT) {
      socketRef.current.send(
        JSON.stringify({ type: MESSAGE_TYPES.CODE_UPDATE, code: newValue })
      );
    }
  };
  
  // Redirects the user back to the lobby
  const backToLobby = () => {
    navigate('/');
  };

  // Requests a code reset from the server
  const sendCodeResetRequest = () => {
    if (userRole === ROLES.STUDENT && socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: MESSAGE_TYPES.CODE_RESET }));
    }
  };
  
  return {
    roomId,
    userRole,
    code,
    isSolved,
    studentsCount,
    handleCodeChange,
    backToLobby,
    sendCodeResetRequest, 
  };
};
