
// 여기서부터 Python 스크립트 실행 로직
// ...
const { exec } = require('child_process');

const inputData = process.argv[2];

exec(`python3 trial.py ${inputData}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    // 에러가 발생하면 클라이언트에게 에러 메시지를 응답
    return res.status(500).send('Internal Server Error');
  }

  // Python 스크립트 실행 결과를 클라이언트에 전송
  console.log(`Python Script Output: ${stdout}`);
  console.error(`Python Script Errors: ${stderr}`);
  // 성공적으로 결과를 전송
  res.send(stdout);
});
