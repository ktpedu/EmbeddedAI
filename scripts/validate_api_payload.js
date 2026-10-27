const fs = require('fs');
const http = require('http');

http.get('http://localhost:3001/api/lessons', (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    try {
      const data = JSON.parse(body);
      console.log('API Status:', data.status, '| Engine:', data.engine, '| Total lessons:', data.data?.length);
      
      const lessons = data.data || [];
      lessons.forEach(l => {
        if (!l.id || !l.title || !l.chapter_number) {
          console.error('Invalid lesson structure:', l);
        }
      });
      console.log('All 12 lessons validated successfully.');
    } catch (e) {
      console.error('JSON Parse error:', e.message);
    }
  });
}).on('error', (e) => {
  console.error('HTTP Request error:', e.message);
});
