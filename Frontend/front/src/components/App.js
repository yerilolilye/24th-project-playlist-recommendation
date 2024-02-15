import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState('');

  const handleRunPythonScript = async () => {
    try {
      const requestData = { inputData: inputText };
      console.log('Request Data:', requestData);
      const response = await fetch('http://34.64.45.132/runPythonScript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputData: inputText }),
      });
      if (!response.ok) {
      // 에러 응답 처리
      	throw new Error(`HTTP error! Status: ${response.status}`);
      }


      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button onClick={handleRunPythonScript}>Run Python Script</button>
      <div>
        <h2>Result:</h2>
        <p>{result}</p>
      </div>
    </div>
  );
}

export default App;


