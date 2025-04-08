import React from 'react';
import Editor from '@monaco-editor/react';
import { useCodeBlock } from '../hooks/useCodeBlock';
import { ROLES } from '../constants';

/**
 * CodeBlock component renders a collaborative code editor room.
 * The component connects to a specific room, displays the user's role,
 * shows the number of students, and handles code editing with live updates.
 */
const CodeBlock = () => {
  const {
    roomId,
    userRole,
    code,
    isSolved,
    studentsCount,
    handleCodeChange,
  } = useCodeBlock();

  return (
    <div>
      <h2>Code Block</h2>
      <p>Room ID: {roomId}</p>
      <p>Role: {userRole}</p>
      <p>Students in the room: {studentsCount}</p>

      <Editor
        height="60vh"
        defaultLanguage="javascript"
        value={code}
        onChange={handleCodeChange}
        options={{
          readOnly: userRole === ROLES.MENTOR,
          fontSize: 16,
        }}
      />

      {isSolved && (
        <div
          style={{
            fontSize: '5rem',
            textAlign: 'center',
            marginTop: '-20px',
          }}
        >
          😄
        </div>
      )}
    </div>
  );
};

export default CodeBlock;
