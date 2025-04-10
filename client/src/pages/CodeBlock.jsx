import React, {useState} from 'react';
import { useCodeBlock } from '../hooks/useCodeBlock';
import RoomInfoPanel from '../components/RoomInfoPanel';
import EditorSection from '../components/EditorSection';
import SmileyModal from '../components/SmileyModal';
import LobbyHeader from '../components/LobbyHeader';
import '../css/CodeBlock.css';

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
    backToLobby,
    sendCodeResetRequest,
  } = useCodeBlock();

  const [showModal, setShowModal] = useState(true);

  return (
    <div>
      <LobbyHeader />
      <div className="code-block-wrapper">
      <div className="top-bar">
        <button className="back-button" onClick={backToLobby}>Back to Lobby</button>
      </div>

      <div className="main-content">
        <div className="room-info-panel">
          <RoomInfoPanel 
          roomId={roomId} 
          userRole={userRole} 
          studentsCount={studentsCount} 
          />
        </div>

        <div className="editor-section">
          <EditorSection
            code={code}
            onResetRequest={sendCodeResetRequest}
            handleCodeChange={handleCodeChange}
            userRole={userRole}
          />
        </div>
      </div>

      {isSolved && showModal && (
        <SmileyModal onClose={() => setShowModal(false)} />
      )}
    </div>
    </div>
  );
};

export default CodeBlock;
