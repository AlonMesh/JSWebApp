import React from "react";
import Editor from "@monaco-editor/react";
import { ROLES } from "../constants";

const EditorSection = ({ code, resetToInitialCode, handleCodeChange, userRole }) => {
    return (
        <div>
            <Editor
                height="60vh"
                defaultLanguage="javascript"
                value={code}
                onChange={handleCodeChange}
                options={{
                    readOnly: userRole === ROLES.MENTOR,
                    fontSize: 16,
                    theme: "vs-dark"
                }}
            />

            {userRole === ROLES.STUDENT && (
                <button onClick={resetToInitialCode} className="reset-button">
                Reset Code
                </button> 
            )}
        </div>
    );
};

export default EditorSection;
