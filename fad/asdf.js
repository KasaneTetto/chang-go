const http = require('http');
const fs = require('fs');

/**
 * POST 요청을 보내는 Promise 래퍼 함수
 * @param {string} postData - JSON.stringify 된 요청 body
 * @returns {Promise<object>} - { statusCode, data }
 */
function sendPostRequest(postData) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'haneul.wiki',
      port: 80,
      path: '/aclgroup',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Cookie': 'honoka: e2X1_dmWstz7E0va8Xg6zH-JU-R0vixTmiF12OQYVnG3chpTBI6vSetsH-htVyhGrqyOWYNUwqU-MHQdPj6HX4wtvxGCdErIHLwKKpbAIV4eVUGVSQM-FuwSqB8YGnno;kotori=s^%^3AwhwvYNX-0rk956GsU__HtgbBU09GnJMq.2tV9YNYc^%^2FmWvmc2vA306ERyPNoN8JC4JW27tsmDxbcU'
      }
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          data: responseData
        });
      });
    });

    req.on('error', (e) => {
      reject(e);
    });

    req.write(postData);
    req.end();
  });
}

async function main() {
  try {
    // a.txt: 각 줄에 IPv4 대역(CIDR 형식)이 있다고 가정
    const ipFileContent = fs.readFileSync('a.txt', 'utf8');
    // b.txt: 각 줄에 "오류있는 IPv4대역 - 텍스트" 형태로 되어 있음.  
    // note로 사용할 텍스트는 대시(-) 이후의 부분 (대시가 없으면 전체 사용)
    const noteFileContent = fs.readFileSync('b.txt', 'utf8');

    // 각 파일의 내용을 줄 단위 배열로 분리 (빈 줄은 제외)
    const ipLines = ipFileContent.split('\n').map(line => line.trim()).filter(Boolean);
    const noteLines = noteFileContent.split('\n').map(line => line.trim()).filter(Boolean);

    // 두 파일의 줄 수 중 더 적은 줄만큼 요청
    const totalLines = Math.min(ipLines.length, noteLines.length);

    for (let i = 0; i < totalLines; i++) {
      const ipValue = ipLines[i];

      // b.txt의 해당 줄에서 '-' 이후의 텍스트를 note로 사용 (없으면 전체 사용)
      let noteText = noteLines[i];
      if (noteText.includes('-')) {
        const parts = noteText.split('-');
        noteText = parts.slice(1).join('-').trim();
      }

      // 요청 body 구성
      const requestBody = {
        group: 'b17c9924-1293-4586-897e-a9071dca4610',
        mode: 'ip',
        ip: ipValue,
        note: noteText,
        duration: 0,
        hidelog: 'N'
      };

      const postData = JSON.stringify(requestBody);
      console.log(`\n[Line ${i + 1}] Request Body: ${postData}`);

      try {
        const response = await sendPostRequest(postData);
        console.log(`[Line ${i + 1}] Response Status: ${response.statusCode}`);
        console.log(`[Line ${i + 1}] Response Data: ${response.data}`);
      } catch (error) {
        console.error(`[Line ${i + 1}] Request Error: ${error.message}`);
      }
    }
  } catch (err) {
    console.error('파일 읽기 에러:', err.message);
  }
}

main();
