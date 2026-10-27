const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;

// Path definitions
const DB_PATH = path.join(__dirname, 'data', 'db.json');
const BACKUP_PATH = path.join(__dirname, 'data', 'db.backup.json');
const SEED_PATH = path.join(__dirname, 'data', 'seed.json');
const CODE_DIR = path.join(__dirname, '..', 'code_examples');
const MEDIA_DIR = path.join(__dirname, '..', 'เอกสารประกอบและสื่อการสอน');

// Load .env configuration safely if present
const envFilePath = path.join(__dirname, '.env');
if (fs.existsSync(envFilePath)) {
  try {
    const envLines = fs.readFileSync(envFilePath, 'utf8').split(/\r?\n/);
    envLines.forEach(l => {
      const trimmed = l.trim();
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const eqIdx = trimmed.indexOf('=');
        const k = trimmed.substring(0, eqIdx).trim();
        const v = trimmed.substring(eqIdx + 1).trim();
        if (!process.env[k]) process.env[k] = v;
      }
    });
  } catch (e) {}
}

// ==========================================
// SUPABASE REALTIME CLOUD DATABASE CLIENT (SERVICE ROLE)
// ==========================================
const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://savyelqzzyzbipucdksn.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || '';
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false }
});

// Security & Standard Middleware
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Static file serving
app.use(express.static(path.join(__dirname, 'public')));
if (fs.existsSync(CODE_DIR)) {
  app.use('/code_examples', express.static(CODE_DIR));
}
if (fs.existsSync(MEDIA_DIR)) {
  app.use('/media_files', express.static(MEDIA_DIR));
}

// ==========================================
// DATE NORMALIZATION (ISO 8601 STANDARD)
// ==========================================
function normalizeToISO(dateInput) {
  if (!dateInput) return new Date().toISOString();
  if (dateInput instanceof Date) return dateInput.toISOString();
  const str = String(dateInput).trim();
  
  if (/^\d{4}-\d{2}-\d{2}T/.test(str)) {
    const d = new Date(str);
    if (!isNaN(d.getTime())) return d.toISOString();
  }

  // Parse DD/MM/YYYY or DD/MM/BE with optional HH:MM:SS
  const match = str.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})(?:\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?/);
  if (match) {
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10) - 1;
    let year = parseInt(match[3], 10);
    if (year > 2400) year -= 543; // Convert Thai Buddhist Era to Gregorian
    const hour = parseInt(match[4] || '0', 10);
    const min = parseInt(match[5] || '0', 10);
    const sec = parseInt(match[6] || '0', 10);
    
    // Thailand UTC+7 offset
    const utcDate = new Date(Date.UTC(year, month, day, hour - 7, min, sec));
    if (!isNaN(utcDate.getTime())) return utcDate.toISOString();
  }

  const fallback = new Date(str);
  return isNaN(fallback.getTime()) ? new Date().toISOString() : fallback.toISOString();
}

// ==========================================
// ASYNC WORKER QUEUE FOR GOOGLE SHEETS
// ==========================================
class SheetSyncQueue {
  constructor() {
    this.queue = [];
    this.isProcessing = false;
    this.stats = { processed: 0, failed: 0 };
  }

  enqueue(taskName, taskFn) {
    this.queue.push({ taskName, taskFn, retries: 0 });
    this.process();
  }

  async process() {
    if (this.isProcessing || this.queue.length === 0) return;
    this.isProcessing = true;
    const task = this.queue.shift();

    try {
      await task.taskFn();
      this.stats.processed++;
      console.log(`[SheetQueue SUCCESS]: ${task.taskName} (Total: ${this.stats.processed})`);
    } catch (err) {
      console.warn(`[SheetQueue WARNING] ${task.taskName} failed: ${err.message}`);
      if (task.retries < 2) {
        task.retries++;
        console.log(`[SheetQueue RETRY] Scheduling retry #${task.retries} for ${task.taskName}`);
        this.queue.push(task);
      } else {
        this.stats.failed++;
        console.error(`[SheetQueue FAILED]: ${task.taskName} failed permanently.`);
      }
    } finally {
      this.isProcessing = false;
      // 300ms throttle to prevent Google Apps Script timeouts
      setTimeout(() => this.process(), 300);
    }
  }
}
const sheetQueue = new SheetSyncQueue();

// ==========================================
// RATE LIMITER MIDDLEWARE (ANTI-SPAM)
// ==========================================
function createRateLimiter(windowMs, maxRequests, message) {
  const ipHits = new Map();
  return (req, res, next) => {
    const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.socket.remoteAddress || 'unknown';
    const now = Date.now();
    const timestamps = ipHits.get(ip) || [];
    const validTimestamps = timestamps.filter(t => now - t < windowMs);
    
    if (validTimestamps.length >= maxRequests) {
      return res.status(429).json({
        status: 'error',
        code: 'RATE_LIMIT_EXCEEDED',
        message: message || 'คำขอถี่เกินไป กรุณารอสักครู่แล้วลองใหม่อีกครั้ง'
      });
    }

    validTimestamps.push(now);
    ipHits.set(ip, validTimestamps);
    if (ipHits.size > 2000) {
      for (const [key, ts] of ipHits.entries()) {
        if (ts.every(t => now - t >= windowMs)) ipHits.delete(key);
      }
    }
    next();
  };
}

const submissionLimiter = createRateLimiter(60 * 1000, 20, 'คุณส่งงานถี่เกินไป กรุณารอ 1 นาทีก่อนส่งอีกครั้ง');
const quizLimiter = createRateLimiter(60 * 1000, 30, 'คุณส่งคำตอบถี่เกินไป กรุณารอสักครู่');
const liveSyncLimiter = createRateLimiter(60 * 1000, 120, 'คำขอซิงค์ข้อมูลถี่เกินไป');

// ==========================================
// AUTHENTICATION & ACCESS CONTROL (PERSISTENT RBAC)
// ==========================================
const ADMIN_PASSCODE = process.env.ADMIN_PASSCODE || 'admin1234';

// Persistent HMAC Session Secret across server reboots
const SESSION_SECRET_FILE = path.join(__dirname, 'data', '.session_secret');
let SESSION_SECRET = '';
try {
  if (fs.existsSync(SESSION_SECRET_FILE)) {
    SESSION_SECRET = fs.readFileSync(SESSION_SECRET_FILE, 'utf-8').trim();
  }
} catch (e) {}
if (!SESSION_SECRET) {
  SESSION_SECRET = crypto.randomBytes(32).toString('hex');
  try {
    fs.writeFileSync(SESSION_SECRET_FILE, SESSION_SECRET, 'utf-8');
  } catch (e) {}
}

function createAdminSession() {
  const payload = {
    role: 'admin',
    createdAt: Date.now(),
    expiresAt: Date.now() + 24 * 60 * 60 * 1000 // 24-hour validity
  };
  const payloadStr = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto.createHmac('sha256', SESSION_SECRET).update(payloadStr).digest('base64url');
  return `${payloadStr}.${signature}`;
}

function isValidAdminToken(token) {
  if (!token || typeof token !== 'string' || !token.includes('.')) return false;
  try {
    const [payloadStr, signature] = token.split('.');
    const expectedSig = crypto.createHmac('sha256', SESSION_SECRET).update(payloadStr).digest('base64url');
    if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSig))) {
      return false;
    }
    const payload = JSON.parse(Buffer.from(payloadStr, 'base64url').toString('utf-8'));
    if (!payload.expiresAt || Date.now() > payload.expiresAt) {
      return false;
    }
    return payload.role === 'admin';
  } catch (e) {
    return false;
  }
}

function requireAdmin(req, res, next) {
  const token = req.headers['x-admin-token'] || req.headers['authorization']?.replace(/^Bearer\s+/i, '');
  if (isValidAdminToken(token)) {
    return next();
  }
  return res.status(403).json({
    status: 'error',
    code: 'UNAUTHORIZED',
    message: 'การดำเนินการนี้ต้องใช้สิทธิ์ครูผู้สอน / ผู้ดูแลระบบ (กรุณาเข้าสู่ระบบด้วยรหัสผ่าน)'
  });
}

// Authentication Endpoints
app.post('/api/auth/login', (req, res) => {
  const { passcode, password } = req.body || {};
  const input = String(passcode || password || '').trim();

  if (input === ADMIN_PASSCODE) {
    const token = createAdminSession();
    return res.json({
      status: 'success',
      token,
      role: 'admin',
      message: 'ยืนยันตัวตนสิทธิ์ครูผู้สอน / ผู้ดูแลระบบสำเร็จ'
    });
  }

  return res.status(401).json({
    status: 'error',
    message: 'รหัสผ่านครูผู้สอนไม่ถูกต้อง'
  });
});

app.get('/api/auth/verify', (req, res) => {
  const token = req.headers['x-admin-token'] || req.headers['authorization']?.replace(/^Bearer\s+/i, '');
  const valid = isValidAdminToken(token);
  res.json({
    status: 'success',
    valid,
    role: valid ? 'admin' : 'student'
  });
});

// Student Sessions Map: token -> { studentId, name, classRoom, loginTime }
const studentSessions = new Map();

// Student Login: กำหนดให้ StudentID เป็นทั้ง User และ Password
app.post('/api/auth/student-login', (req, res) => {
  const { student_id, username, password } = req.body || {};
  const rawId = String(student_id || username || '').trim();
  const rawPass = String(password || '').trim();

  if (!rawId || !rawPass) {
    return res.status(400).json({
      status: 'error',
      message: 'กรุณากรอกรหัสนักเรียน (StudentID) และรหัสผ่าน'
    });
  }

  // กำหนดเงื่อนไข: StudentID เป็นทั้ง User และ Password
  if (rawId !== rawPass) {
    return res.status(401).json({
      status: 'error',
      message: 'รหัสผ่านไม่ถูกต้อง (กำหนดให้ใช้รหัสนักเรียน 5 หลักเป็นทั้ง Username และ Password)'
    });
  }

  const db = readDB();
  const students = db.students || [];
  const student = students.find(s => String(s.student_id).trim() === rawId);

  if (!student) {
    return res.status(404).json({
      status: 'error',
      message: `ไม่พบรหัสนักเรียน "${rawId}" ในฐานข้อมูลห้อง ม.5/12`
    });
  }

  const token = 'std_' + crypto.randomBytes(24).toString('hex');
  studentSessions.set(token, {
    studentId: student.student_id,
    name: student.name,
    classRoom: student.class_room || 'ม.5/12',
    loginTime: Date.now()
  });

  return res.json({
    status: 'success',
    token,
    role: 'student',
    student: {
      id: student.student_id,
      student_id: student.student_id,
      username: student.student_id,
      name: student.name,
      full_name: student.name,
      class_room: student.class_room || 'ม.5/12',
      role: 'student'
    },
    message: `เข้าสู่ระบบสำเร็จ: ${student.name} (${student.class_room || 'ม.5/12'})`
  });
});

// ==============================================================
// GOOGLE SHEET REAL-TIME BIDIRECTIONAL SYNC ENGINE
// ==============================================================
const https = require('https');
const SPREADSHEET_ID = '1SLgcSTaoFcy2kXb_oas70A9uImrhZWzcubnVf8yqlBM';
const GOOGLE_SHEET_CSV_URL = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Student`;

let lastSheetSyncTime = 0;
let lastSubmissionsSyncTime = 0;

function fetchGoogleSheetCSV(url = GOOGLE_SHEET_CSV_URL) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchGoogleSheetCSV(res.headers.location).then(resolve).catch(reject);
      }
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function fetchGoogleSheetCSVBySheet(sheetName) {
  const url = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(sheetName)}`;
  return fetchGoogleSheetCSV(url);
}

// Robust CSV parser supporting quotes, escaped quotes, commas inside quotes, and newlines
function parseCSV(text) {
  if (!text) return [];
  const lines = [];
  let row = [];
  let inQuotes = false;
  let currentToken = '';

  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    const next = text[i + 1];

    if (c === '"') {
      if (inQuotes && next === '"') {
        currentToken += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      row.push(currentToken.trim());
      currentToken = '';
    } else if ((c === '\r' || c === '\n') && !inQuotes) {
      if (c === '\r' && next === '\n') i++;
      row.push(currentToken.trim());
      currentToken = '';
      if (row.some(cell => cell.length > 0)) lines.push(row);
      row = [];
    } else {
      currentToken += c;
    }
  }
  if (currentToken.length > 0 || row.length > 0) {
    row.push(currentToken.trim());
    if (row.some(cell => cell.length > 0)) lines.push(row);
  }
  return lines;
}

function resolveSheetChapter(chapterText, taskType, db) {
  let chNum = null;
  const numMatch = (chapterText || '').match(/(?:บทที่|Unit|ch|chapter)\s*(\d+)/i) || (chapterText || '').match(/(\d+)/);
  if (numMatch) {
    chNum = parseInt(numMatch[1], 10);
  }

  const chNumStr = chNum ? String(chNum).padStart(2, '0') : '01';
  const chapterId = `ch${chNumStr}`;

  let targetId = '';
  if (taskType === 'worksheet') {
    const ws = (db.worksheets || []).find(w => w.chapter_id === chapterId || w.chapter_number === chNum);
    targetId = ws ? ws.id : `ws${chNumStr}`;
  } else {
    const practical = (db.practical_exams || []).find(p => p.chapter_id === chapterId || p.unit_number === chNum);
    targetId = practical ? practical.id : `prac_${chNumStr}`;
  }

  return { chapterId, targetId, chNum };
}

function parseSheetScore(rawScore) {
  if (!rawScore || rawScore === '-' || rawScore === 'null' || rawScore === 'undefined') return null;
  const cleaned = String(rawScore).trim();
  if (!cleaned) return null;
  const match = cleaned.match(/^([\d.]+)/);
  if (match) {
    const num = parseFloat(match[1]);
    return isNaN(num) ? null : num;
  }
  return null;
}

async function syncStudentsFromGoogleSheet() {
  try {
    const csv = await fetchGoogleSheetCSVBySheet('Student');
    const rows = parseCSV(csv);
    if (!rows || rows.length <= 1) return null;

    const students = [];
    for (let i = 1; i < rows.length; i++) {
      const cols = rows[i];
      const studentId = cols[0];
      const name = cols[1];
      const className = cols[2] || 'ม.5/12';
      if (studentId && name) {
        students.push({
          id: `std_${studentId}`,
          student_id: studentId,
          username: studentId,
          name: name,
          full_name: name,
          class_room: className,
          role: 'student'
        });
      }
    }
    if (students.length > 0) {
      const db = readDB();
      db.students = students;
      db.students_last_synced = new Date().toISOString();

      const validStudentIds = new Set(students.map(s => s.student_id));
      const studentNameMap = new Map(students.map(s => [s.student_id, s.name]));

      const adminUsers = (db.users || []).filter(u => u.role === 'admin');
      const syncedStudentUsers = students.map(s => ({
        id: s.id,
        username: s.student_id,
        full_name: s.name,
        role: 'student',
        class_room: s.class_room,
        student_number: parseInt(s.student_id, 10) || 0
      }));
      db.users = [...adminUsers, ...syncedStudentUsers];

      if (db.scores) {
        db.scores = db.scores
          .filter(sc => validStudentIds.has(sc.student_id))
          .map(sc => {
            sc.student_name = studentNameMap.get(sc.student_id) || sc.student_name;
            return sc;
          });
      }

      if (db.submissions) {
        db.submissions = db.submissions
          .filter(sub => validStudentIds.has(sub.student_id))
          .map(sub => {
            sub.student_name = studentNameMap.get(sub.student_id) || sub.student_name;
            return sub;
          });
      }

      writeDB(db);
      lastSheetSyncTime = Date.now();
      return students;
    }
  } catch (err) {
    console.error('[Google Sheet Sync Error (Students)]:', err.message);
  }
  return null;
}

// Real-time synchronization for Submissions & Grades (Strict Single Source of Truth from Google Sheet)
async function syncSubmissionsAndGradesFromGoogleSheet() {
  try {
    const [practicalCsv, worksheetCsv] = await Promise.all([
      fetchGoogleSheetCSVBySheet('practical').catch(() => ''),
      fetchGoogleSheetCSVBySheet('worksheet').catch(() => '')
    ]);

    const practicalRows = parseCSV(practicalCsv);
    const worksheetRows = parseCSV(worksheetCsv);

    const db = readDB();
    if (!db.submissions) db.submissions = [];
    if (!db.scores) db.scores = [];

    // Temporary preserve very recent local submissions/grades (< 15 seconds) to prevent flicker during write-to-sheet
    const recentSubmissions = (db.submissions || []).filter(s => {
      const t = new Date(s.submitted_at || 0).getTime();
      return (Date.now() - t) < 15000;
    });

    const recentScores = (db.scores || []).filter(s => {
      const isSheetCat = s.exam_category === 'practical' || s.exam_category === 'worksheet';
      if (!isSheetCat) return false;
      const t = new Date(s.submitted_at || 0).getTime();
      return (Date.now() - t) < 15000;
    });

    const freshSubmissions = [];
    const freshScores = [];

    const processSheetRows = (rows, taskType) => {
      if (!rows || rows.length <= 1) return;
      const header = rows[0].map(h => (h || '').toLowerCase());

      const findColIdx = (keywords, fallback) => {
        for (let i = 0; i < header.length; i++) {
          for (let kw of keywords) {
            if (header[i].indexOf(kw) !== -1) return i;
          }
        }
        return fallback;
      };

      const colTime = findColIdx(['timestamp', 'วัน-เวลา'], 0);
      const colStdId = findColIdx(['studentid', 'รหัสนักเรียน'], 1);
      const colName = findColIdx(['name', 'ชื่อ-นามสกุล'], 2);
      const colChapter = findColIdx(['chapter', 'บทเรียน'], 3);
      const colUrl = findColIdx(['url', 'ลิงก์'], 4);
      const colNotes = findColIdx(['notes', 'บันทึก'], 5);
      const colScore = findColIdx(['score', 'คะแนน'], 6);
      const colFeedback = findColIdx(['feedback', 'ข้อเสนอแนะ'], 7);
      const colGradedAt = findColIdx(['graded at', 'เวลาที่ประเมิน'], 8);

      for (let r = 1; r < rows.length; r++) {
        const row = rows[r];
        const studentId = (row[colStdId] || '').trim();
        if (!studentId) continue;

        const studentName = (row[colName] || '').trim();
        const chapterRaw = (row[colChapter] || '').trim();
        const url = (row[colUrl] || '').trim();
        const notes = (row[colNotes] || '').trim();
        const rawScore = (row[colScore] || '').trim();
        const feedback = (row[colFeedback] || '').trim();
        const timeStr = (row[colTime] || '').trim();
        const gradedAtStr = (row[colGradedAt] || '').trim();

        const { chapterId, targetId } = resolveSheetChapter(chapterRaw, taskType, db);
        const parsedScore = parseSheetScore(rawScore);

        // 1. Fresh submission strictly from Google Sheet row
        if (url && url !== '-') {
          const sub = {
            id: `sub_${taskType}_${studentId}_${chapterId}`,
            student_id: studentId,
            student_name: studentName,
            chapter_id: chapterId,
            task_type: taskType,
            report_url: url,
            notes: notes,
            status: parsedScore !== null ? 'graded' : 'submitted',
            submitted_at: normalizeToISO(timeStr)
          };
          if (parsedScore !== null) sub.score = parsedScore;
          freshSubmissions.push(sub);
        }

        // 2. Fresh score strictly from Google Sheet row
        if (parsedScore !== null) {
          const existingPrac = (db.scores || []).find(s => s.student_id === studentId && s.target_id === targetId && s.exam_category === 'practical');
          let rubricsBreakdown = existingPrac && existingPrac.score === parsedScore ? existingPrac.rubrics_breakdown : undefined;

          if (taskType === 'practical' && !rubricsBreakdown) {
            const practicalExam = (db.practical_exams || []).find(p => p.id === targetId);
            if (practicalExam && Array.isArray(practicalExam.rubrics) && practicalExam.rubrics.length > 0) {
              const totalMax = practicalExam.rubrics.reduce((acc, rb) => acc + (parseFloat(rb.points) || 0), 0) || 10;
              const ratio = parsedScore / totalMax;
              let accumulated = 0;
              rubricsBreakdown = practicalExam.rubrics.map((rb, idx) => {
                const max = parseFloat(rb.points) || 0;
                let cur = idx === practicalExam.rubrics.length - 1 
                  ? Math.round((parsedScore - accumulated) * 10) / 10 
                  : Math.round((max * ratio) * 10) / 10;
                accumulated += cur;
                return {
                  title: rb.title,
                  maxPoints: max,
                  currentPoints: Math.max(0, Math.min(max, cur))
                };
              });
            }
          }

          const sc = {
            id: `score_${taskType}_${studentId}_${chapterId}`,
            student_id: studentId,
            student_name: studentName || 'นักเรียน',
            exam_category: taskType,
            target_id: targetId,
            chapter_id: chapterId,
            score: parsedScore,
            max_score: 10,
            percentage: Math.round((parsedScore / 10) * 100),
            notes: feedback,
            submitted_at: normalizeToISO(gradedAtStr || timeStr)
          };
          if (rubricsBreakdown) sc.rubrics_breakdown = rubricsBreakdown;
          freshScores.push(sc);
        }
      }
    };

    processSheetRows(practicalRows, 'practical');
    processSheetRows(worksheetRows, 'worksheet');

    // Merge recent (<15s) actions if not already in fresh lists
    recentSubmissions.forEach(recSub => {
      if (!freshSubmissions.some(s => s.student_id === recSub.student_id && s.chapter_id === recSub.chapter_id && s.task_type === recSub.task_type)) {
        freshSubmissions.push(recSub);
      }
    });

    recentScores.forEach(recSc => {
      if (!freshScores.some(s => s.student_id === recSc.student_id && s.chapter_id === recSc.chapter_id && s.exam_category === recSc.exam_category)) {
        freshScores.push(recSc);
      }
    });

    // Retain non-sheet categories (chapter quizzes, midterm, final)
    const nonSheetScores = (db.scores || []).filter(s => s.exam_category !== 'practical' && s.exam_category !== 'worksheet');

    // STRICT REPLACEMENT: Only what is in Google Sheet is kept!
    db.submissions = freshSubmissions;
    db.scores = [...nonSheetScores, ...freshScores];

    db.last_realtime_sync = new Date().toISOString();
    writeDB(db);
    lastSubmissionsSyncTime = Date.now();

    console.log(`[Google Sheet Real-Time Sync (STRICT)] ซิงค์ข้อมูลสำเร็จ: การส่งงาน ${freshSubmissions.length} รายการ, คะแนน ${freshScores.length} รายการ (ตรงกับ Google Sheet 100%) เมื่อ ${db.last_realtime_sync}`);
    return { success: true, submissions_count: freshSubmissions.length, scores_count: freshScores.length, last_synced: db.last_realtime_sync };
  } catch (err) {
    console.error('[Google Sheet Real-Time Sync Error]:', err.message);
    return { success: false, error: err.message };
  }
}

async function syncAllFromGoogleSheet() {
  await syncStudentsFromGoogleSheet();
  return await syncSubmissionsAndGradesFromGoogleSheet();
}

// Auto-run background sync intervals (2-minute periodic safety sync)
setInterval(() => {
  syncSubmissionsAndGradesFromGoogleSheet().catch(e => console.warn('Interval sync error:', e.message));
}, 120000); // Poll Google Sheets every 2 minutes as backup sync

setInterval(() => {
  syncStudentsFromGoogleSheet().catch(e => console.warn('Student sync interval error:', e.message));
}, 300000); // Poll student roster every 5 minutes

// API: Live Real-time Sync endpoint (Powered by Supabase Cloud Database)
app.get('/api/sync/live', liveSyncLimiter, async (req, res) => {
  try {
    const [resStd, resSub, resSco] = await Promise.all([
      supabase.from('students').select('*').order('student_id', { ascending: true }),
      supabase.from('submissions').select('*').order('created_at', { ascending: false }),
      supabase.from('scores').select('*').order('created_at', { ascending: false })
    ]);

    if (!resStd.error && !resSub.error && !resSco.error) {
      const students = resStd.data || [];
      const submissions = resSub.data || [];
      const scores = resSco.data || [];

      const db = readDB();
      db.students = students;
      db.submissions = submissions;
      db.scores = scores;
      db.last_realtime_sync = new Date().toISOString();
      writeDB(db);

      return res.json({
        status: 'success',
        engine: 'supabase',
        last_synced: db.last_realtime_sync,
        students,
        scores,
        submissions,
        students_count: students.length,
        scores_count: scores.length,
        submissions_count: submissions.length
      });
    }
  } catch (err) {
    console.warn('[Supabase Sync fallback to local/sheet]:', err.message);
  }

  // Fallback to local / sheet sync if offline
  if (req.query.force === 'true' || Date.now() - lastSubmissionsSyncTime > 30000) {
    await syncSubmissionsAndGradesFromGoogleSheet();
  }
  const db = readDB();
  res.json({
    status: 'success',
    engine: 'local',
    last_synced: db.last_realtime_sync || new Date().toISOString(),
    students: db.students || [],
    scores: db.scores || [],
    submissions: db.submissions || [],
    students_count: (db.students || []).length,
    scores_count: (db.scores || []).length,
    submissions_count: (db.submissions || []).length
  });
});

app.post('/api/sync/live', liveSyncLimiter, async (req, res) => {
  try {
    const [resStd, resSub, resSco] = await Promise.all([
      supabase.from('students').select('*').order('student_id', { ascending: true }),
      supabase.from('submissions').select('*').order('created_at', { ascending: false }),
      supabase.from('scores').select('*').order('created_at', { ascending: false })
    ]);

    if (!resStd.error && !resSub.error && !resSco.error) {
      const students = resStd.data || [];
      const submissions = resSub.data || [];
      const scores = resSco.data || [];

      const db = readDB();
      db.students = students;
      db.submissions = submissions;
      db.scores = scores;
      db.last_realtime_sync = new Date().toISOString();
      writeDB(db);

      return res.json({
        status: 'success',
        engine: 'supabase',
        message: 'ซิงค์ข้อมูลสดจาก Supabase สำเร็จแล้ว',
        last_synced: db.last_realtime_sync,
        students,
        scores,
        submissions,
        students_count: students.length,
        scores_count: scores.length,
        submissions_count: submissions.length
      });
    }
  } catch (err) {
    console.warn('[Supabase POST sync fallback]:', err.message);
  }

  const result = await syncAllFromGoogleSheet();
  const db = readDB();
  res.json({
    status: 'success',
    message: `ซิงค์ข้อมูลสดจากชีตสำเร็จแล้ว (อัปเดต ${result ? result.submissions_count : 0} รายการ)`,
    last_synced: db.last_realtime_sync || new Date().toISOString(),
    students: db.students || [],
    scores: db.scores || [],
    submissions: db.submissions || [],
    students_count: (db.students || []).length,
    scores_count: (db.scores || []).length,
    submissions_count: (db.submissions || []).length
  });
});

// รายชื่อนักเรียนทั้งหมด (ดึงสดจาก Supabase เป็นหลัก)
app.get('/api/students', async (req, res) => {
  try {
    const { data, error } = await supabase.from('students').select('*').order('student_id', { ascending: true });
    if (!error && data && data.length > 0) {
      return res.json({
        status: 'success',
        engine: 'supabase',
        last_synced: new Date().toISOString(),
        total: data.length,
        data: data
      });
    }
  } catch (e) {
    console.warn('[Supabase students fetch warning]:', e.message);
  }

  const db = readDB();
  res.json({
    status: 'success',
    last_synced: db.students_last_synced,
    total: (db.students || []).length,
    data: db.students || []
  });
});

// Endpoint ซิงค์ข้อมูลนักเรียนสดจาก Google Sheet ทันที
app.post('/api/students/sync', async (req, res) => {
  const students = await syncStudentsFromGoogleSheet();
  if (students && students.length > 0) {
    res.json({
      status: 'success',
      message: `ซิงค์ข้อมูลนักเรียนจาก Google Sheet สำเร็จ (${students.length} คน)`,
      total: students.length,
      data: students
    });
  } else {
    const db = readDB();
    res.json({
      status: 'warning',
      message: 'ไม่สามารถติดต่อ Google Sheet ได้ในขณะนี้ จึงใช้ข้อมูลที่มีอยู่เดิม',
      total: (db.students || []).length,
      data: db.students || []
    });
  }
});

app.post('/api/auth/logout', (req, res) => {
  const token = req.headers['x-admin-token'] || req.headers['x-student-token'] || req.headers['authorization']?.replace(/^Bearer\s+/i, '');
  if (token) {
    adminSessions.delete(token);
    studentSessions.delete(token);
  }
  res.json({ status: 'success', message: 'ออกจากระบบสำเร็จ' });
});

// ==========================================
// DATABASE HELPERS WITH ATOMIC WRITE MUTEX
// ==========================================
function readDB() {
  try {
    if (!fs.existsSync(DB_PATH)) {
      if (fs.existsSync(SEED_PATH)) {
        fs.copyFileSync(SEED_PATH, DB_PATH);
      } else {
        return { lessons: [], quizzes: [], practical_exams: [], worksheets: [], materials: [], scores: [], users: [], submissions: [] };
      }
    }
    const raw = fs.readFileSync(DB_PATH, 'utf-8');
    const parsed = JSON.parse(raw);
    if (!parsed.submissions) parsed.submissions = [];
    return parsed;
  } catch (err) {
    console.error('Error reading db.json:', err);
    return { lessons: [], quizzes: [], practical_exams: [], worksheets: [], materials: [], scores: [], users: [], submissions: [] };
  }
}

// Atomic file write with automatic backup snapshot to prevent corruption
function writeDB(data) {
  try {
    // 1. Snapshot previous valid DB before rewriting
    if (fs.existsSync(DB_PATH)) {
      try {
        fs.copyFileSync(DB_PATH, BACKUP_PATH);
      } catch (backupErr) {
        console.warn('DB Backup snapshot warning:', backupErr.message);
      }
    }

    const tmpPath = `${DB_PATH}.${Date.now()}.${Math.random().toString(36).substring(2, 8)}.tmp`;
    fs.writeFileSync(tmpPath, JSON.stringify(data, null, 2), 'utf-8');
    fs.renameSync(tmpPath, DB_PATH);
    return true;
  } catch (err) {
    console.error('Error writing to db.json atomically:', err);
    try {
      fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf-8');
      return true;
    } catch (fallbackErr) {
      console.error('Fatal fallback error writing db.json:', fallbackErr);
      return false;
    }
  }
}

// ==========================================
// 1. SYSTEM & STATS APIS
// ==========================================
app.get('/api/system', (req, res) => {
  const db = readDB();
  res.json({
    status: 'success',
    system_info: db.system_info || {
      course_title_th: 'ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว',
      course_title_en: 'Embedded Artificial Intelligence',
      course_type: 'รายวิชาเพิ่มเติม (หลักสูตรแกนกลาง / สพฐ.)',
      institution: 'กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี',
      curriculum_reference: 'Embedded Artificial Intelligence Curriculum (Arduino UNO Q & Edge Impulse Series)',
      playlist_url: 'https://youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU',
      version: '2.5.0',
      last_updated: new Date().toISOString()
    },
    users: db.users || []
  });
});

app.get('/api/stats', async (req, res) => {
  try {
    const [les, prac, ws, sco, qz] = await Promise.all([
      supabase.from('lessons').select('count', { count: 'exact' }),
      supabase.from('practical_exams').select('count', { count: 'exact' }),
      supabase.from('worksheets').select('count', { count: 'exact' }),
      supabase.from('scores').select('score, percentage'),
      supabase.from('quizzes').select('count', { count: 'exact' })
    ]);

    const db = readDB();
    const totalLessons = les.count ?? (db.lessons || []).length;
    const totalPractical = prac.count ?? (db.practical_exams || []).length;
    const totalWorksheets = ws.count ?? (db.worksheets || []).length;
    const totalQuizzes = qz.count && qz.count > 0 ? qz.count : (db.quizzes || []).length;
    const scores = sco.data || (db.scores || []);
    const totalSubmissions = scores.length;
    let avgPercentage = 0;
    if (totalSubmissions > 0) {
      const sum = scores.reduce((acc, s) => acc + (parseFloat(s.percentage) || 0), 0);
      avgPercentage = Math.round((sum / totalSubmissions) * 10) / 10;
    }

    return res.json({
      status: 'success',
      engine: 'supabase',
      stats: {
        totalLessons,
        totalQuizzes,
        totalPractical,
        totalWorksheets,
        totalMaterials: (db.materials || []).length,
        totalSubmissions,
        avgPercentage
      }
    });
  } catch (e) {
    console.warn('[Supabase stats fallback]:', e.message);
  }
  const db = readDB();
  const totalLessons = (db.lessons || []).length;
  const totalQuizzes = (db.quizzes || []).length;
  const totalPractical = (db.practical_exams || []).length;
  const totalWorksheets = (db.worksheets || []).length;
  const totalMaterials = (db.materials || []).length;
  const totalSubmissions = (db.scores || []).length;
  
  let avgPercentage = 0;
  if (totalSubmissions > 0) {
    const sum = db.scores.reduce((acc, s) => acc + (parseFloat(s.percentage) || 0), 0);
    avgPercentage = Math.round((sum / totalSubmissions) * 10) / 10;
  }

  res.json({
    status: 'success',
    engine: 'local',
    stats: {
      totalLessons,
      totalQuizzes,
      totalPractical,
      totalWorksheets,
      totalMaterials,
      totalSubmissions,
      avgPercentage
    }
  });
});

// ==========================================
// 2. LESSONS CRUD (บทเรียน)
// ==========================================
app.get('/api/lessons', async (req, res) => {
  const db = readDB();
  const localMap = new Map((db.lessons || []).map(l => [l.id, l]));

  try {
    const { data, error } = await supabase.from('lessons').select('*').order('chapter_number', { ascending: true });
    if (!error && data && data.length > 0) {
      const merged = data.map(item => {
        const local = localMap.get(item.id) || {};
        return {
          ...item,
          ...local,
          video_episodes: local.video_episodes || item.video_episodes,
          video_url: local.video_url || item.video_url,
          slide_url: local.slide_url || item.slide_url,
          pdf_url: local.pdf_url || local.slide_url || item.pdf_url || item.slide_url
        };
      });
      return res.json({ status: 'success', engine: 'supabase', data: merged });
    }
  } catch (e) {
    console.warn('[Supabase lessons fetch fallback]:', e.message);
  }
  const sorted = (db.lessons || []).sort((a, b) => a.chapter_number - b.chapter_number);
  res.json({ status: 'success', engine: 'local', data: sorted });
});

app.get('/api/lessons/:id', async (req, res) => {
  const db = readDB();
  const local = (db.lessons || []).find(l => l.id === req.params.id);

  try {
    const { data, error } = await supabase.from('lessons').select('*').eq('id', req.params.id).maybeSingle();
    if (!error && data) {
      const merged = {
        ...data,
        ...(local || {}),
        video_episodes: (local ? local.video_episodes : undefined) || data.video_episodes,
        video_url: (local ? local.video_url : undefined) || data.video_url,
        slide_url: (local ? local.slide_url : undefined) || data.slide_url,
        pdf_url: (local ? (local.pdf_url || local.slide_url) : undefined) || data.pdf_url || data.slide_url
      };
      return res.json({ status: 'success', engine: 'supabase', data: merged });
    }
  } catch (e) {}

  if (!local) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบบทเรียนที่ระบุ' });
  }
  res.json({ status: 'success', engine: 'local', data: local });
});

// Protected: Create lesson (ครู / Admin)
app.post('/api/lessons', requireAdmin, (req, res) => {
  const db = readDB();
  const { title, title_en, description, objectives, video_url, slide_url, code_filename, duration_hours } = req.body;
  
  if (!title) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกชื่อบทเรียน' });
  }

  const newNum = (db.lessons.length > 0 ? Math.max(...db.lessons.map(l => l.chapter_number || 0)) : 0) + 1;
  const newId = `ch${String(newNum).padStart(2, '0')}`;

  const newLesson = {
    id: newId,
    chapter_number: newNum,
    title,
    title_en: title_en || `Chapter ${newNum}`,
    description: description || '',
    objectives: Array.isArray(objectives) ? objectives : (objectives ? objectives.split('\n').filter(Boolean) : []),
    video_url: video_url || '',
    slide_url: slide_url || '',
    code_filename: code_filename || 'main.py',
    duration_hours: Number(duration_hours) || 3,
    created_at: new Date().toISOString()
  };

  db.lessons.push(newLesson);
  writeDB(db);

  // Sync to Supabase
  supabase.from('lessons').upsert(newLesson).then(({ error }) => {
    if (error) console.warn('[Supabase Lesson Insert Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Lesson Insert Catch]:', e.message));

  res.status(201).json({ status: 'success', message: 'เพิ่มบทเรียนใหม่เรียบร้อยแล้ว', data: newLesson });
});

// Protected: Update lesson (ครู / Admin)
app.put('/api/lessons/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const index = db.lessons.findIndex(l => l.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบบทเรียนที่ต้องการแก้ไข' });
  }

  const { title, title_en, description, objectives, video_url, slide_url, code_filename, duration_hours, chapter_number } = req.body;

  db.lessons[index] = {
    ...db.lessons[index],
    title: title !== undefined ? title : db.lessons[index].title,
    title_en: title_en !== undefined ? title_en : db.lessons[index].title_en,
    chapter_number: chapter_number !== undefined ? Number(chapter_number) : db.lessons[index].chapter_number,
    description: description !== undefined ? description : db.lessons[index].description,
    objectives: Array.isArray(objectives) ? objectives : (objectives ? objectives.split('\n').filter(Boolean) : db.lessons[index].objectives),
    video_url: video_url !== undefined ? video_url : db.lessons[index].video_url,
    slide_url: slide_url !== undefined ? slide_url : db.lessons[index].slide_url,
    code_filename: code_filename !== undefined ? code_filename : db.lessons[index].code_filename,
    duration_hours: duration_hours !== undefined ? Number(duration_hours) : db.lessons[index].duration_hours,
    updated_at: new Date().toISOString()
  };

  writeDB(db);

  // Sync to Supabase
  supabase.from('lessons').upsert(db.lessons[index]).then(({ error }) => {
    if (error) console.warn('[Supabase Lesson Update Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Lesson Update Catch]:', e.message));

  res.json({ status: 'success', message: 'แก้ไขข้อมูลบทเรียนเรียบร้อยแล้ว', data: db.lessons[index] });
});

// Protected: Delete lesson (ครู / Admin)
app.delete('/api/lessons/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const initialLength = db.lessons.length;
  db.lessons = db.lessons.filter(l => l.id !== req.params.id);

  if (db.lessons.length === initialLength) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบบทเรียนที่ต้องการลบ' });
  }

  writeDB(db);

  // Sync delete to Supabase
  supabase.from('lessons').delete().eq('id', req.params.id).then(({ error }) => {
    if (error) console.warn('[Supabase Lesson Delete Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Lesson Delete Catch]:', e.message));

  res.json({ status: 'success', message: 'ลบบทเรียนเรียบร้อยแล้ว' });
});

// ==========================================
// 3. QUIZZES CRUD (คลังข้อสอบ)
// ==========================================
app.get('/api/quizzes', async (req, res) => {
  const { category, chapter_id } = req.query;
  try {
    let query = supabase.from('quizzes').select('*');
    if (category) query = query.eq('category', category);
    if (chapter_id) query = query.eq('chapter_id', chapter_id);
    const { data, error } = await query;
    if (!error && data && data.length > 0) {
      return res.json({ status: 'success', engine: 'supabase', count: data.length, data });
    }
  } catch (e) {
    console.warn('[Supabase quizzes fetch fallback]:', e.message);
  }
  const db = readDB();
  let items = db.quizzes || [];

  if (category) {
    items = items.filter(q => q.category === category);
  }
  if (chapter_id) {
    items = items.filter(q => q.chapter_id === chapter_id);
  }

  res.json({ status: 'success', engine: 'local', count: items.length, data: items });
});

app.get('/api/quizzes/:id', async (req, res) => {
  try {
    const { data, error } = await supabase.from('quizzes').select('*').eq('id', req.params.id).maybeSingle();
    if (!error && data) {
      return res.json({ status: 'success', engine: 'supabase', data });
    }
  } catch (e) {}
  const db = readDB();
  const item = (db.quizzes || []).find(q => q.id === req.params.id);
  if (!item) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบข้อสอบที่ระบุ' });
  }
  res.json({ status: 'success', engine: 'local', data: item });
});

// Protected: Create quiz (ครู / Admin)
app.post('/api/quizzes', requireAdmin, (req, res) => {
  const db = readDB();
  const { chapter_id, category, question_text, options, correct_index, explanation, points } = req.body;

  if (!question_text || !Array.isArray(options) || options.length !== 4) {
    return res.status(400).json({ status: 'error', message: 'ข้อมูลข้อสอบไม่สมบูรณ์ ต้องมีคำถามและ 4 ตัวเลือก' });
  }

  const newId = `q_custom_${Date.now()}`;
  const newQuestion = {
    id: newId,
    chapter_id: chapter_id || 'ch01',
    category: category || 'chapter_quiz',
    question_text,
    options,
    correct_index: Number(correct_index) || 0,
    explanation: explanation || 'เฉลยเชิงวิชาการตามมาตรฐานคำสั่งและสถาปัตยกรรมระบบ',
    points: Number(points) || 1
  };

  db.quizzes = db.quizzes || [];
  db.quizzes.push(newQuestion);
  writeDB(db);

  // Sync to Supabase
  supabase.from('quizzes').upsert(newQuestion).then(({ error }) => {
    if (error) console.warn('[Supabase Quiz Insert Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Quiz Insert Catch]:', e.message));

  res.status(201).json({ status: 'success', message: 'เพิ่มข้อสอบใหม่เรียบร้อยแล้ว', data: newQuestion });
});

// Protected: Update quiz (ครู / Admin)
app.put('/api/quizzes/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const index = (db.quizzes || []).findIndex(q => q.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบข้อสอบที่ต้องการแก้ไข' });
  }

  const { question_text, options, correct_index, explanation, points, chapter_id, category } = req.body;

  db.quizzes[index] = {
    ...db.quizzes[index],
    question_text: question_text !== undefined ? question_text : db.quizzes[index].question_text,
    options: options !== undefined ? options : db.quizzes[index].options,
    correct_index: correct_index !== undefined ? Number(correct_index) : db.quizzes[index].correct_index,
    explanation: explanation !== undefined ? explanation : db.quizzes[index].explanation,
    points: points !== undefined ? Number(points) : db.quizzes[index].points,
    chapter_id: chapter_id !== undefined ? chapter_id : db.quizzes[index].chapter_id,
    category: category !== undefined ? category : db.quizzes[index].category
  };

  writeDB(db);

  // Sync to Supabase
  supabase.from('quizzes').upsert(db.quizzes[index]).then(({ error }) => {
    if (error) console.warn('[Supabase Quiz Update Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Quiz Update Catch]:', e.message));

  res.json({ status: 'success', message: 'แก้ไขข้อสอบเรียบร้อยแล้ว', data: db.quizzes[index] });
});

// Protected: Delete quiz (ครู / Admin)
app.delete('/api/quizzes/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const initialLength = (db.quizzes || []).length;
  db.quizzes = (db.quizzes || []).filter(q => q.id !== req.params.id);

  if (db.quizzes.length === initialLength) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบข้อสอบที่ต้องการลบ' });
  }

  writeDB(db);

  // Sync delete to Supabase
  supabase.from('quizzes').delete().eq('id', req.params.id).then(({ error }) => {
    if (error) console.warn('[Supabase Quiz Delete Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Quiz Delete Catch]:', e.message));

  res.json({ status: 'success', message: 'ลบข้อสอบออกจากคลังสำเร็จ' });
});

// Student exam submission & auto-grading (Open to all students with rate limiter)
app.post('/api/quizzes/submit', quizLimiter, (req, res) => {
  const db = readDB();
  const { student_id, student_name, category, target_id, answers } = req.body;

  if (!answers || typeof answers !== 'object') {
    return res.status(400).json({ status: 'error', message: 'ไม่พบข้อมูลคำตอบที่ส่ง' });
  }

  let targetQuestions = [];
  if (category === 'midterm') {
    targetQuestions = db.quizzes.filter(q => q.category === 'midterm');
  } else if (category === 'final') {
    targetQuestions = db.quizzes.filter(q => q.category === 'final');
  } else {
    targetQuestions = db.quizzes.filter(q => q.chapter_id === target_id);
  }

  if (targetQuestions.length === 0) {
    return res.status(400).json({ status: 'error', message: 'ไม่พบชุดข้อสอบที่ระบุ' });
  }

  let totalPoints = 0;
  let earnedPoints = 0;
  const review = [];

  targetQuestions.forEach(q => {
    const p = q.points || 1;
    totalPoints += p;
    const studentAnswerIndex = answers[q.id];
    const isCorrect = studentAnswerIndex !== undefined && Number(studentAnswerIndex) === q.correct_index;

    if (isCorrect) {
      earnedPoints += p;
    }

    review.push({
      question_id: q.id,
      question_text: q.question_text,
      options: q.options,
      student_answer: studentAnswerIndex !== undefined ? Number(studentAnswerIndex) : null,
      correct_answer: q.correct_index,
      is_correct: isCorrect,
      explanation: q.explanation
    });
  });

  const percentage = Math.round((earnedPoints / totalPoints) * 1000) / 10;

  const scoreRecord = {
    id: `score_${Date.now()}`,
    student_id: student_id || 'guest_student',
    student_name: student_name || 'นักเรียนผู้สอบ',
    exam_category: category || 'chapter_quiz',
    target_id: target_id || category,
    score: earnedPoints,
    max_score: totalPoints,
    percentage: percentage,
    submitted_at: new Date().toISOString()
  };

  db.scores = db.scores || [];
  db.scores.push(scoreRecord);
  writeDB(db);

  // Sync to Supabase cloud database
  supabase.from('scores').upsert({
    id: scoreRecord.id,
    student_id: scoreRecord.student_id,
    student_name: scoreRecord.student_name,
    exam_category: scoreRecord.exam_category,
    target_id: scoreRecord.target_id,
    chapter_id: category && category.startsWith('ch') ? category : null,
    score: scoreRecord.score,
    max_score: scoreRecord.max_score,
    percentage: scoreRecord.percentage,
    submitted_at: scoreRecord.submitted_at
  }).then(({ error }) => {
    if (error) console.warn('[Supabase Quiz Score Warning]:', error.message);
  }).catch(err => console.warn('[Supabase Quiz Score Catch]:', err.message));

  res.json({
    status: 'success',
    result: {
      score: earnedPoints,
      max_score: totalPoints,
      percentage: percentage,
      passed: percentage >= 50.0,
      review: review
    }
  });
});

// ==========================================
// 4. PRACTICAL EXAMS
// ==========================================
app.get('/api/practical', async (req, res) => {
  try {
    const { data, error } = await supabase.from('practical_exams').select('*').order('unit_number', { ascending: true });
    if (!error && data && data.length > 0) {
      return res.json({ status: 'success', engine: 'supabase', data });
    }
  } catch (e) {
    console.warn('[Supabase practical fetch fallback]:', e.message);
  }
  const db = readDB();
  res.json({ status: 'success', engine: 'local', data: db.practical_exams || [] });
});

// Protected: Create practical exam task (ครู / Admin)
app.post('/api/practical', requireAdmin, (req, res) => {
  const db = readDB();
  const { unit_number, chapter_id, title, scenario, rubrics, code_reference, max_score } = req.body;

  if (!title || !chapter_id) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกชื่อโจทย์และระบุบทเรียน' });
  }

  const uNum = parseInt(unit_number, 10) || ((db.practical_exams || []).length + 1);
  const newPractical = {
    id: `prac_${String(uNum).padStart(2, '0')}_${Date.now().toString().slice(-4)}`,
    unit_number: uNum,
    chapter_id: chapter_id || `ch${String(uNum).padStart(2, '0')}`,
    title: title.trim(),
    scenario: scenario ? scenario.trim() : '',
    rubrics: rubrics ? rubrics.trim() : '',
    code_reference: code_reference ? code_reference.trim() : '',
    max_score: parseInt(max_score, 10) || 10
  };

  if (!db.practical_exams) db.practical_exams = [];
  db.practical_exams.push(newPractical);
  writeDB(db);

  // Sync to Supabase
  supabase.from('practical_exams').upsert(newPractical).then(({ error }) => {
    if (error) console.warn('[Supabase Practical Insert Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Practical Insert Catch]:', e.message));

  res.status(201).json({ status: 'success', message: 'เพิ่มโจทย์ข้อสอบภาคปฏิบัติสำเร็จ', data: newPractical });
});

// Protected: Update practical exam task (ครู / Admin)
app.put('/api/practical/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const index = (db.practical_exams || []).findIndex(p => p.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบโจทย์ปฏิบัติการที่ต้องการแก้ไข' });
  }

  const { unit_number, chapter_id, title, scenario, rubrics, code_reference, max_score } = req.body;
  if (!title) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกชื่อโจทย์' });
  }

  const existing = db.practical_exams[index];
  db.practical_exams[index] = {
    ...existing,
    unit_number: unit_number !== undefined ? parseInt(unit_number, 10) : existing.unit_number,
    chapter_id: chapter_id !== undefined ? chapter_id : existing.chapter_id,
    title: title.trim(),
    scenario: scenario !== undefined ? scenario.trim() : existing.scenario,
    rubrics: rubrics !== undefined ? rubrics.trim() : existing.rubrics,
    code_reference: code_reference !== undefined ? code_reference.trim() : existing.code_reference,
    max_score: max_score !== undefined ? parseInt(max_score, 10) : existing.max_score
  };

  writeDB(db);

  // Sync to Supabase
  supabase.from('practical_exams').upsert(db.practical_exams[index]).then(({ error }) => {
    if (error) console.warn('[Supabase Practical Update Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Practical Update Catch]:', e.message));

  res.json({ status: 'success', message: 'แก้ไขโจทย์ข้อสอบปฏิบัติสำเร็จ', data: db.practical_exams[index] });
});

// Protected: Delete practical exam task (ครู / Admin)
app.delete('/api/practical/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const initialLen = (db.practical_exams || []).length;
  db.practical_exams = (db.practical_exams || []).filter(p => p.id !== req.params.id);

  if (db.practical_exams.length === initialLen) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบโจทย์ปฏิบัติการที่ต้องการลบ' });
  }

  writeDB(db);

  // Sync delete to Supabase
  supabase.from('practical_exams').delete().eq('id', req.params.id).then(({ error }) => {
    if (error) console.warn('[Supabase Practical Delete Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Practical Delete Catch]:', e.message));

  res.json({ status: 'success', message: 'ลบโจทย์ข้อสอบปฏิบัติสำเร็จ' });
});

// Protected: Teacher grades practical task (ครู / Admin)
app.post('/api/practical/grade', requireAdmin, (req, res) => {
  const db = readDB();
  const { student_id, student_name, practical_id, score, notes, rubrics_breakdown } = req.body;

  if (!student_id || practical_id === undefined || score === undefined) {
    return res.status(400).json({ status: 'error', message: 'ข้อมูลการบันทึกคะแนนไม่ครบถ้วน' });
  }

  const pScore = parseFloat(score);
  const existingIdx = (db.scores || []).findIndex(s => s.student_id === student_id && s.target_id === practical_id && s.exam_category === 'practical');

  const practical = (db.practical_exams || []).find(p => p.id === practical_id);
  const chId = practical ? practical.chapter_id : practical_id;

  const scoreRecord = {
    id: existingIdx >= 0 ? db.scores[existingIdx].id : `score_prac_${Date.now()}`,
    student_id,
    student_name: student_name || 'นักเรียนผู้รับการประเมิน',
    exam_category: 'practical',
    target_id: practical_id,
    chapter_id: chId,
    score: pScore,
    max_score: 10,
    percentage: Math.round((pScore / 10) * 100),
    notes: notes || '',
    rubrics_breakdown: rubrics_breakdown || null,
    submitted_at: normalizeToISO(new Date().toISOString())
  };

  if (!db.scores) db.scores = [];
  if (existingIdx >= 0) {
    db.scores[existingIdx] = scoreRecord;
  } else {
    db.scores.push(scoreRecord);
  }

  // Update submission status in db.submissions if present
  if (db.submissions) {
    const sub = db.submissions.find(s => s.student_id === student_id && (s.chapter_id === chId || s.chapter_id === practical_id) && (s.task_type || 'practical') === 'practical');
    if (sub) {
      sub.status = 'graded';
      sub.score = pScore;
    }
  }

  writeDB(db);

  // Sync score and submission status to Supabase Cloud Database
  supabase.from('scores').upsert({
    id: scoreRecord.id,
    student_id: scoreRecord.student_id,
    student_name: scoreRecord.student_name,
    exam_category: 'practical',
    target_id: scoreRecord.target_id,
    chapter_id: chId,
    score: scoreRecord.score,
    max_score: 10,
    percentage: scoreRecord.percentage,
    notes: scoreRecord.notes || '',
    rubrics_breakdown: scoreRecord.rubrics_breakdown || null,
    submitted_at: scoreRecord.submitted_at
  }).then(({ error }) => {
    if (error) console.warn('[Supabase Grade Practical Warning]:', error.message);
  }).catch(err => console.warn('[Supabase Grade Practical Catch]:', err.message));

  supabase.from('submissions')
    .update({ status: 'graded', score: pScore })
    .eq('student_id', student_id)
    .eq('task_type', 'practical')
    .then(({ error }) => {
      if (error) console.warn('[Supabase Submission Status Warning]:', error.message);
    }).catch(err => console.warn('[Supabase Submission Status Catch]:', err.message));

  // Asynchronous Background Queue to Google Sheet (non-blocking)
  sheetQueue.enqueue(`บันทึกเกรดปฏิบัติ: ${scoreRecord.student_name} (${scoreRecord.score}/10)`, () => sendGradeToGoogleSheet(scoreRecord));

  res.json({ status: 'success', message: 'บันทึกผลการประเมินข้อสอบภาคปฏิบัติสำเร็จ', data: scoreRecord });
});

// Protected: Grade Lab Worksheet (ครู / Admin)
app.post('/api/worksheets/grade', requireAdmin, (req, res) => {
  const db = readDB();
  const { student_id, student_name, chapter_id, worksheet_id, score, notes } = req.body;

  if (!student_id || (!chapter_id && !worksheet_id) || score === undefined) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกข้อมูลการประเมินใบงานให้ครบถ้วน' });
  }

  const wScore = parseFloat(score);
  const targetId = worksheet_id || chapter_id;
  const existingIdx = (db.scores || []).findIndex(s => s.student_id === student_id && (s.target_id === targetId || s.chapter_id === chapter_id) && s.exam_category === 'worksheet');

  const scoreRecord = {
    id: existingIdx >= 0 ? db.scores[existingIdx].id : `score_ws_${Date.now()}`,
    student_id,
    student_name: student_name || 'นักเรียนผู้รับการประเมิน',
    exam_category: 'worksheet',
    target_id: targetId,
    chapter_id: chapter_id,
    score: wScore,
    max_score: 10,
    percentage: Math.round((wScore / 10) * 100),
    notes: notes || '',
    rubrics_breakdown: null,
    submitted_at: normalizeToISO(new Date().toISOString())
  };

  if (!db.scores) db.scores = [];
  if (existingIdx >= 0) {
    db.scores[existingIdx] = scoreRecord;
  } else {
    db.scores.push(scoreRecord);
  }

  // Update submission status in db.submissions if present
  if (db.submissions) {
    const sub = db.submissions.find(s => s.student_id === student_id && (s.chapter_id === chapter_id || s.chapter_id === targetId) && s.task_type === 'worksheet');
    if (sub) {
      sub.status = 'graded';
      sub.score = wScore;
    }
  }

  writeDB(db);

  // Sync score and submission status to Supabase Cloud Database
  supabase.from('scores').upsert({
    id: scoreRecord.id,
    student_id: scoreRecord.student_id,
    student_name: scoreRecord.student_name,
    exam_category: 'worksheet',
    target_id: scoreRecord.target_id,
    chapter_id: scoreRecord.chapter_id,
    score: scoreRecord.score,
    max_score: 10,
    percentage: scoreRecord.percentage,
    notes: scoreRecord.notes || '',
    rubrics_breakdown: null,
    submitted_at: scoreRecord.submitted_at
  }).then(({ error }) => {
    if (error) console.warn('[Supabase Grade Worksheet Warning]:', error.message);
  }).catch(err => console.warn('[Supabase Grade Worksheet Catch]:', err.message));

  supabase.from('submissions')
    .update({ status: 'graded', score: wScore })
    .eq('student_id', student_id)
    .eq('task_type', 'worksheet')
    .then(({ error }) => {
      if (error) console.warn('[Supabase Submission Status Warning]:', error.message);
    }).catch(err => console.warn('[Supabase Submission Status Catch]:', err.message));

  // Asynchronous Background Queue to Google Sheet (non-blocking)
  sheetQueue.enqueue(`บันทึกเกรดใบงาน: ${scoreRecord.student_name} (${scoreRecord.score}/10)`, () => sendGradeToGoogleSheet(scoreRecord));

  res.json({ status: 'success', message: 'บันทึกผลการประเมินใบงานปฏิบัติการสำเร็จ', data: scoreRecord });
});

// Helper to push grade (practical or worksheet) to Google Sheet
async function sendGradeToGoogleSheet(gradeRecord) {
  const db = readDB();
  const webhookUrl = process.env.GOOGLE_SHEET_SUBMISSION_WEBHOOK_URL || db.google_sheet_webhook_url;
  if (!webhookUrl) {
    return { success: false, reason: 'no_webhook_configured' };
  }

  try {
    const isWorksheet = gradeRecord.exam_category === 'worksheet';
    const targetSheet = isWorksheet ? 'worksheet' : 'practical';
    const taskType = isWorksheet ? 'worksheet' : 'practical';

    let chapterDisplay = gradeRecord.target_id || '';
    let chId = gradeRecord.chapter_id || gradeRecord.target_id || '';
    let unitNum = null;

    if (isWorksheet) {
      const ws = (db.worksheets || []).find(w => w.id === gradeRecord.target_id || w.chapter_id === gradeRecord.chapter_id || w.chapter_id === gradeRecord.target_id);
      if (ws) {
        chapterDisplay = ws.title || `ใบงานบทที่ ${ws.chapter_number}`;
        chId = ws.chapter_id;
        unitNum = ws.chapter_number;
      }
    } else {
      const practical = (db.practical_exams || []).find(p => p.id === gradeRecord.target_id || p.id === gradeRecord.practical_id || p.chapter_id === gradeRecord.target_id);
      if (practical) {
        chapterDisplay = `บทที่ ${practical.unit_number}: ${practical.title}`;
        chId = practical.chapter_id;
        unitNum = practical.unit_number;
      }
    }

    const sub = (db.submissions || []).find(s => 
      s.student_id === gradeRecord.student_id && 
      (s.chapter_id === chId || s.chapter_id === gradeRecord.target_id) && 
      (s.task_type || 'practical') === taskType
    );

    const payload = {
      action: 'grade',
      sheet_name: targetSheet,
      task_type: taskType,
      timestamp: new Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' }),
      student_id: gradeRecord.student_id,
      student_name: gradeRecord.student_name,
      chapter_id: chapterDisplay,
      chapter_code: chId,
      unit_number: unitNum,
      report_url: sub ? sub.report_url : '',
      score: gradeRecord.score,
      max_score: gradeRecord.max_score || 10,
      score_display: `${gradeRecord.score} / ${gradeRecord.max_score || 10}`,
      teacher_notes: gradeRecord.notes || ''
    };

    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    console.log(`[Google Sheet Grade Sync] บันทึกคะแนนของ ${gradeRecord.student_name} (${gradeRecord.score}/10) ลงชีต ${targetSheet} สำเร็จ (HTTP ${response.status})`);
    return { success: true, status: response.status };
  } catch (err) {
    console.error(`[Google Sheet Grade Sync Error]:`, err.message);
    return { success: false, error: err.message };
  }
}

// Helper to push lab submission to Google Sheet (separated sheets: practical / worksheet)
async function sendSubmissionToGoogleSheet(subRecord) {
  const db = readDB();
  const webhookUrl = process.env.GOOGLE_SHEET_SUBMISSION_WEBHOOK_URL || db.google_sheet_webhook_url;
  if (!webhookUrl) {
    return { success: false, reason: 'no_webhook_configured' };
  }

  try {
    const practical = (db.practical_exams || []).find(p => p.chapter_id === subRecord.chapter_id || p.id === subRecord.chapter_id);
    const chapterDisplay = practical ? `บทที่ ${practical.unit_number}: ${practical.title}` : subRecord.chapter_id;

    const taskType = subRecord.task_type === 'worksheet' ? 'worksheet' : 'practical';
    const targetSheet = taskType === 'worksheet' ? 'worksheet' : 'practical';

    const payload = {
      action: 'submission',
      sheet_name: targetSheet,
      task_type: taskType,
      timestamp: new Date().toLocaleString('th-TH', { timeZone: 'Asia/Bangkok' }),
      student_id: subRecord.student_id,
      student_name: subRecord.student_name,
      chapter_id: chapterDisplay,
      chapter_code: subRecord.chapter_id,
      unit_number: practical ? practical.unit_number : null,
      report_url: subRecord.report_url,
      notes: subRecord.notes
    };

    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    console.log(`[Google Sheet Sync] บันทึกงาน (${taskType}) ของ ${subRecord.student_name} ลงชีต ${targetSheet} สำเร็จ (HTTP ${response.status})`);
    return { success: true, status: response.status };
  } catch (err) {
    console.error('[Google Sheet Sync Error]:', err.message);
    return { success: false, error: err.message };
  }
}

// Student submits lab work or practical report (Protected by submission rate limiter)
app.post('/api/submissions', submissionLimiter, async (req, res) => {
  const db = readDB();
  if (!db.submissions) db.submissions = [];
  const { student_id, student_name, chapter_id, report_url, notes, task_type } = req.body;

  if (!student_id || !chapter_id) {
    return res.status(400).json({ status: 'error', message: 'ข้อมูลการส่งงานไม่ครบถ้วน' });
  }

  const effectiveTaskType = task_type === 'worksheet' ? 'worksheet' : 'practical';
  const existingIdx = db.submissions.findIndex(s => 
    s.student_id === student_id && 
    s.chapter_id === chapter_id && 
    (s.task_type || 'practical') === effectiveTaskType
  );

  const subRecord = {
    id: existingIdx >= 0 ? db.submissions[existingIdx].id : `sub_${Date.now()}`,
    student_id,
    student_name: student_name || 'นักเรียน',
    chapter_id,
    task_type: effectiveTaskType,
    report_url: report_url || '',
    notes: notes || '',
    status: 'submitted',
    submitted_at: normalizeToISO(new Date().toISOString())
  };

  if (existingIdx >= 0) {
    // Preserve existing score if already graded
    if (db.submissions[existingIdx].score !== undefined) {
      subRecord.score = db.submissions[existingIdx].score;
      subRecord.status = db.submissions[existingIdx].status || 'graded';
    }
    db.submissions[existingIdx] = subRecord;
  } else {
    db.submissions.push(subRecord);
  }
  writeDB(db);

  // Sync submission to Supabase Cloud Database
  supabase.from('submissions').upsert({
    id: subRecord.id,
    student_id: subRecord.student_id,
    student_name: subRecord.student_name,
    chapter_id: subRecord.chapter_id,
    task_type: subRecord.task_type,
    report_url: subRecord.report_url,
    notes: subRecord.notes,
    status: subRecord.status || 'submitted',
    score: subRecord.score !== undefined ? subRecord.score : null,
    submitted_at: subRecord.submitted_at
  }).then(({ error }) => {
    if (error) console.warn('[Supabase Submission Upsert Warning]:', error.message);
  }).catch(err => console.warn('[Supabase Submission Upsert Catch]:', err.message));

  // Asynchronous Background Queue to Google Sheet (non-blocking)
  sheetQueue.enqueue(`ส่งงาน: ${subRecord.student_name} (${subRecord.task_type})`, () => sendSubmissionToGoogleSheet(subRecord));

  const msg = effectiveTaskType === 'worksheet' 
    ? 'บันทึกการส่งใบงานปฏิบัติการประจำบทเรียบร้อยแล้ว!' 
    : 'บันทึกการส่งรายงานโจทย์ปฏิบัติการเรียบร้อยแล้ว!';

  res.json({ status: 'success', message: msg, data: subRecord });
});

app.get('/api/submissions', async (req, res) => {
  const adminToken = req.headers['x-admin-token'] || req.headers['authorization']?.replace(/^Bearer\s+/i, '');
  const isAdmin = isValidAdminToken(adminToken);
  const studentToken = req.headers['x-student-token'];
  const studentSession = studentToken ? studentSessions.get(studentToken) : null;
  const headerStudentId = req.headers['x-student-id'];
  const { student_id, task_type } = req.query;

  // Enforce Privacy (PDPA): นักเรียนดูได้เฉพาะของตนเองเท่านั้น จะดูของเพื่อนไม่ได้
  let effectiveStudentId = null;
  if (!isAdmin) {
    effectiveStudentId = studentSession ? studentSession.studentId : (headerStudentId || student_id);
    if (!effectiveStudentId) {
      return res.json({ status: 'success', engine: 'guarded', data: [] });
    }
  } else {
    effectiveStudentId = student_id || null;
  }

  try {
    let query = supabase.from('submissions').select('*').order('submitted_at', { ascending: false });
    if (effectiveStudentId) query = query.eq('student_id', effectiveStudentId);
    if (task_type) query = query.eq('task_type', task_type);
    const { data, error } = await query;
    if (!error && data) {
      return res.json({ status: 'success', engine: 'supabase', data });
    }
  } catch (e) {
    console.warn('[Supabase submissions fetch fallback]:', e.message);
  }
  const db = readDB();
  let list = db.submissions || [];
  if (effectiveStudentId) {
    list = list.filter(s => s.student_id === effectiveStudentId);
  }
  if (task_type) {
    list = list.filter(s => (s.task_type || 'practical') === task_type);
  }
  res.json({ status: 'success', engine: 'local', data: list });
});

// Google Sheet Integration Settings & Sync
app.get('/api/admin/google-sheet-config', (req, res) => {
  const db = readDB();
  res.json({
    status: 'success',
    data: {
      spreadsheet_id: '1SLgcSTaoFcy2kXb_oas70A9uImrhZWzcubnVf8yqlBM',
      sheet_name: 'worksheet',
      webhook_url: db.google_sheet_webhook_url || process.env.GOOGLE_SHEET_SUBMISSION_WEBHOOK_URL || '',
      has_webhook: Boolean(db.google_sheet_webhook_url || process.env.GOOGLE_SHEET_SUBMISSION_WEBHOOK_URL)
    }
  });
});

app.post('/api/admin/google-sheet-config', requireAdmin, (req, res) => {
  const { webhook_url } = req.body;
  const db = readDB();
  db.google_sheet_webhook_url = (webhook_url || '').trim();
  writeDB(db);
  res.json({ status: 'success', message: 'บันทึกการตั้งค่า Google Sheet Webhook สำเร็จ', webhook_url: db.google_sheet_webhook_url });
});

app.post('/api/admin/sync-all-submissions', requireAdmin, async (req, res) => {
  const db = readDB();
  const webhookUrl = process.env.GOOGLE_SHEET_SUBMISSION_WEBHOOK_URL || db.google_sheet_webhook_url;
  if (!webhookUrl) {
    return res.status(400).json({ status: 'error', message: 'กรุณาตั้งค่า Google Apps Script Webhook URL ก่อนทำการซิงค์' });
  }

  const list = db.submissions || [];
  let sentCount = 0;
  for (const item of list) {
    try {
      await sendSubmissionToGoogleSheet(item);
      sentCount++;
    } catch (e) {
      console.warn('Sync submission item failed:', e.message);
    }
  }

  // Also sync practical & worksheet grades to respective tabs (practical & worksheet)
  const practicalScores = (db.scores || []).filter(s => s.exam_category === 'practical');
  const worksheetScores = (db.scores || []).filter(s => s.exam_category === 'worksheet');
  const allGradedScores = [...practicalScores, ...worksheetScores];
  let gradeSentCount = 0;
  for (const score of allGradedScores) {
    try {
      await sendGradeToGoogleSheet(score);
      gradeSentCount++;
    } catch (e) {
      console.warn('Sync grade item failed:', e.message);
    }
  }

  res.json({
    status: 'success',
    message: `ซิงค์ข้อมูลส่งงาน (${sentCount}/${list.length} รายการ) และคะแนนประเมิน (${gradeSentCount}/${allGradedScores.length} รายการ ทั้งโจทย์ปฏิบัติและใบงาน) ไปยัง Google Sheet (แท็บ practical และ worksheet) เรียบร้อยแล้ว`
  });
});

// ==========================================
// 5. WORKSHEETS & MATERIALS CRUD
// ==========================================
app.get('/api/worksheets', async (req, res) => {
  try {
    const { data, error } = await supabase.from('worksheets').select('*').order('chapter_number', { ascending: true });
    if (!error && data && data.length > 0) {
      return res.json({ status: 'success', engine: 'supabase', data });
    }
  } catch (e) {
    console.warn('[Supabase worksheets fetch fallback]:', e.message);
  }
  const db = readDB();
  res.json({ status: 'success', engine: 'local', data: db.worksheets || [] });
});

// Protected: Create worksheet (ครู / Admin)
app.post('/api/worksheets', requireAdmin, (req, res) => {
  const db = readDB();
  const { chapter_number, chapter_id, title, time_minutes, instructions, file_name, file_url, view_url, code_reference, status } = req.body;

  if (!title || !chapter_id) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกชื่อใบงานและระบุบทเรียน' });
  }

  const chNum = parseInt(chapter_number, 10) || ((db.worksheets || []).length + 1);
  const newWorksheet = {
    id: `ws_${String(chNum).padStart(2, '0')}_${Date.now().toString().slice(-4)}`,
    chapter_number: chNum,
    chapter_id: chapter_id || `ch${String(chNum).padStart(2, '0')}`,
    title: title.trim(),
    time_minutes: parseInt(time_minutes, 10) || 60,
    instructions: instructions ? instructions.trim() : '',
    file_name: file_name ? file_name.trim() : `Lab_Worksheet_${String(chNum).padStart(2, '0')}.pdf`,
    file_url: file_url ? file_url.trim() : `/worksheets/Lab_Worksheet_${String(chNum).padStart(2, '0')}.pdf`,
    view_url: view_url ? view_url.trim() : `/worksheets/worksheet${String(chNum).padStart(2, '0')}.html`,
    code_reference: code_reference ? code_reference.trim() : '',
    status: status || 'active'
  };

  if (!db.worksheets) db.worksheets = [];
  db.worksheets.push(newWorksheet);
  writeDB(db);

  // Sync to Supabase
  supabase.from('worksheets').upsert(newWorksheet).then(({ error }) => {
    if (error) console.warn('[Supabase Worksheet Insert Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Worksheet Insert Catch]:', e.message));

  res.status(201).json({ status: 'success', message: 'เพิ่มใบงานปฏิบัติการสำเร็จ', data: newWorksheet });
});

// Protected: Update worksheet (ครู / Admin)
app.put('/api/worksheets/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const index = (db.worksheets || []).findIndex(w => w.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบใบงานที่ต้องการแก้ไข' });
  }

  const { chapter_number, chapter_id, title, time_minutes, instructions, file_name, file_url, view_url, code_reference, status } = req.body;
  if (!title) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกชื่อใบงาน' });
  }

  const existing = db.worksheets[index];
  db.worksheets[index] = {
    ...existing,
    chapter_number: chapter_number !== undefined ? parseInt(chapter_number, 10) : existing.chapter_number,
    chapter_id: chapter_id !== undefined ? chapter_id : existing.chapter_id,
    title: title.trim(),
    time_minutes: time_minutes !== undefined ? parseInt(time_minutes, 10) : existing.time_minutes,
    instructions: instructions !== undefined ? instructions.trim() : existing.instructions,
    file_name: file_name !== undefined ? file_name.trim() : existing.file_name,
    file_url: file_url !== undefined ? file_url.trim() : existing.file_url,
    view_url: view_url !== undefined ? view_url.trim() : existing.view_url,
    code_reference: code_reference !== undefined ? code_reference.trim() : existing.code_reference,
    status: status || existing.status || 'active'
  };

  writeDB(db);

  // Sync to Supabase
  supabase.from('worksheets').upsert(db.worksheets[index]).then(({ error }) => {
    if (error) console.warn('[Supabase Worksheet Update Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Worksheet Update Catch]:', e.message));

  res.json({ status: 'success', message: 'แก้ไขใบงานปฏิบัติการสำเร็จ', data: db.worksheets[index] });
});

// Protected: Delete worksheet (ครู / Admin)
app.delete('/api/worksheets/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const initialLen = (db.worksheets || []).length;
  db.worksheets = (db.worksheets || []).filter(w => w.id !== req.params.id);

  if (db.worksheets.length === initialLen) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบใบงานที่ต้องการลบ' });
  }

  writeDB(db);

  // Sync delete to Supabase
  supabase.from('worksheets').delete().eq('id', req.params.id).then(({ error }) => {
    if (error) console.warn('[Supabase Worksheet Delete Warning]:', error.message);
  }).catch(e => console.warn('[Supabase Worksheet Delete Catch]:', e.message));

  res.json({ status: 'success', message: 'ลบใบงานปฏิบัติการสำเร็จ' });
});

app.get('/api/materials', (req, res) => {
  const db = readDB();
  res.json({ status: 'success', data: db.materials || [] });
});

// Protected: Create material (ครู / Admin)
app.post('/api/materials', requireAdmin, (req, res) => {
  const db = readDB();
  const { chapter_id, type, title, url } = req.body;
  if (!title) {
    return res.status(400).json({ status: 'error', message: 'กรุณากรอกชื่อสื่อหรือเอกสาร' });
  }

  const newMat = {
    id: `mat_${Date.now()}`,
    chapter_id: chapter_id || 'ch01',
    type: type || 'slide',
    title,
    url: url || '#'
  };

  db.materials.push(newMat);
  writeDB(db);
  res.status(201).json({ status: 'success', message: 'เพิ่มสื่อการสอนสำเร็จ', data: newMat });
});

// Protected: Delete material (ครู / Admin)
app.delete('/api/materials/:id', requireAdmin, (req, res) => {
  const db = readDB();
  const initialLen = db.materials.length;
  db.materials = db.materials.filter(m => m.id !== req.params.id);
  if (db.materials.length === initialLen) {
    return res.status(404).json({ status: 'error', message: 'ไม่พบรายการสื่อที่ต้องการลบ' });
  }
  writeDB(db);
  res.json({ status: 'success', message: 'ลบรายการสื่อสำเร็จ' });
});

// ==========================================
// 6. SCORES & GRADEBOOK (สมุดบันทึกคะแนน)
// ==========================================
app.get('/api/scores', async (req, res) => {
  const adminToken = req.headers['x-admin-token'] || req.headers['authorization']?.replace(/^Bearer\s+/i, '');
  const isAdmin = isValidAdminToken(adminToken);
  const studentToken = req.headers['x-student-token'];
  const studentSession = studentToken ? studentSessions.get(studentToken) : null;
  const headerStudentId = req.headers['x-student-id'];
  const { student_id, exam_category } = req.query;

  // Enforce Privacy (PDPA): นักเรียนดูได้เฉพาะคะแนนของตนเองเท่านั้น จะดูของเพื่อนไม่ได้
  let effectiveStudentId = null;
  if (!isAdmin) {
    effectiveStudentId = studentSession ? studentSession.studentId : (headerStudentId || student_id);
    if (!effectiveStudentId) {
      return res.json({ status: 'success', engine: 'guarded', data: [] });
    }
  } else {
    effectiveStudentId = student_id || null;
  }

  try {
    let query = supabase.from('scores').select('*').order('created_at', { ascending: false });
    if (effectiveStudentId) query = query.eq('student_id', effectiveStudentId);
    if (exam_category) query = query.eq('exam_category', exam_category);
    const { data, error } = await query;
    if (!error && data) {
      return res.json({ status: 'success', engine: 'supabase', data });
    }
  } catch (e) {
    console.warn('[Supabase scores fetch fallback]:', e.message);
  }
  const db = readDB();
  let items = db.scores || [];
  if (effectiveStudentId) {
    items = items.filter(s => s.student_id === effectiveStudentId);
  }
  if (exam_category) {
    items = items.filter(s => s.exam_category === exam_category);
  }
  res.json({ status: 'success', engine: 'local', data: items });
});

// Protected: Export scores CSV endpoint (รองรับ UTF-8 BOM สำหรับ Excel ภาษาไทย)
app.get('/api/export/scores-csv', requireAdmin, (req, res) => {
  const db = readDB();
  const scores = db.scores || [];
  let csv = '\uFEFFรหัสนักเรียน,ชื่อ-นามสกุล,หมวดหมู่การสอบ,รหัสข้อสอบ/บท,คะแนนที่ได้,คะแนนเต็ม,ร้อยละ,เวลาที่ส่ง\n';
  scores.forEach(s => {
    csv += `"${s.student_id}","${s.student_name}","${s.exam_category}","${s.target_id}",${s.score},${s.max_score},${s.percentage},"${s.submitted_at}"\n`;
  });
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename="scores_kt_edu_edgeai.csv"');
  res.send(csv);
});

// ==========================================
// 7. DATABASE RESET (คืนค่าข้อมูลมาตรฐาน)
// ==========================================
// Protected: Reset database (ครู / Admin)
app.post('/api/reset-database', requireAdmin, (req, res) => {
  try {
    if (fs.existsSync(SEED_PATH)) {
      fs.copyFileSync(SEED_PATH, DB_PATH);
      res.json({ status: 'success', message: 'คืนค่าฐานข้อมูลเริ่มต้นเรียบร้อยแล้ว' });
    } else {
      res.status(500).json({ status: 'error', message: 'ไม่พบไฟล์ต้นฉบับ seed.json' });
    }
  } catch (err) {
    res.status(500).json({ status: 'error', message: err.message });
  }
});

// Protected: Download database backup snapshot (ครู / Admin)
app.get('/api/database/backup', requireAdmin, (req, res) => {
  if (fs.existsSync(BACKUP_PATH)) {
    res.download(BACKUP_PATH, `edgeai_db_backup_${Date.now()}.json`);
  } else if (fs.existsSync(DB_PATH)) {
    res.download(DB_PATH, `edgeai_db_${Date.now()}.json`);
  } else {
    res.status(404).json({ status: 'error', message: 'ไม่พบไฟล์สำรองข้อมูล' });
  }
});

// Start listening with auto-port fallback if port is in use
function startServer(portToTry) {
  const server = app.listen(portToTry, () => {
    console.log(`=======================================================`);
    console.log(` ระบบเว็บบทเรียนออนไลน์: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว`);
    console.log(` Embedded Artificial Intelligence Learning Platform`);
    console.log(` URL: http://localhost:${portToTry}`);
    console.log(` บทบาท: นักเรียน (Student) และ ครู/Admin (Protected RBAC)`);
    console.log(` รหัสผ่านผู้ดูแลระบบ (Admin Passcode): ${ADMIN_PASSCODE}`);
    console.log(`=======================================================`);
    
    // ซิงค์ข้อมูลนักเรียนล่าสุดจาก Google Sheet ทันทีที่สตาร์ตเซิร์ฟเวอร์
    syncStudentsFromGoogleSheet().catch(e => console.error('[Initial Sheet Sync Error]:', e.message));
  });

  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.warn(`[PORT NOTICE] พอร์ต ${portToTry} มีโปรเซสอื่นใช้งานอยู่ กำลังสลับไปใช้พอร์ต ${portToTry + 1}...`);
      startServer(portToTry + 1);
    } else {
      console.error('[Server Error]:', err);
    }
  });
}

startServer(Number(PORT));

