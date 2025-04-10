import React from "react";
import Editor from "@monaco-editor/react";
import { ROLES } from "../constants";

/**
 * EditorSection component renders a code editor using Monaco Editor.
 * It allows users to edit code and reset it to its initial state.
*/
const EditorSection = ({ code, onResetRequest, handleCodeChange, userRole }) => {
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
            theme: "vs-dark",
          }}
        />

        {userRole === ROLES.STUDENT && (
          <button onClick={onResetRequest} className="reset-button">
            Reset Code
          </button>
        )}
      </div>
    );
};

export default EditorSection;
