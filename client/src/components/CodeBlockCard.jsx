import React, {useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import CodeSnippetPreview from './CodeSnippetPreview';
import { fetchCodeBlock } from '../api/api';

/**
 * A component that represents a code block card in the lobby page to display and direct to the code block.
 * Contains title, a preview of the code, and a button to join the code block.
 */
const CodeBlockCard = ({ id, title }) => {
    const [block, setBlock] = React.useState({});
    const navigate = useNavigate();

    useEffect(() => {
        fetchCodeBlock(id).then((data) => {
            setBlock(data);
        });
    }, [id]);
    
    return (
        <div className="code-block-card">
        <h3>{title}</h3>
        <CodeSnippetPreview code={block.initial_code} />
        <button onClick={() => navigate(`/code/${id}`)}>Click to join room</button>
        </div>
    );
    }

export default CodeBlockCard;