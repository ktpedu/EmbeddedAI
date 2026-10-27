const fs = require('fs');
const path = require('path');

const appJsPath = path.join(__dirname, '..', 'web_learning_platform', 'public', 'js', 'app.js');
let content = fs.readFileSync(appJsPath, 'utf8');

// 1. Static fallback for fetchAllData
const targetData = `    state.lessons = resLessons.data || [];
    state.quizzes = resQuizzes.data || [];
    state.practicalExams = resPractical.data || [];
    state.worksheets = resWorksheets.data || [];
    state.materials = resMaterials.data || [];
    state.scores = resScores.data || [];
    state.stats = resStats.stats || {};
    state.students = resStudents.data || [];
    state.submissions = resSubmissions.data || [];`;

const replacementData = targetData + `\n
    // Fallback โหลดข้อมูล Static สำหรับ GitHub Pages / Static Hosting
    if (!state.lessons || state.lessons.length === 0) {
      try {
        const seedRes = await fetch('data/seed.json');
        if (seedRes.ok) {
          const seed = await seedRes.json();
          state.lessons = seed.lessons || [];
          if (!state.quizzes.length) state.quizzes = seed.quizzes || [];
          if (!state.practicalExams.length) state.practicalExams = seed.practical_exams || [];
          if (!state.worksheets.length) state.worksheets = seed.worksheets || [];
          if (!state.materials.length) state.materials = seed.materials || [];
          if (!state.students.length) state.students = seed.students || [];
          if (!state.scores.length) state.scores = seed.scores || [];
          console.log('[GitHub Pages Mode] โหลด seed.json สำเร็จ');
        }
      } catch (e) {
        console.warn('[Static Fallback Notice]:', e.message);
      }
    }`;

// Normalize line endings for replacement
const isCRLF = content.includes('\r\n');
const normalizedTarget = isCRLF ? targetData.replace(/\n/g, '\r\n') : targetData;
const normalizedReplacement = isCRLF ? replacementData.replace(/\n/g, '\r\n') : replacementData;

if (content.includes(normalizedTarget)) {
  content = content.replace(normalizedTarget, normalizedReplacement);
  console.log('1. Injected static data fallback successfully!');
} else {
  console.warn('Target 1 not matched');
}

// 2. Prevent loud error toast on initial load if API server is offline
const targetError = `  } catch (err) {
    console.error('Error fetching data:', err);
    showToast('เกิดข้อผิดพลาดในการโหลดข้อมูลจากเซิร์ฟเวอร์', 'error');
  }`;

const replacementError = `  } catch (err) {
    console.warn('Backend API offline, continuing in static mode:', err.message);
    try {
      const seedRes = await fetch('data/seed.json');
      if (seedRes.ok) {
        const seed = await seedRes.json();
        state.lessons = seed.lessons || [];
        state.quizzes = seed.quizzes || [];
        state.practicalExams = seed.practical_exams || [];
        state.worksheets = seed.worksheets || [];
        state.materials = seed.materials || [];
        state.students = seed.students || [];
        state.scores = seed.scores || [];
      }
    } catch (e) {}
  }`;

const normTargetErr = isCRLF ? targetError.replace(/\n/g, '\r\n') : targetError;
const normReplErr = isCRLF ? replacementError.replace(/\n/g, '\r\n') : replacementError;

if (content.includes(normTargetErr)) {
  content = content.replace(normTargetErr, normReplErr);
  console.log('2. Injected error handler fallback successfully!');
} else {
  console.warn('Target 2 not matched');
}

fs.writeFileSync(appJsPath, content, 'utf8');
console.log('Done modifying app.js.');
