import React, { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { connectToRoom } from '../socket';
import Editor from '@monaco-editor/react';

const CodeBlock = () => {
    const { id } = useParams(); // Get the room ID from the URL parameters
    const navigate = useNavigate(); // Hook to programmatically navigate
    const [role, setRole] = useState(null); // Role of the user (either 'host' or 'guest')
    const [code, setCode] = useState(""); // Code to be edited in the editor
    const [studentsCount, setStudentsCount] = useState(0); // Number of students in the room
    const socketRef = useRef(null); // Ref to store the socket connection
    // const editorRef = useRef(null); // Ref to store the editor instance

    useEffect(() => {
        // Flag to check if the component is unmounted
        let isUnmounted = false;

        const socket = connectToRoom(id, (data) => {
            if (isUnmounted) return; // Ignore messages after unmount

            if (data.type === 'role') {
                setRole(data.role); // Set the role based on the data received from the socket
            } else if (data.type === 'participants') {
                setStudentsCount(data.students_count); // Update the number of students in the room
            } else if (data.type === 'redirect') {
                alert("Mentor has left the room. Redirecting to lobby.");
                navigate('/'); // Redirect to the lobby
            } else if (data.type === 'code_update') {
                setCode(data.code); // Update the code in the editor
            }
        });
        
        // Store the socket connection in the ref
        socketRef.current = socket;

        return () => {
            isUnmounted = true;
            if (
              socketRef.current &&
              (socketRef.current.readyState === WebSocket.OPEN ||
               socketRef.current.readyState === WebSocket.CONNECTING)
            ) {
              socketRef.current.close();
            }
            socketRef.current = null;
          };
          }, [id, navigate]); // Dependencies for useEffect: id and navigate

          const handleCodeChange = (newValue) => {
            setCode(newValue);
            if (role === 'student') {
              socketRef.current.send(JSON.stringify({
                type: 'code_update',
                code: newValue
              }));
            }
          };        

    return (
        <div>
            <h2>Code Block</h2>
            <p>Room ID: {id}</p>
            <p>Role: {role}</p>
            <p>Students in the room: {studentsCount}</p>
            <Editor
                height="60vh"
                defaultLanguage="javascript"
                value={code}
                onChange={handleCodeChange}
                options={{
                readOnly: role === 'mentor',
                fontSize: 16,
                }}
            />
        </div>
    );
};

export default CodeBlock;