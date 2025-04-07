import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Lobby from './pages/Lobby';
import CodeBlock from './pages/CodeBlock';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Lobby />} />
        {/* /code/:id route to be added later */}
        <Route path="/code/:id" element={<CodeBlock />} />
      </Routes>
    </Router>
  );
}

export default App;
