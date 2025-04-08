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

  // Used for navigation (e.g., redirecting when mentor disconnects)
  const navigate = useNavigate();

  // State hooks
  const [userRole, setUserRole] = useState(null); // 'mentor' or 'student'
  const [code, setCode] = useState(''); // Code shown in the editor
  const [studentsCount, setStudentsCount] = useState(0); // Number of students
  const [isSolved, setIsSolved] = useState(false); // True if code matches the solution

  // WebSocket connection reference
  const socketRef = useRef(null);

  /**
   * Handles incoming WebSocket messages.
   * Delegates logic by message type.
   */
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
        break;
      case MESSAGE_TYPES.SOLVED:
        setIsSolved(true);
        break;
      default:
        break;
    }
  }, [navigate]);

  /**
   * Establish WebSocket connection on component mount,
   * and clean it up when the component unmounts.
   */
  useEffect(() => {
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

  /**
   * Triggered when the code editor content changes.
   * Sends the new code to the server if the user is a student.
   */
  const handleCodeChange = (newValue) => {
    setCode(newValue);
    if (userRole === ROLES.STUDENT) {
      socketRef.current.send(
        JSON.stringify({ type: MESSAGE_TYPES.CODE_UPDATE, code: newValue })
      );
    }
  };

  return {
    roomId,
    userRole,
    code,
    isSolved,
    studentsCount,
    handleCodeChange,
  };
};
