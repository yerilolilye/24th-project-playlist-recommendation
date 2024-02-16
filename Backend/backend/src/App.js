// backend/src/App.js
const express = require('express');
const cors = require('cors');
const { execSync } = require('child_process');

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
    console.log('Output:', stdout);
    res.send(stdout);
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).send('Internal Server Error');
  }
});

function runPythonScriptSync(inputData) {
  try {
    const stdout = execSync(`python3 /home/dragonleedaniel0401/backend/src/logic/python_files/playlist.py ${inputData}`);
    return stdout.toString();
  } catch (error) {
    throw error;
  }
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});


