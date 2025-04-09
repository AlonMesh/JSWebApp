import React from 'react';
import { FaUsers } from 'react-icons/fa';

const RoomInfoPanel = ({ roomId, userRole, studentsCount }) => {
    return (
        <div>
            <h2>Room Info</h2>
            <p>Room ID: {roomId}</p>
            <p>Role: {userRole}</p>
            <div className="room-icon">
            <FaUsers />
            <p>Students: {studentsCount}</p>
            </div>
            <button className="share-button"
            onClick={() => navigator.clipboard.writeText(window.location.href)}
            >
            Share Room
            </button>
        </div>
    )
}

export default RoomInfoPanel;