// backend/src/App.js
const express = require('express');
const cors = require('cors');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.get('/api/data', (req, res) => {
  res.json({ message: 'Data from the backend!' });
});

app.post('/runPythonScript', (req, res) => {
  const inputData = req.body.inputData;
  console.log('Received Data:', inputData);

  try {
    const stdout = runPythonScriptSync(inputData);
    res.send(stdout);
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).send('Internal Server Error');
  }
});

function runPythonScriptSync(inputData) {
  try {
    const scriptPath = `${__dirname}/logic/python_files/playlist.py`;
    const stdout = execSync(`python3 ${scriptPath} ${inputData}`);
    // 결과 데이터가 저장된 파일 읽기
    const resultPath = '/home/dragonleedaniel0401/Backend/backend/result.json';
    const data = fs.readFileSync(resultPath, { encoding: "UTF-8" });
    
    // 파일 내용을 JSON으로 파싱
    const jsonData = JSON.parse(data);
    return jsonData;
  } catch (error) {
    throw error;
  }
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
