/**
 * แพลตฟอร์มบทเรียนออนไลน์ รายวิชา ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded AI)
 * depa Thailand Digital Learning Platform Controller
 */

// Global Application State

// Security & Sanitization Utilities
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function getAuthHeaders(extra = {}) {
  const token = sessionStorage.getItem('edgeai_admin_token') || '';
  const stdToken = sessionStorage.getItem('edgeai_student_token') || '';
  const stdId = state.currentUser?.student_id || '';
  return {
    'Content-Type': 'application/json',
    'x-admin-token': token,
    'x-student-token': stdToken,
    'x-student-id': stdId,
    ...extra
  };
}

const state = {
  currentRole: localStorage.getItem('edgeai_role') || 'student', // 'student' or 'admin'
  currentUser: null, // null by default, only populated when a student explicitly logs in
  students: [],
  lessons: [],
  quizzes: [],
  practicalExams: [],
  worksheets: [],
  materials: [],
  scores: [],
  submissions: [],
  worksheetFilter: 'all',
  worksheetSearch: '',
  activeExam: null, // Holds currently running exam data
  stats: null
};

// ==============================================================
// 1. INITIALIZATION & DATA FETCHING & SUPABASE REAL-TIME ENGINE
// ==============================================================
const SUPABASE_URL = 'https://savyelqzzyzbipucdksn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNhdnllbHF6enl6YmlwdWNka3NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIxMzUxNTAsImV4cCI6MjEwNzcxMTE1MH0.-Qm9nNaiklOcnQi0p3P2k2MPQsF06HbgMuUrSMovjos';
let supabaseClient = null;
let liveSyncInterval = null;
let isSyncingLive = false;
let realtimeDebounceTimer = null;

function queueLiveSync() {
  if (realtimeDebounceTimer) clearTimeout(realtimeDebounceTimer);
  realtimeDebounceTimer = setTimeout(() => {
    triggerLiveSheetSync(false);
  }, 350);
}

function initSupabaseRealtime() {
  if (typeof window.supabase === 'undefined' || !window.supabase.createClient) {
    console.warn('Supabase SDK not loaded, continuing with HTTP polling.');
    return;
  }
  try {
    supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    supabaseClient
      .channel('realtime-edgeai-channel')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'submissions' }, (payload) => {
        console.log('⚡ [Supabase Realtime] Submissions updated:', payload);
        queueLiveSync();
      })
      .on('postgres_changes', { event: '*', schema: 'public', table: 'scores' }, (payload) => {
        console.log('⚡ [Supabase Realtime] Scores updated:', payload);
        queueLiveSync();
      })
      .on('postgres_changes', { event: '*', schema: 'public', table: 'students' }, (payload) => {
        console.log('⚡ [Supabase Realtime] Students updated:', payload);
        queueLiveSync();
      })
      .subscribe((status) => {
        const statusEl = document.getElementById('realtimeSyncStatusText');
        if (statusEl && status === 'SUBSCRIBED') {
          statusEl.textContent = '⚡ Supabase Realtime สด';
        }
      });
  } catch (err) {
    console.warn('Supabase Realtime subscription error:', err.message);
  }
}

async function triggerLiveSheetSync(showToastOnSuccess = false) {
  if (isSyncingLive) return;
  isSyncingLive = true;

  const icon = document.getElementById('iconRealtimeSync');
  if (icon) icon.classList.add('fa-spin');

  try {
    const res = await fetch('/api/sync/live' + (showToastOnSuccess ? '?force=true' : ''));
    const json = await res.json();

    if (json.status === 'success') {
      if (json.scores) state.scores = json.scores;
      if (json.submissions) state.submissions = json.submissions;
      if (json.students && json.students.length > 0) state.students = json.students;

      const statusEl = document.getElementById('realtimeSyncStatusText');
      if (statusEl) {
        const d = new Date(json.last_synced || Date.now());
        const timeFormatted = d.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        statusEl.textContent = `⚡ ซิงค์สด: ${timeFormatted}`;
        statusEl.title = `ซิงค์ข้อมูลสดจาก Supabase สำเร็จเมื่อ ${timeFormatted}`;
      }

      // Re-render UI components safely without destroying active input focus
      const activeEl = document.activeElement;
      const isUserTyping = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA') && activeEl.closest('#adminGradingContainer, #gradingSection, form');

      if (typeof currentTab !== 'undefined') {
        if (currentTab === 'admin') {
          if (typeof currentAdminSubTab !== 'undefined' && currentAdminSubTab === 'grading') {
            renderGradingStudentRoster();
            const activeStdId = document.getElementById('gradeStudentSelect')?.value;
            if (activeStdId && !isUserTyping) {
              onGradeStudentChange();
            }
          } else if (typeof currentAdminSubTab !== 'undefined' && currentAdminSubTab === 'submissions') {
            renderAdminSubmissions();
          }
        } else if (currentTab === 'worksheets') {
          renderWorksheets();
        } else if (currentTab === 'practical') {
          renderPracticalExams();
        } else if (currentTab === 'scores') {
          renderScores();
        }
      }

      if (showToastOnSuccess) {
        showToast('ซิงค์ข้อมูลสดจาก Supabase สำเร็จแล้ว', 'success');
      }
    }
  } catch (err) {
    console.warn('[Live Sync Warning]:', err.message);
  } finally {
    isSyncingLive = false;
    if (icon) icon.classList.remove('fa-spin');
  }
}

function startRealTimeSyncLoop() {
  if (liveSyncInterval) clearInterval(liveSyncInterval);
  // Relaxed heartbeat poll every 30 seconds as background resilience
  liveSyncInterval = setInterval(() => {
    triggerLiveSheetSync(false);
  }, 30000);
}

document.addEventListener('DOMContentLoaded', async () => {
  try { initFontStyle(); } catch (e) { console.warn('initFontStyle err:', e); }
  try { initStudentProfile(); } catch (e) { console.warn('initStudentProfile err:', e); }

  await fetchAllData();

  try { applyRoleUI(); } catch (e) { console.warn('applyRoleUI err:', e); }
  try { renderAllViews(); } catch (e) { console.error('renderAllViews err:', e); }
  try { populateDropdowns(); } catch (e) { console.warn('populateDropdowns err:', e); }
  try { initSlider(); } catch (e) { console.warn('initSlider err:', e); }
  try { handleUrlDeepLinking(); } catch (e) { console.warn('handleUrlDeepLinking err:', e); }
  try { initSupabaseRealtime(); } catch (e) { console.warn('initSupabaseRealtime err:', e); }
  try { startRealTimeSyncLoop(); } catch (e) { console.warn('startRealTimeSyncLoop err:', e); }
});

async function fetchAllData() {
  try {
    const authHeaders = getAuthHeaders();
    const isAdmin = (state.currentRole === 'admin' && !!sessionStorage.getItem('edgeai_admin_token'));
    const isStudent = (state.currentRole === 'student' && state.currentUser?.student_id);

    let scoresUrl = '/api/scores';
    let subsUrl = '/api/submissions';
    if (!isAdmin && isStudent) {
      scoresUrl = `/api/scores?student_id=${encodeURIComponent(state.currentUser.student_id)}`;
      subsUrl = `/api/submissions?student_id=${encodeURIComponent(state.currentUser.student_id)}`;
    }

    const [resLessons, resQuizzes, resPractical, resWorksheets, resMaterials, resScores, resStats, resStudents, resSubmissions] = await Promise.all([
      fetch('/api/lessons').then(r => r.json()).catch(err => { console.error('/api/lessons fetch err:', err); return { data: [] }; }),
      fetch('/api/quizzes').then(r => r.json()).catch(err => { console.error('/api/quizzes fetch err:', err); return { data: [] }; }),
      fetch('/api/practical').then(r => r.json()).catch(err => { console.error('/api/practical fetch err:', err); return { data: [] }; }),
      fetch('/api/worksheets').then(r => r.json()).catch(err => { console.error('/api/worksheets fetch err:', err); return { data: [] }; }),
      fetch('/api/materials').then(r => r.json()).catch(err => { console.error('/api/materials fetch err:', err); return { data: [] }; }),
      fetch(scoresUrl, { headers: authHeaders }).then(r => r.json()).catch(err => { console.error('/api/scores fetch err:', err); return { data: [] }; }),
      fetch('/api/stats', { headers: authHeaders }).then(r => r.json()).catch(err => { console.error('/api/stats fetch err:', err); return { stats: {} }; }),
      fetch('/api/students', { headers: authHeaders }).then(r => r.json()).catch(err => { console.error('/api/students fetch err:', err); return { data: [] }; }),
      fetch(subsUrl, { headers: authHeaders }).then(r => r.json()).catch(err => { console.error('/api/submissions fetch err:', err); return { data: [] }; })
    ]);

    state.lessons = resLessons.data || [];
    state.quizzes = resQuizzes.data || [];
    state.practicalExams = resPractical.data || [];
    state.worksheets = resWorksheets.data || [];
    state.materials = resMaterials.data || [];
    state.scores = resScores.data || [];
    state.stats = resStats.stats || {};
    state.students = resStudents.data || [];
    state.submissions = resSubmissions.data || [];

    // หากมีนักเรียนล็อกอินอยู่ ให้ซิงค์ชื่อและห้องล่าสุดจากฐานข้อมูลทันที (แก้ปัญหาชื่อเก่าค้างใน localStorage)
    if (state.currentUser && state.currentUser.student_id) {
      const fresh = state.students.find(s => s.student_id === state.currentUser.student_id);
      if (fresh) {
        state.currentUser.name = fresh.name;
        state.currentUser.class_room = fresh.class_room || 'ม.5/12';
        localStorage.setItem('edgeai_student_user', JSON.stringify(fresh));
        updateStudentNavUI(fresh);
      }
    }
  } catch (err) {
    console.error('Error fetching data:', err);
    showToast('เกิดข้อผิดพลาดในการโหลดข้อมูลจากเซิร์ฟเวอร์', 'error');
  }
}

// ==============================================================
// 2. ROLE SWITCHER & ACCESS CONTROL (RBAC)
// ==============================================================
function toggleRoleDropdown() {
  const dd = document.getElementById('roleDropdown');
  dd?.classList.toggle('hidden');
}

// Close dropdown when clicked outside
document.addEventListener('click', (e) => {
  const btn = document.getElementById('roleSwitchBtn');
  const dd = document.getElementById('roleDropdown');
  if (btn && dd && !btn.contains(e.target) && !dd.contains(e.target)) {
    dd.classList.add('hidden');
  }
});

function requestAdminRole() {
  document.getElementById('roleDropdown')?.classList.add('hidden');
  const token = sessionStorage.getItem('edgeai_admin_token');
  if (token) {
    fetch('/api/auth/verify', { headers: { 'x-admin-token': token } })
      .then(r => r.json())
      .then(res => {
        if (res.valid) {
          setRole('admin');
        } else {
          sessionStorage.removeItem('edgeai_admin_token');
          openAdminAuthModal();
        }
      })
      .catch(() => openAdminAuthModal());
  } else {
    openAdminAuthModal();
  }
}

function openAdminAuthModal() {
  const modal = document.getElementById('adminAuthModal');
  const input = document.getElementById('adminPasscodeInput');
  const err = document.getElementById('adminAuthError');
  if (err) err.classList.add('hidden');
  if (input) input.value = '';
  if (modal) modal.classList.remove('hidden');
  setTimeout(() => input?.focus(), 150);
}

function togglePasscodeVisibility() {
  const input = document.getElementById('adminPasscodeInput');
  const icon = document.getElementById('passcodeToggleIcon');
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    icon?.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    input.type = 'password';
    icon?.classList.replace('fa-eye-slash', 'fa-eye');
  }
}

async function handleAdminLogin(event) {
  event.preventDefault();
  const input = document.getElementById('adminPasscodeInput');
  const err = document.getElementById('adminAuthError');
  const errMsg = document.getElementById('adminAuthErrorMsg');
  const passcode = (input?.value || '').trim();

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ passcode })
    });
    const data = await res.json();

    if (res.ok && data.token) {
      sessionStorage.setItem('edgeai_admin_token', data.token);
      closeModal('adminAuthModal');
      setRole('admin');
      await fetchAllData();
      renderScores();
      showToast('เข้าสู่ระบบสิทธิ์ครูผู้สอน / ผู้ดูแลระบบสำเร็จ', 'success');
    } else {
      if (err) {
        if (errMsg) errMsg.textContent = data.message || 'รหัสผ่านไม่ถูกต้อง';
        err.classList.remove('hidden');
      }
      input?.focus();
      input?.select();
    }
  } catch (e) {
    if (err) {
      if (errMsg) errMsg.textContent = 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้';
      err.classList.remove('hidden');
    }
  }
}

async function logoutAdmin() {
  const token = sessionStorage.getItem('edgeai_admin_token');
  if (token) {
    fetch('/api/auth/logout', {
      method: 'POST',
      headers: { 'x-admin-token': token }
    }).catch(() => {});
  }
  sessionStorage.removeItem('edgeai_admin_token');
  setRole('student');
  initStudentProfile();
  await fetchAllData();
  renderScores();
  showToast('ล็อกสิทธิ์แอดมินแล้ว กลับสู่โหมดนักเรียน', 'info');
}

// ==============================================================
// 2.2 STUDENT AUTHENTICATION & PROFILE CONTROLLERS (ห้อง ม.5/12)
// ==============================================================
function initStudentProfile() {
  const savedUser = localStorage.getItem('edgeai_student_user');
  if (savedUser) {
    try {
      const student = JSON.parse(savedUser);
      if (student && student.student_id) {
        // อ้างอิงข้อมูลล่าสุดจาก state.students ที่ซิงค์มาจาก Google Sheet เสมอ
        const fresh = (state.students || []).find(s => s.student_id === student.student_id) || student;
        state.currentUser = {
          id: fresh.student_id,
          student_id: fresh.student_id,
          name: fresh.name,
          class_room: fresh.class_room || 'ม.5/12',
          role: 'student'
        };
        localStorage.setItem('edgeai_student_user', JSON.stringify(fresh));
        updateStudentNavUI(fresh);
        applyRoleUI();
        updateGuestNotices();
        return;
      }
    } catch (e) {
      console.error('Error parsing saved student profile:', e);
    }
  }

  // ไม่ได้เข้าสู่ระบบ: ให้แสดงปุ่ม "เข้าสู่ระบบนักเรียน" (ไม่ล็อกอินสุ่มคนแรกอัตโนมัติ)
  state.currentUser = null;
  updateStudentNavUI(null);
  applyRoleUI();
  updateGuestNotices();
}

function updateStudentNavUI(student) {
  const loginBtn = document.getElementById('studentLoginBtn');
  const loggedInInfo = document.getElementById('studentLoggedInInfo');
  const navId = document.getElementById('navStudentId');
  const navName = document.getElementById('navStudentName');
  const navClass = document.getElementById('navStudentClass');
  const logoutDropdownItem = document.getElementById('studentLogoutDropdownItem');

  if (student && student.student_id) {
    if (loginBtn) {
      loginBtn.classList.add('hidden');
      loginBtn.style.display = 'none';
    }
    if (loggedInInfo) {
      loggedInInfo.classList.remove('hidden');
      loggedInInfo.style.display = 'flex';
    }
    if (navId) navId.textContent = student.student_id;
    if (navName) navName.textContent = student.name;
    if (navClass) navClass.textContent = `ห้อง ${student.class_room || 'ม.5/12'}`;
    if (logoutDropdownItem) {
      logoutDropdownItem.classList.remove('hidden');
      logoutDropdownItem.style.display = 'block';
    }
  } else {
    if (loginBtn) {
      loginBtn.classList.remove('hidden');
      loginBtn.style.display = 'flex';
    }
    if (loggedInInfo) {
      loggedInInfo.classList.add('hidden');
      loggedInInfo.style.display = 'none';
    }
    if (logoutDropdownItem) {
      logoutDropdownItem.classList.add('hidden');
      logoutDropdownItem.style.display = 'none';
    }
  }
}

function openStudentLoginModal() {
  const modal = document.getElementById('studentLoginModal');
  const err = document.getElementById('studentAuthError');
  if (err) err.classList.add('hidden');

  if (modal) modal.classList.remove('hidden');
  const input = document.getElementById('studentLoginIdInput');
  setTimeout(() => input?.focus(), 150);
}

function onStudentIdInput(val) {
  const autoFill = document.getElementById('autoFillPasswordCheckbox')?.checked;
  if (autoFill) {
    const passInput = document.getElementById('studentLoginPassInput');
    if (passInput) passInput.value = val.trim();
  }
}

function toggleAutoFillPassword(checked) {
  if (checked) {
    const idVal = document.getElementById('studentLoginIdInput')?.value || '';
    const passInput = document.getElementById('studentLoginPassInput');
    if (passInput) passInput.value = idVal.trim();
  }
}

function toggleStudentPassVisibility() {
  const input = document.getElementById('studentLoginPassInput');
  const icon = document.getElementById('studentPassToggleIcon');
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    icon?.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    input.type = 'password';
    icon?.classList.replace('fa-eye-slash', 'fa-eye');
  }
}

async function handleStudentLogin(event) {
  event.preventDefault();
  const idInput = document.getElementById('studentLoginIdInput');
  const passInput = document.getElementById('studentLoginPassInput');
  const err = document.getElementById('studentAuthError');
  const errMsg = document.getElementById('studentAuthErrorMsg');

  const student_id = (idInput?.value || '').trim();
  const password = (passInput?.value || '').trim();

  try {
    const res = await fetch('/api/auth/student-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id, password })
    });
    const data = await res.json();

    if (res.ok && data.status === 'success') {
      localStorage.setItem('edgeai_student_user', JSON.stringify(data.student));
      if (data.token) sessionStorage.setItem('edgeai_student_token', data.token);

      state.currentUser = {
        id: data.student.student_id,
        student_id: data.student.student_id,
        name: data.student.name,
        class_room: data.student.class_room || 'ม.5/12',
        role: 'student'
      };

      sessionStorage.removeItem('edgeai_admin_token');
      updateStudentNavUI(data.student);
      closeModal('studentLoginModal');
      showToast(data.message || `ยินดีต้อนรับ ${data.student.name}`, 'success');
      setRole('student');
      await fetchAllData();
      applyRoleUI();
      renderPracticalTasks();
      renderWorksheets();
      renderScores();
      updateGuestNotices();
      switchTab('lessons');
    } else {
      if (err) {
        if (errMsg) errMsg.textContent = data.message || 'รหัสผ่านไม่ถูกต้อง (กำหนดให้ใช้รหัสนักเรียนเป็นทั้ง Username และ Password)';
        err.classList.remove('hidden');
      }
      passInput?.focus();
      passInput?.select();
    }
  } catch (e) {
    if (err) {
      if (errMsg) errMsg.textContent = 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้';
      err.classList.remove('hidden');
    }
  }
}

function logoutStudent() {
  localStorage.removeItem('edgeai_student_user');
  sessionStorage.removeItem('edgeai_student_token');
  state.currentUser = null;
  state.scores = [];
  state.submissions = [];
  updateStudentNavUI(null);
  applyRoleUI();
  renderPracticalTasks();
  renderWorksheets();
  renderScores();
  updateGuestNotices();
  document.getElementById('roleDropdown')?.classList.add('hidden');
  showToast('ออกจากระบบเรียบร้อยแล้ว (เข้าสู่โหมดผู้เข้าชมทั่วไป)', 'info');
}

async function syncGoogleSheetStudents() {
  showToast('กำลังดึงข้อมูลล่าสุดจาก Google Sheet...', 'info');
  try {
    const res = await fetch('/api/students/sync', { method: 'POST' });
    const json = await res.json();
    if (json.status === 'success') {
      state.students = json.data || [];
      await fetchAllData();
      populateDropdowns();
      if (state.currentUser && state.currentUser.student_id) {
        const fresh = state.students.find(s => s.student_id === state.currentUser.student_id);
        if (fresh) {
          state.currentUser.name = fresh.name;
          state.currentUser.class_room = fresh.class_room || 'ม.5/12';
          localStorage.setItem('edgeai_student_user', JSON.stringify(fresh));
          updateStudentNavUI(fresh);
        }
      }
      renderScores();
      renderAllViews();
      showToast(json.message || 'ซิงค์ข้อมูลนักเรียนสำเร็จ!', 'success');
    } else {
      showToast(json.message || 'ไม่สามารถติดต่อ Google Sheet ได้', 'warning');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์เพื่อซิงค์ข้อมูล', 'error');
  }
}

function setRoleToGuest() {
  document.getElementById('roleDropdown')?.classList.add('hidden');
  logoutStudent();
}

function onSelectStudentRole() {
  document.getElementById('roleDropdown')?.classList.add('hidden');
  if (!state.currentUser || !state.currentUser.student_id) {
    openStudentLoginModal();
  } else {
    setRole('student');
  }
}

function setRole(role) {
  if (role === 'admin') {
    const token = sessionStorage.getItem('edgeai_admin_token');
    if (!token) {
      requestAdminRole();
      return;
    }
  }
  state.currentRole = role;
  localStorage.setItem('edgeai_role', role);
  document.getElementById('roleDropdown')?.classList.add('hidden');
  applyRoleUI();
  renderAllViews();
  showToast(`สลับบทบาทสำเร็จ: ${role === 'admin' ? 'ครูผู้สอน / ผู้ดูแลระบบ (โหมดจัดการข้อมูล)' : 'นักเรียน (Student Mode)'}`, 'success');
}

function isLoggedIn() {
  const isStudent = !!(state.currentUser && state.currentUser.student_id);
  const isAdmin = (state.currentRole === 'admin' && !!sessionStorage.getItem('edgeai_admin_token'));
  return isStudent || isAdmin;
}

function updateGuestNotices() {
  const loggedIn = isLoggedIn();

  const wsNotice = document.getElementById('worksheetsGuestNotice');
  if (wsNotice) {
    if (!loggedIn) {
      wsNotice.classList.remove('hidden');
    } else {
      wsNotice.classList.add('hidden');
    }
  }

  const qzNotice = document.getElementById('quizzesGuestNotice');
  if (qzNotice) {
    if (!loggedIn) {
      qzNotice.classList.remove('hidden');
    } else {
      qzNotice.classList.add('hidden');
    }
  }

  const scoresGatekeeper = document.getElementById('scoresGatekeeperLock');
  const scoresContent = document.getElementById('scoresContentArea');
  if (scoresGatekeeper && scoresContent) {
    if (!loggedIn) {
      scoresGatekeeper.classList.remove('hidden');
      scoresContent.classList.add('hidden');
    } else {
      scoresGatekeeper.classList.add('hidden');
      scoresContent.classList.remove('hidden');
    }
  }
}

function applyRoleUI() {
  const roleBadge = document.getElementById('roleBadge');
  const roleText = document.getElementById('roleText');
  const adminBanner = document.getElementById('adminModeBanner');
  const adminTabBtn = document.getElementById('tabBtn-admin');
  const adminOnlyElements = document.querySelectorAll('.admin-only');

  const isAdmin = (state.currentRole === 'admin' && !!sessionStorage.getItem('edgeai_admin_token'));
  const isStudent = !!(state.currentUser && state.currentUser.student_id);

  if (isAdmin) {
    if (roleBadge) {
      roleBadge.className = 'hidden sm:flex items-center px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#fff200] text-[#173b6b] shadow border border-yellow-400';
      roleBadge.innerHTML = '<i class="fa-solid fa-chalkboard-user mr-1.5 text-[#173b6b]"></i>ครูผู้สอน / Admin';
    }
    if (adminBanner) {
      adminBanner.style.setProperty('display', 'block', 'important');
      adminBanner.classList.remove('hidden');
    }
    if (adminTabBtn) {
      adminTabBtn.style.setProperty('display', 'inline-flex', 'important');
      adminTabBtn.classList.remove('hidden');
    }
    adminOnlyElements.forEach(el => {
      el.style.setProperty('display', 'block', 'important');
      el.classList.remove('hidden');
    });
  } else if (isStudent) {
    if (roleBadge) {
      roleBadge.className = 'hidden sm:flex items-center px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#fff200] text-[#173b6b] shadow border border-yellow-400';
      roleBadge.innerHTML = `<i class="fa-solid fa-user-graduate mr-1.5 text-[#173b6b]"></i>นักเรียน: ${escapeHtml(state.currentUser.name)}`;
    }
    if (adminBanner) {
      adminBanner.style.setProperty('display', 'none', 'important');
      adminBanner.classList.add('hidden');
    }
    if (adminTabBtn) {
      adminTabBtn.style.setProperty('display', 'none', 'important');
      adminTabBtn.classList.add('hidden');
    }
    adminOnlyElements.forEach(el => {
      el.style.setProperty('display', 'none', 'important');
      el.classList.add('hidden');
    });
  } else {
    // Guest / Visitor
    if (roleBadge) {
      roleBadge.className = 'hidden sm:flex items-center px-3.5 py-1.5 rounded-full text-xs font-bold bg-white/15 text-white shadow border border-white/20';
      roleBadge.innerHTML = '<i class="fa-solid fa-globe mr-1.5 text-[#fff200]"></i>ผู้เข้าชมทั่วไป (Guest)';
    }
    if (adminBanner) {
      adminBanner.style.setProperty('display', 'none', 'important');
      adminBanner.classList.add('hidden');
    }
    if (adminTabBtn) {
      adminTabBtn.style.setProperty('display', 'none', 'important');
      adminTabBtn.classList.add('hidden');
    }
    adminOnlyElements.forEach(el => {
      el.style.setProperty('display', 'none', 'important');
      el.classList.add('hidden');
    });
  }

  // Update guest notice banners across tabs
  updateGuestNotices();

  // Security Kick-out: ถ้านักเรียนหรือ Guest อยู่หน้า Admin CMS ให้เด้งกลับไปหน้าบทเรียนทันที
  const adminSec = document.getElementById('section-admin');
  const activeTab = document.querySelector('.nav-tab.active');
  if (!isAdmin && ((activeTab && activeTab.id === 'tabBtn-admin') || (adminSec && !adminSec.classList.contains('hidden')))) {
    switchTab('lessons');
  }
}

// ==============================================================
// 2.5 HERO IMAGE CAROUSEL / SLIDER & ACCESSIBILITY CONTROLLERS
// ==============================================================
let currentSlide = 0;
let slideInterval = null;
const SLIDE_DURATION = 5000; // สลับสไลด์อัตโนมัติทุก 5 วินาที

function initSlider() {
  const track = document.getElementById('sliderTrack');
  const slides = document.querySelectorAll('.slide-item');
  const sliderContainer = document.getElementById('heroSliderSection');
  if (!track || slides.length === 0) return;

  // Touch Swipe Support สำหรับสมาร์ตโฟน/แท็บเล็ต
  let touchStartX = 0;
  let touchEndX = 0;

  if (sliderContainer) {
    // พักการสลับสไลด์เมื่อผู้ใช้นำเมาส์ชี้ (Pause on hover)
    sliderContainer.addEventListener('mouseenter', () => pauseAutoSlide());
    sliderContainer.addEventListener('mouseleave', () => startAutoSlide());

    sliderContainer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    sliderContainer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const swipeThreshold = 45;
      if (touchEndX < touchStartX - swipeThreshold) {
        nextSlide();
      } else if (touchEndX > touchStartX + swipeThreshold) {
        prevSlide();
      }
    }, { passive: true });
  }

  updateSliderUI();
  startAutoSlide();
}

function updateSliderUI() {
  const track = document.getElementById('sliderTrack');
  const slides = document.querySelectorAll('.slide-item');
  const dots = document.querySelectorAll('.slider-dot');
  if (!track || slides.length === 0) return;

  const total = slides.length;
  if (currentSlide < 0) currentSlide = total - 1;
  if (currentSlide >= total) currentSlide = 0;

  // เลื่อนตำแหน่งภาพแบนเนอร์แนวนอนอย่างราบรื่น
  track.style.transform = `translateX(-${currentSlide * 100}%)`;

  // อัปเดตจุด Indicator ให้สอดคล้องกับสไลด์ที่กำลังแสดง
  dots.forEach((dot, idx) => {
    if (idx === currentSlide) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
}

function nextSlide() {
  const slides = document.querySelectorAll('.slide-item');
  if (slides.length === 0) return;
  currentSlide = (currentSlide + 1) % slides.length;
  updateSliderUI();
  resetAutoSlide();
}

function prevSlide() {
  const slides = document.querySelectorAll('.slide-item');
  if (slides.length === 0) return;
  currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  updateSliderUI();
  resetAutoSlide();
}

function goToSlide(index) {
  currentSlide = index;
  updateSliderUI();
  resetAutoSlide();
}

function startAutoSlide() {
  if (slideInterval) clearInterval(slideInterval);
  slideInterval = setInterval(() => {
    const slides = document.querySelectorAll('.slide-item');
    if (slides.length === 0) return;
    currentSlide = (currentSlide + 1) % slides.length;
    updateSliderUI();
  }, SLIDE_DURATION);
}

function pauseAutoSlide() {
  if (slideInterval) {
    clearInterval(slideInterval);
    slideInterval = null;
  }
}

function resetAutoSlide() {
  pauseAutoSlide();
  startAutoSlide();
}

// ระบบปรับขนาดตัวอักษรเพื่อการเข้าถึง (Accessibility: Font Resizer A-, A, A+)
let currentFontSizeLevel = 0; // -1: 14px, 0: 16px, 1: 18px
function changeFontSize(delta) {
  const root = document.documentElement;
  currentFontSizeLevel = delta;

  if (delta === -1) {
    root.style.fontSize = '14px';
    showToast('ปรับขนาดตัวอักษร: กะทัดรัด (A-)', 'info');
  } else if (delta === 1) {
    root.style.fontSize = '18px';
    showToast('ปรับขนาดตัวอักษร: ขยายใหญ่ (A+)', 'info');
  } else {
    root.style.fontSize = '16px';
    showToast('ปรับขนาดตัวอักษร: ขนาดมาตรฐาน (A)', 'info');
  }
}

// ระบบสลับแบบอักษร (Google Noto Sans Thai / Prompt / สารบรรณ)
function setFontStyle(style) {
  applyFontStyle(style, true);
}

function applyFontStyle(style, notify = true) {
  const root = document.documentElement;
  root.classList.remove('font-style-noto', 'font-style-prompt', 'font-style-sarabun');
  root.classList.add(`font-style-${style}`);
  localStorage.setItem('edgeai_font_style', style);

  // อัปเดตสีปุ่มให้สอดคล้องกับฟอนต์ที่เลือก
  ['noto', 'prompt', 'sarabun'].forEach(s => {
    const btn = document.getElementById(`fontBtn-${s}`);
    if (btn) {
      if (s === style) {
        btn.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-[#fff200] text-[#173b6b] shadow transition';
      } else {
        btn.className = 'px-2 py-0.5 rounded text-[11px] text-slate-300 hover:text-white hover:bg-white/10 transition';
      }
    }
  });

  if (notify) {
    const fontNames = {
      noto: 'Google Noto Sans Thai (อ่านง่าย ชัดเจน สบายตา)',
      prompt: 'Prompt (โมเดิร์น ดีไซน์)',
      sarabun: 'สารบรรณ (ทางการมาตรฐาน)'
    };
    showToast(`เปลี่ยนแบบอักษร: ${fontNames[style] || style}`, 'info');
  }
}

function initFontStyle() {
  const saved = localStorage.getItem('edgeai_font_style') || 'noto';
  applyFontStyle(saved, false);
}

// ==============================================================
// 3. TAB NAVIGATION (depa THEME)
// ==============================================================
function switchTab(tabName) {
  // Strict RBAC Guard: ป้องกันไม่ให้นักเรียนเข้าถึงแท็บ Admin CMS
  if (tabName === 'admin' && state.currentRole !== 'admin') {
    showToast('การจัดการระบบต้องใช้สิทธิ์ครูผู้สอน / ผู้ดูแลระบบ (กรุณายืนยันรหัสผ่าน)', 'error');
    requestAdminRole();
    return;
  }

  document.querySelectorAll('.tab-section').forEach(s => s.classList.add('hidden'));
  document.querySelectorAll('.nav-tab').forEach(b => {
    b.classList.remove('active', 'text-[#fff200]', 'bg-[#173b6b]');
    b.classList.add('text-slate-200');
  });

  const targetSection = document.getElementById(`section-${tabName}`);
  const targetBtn = document.getElementById(`tabBtn-${tabName}`);

  if (targetSection) targetSection.classList.remove('hidden');
  if (targetBtn) {
    targetBtn.classList.add('active', 'text-[#fff200]', 'bg-[#173b6b]');
    targetBtn.classList.remove('text-slate-200');
  }

  // Refresh tab-specific dynamic states
  if (tabName === 'lessons') renderLessons();
  if (tabName === 'scores') renderScores();
  if (tabName === 'worksheets') { renderPracticalTasks(); renderWorksheets(); }
  updateGuestNotices();

  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==============================================================
// 4. LESSONS VIEW & CRUD (depa STYLE)
// ==============================================================
function renderLessons() {
  const container = document.getElementById('lessonsGrid');
  if (!container) return;

  if (!state.lessons || state.lessons.length === 0) {
    container.innerHTML = `<div class="col-span-3 text-center py-12 text-slate-400">ไม่พบข้อมูลบทเรียน</div>`;
    return;
  }

  container.innerHTML = state.lessons.map(lesson => {
    const descText = lesson.description || lesson.summary || 'ไม่มีคำอธิบาย';
    return `
      <div class="lesson-card bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col justify-between">
        <div class="p-6">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-bold px-3 py-1 rounded-full bg-[#173b6b]/10 text-[#173b6b] border border-[#173b6b]/20">
              บทที่ ${lesson.chapter_number}
            </span>
            <span class="text-xs text-slate-400 flex items-center gap-1 font-mono">
              <i class="fa-regular fa-clock"></i> ${lesson.duration_hours || 3} คาบ
            </span>
          </div>
          <h3 class="text-base font-bold text-slate-900 leading-snug hover:text-[#173b6b] cursor-pointer" onclick="viewLessonDetails('${lesson.id}')">
            ${lesson.title}
          </h3>
          <p class="text-xs text-slate-500 font-mono mt-1">${lesson.title_en || ''}</p>
          <p class="text-xs text-slate-600 mt-3 line-clamp-3 leading-relaxed">
            ${descText}
          </p>
        </div>

        <div class="bg-slate-50 px-6 py-3.5 border-t border-slate-100 flex items-center justify-between">
          <div class="flex items-center gap-2">
            ${[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].includes(lesson.chapter_number) ? `
              <a href="chapter${String(lesson.chapter_number).padStart(2, '0')}.html" class="btn-depa-yellow text-xs font-bold px-3 py-1.5 rounded-lg inline-flex items-center gap-1.5 shadow-sm whitespace-nowrap flex-shrink-0">
                <i class="fa-solid fa-book-open"></i> เข้าเรียนฉบับเต็ม
              </a>
              <button onclick="viewLessonDetails('${lesson.id}')" class="text-xs text-slate-500 hover:text-[#173b6b] flex items-center gap-1" title="ดูสรุปสังเขป">
                <i class="fa-solid fa-circle-info"></i> สังเขป
              </button>
            ` : `
              <button onclick="viewLessonDetails('${lesson.id}')" class="text-xs font-bold text-[#173b6b] hover:text-[#0d2342] flex items-center gap-1.5">
                <i class="fa-solid fa-circle-play text-red-600"></i> เข้าเรียน / ดูเนื้อหา
              </button>
            `}
          </div>
          
          ${state.currentRole === 'admin' ? `
            <div class="flex space-x-1">
              <button onclick="prepareEditLesson('${lesson.id}')" class="p-1.5 text-xs text-[#173b6b] hover:bg-blue-50 rounded" title="แก้ไข">
                <i class="fa-solid fa-pen-to-square"></i>
              </button>
              <button onclick="deleteLesson('${lesson.id}')" class="p-1.5 text-xs text-red-600 hover:bg-red-50 rounded" title="ลบ">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function viewLessonDetails(id) {
  const lesson = state.lessons.find(l => l.id === id);
  if (!lesson) return;

  document.getElementById('viewLessonBadge').textContent = `บทที่ ${lesson.chapter_number}`;
  document.getElementById('viewLessonTitle').textContent = lesson.title;
  document.getElementById('viewLessonDesc').textContent = lesson.description || lesson.summary || 'ไม่มีคำอธิบาย';
  document.getElementById('viewLessonCodeFile').textContent = lesson.code_filename || 'main.py';

  // Objectives
  const objList = document.getElementById('viewLessonObjectives');
  const objs = Array.isArray(lesson.objectives) ? lesson.objectives : [];
  objList.innerHTML = objs.map(o => `<li>${o}</li>`).join('') || '<li>ศึกษาเนื้อหาตามมาตรฐานรายวิชา</li>';

  // Video & Slide Links
  const videoBtn = document.getElementById('viewLessonVideoLink');
  videoBtn.href = lesson.video_url || 'https://youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU';
  videoBtn.onclick = (e) => {
    if (window.openChapterVideoModal) {
      e.preventDefault();
      closeModal('lessonViewerModal');
      window.openChapterVideoModal(lesson.chapter_number);
    }
  };

  const slideBtn = document.getElementById('viewLessonSlideLink');
  slideBtn.href = lesson.slide_url || 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu';

  // Multiple Video Episodes
  const epBox = document.getElementById('viewLessonEpisodesContainer');
  const epList = document.getElementById('viewLessonEpisodesList');
  if (epBox && epList) {
    const eps = lesson.video_episodes || (window.CHAPTER_VIDEOS && window.CHAPTER_VIDEOS[lesson.chapter_number] && window.CHAPTER_VIDEOS[lesson.chapter_number].episodes);
    if (eps && eps.length > 1) {
      epBox.classList.remove('hidden');
      epList.innerHTML = eps.map(e => {
        const targetId = e.id || e.video_url || e.ep;
        const targetUrl = e.video_url || (e.id ? 'https://www.youtube.com/watch?v=' + e.id : '');
        return `
          <button type="button" onclick="closeModal('lessonViewerModal'); if(window.openChapterVideoModal) window.openChapterVideoModal(${lesson.chapter_number}, '${targetId}'); else window.open('${targetUrl}', '_blank');" class="px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 hover:border-red-400 hover:bg-red-50 text-slate-700 hover:text-red-700 font-semibold text-xs flex items-center gap-1.5 transition shadow-sm cursor-pointer">
            <i class="fa-brands fa-youtube text-red-600"></i>
            <span><strong>${e.ep}</strong>: ${e.label || e.title}</span>
          </button>
        `;
      }).join('');
    } else {
      epBox.classList.add('hidden');
      epList.innerHTML = '';
    }
  }

  // Dedicated Page Link
  const dedicatedBtn = document.getElementById('viewDedicatedLessonPageBtn');
  if (dedicatedBtn) {
    if ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].includes(lesson.chapter_number)) {
      dedicatedBtn.href = `chapter${String(lesson.chapter_number).padStart(2, '0')}.html`;
      dedicatedBtn.classList.remove('hidden');
    } else {
      dedicatedBtn.classList.add('hidden');
    }
  }

  // Store for modal start exam
  document.getElementById('lessonViewerModal').setAttribute('data-chapter-id', lesson.id);

  openModal('lessonViewerModal');
}

function startLessonExamFromModal() {
  if (!isLoggedIn()) {
    closeModal('lessonViewerModal');
    showToast('กรุณาเข้าสู่ระบบนักเรียนก่อนเริ่มทำแบบทดสอบเพื่อบันทึกคะแนน', 'warning');
    openStudentLoginModal();
    return;
  }
  const chId = document.getElementById('lessonViewerModal').getAttribute('data-chapter-id');
  closeModal('lessonViewerModal');
  switchTab('quizzes');
  const select = document.getElementById('examChapterSelect');
  if (select) select.value = chId;
  startChapterExam();
}

function prepareCreateLesson() {
  document.getElementById('lessonModalTitle').textContent = 'เพิ่มบทเรียนใหม่';
  document.getElementById('lessonFormId').value = '';
  document.getElementById('lessonFormChapter').value = (state.lessons.length > 0 ? Math.max(...state.lessons.map(l => l.chapter_number || 0)) : 0) + 1;
  document.getElementById('lessonFormTitle').value = '';
  document.getElementById('lessonFormTitleEn').value = '';
  document.getElementById('lessonFormDesc').value = '';
  document.getElementById('lessonFormObjectives').value = '';
  document.getElementById('lessonFormVideo').value = 'https://youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU';
  document.getElementById('lessonFormSlide').value = 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu';
  openModal('lessonModal');
}

function prepareEditLesson(id) {
  const lesson = state.lessons.find(l => l.id === id);
  if (!lesson) return;

  document.getElementById('lessonModalTitle').textContent = `แก้ไขบทเรียนที่ ${lesson.chapter_number}`;
  document.getElementById('lessonFormId').value = lesson.id;
  document.getElementById('lessonFormChapter').value = lesson.chapter_number;
  document.getElementById('lessonFormTitle').value = lesson.title;
  document.getElementById('lessonFormTitleEn').value = lesson.title_en || '';
  document.getElementById('lessonFormDesc').value = lesson.description || '';
  document.getElementById('lessonFormObjectives').value = Array.isArray(lesson.objectives) ? lesson.objectives.join('\n') : '';
  document.getElementById('lessonFormVideo').value = lesson.video_url || '';
  document.getElementById('lessonFormSlide').value = lesson.slide_url || '';

  openModal('lessonModal');
}

async function handleSaveLesson(e) {
  e.preventDefault();
  const id = document.getElementById('lessonFormId').value;
  const payload = {
    chapter_number: parseInt(document.getElementById('lessonFormChapter').value, 10),
    title: document.getElementById('lessonFormTitle').value.trim(),
    title_en: document.getElementById('lessonFormTitleEn').value.trim(),
    description: document.getElementById('lessonFormDesc').value.trim(),
    objectives: document.getElementById('lessonFormObjectives').value.split('\n').map(s => s.trim()).filter(Boolean),
    video_url: document.getElementById('lessonFormVideo').value.trim(),
    slide_url: document.getElementById('lessonFormSlide').value.trim()
  };

  try {
    let res;
    if (id) {
      res = await fetch(`/api/lessons/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    } else {
      res = await fetch('/api/lessons', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    }

    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      closeModal('lessonModal');
      await fetchAllData();
      renderAllViews();
    } else {
      showToast(json.message || 'บันทึกไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์', 'error');
  }
}

async function deleteLesson(id) {
  if (!confirm(`ยืนยันการลบบทเรียนนี้หรือไม่? ข้อมูลจะถูกลบออกจากระบบทันที`)) return;

  try {
    const res = await fetch(`/api/lessons/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      await fetchAllData();
      renderAllViews();
    } else {
      showToast(json.message || 'ลบไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการลบ', 'error');
  }
}

// ==============================================================
// 5. WORKSHEETS & PRACTICAL TASKS
// ==============================================================
function setWorksheetFilter(filter) {
  state.worksheetFilter = filter;
  const buttons = document.querySelectorAll('.ws-filter-btn');
  buttons.forEach(b => {
    if (b.dataset.filter === filter) {
      b.classList.remove('bg-slate-100', 'text-slate-700', 'border-slate-200');
      b.classList.add('bg-[#173b6b]', 'text-white', 'border-[#173b6b]', 'active');
    } else {
      b.classList.remove('bg-[#173b6b]', 'text-white', 'border-[#173b6b]', 'active');
      b.classList.add('bg-slate-100', 'text-slate-700', 'border-slate-200');
    }
  });
  renderPracticalTasks();
  renderWorksheets();
}

function handleWorksheetSearch() {
  const input = document.getElementById('worksheetSearchInput');
  state.worksheetSearch = input ? input.value : '';
  renderPracticalTasks();
  renderWorksheets();
}

function renderPracticalTasks() {
  const container = document.getElementById('practicalList');
  if (!container) return;

  const filter = state.worksheetFilter || 'all';
  const search = (state.worksheetSearch || '').trim().toLowerCase();

  const filtered = state.practicalExams.filter(p => {
    const u = parseInt(p.unit_number);
    let matchModule = true;
    if (filter === 'part1') matchModule = (u >= 1 && u <= 4);
    else if (filter === 'part2') matchModule = (u >= 5 && u <= 10);
    else if (filter === 'part3') matchModule = (u >= 11 && u <= 12);
    if (!matchModule) return false;

    if (search) {
      const rubricsText = formatRubricsText(p.rubrics);
      const text = `${p.title} ${p.scenario || p.description || ''} ${rubricsText} ${p.code_reference || ''} บทที่ ${p.unit_number}`.toLowerCase();
      if (!text.includes(search)) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="bg-white p-8 rounded-2xl border border-slate-200 text-center text-slate-500 text-xs">
        <i class="fa-solid fa-magnifying-glass text-2xl text-slate-300 mb-2"></i>
        <div>ไม่พบโจทย์ปฏิบัติการที่ตรงกับคำค้นหาหรือหมวดหมู่ที่เลือก</div>
      </div>
    `;
    return;
  }

  const currentStudentId = state.currentUser ? state.currentUser.student_id : null;

  container.innerHTML = filtered.map(p => {
    const chNum = p.unit_number;
    const chFile = `chapter${String(chNum).padStart(2, '0')}.html`;

    // Status check for student (Separated for Practical Task)
    const myScore = currentStudentId ? (state.scores || []).find(s => s.student_id === currentStudentId && s.target_id === p.id && s.exam_category === 'practical') : null;
    const mySub = currentStudentId ? (state.submissions || []).find(s => s.student_id === currentStudentId && s.chapter_id === p.chapter_id && (s.task_type || 'practical') === 'practical') : null;

    let statusBadge = '';
    if (myScore) {
      statusBadge = `
        <div class="flex items-center gap-1.5">
          <span class="text-xs bg-emerald-100 text-emerald-800 border border-emerald-300 px-3 py-1 rounded-full font-bold flex items-center gap-1.5 shadow-sm">
            <i class="fa-solid fa-circle-check text-emerald-600"></i> ประเมินแล้ว: ${myScore.score}/10 คะแนน (${myScore.percentage}%)
          </span>
          ${mySub ? `
          <button onclick="openStudentSubmissionModal('${p.chapter_id}', 'โจทย์ปฏิบัติการบทที่ ${p.unit_number}', 'practical')" class="text-[11px] text-[#173b6b] hover:underline flex items-center gap-1 font-semibold bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded-md transition" title="คลิกเพื่อดูหรืออัปเดตลิงก์รายงานโจทย์ปฏิบัติ">
            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> รายงานโจทย์ปฏิบัติ
          </button>
          ` : ''}
        </div>
      `;
    } else if (mySub) {
      statusBadge = `
        <button onclick="openStudentSubmissionModal('${p.chapter_id}', 'โจทย์ปฏิบัติการบทที่ ${p.unit_number}', 'practical')" class="text-xs bg-blue-100 hover:bg-blue-200 text-blue-900 border border-blue-300 px-3 py-1 rounded-full font-bold flex items-center gap-1.5 shadow-sm transition" title="คลิกเพื่อดูหรืออัปเดตลิงก์รายงานโจทย์ปฏิบัติ">
          <i class="fa-solid fa-clock text-blue-600"></i> ส่งรายงานโจทย์ปฏิบัติแล้ว (รอตรวจ)
        </button>
      `;
    } else if (currentStudentId && state.currentRole === 'student') {
      statusBadge = `
        <button onclick="openStudentSubmissionModal('${p.chapter_id}', 'โจทย์ปฏิบัติการบทที่ ${p.unit_number}', 'practical')" class="text-xs bg-yellow-100 hover:bg-yellow-200 text-[#173b6b] border border-yellow-300 px-3 py-1 rounded-full font-bold flex items-center gap-1.5 transition shadow-sm">
          <i class="fa-solid fa-cloud-arrow-up text-amber-600"></i> ส่งงานโจทย์ปฏิบัติ
        </button>
      `;
    } else if (state.currentRole === 'admin') {
      statusBadge = `
        <button onclick="quickGradePractical('${p.id}')" class="text-xs btn-depa-blue px-3 py-1 rounded-full font-bold flex items-center gap-1.5 transition shadow-sm hover:scale-105">
          <i class="fa-solid fa-clipboard-check text-yellow-300"></i> ตรวจให้คะแนนรูบริก
        </button>
      `;
    } else {
      statusBadge = `
        <button onclick="openStudentLoginModal()" class="text-xs bg-slate-100 hover:bg-yellow-100 text-[#173b6b] border border-slate-300 px-3 py-1 rounded-full font-bold flex items-center gap-1.5 transition shadow-sm" title="เข้าสู่ระบบนักเรียนเพื่อส่งรายงานโจทย์ปฏิบัติ">
          <i class="fa-solid fa-lock text-amber-600"></i> เข้าสู่ระบบเพื่อส่งงาน
        </button>
      `;
    }

    const rubricsDisplay = formatRubricsText(p.rubrics);

    return `
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 hover:border-[#173b6b] transition">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-3 py-1 rounded-full bg-yellow-100 text-[#173b6b] border border-yellow-300">
              โจทย์ปฏิบัติการบทที่ ${p.unit_number}
            </span>
            ${statusBadge}
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-slate-500 font-mono">คะแนนเต็ม ${p.max_score || 10} คะแนน</span>
            <a href="${chFile}" class="text-xs text-[#173b6b] hover:text-blue-700 font-bold flex items-center gap-1 bg-slate-100 hover:bg-yellow-100 px-2.5 py-1 rounded-lg transition" title="เปิดดูเนื้อหาบทเรียนที่เกี่ยวข้อง">
              <i class="fa-solid fa-book-open"></i> บทเรียน
            </a>
          </div>
        </div>
        <h3 class="text-base font-bold text-slate-900">${p.title}</h3>
        <div class="mt-3 text-xs text-slate-700 bg-slate-50 p-4 rounded-xl leading-relaxed whitespace-pre-line border border-slate-200">
          <strong>สถานการณ์และภารกิจการปฏิบัติ:</strong>\n${p.scenario || p.description || 'ให้นักเรียนปฏิบัติการตามขั้นตอน'}
        </div>
        <div class="mt-3 text-xs text-slate-600 leading-relaxed whitespace-pre-line bg-yellow-50/50 p-3.5 rounded-xl border border-yellow-200/60">
          <strong class="text-[#173b6b]"><i class="fa-solid fa-list-check mr-1 text-yellow-600"></i>เกณฑ์การให้คะแนนรูบริก (Rubrics):</strong>\n${rubricsDisplay || 'ประเมินความถูกต้องตามเกณฑ์มาตรฐาน'}
        </div>
        ${p.code_reference ? `
        <div class="mt-3 pt-2.5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-500 font-mono">
          <div class="flex items-center gap-2">
            <button onclick="openCodeViewerModal('${p.code_reference}', 'บทที่ ${p.unit_number}: ${escapeHtml(p.title)}')" class="text-blue-600 hover:text-blue-800 font-bold flex items-center gap-1 bg-blue-50 hover:bg-blue-100 px-2.5 py-1 rounded-lg border border-blue-200 transition">
              <i class="fa-solid fa-code"></i> พรีวิวโค้ดสคริปต์ (${p.code_reference.split('/').pop()})
            </button>
            <a href="/${p.code_reference}" download class="text-slate-400 hover:text-slate-700 p-1" title="ดาวน์โหลดไฟล์ .py โดยตรง">
              <i class="fa-solid fa-download"></i>
            </a>
          </div>
          <span class="text-slate-400">บทที่ ${p.unit_number}</span>
        </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function renderWorksheets() {
  const container = document.getElementById('worksheetsList');
  if (!container) return;

  const filter = state.worksheetFilter || 'all';
  const search = (state.worksheetSearch || '').trim().toLowerCase();

  const filtered = state.worksheets.filter(w => {
    const u = parseInt(w.chapter_number);
    let matchModule = true;
    if (filter === 'part1') matchModule = (u >= 1 && u <= 4);
    else if (filter === 'part2') matchModule = (u >= 5 && u <= 10);
    else if (filter === 'part3') matchModule = (u >= 11 && u <= 12);
    if (!matchModule) return false;

    if (search) {
      const text = `${w.title} ${w.instructions} ${w.code_reference} บทที่ ${w.chapter_number}`.toLowerCase();
      if (!text.includes(search)) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="p-6 text-center text-slate-400 text-xs">
        ไม่พบใบงานที่ตรงกับเงื่อนไข
      </div>
    `;
    return;
  }

  const currentStudentId = state.currentUser ? state.currentUser.student_id : null;

  container.innerHTML = filtered.map(w => {
    const chNum = w.chapter_number;
    const chNumStr = String(chNum).padStart(2, '0');
    const chFile = `chapter${chNumStr}.html`;
    const pdfUrl = w.file_url || `/worksheets/Lab_Worksheet_${chNumStr}.pdf`;
    const viewUrl = w.view_url || `/worksheets/worksheet${chNumStr}.html`;
    const pdfName = w.file_name || `Lab_Worksheet_${chNumStr}.pdf`;

    const mySub = currentStudentId ? (state.submissions || []).find(s => s.student_id === currentStudentId && s.chapter_id === w.chapter_id && s.task_type === 'worksheet') : null;
    const myScore = currentStudentId ? (state.scores || []).find(s => s.student_id === currentStudentId && (s.target_id === w.id || s.chapter_id === w.chapter_id || s.target_id === w.chapter_id) && s.exam_category === 'worksheet') : null;

    return `
      <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2.5 hover:bg-yellow-50/40 hover:border-yellow-300 transition">
        <div class="flex items-start justify-between gap-2">
          <div class="flex items-center space-x-2.5">
            <span class="w-8 h-8 rounded-lg bg-red-100 text-red-600 flex items-center justify-center flex-shrink-0 font-bold text-xs shadow-sm">
              <i class="fa-solid fa-file-pdf text-sm"></i>
            </span>
            <div>
              <div class="text-xs font-bold text-slate-900 leading-snug">${w.title}</div>
              <div class="text-[11px] text-slate-500 font-mono mt-0.5">ระยะเวลา: ${w.time_minutes} นาที • บทที่ ${w.chapter_number}</div>
            </div>
          </div>
          <div class="flex items-center gap-1.5 flex-shrink-0">
            <a href="${pdfUrl}" download="${pdfName}" class="text-xs btn-depa-blue px-3 py-1.5 rounded-lg font-bold shadow-sm whitespace-nowrap flex items-center gap-1" title="ดาวน์โหลดไฟล์ใบงาน PDF ตรงตามบทเรียน">
              <i class="fa-solid fa-download text-[10px]"></i> ดาวน์โหลด
            </a>
            <a href="${viewUrl}" target="_blank" class="text-xs bg-white hover:bg-yellow-100 text-[#173b6b] border border-slate-300 px-2.5 py-1.5 rounded-lg font-bold shadow-sm whitespace-nowrap flex items-center gap-1" title="เปิดดูใบงานฉบับเต็ม / สั่งพิมพ์ A4">
              <i class="fa-solid fa-print text-[10px]"></i> พิมพ์
            </a>
          </div>
        </div>
        ${w.instructions ? `
        <div class="text-[11px] text-slate-600 bg-white p-2.5 rounded-xl border border-slate-200/80 leading-relaxed">
          <i class="fa-solid fa-circle-info text-blue-600 mr-1"></i> ${w.instructions}
        </div>
        ` : ''}
        <div class="flex flex-wrap items-center justify-between gap-2 text-[11px] pt-1 border-t border-slate-200/60">
          <div class="flex flex-wrap items-center gap-2">
            <a href="${chFile}" class="text-[#173b6b] hover:text-blue-700 font-bold flex items-center gap-1">
              <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> ไปยังคู่มือบทเรียน
            </a>
            ${currentStudentId && state.currentRole === 'student' ? (
              myScore ? `
                <span class="text-xs bg-emerald-100 text-emerald-800 border border-emerald-300 px-2.5 py-0.5 rounded-full font-bold flex items-center gap-1 shadow-sm">
                  <i class="fa-solid fa-circle-check text-emerald-600"></i> ประเมินใบงานแล้ว: ${myScore.score}/10 คะแนน (${myScore.percentage}%)
                </span>
                ${mySub ? `
                <button onclick="openStudentSubmissionModal('${w.chapter_id}', '${escapeHtml(w.title)}', 'worksheet')" class="text-[11px] text-[#173b6b] hover:underline flex items-center gap-1 font-semibold bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded-md transition" title="คลิกเพื่อดูหรืออัปเดตลิงก์ใบงานที่ส่ง">
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> ใบงานที่ส่ง
                </button>
                ` : ''}
              ` : (
                mySub ? `
                  <button onclick="openStudentSubmissionModal('${w.chapter_id}', '${escapeHtml(w.title)}', 'worksheet')" class="text-xs bg-indigo-100 hover:bg-indigo-200 text-indigo-900 border border-indigo-300 px-2.5 py-0.5 rounded-full font-bold flex items-center gap-1 shadow-sm transition" title="คลิกเพื่อดูหรืออัปเดตลิงก์ใบงานที่ส่ง">
                    <i class="fa-solid fa-clock text-indigo-600"></i> ส่งใบงานแล้ว (รอตรวจ)
                  </button>
                ` : `
                  <button onclick="openStudentSubmissionModal('${w.chapter_id}', '${escapeHtml(w.title)}', 'worksheet')" class="text-xs bg-yellow-100 hover:bg-yellow-200 text-[#173b6b] border border-yellow-300 px-2.5 py-0.5 rounded-full font-bold flex items-center gap-1 transition shadow-sm">
                    <i class="fa-solid fa-cloud-arrow-up text-amber-600"></i> ส่งใบงานปฏิบัติการ
                  </button>
                `
              )
            ) : (state.currentRole !== 'admin' ? `
              <button onclick="openStudentLoginModal()" class="text-xs bg-slate-100 hover:bg-yellow-100 text-[#173b6b] border border-slate-300 px-2.5 py-0.5 rounded-full font-bold flex items-center gap-1 transition shadow-sm" title="เข้าสู่ระบบนักเรียนเพื่อส่งใบงาน">
                <i class="fa-solid fa-lock text-amber-600"></i> เข้าสู่ระบบเพื่อส่งใบงาน
              </button>
            ` : '')}
            ${state.currentRole === 'admin' ? `
            <button onclick="quickGradeWorksheetByChapter('${w.chapter_id}')" class="text-xs bg-[#173b6b] hover:bg-[#122e53] text-[#fff200] px-2.5 py-0.5 rounded-md font-bold flex items-center gap-1 shadow-sm transition">
              <i class="fa-solid fa-file-signature"></i> ตรวจคะแนนใบงาน
            </button>
            <button onclick="quickGradePracticalByChapter('${w.chapter_id}')" class="text-xs text-blue-700 hover:text-blue-900 font-bold flex items-center gap-1 bg-blue-50 hover:bg-blue-100 px-2 py-0.5 rounded border border-blue-200">
              <i class="fa-solid fa-clipboard-check text-emerald-600"></i> ตรวจรูบริกโจทย์
            </button>
            ` : ''}
          </div>
          ${w.code_reference ? `
          <button onclick="openCodeViewerModal('${w.code_reference}', '${escapeHtml(w.title)}')" class="text-slate-500 hover:text-slate-800 font-mono text-[10px] flex items-center gap-1">
            <i class="fa-solid fa-code"></i> โค้ดตัวอย่าง
          </button>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

// Interactive Code Viewer Modal
async function openCodeViewerModal(codePath, title) {
  const modal = document.getElementById('codePreviewModal');
  const titleEl = document.getElementById('codeModalTitle');
  const contentEl = document.getElementById('codeModalContent');
  const downloadLink = document.getElementById('codeModalDownloadLink');
  const metaEl = document.getElementById('codeModalMeta');

  if (!modal) return;
  modal.classList.remove('hidden');

  const filename = codePath.split('/').pop() || 'script.py';
  if (titleEl) titleEl.textContent = filename;
  if (downloadLink) {
    downloadLink.href = '/' + codePath;
    downloadLink.download = filename;
  }
  if (metaEl) metaEl.innerHTML = `<i class="fa-solid fa-code text-blue-400 mr-1"></i> ${escapeHtml(title || codePath)}`;
  if (contentEl) contentEl.textContent = 'กำลังโหลดเนื้อหาโค้ดจากระบบ...';

  try {
    const res = await fetch('/' + codePath);
    if (!res.ok) throw new Error('File not found');
    const text = await res.text();
    const lines = text.split('\n');
    const numbered = lines.map((line, idx) => {
      const lineNum = String(idx + 1).padStart(3, ' ');
      return `<span class="text-slate-500 select-none mr-3">${lineNum} |</span>${escapeHtml(line)}`;
    }).join('\n');
    if (contentEl) {
      contentEl.innerHTML = `<pre class="font-mono text-xs leading-relaxed whitespace-pre">${numbered}</pre>`;
      contentEl.dataset.rawCode = text;
    }
  } catch (err) {
    if (contentEl) contentEl.innerHTML = `<div class="text-red-400 p-4"><i class="fa-solid fa-triangle-exclamation mr-1"></i> ไม่สามารถโหลดไฟล์โค้ดได้ (${err.message})</div>`;
  }
}

function copyCodeFromModal() {
  const contentEl = document.getElementById('codeModalContent');
  const rawCode = contentEl ? contentEl.dataset.rawCode : null;
  const btn = document.getElementById('copyCodeBtn');

  if (!rawCode) return;
  navigator.clipboard.writeText(rawCode).then(() => {
    if (btn) {
      btn.innerHTML = '<i class="fa-solid fa-check text-green-400"></i> คัดลอกสำเร็จ!';
      setTimeout(() => {
        btn.innerHTML = '<i class="fa-solid fa-copy"></i> คัดลอกโค้ด';
      }, 2000);
    }
    showToast('คัดลอกโค้ดลงคลิปบอร์ดแล้ว', 'success');
  }).catch(() => {
    showToast('ไม่สามารถคัดลอกได้', 'error');
  });
}

// Student Submission Modal (Separated between Practical Task and Lab Worksheet)
function openStudentSubmissionModal(chapterId, displayTitle, taskType = 'practical') {
  const modal = document.getElementById('studentSubmissionModal');
  const chInput = document.getElementById('submissionChapterId');
  const typeInput = document.getElementById('submissionTaskType');
  const modalTitle = document.getElementById('submissionModalTitle');
  const taskTypeBadge = document.getElementById('submissionTaskTypeBadge');
  const chDisplay = document.getElementById('submissionChapterDisplay');
  const stdDisplay = document.getElementById('submissionStudentDisplay');
  const urlLabel = document.getElementById('submissionUrlLabel');
  const reportInput = document.getElementById('submissionReportUrl');
  const urlHint = document.getElementById('submissionUrlHint');
  const notesLabel = document.getElementById('submissionNotesLabel');
  const notesInput = document.getElementById('submissionNotes');

  if (!modal) return;

  const user = state.currentUser;
  if (!user || user.role === 'admin' || !user.student_id) {
    showToast('กรุณาเข้าสู่ระบบในบทบาทนักเรียนเพื่อส่งงาน', 'info');
    openStudentLoginModal();
    return;
  }

  const effectiveTaskType = taskType === 'worksheet' ? 'worksheet' : 'practical';
  if (chInput) chInput.value = chapterId;
  if (typeInput) typeInput.value = effectiveTaskType;
  if (chDisplay) chDisplay.textContent = displayTitle || chapterId;
  if (stdDisplay) stdDisplay.textContent = `${user.student_id} - ${user.name} (${user.class_room || 'ม.5/12'})`;

  if (effectiveTaskType === 'worksheet') {
    if (modalTitle) modalTitle.textContent = 'ส่งใบงานปฏิบัติการประจำบท (Lab Worksheet)';
    if (taskTypeBadge) {
      taskTypeBadge.className = 'text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-800 border border-indigo-300';
      taskTypeBadge.innerHTML = '<i class="fa-solid fa-file-lines mr-1 text-indigo-600"></i> ใบงานประจำบท';
    }
    if (urlLabel) urlLabel.textContent = 'ลิงก์เอกสารใบงานปฏิบัติการ (Google Drive / PDF / รูปถ่ายใบงาน):';
    if (reportInput) reportInput.placeholder = 'https://drive.google.com/... (ไฟล์ PDF หรือ โฟลเดอร์รูปใบงาน)';
    if (urlHint) urlHint.textContent = '* สำหรับส่งไฟล์ใบงาน PDF หรือรูปถ่ายใบงานที่นักเรียนตอบคำถามคิดวิเคราะห์ครบถ้วน';
    if (notesLabel) notesLabel.textContent = 'บันทึกสรุปเนื้อหาใบงาน / ข้อความถึงครูผู้สอน (Notes):';
  } else {
    if (modalTitle) modalTitle.textContent = 'ส่งรายงานโจทย์ข้อสอบปฏิบัติ (Practical Exam)';
    if (taskTypeBadge) {
      taskTypeBadge.className = 'text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-300';
      taskTypeBadge.innerHTML = '<i class="fa-solid fa-microchip mr-1 text-amber-600"></i> โจทย์ข้อสอบปฏิบัติ (เต็ม 10 คะแนน)';
    }
    if (urlLabel) urlLabel.textContent = 'ลิงก์รายงานผลการปฏิบัติการ / โค้ด GitHub / Google Drive:';
    if (reportInput) reportInput.placeholder = 'https://drive.google.com/... หรือ https://github.com/...';
    if (urlHint) urlHint.textContent = '* กรุณาเปิดสิทธิ์ลิงก์ Google Drive ให้เป็น "ทุกคนที่มีลิงก์สามารถดูได้"';
    if (notesLabel) notesLabel.textContent = 'บันทึกสรุปผลการรันคำสั่งและข้อค้นพบสำคัญ (Key Findings):';
  }

  const existing = (state.submissions || []).find(s => 
    s.student_id === user.student_id && 
    s.chapter_id === chapterId && 
    (s.task_type || 'practical') === effectiveTaskType
  );

  if (existing) {
    if (reportInput) reportInput.value = existing.report_url || '';
    if (notesInput) notesInput.value = existing.notes || '';
  } else {
    if (reportInput) reportInput.value = '';
    if (notesInput) notesInput.value = '';
  }

  modal.classList.remove('hidden');
}

async function handleStudentSubmitLab(e) {
  e.preventDefault();
  const chapter_id = document.getElementById('submissionChapterId').value;
  const task_type = document.getElementById('submissionTaskType')?.value || 'practical';
  const report_url = document.getElementById('submissionReportUrl').value;
  const notes = document.getElementById('submissionNotes').value;

  const user = state.currentUser;
  if (!user || !user.student_id) {
    showToast('กรุณาเข้าสู่ระบบก่อนส่งงาน', 'error');
    return;
  }

  const submitBtn = e.target.querySelector('button[type="submit"]') || document.getElementById('btnSubmitLab');
  let originalBtnHtml = '';
  if (submitBtn) {
    originalBtnHtml = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>กำลังบันทึกข้อมูล...';
  }

  try {
    const res = await fetch('/api/submissions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: user.student_id,
        student_name: user.name,
        chapter_id,
        task_type,
        report_url,
        notes
      })
    });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message || 'ส่งงานเรียบร้อยแล้ว!', 'success');
      closeModal('studentSubmissionModal');
      await fetchAllData();
      renderPracticalTasks();
      renderWorksheets();
      if (state.currentRole === 'admin') {
        renderAdminSubmissions();
      }
    } else {
      showToast(json.message || 'เกิดข้อผิดพลาดในการส่งงาน', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์', 'error');
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnHtml;
    }
  }
}

// ==============================================================
// 5. PRACTICAL EXAMS & RUBRIC / WORKSHEET GRADING STUDIO CONTROLLER
// ==============================================================
let currentRubricsState = [];
let currentRosterFilter = 'all'; // 'all' | 'pending_practical' | 'pending_worksheet' | 'pending' | 'graded'
let currentGradingMode = 'practical'; // 'practical' | 'worksheet'

function setGradingMode(mode) {
  currentGradingMode = mode;
  const btnPractical = document.getElementById('gradingModeBtn-practical');
  const btnWorksheet = document.getElementById('gradingModeBtn-worksheet');
  const formPractical = document.getElementById('gradingFormContainer-practical');
  const formWorksheet = document.getElementById('gradingFormContainer-worksheet');

  if (mode === 'worksheet') {
    if (btnPractical) btnPractical.className = "flex-1 py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 text-slate-600 hover:bg-white transition";
    if (btnWorksheet) btnWorksheet.className = "flex-1 py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 bg-indigo-700 text-white shadow-sm transition";
    if (formPractical) formPractical.classList.add('hidden');
    if (formWorksheet) formWorksheet.classList.remove('hidden');
  } else {
    if (btnPractical) btnPractical.className = "flex-1 py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 bg-[#173b6b] text-white shadow-sm transition";
    if (btnWorksheet) btnWorksheet.className = "flex-1 py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 text-slate-600 hover:bg-white transition";
    if (formPractical) formPractical.classList.remove('hidden');
    if (formWorksheet) formWorksheet.classList.add('hidden');
  }
}

function formatRubricsText(rubrics) {
  if (!rubrics) return '';
  if (typeof rubrics === 'string') return rubrics;
  if (Array.isArray(rubrics)) {
    return rubrics.map(r => (typeof r === 'object' && r !== null ? (r.text || r.title || JSON.stringify(r)) : String(r))).join('\n');
  }
  if (typeof rubrics === 'object') return rubrics.text || JSON.stringify(rubrics);
  return String(rubrics);
}

function parseRubrics(rubricsData) {
  const rubricsStr = formatRubricsText(rubricsData);
  if (!rubricsStr) return [
    { title: 'การต่อวงจรและเตรียมฮาร์ดแวร์', maxPoints: 3, currentPoints: 3 },
    { title: 'การรันคำสั่งและการเขียนโปรแกรม', maxPoints: 4, currentPoints: 4 },
    { title: 'การบันทึกผลและตอบคำถามคิดวิเคราะห์', maxPoints: 3, currentPoints: 3 }
  ];

  const lines = rubricsStr.split('\n').filter(l => l.trim().startsWith('*'));
  if (lines.length === 0) return [
    { title: 'การต่อวงจรและเตรียมฮาร์ดแวร์', maxPoints: 3, currentPoints: 3 },
    { title: 'การรันคำสั่งและการเขียนโปรแกรม', maxPoints: 4, currentPoints: 4 },
    { title: 'การบันทึกผลและตอบคำถามคิดวิเคราะห์', maxPoints: 3, currentPoints: 3 }
  ];

  return lines.map((l, idx) => {
    const matchPoints = l.match(/\((\d+(?:\.\d+)?)\s*คะแนน\)/);
    const max = matchPoints ? parseFloat(matchPoints[1]) : (idx === 1 ? 4 : 3);
    const matchTitle = l.match(/\*\*(.*?)\*\*/);
    let title = matchTitle ? matchTitle[1] : `เกณฑ์ข้อที่ ${idx + 1}`;
    title = title.replace(/\(\d+(?:\.\d+)?\s*คะแนน\)/, '').trim().replace(/[:\s]+$/, '');
    return { title, maxPoints: max, currentPoints: max };
  });
}

function setRosterFilter(filter) {
  currentRosterFilter = filter;
  ['all', 'pending_practical', 'pending_worksheet', 'pending', 'graded'].forEach(f => {
    const btn = document.getElementById(`rosterTab-${f}`);
    if (btn) {
      if (f === filter) {
        btn.className = "roster-tab px-2.5 py-0.5 rounded-lg font-bold bg-[#173b6b] text-white shadow-sm";
      } else {
        btn.className = "roster-tab px-2.5 py-0.5 rounded-lg font-bold text-slate-600 hover:bg-slate-100 transition";
      }
    }
  });
  renderGradingStudentRoster();
}

function renderGradingStudentRoster() {
  const rosterContainer = document.getElementById('gradingStudentRosterList');
  if (!rosterContainer) return;

  const pId = document.getElementById('gradeUnitSelect')?.value;
  const practical = (state.practicalExams || []).find(p => p.id === pId);
  const chapterId = practical ? practical.chapter_id : null;
  const ws = (state.worksheets || []).find(w => w.chapter_id === chapterId || w.chapter_number === practical?.unit_number);
  const wsId = ws ? ws.id : (chapterId ? `ws_${chapterId}` : null);

  const currentStdId = document.getElementById('gradeStudentSelect')?.value;
  const search = (document.getElementById('rosterSearchInput')?.value || '').trim().toLowerCase();

  const students = state.students || [];
  if (students.length === 0) {
    rosterContainer.innerHTML = `<div class="p-4 text-center text-xs text-slate-400">ยังไม่มีข้อมูลนักเรียนในระบบ</div>`;
    return;
  }

  // Pre-calculate status for all students
  let practicalGradedCount = 0;
  let worksheetGradedCount = 0;
  let submittedCount = 0;

  const items = students.map(s => {
    const practicalGrade = (state.scores || []).find(sc => sc.student_id === s.student_id && sc.target_id === pId && sc.exam_category === 'practical');
    const worksheetGrade = (state.scores || []).find(sc => sc.student_id === s.student_id && (sc.target_id === wsId || sc.chapter_id === chapterId || sc.target_id === chapterId) && sc.exam_category === 'worksheet');
    const subPractical = (state.submissions || []).find(sub => sub.student_id === s.student_id && sub.chapter_id === chapterId && (sub.task_type || 'practical') === 'practical');
    const subWorksheet = (state.submissions || []).find(sub => sub.student_id === s.student_id && sub.chapter_id === chapterId && sub.task_type === 'worksheet');
    
    if (practicalGrade) practicalGradedCount++;
    if (worksheetGrade) worksheetGradedCount++;
    if (subPractical || subWorksheet) submittedCount++;

    return {
      student: s,
      practicalGrade,
      worksheetGrade,
      subPractical,
      subWorksheet,
      hasSubmission: Boolean(subPractical || subWorksheet),
      isFullyGraded: Boolean(practicalGrade && worksheetGrade)
    };
  });

  // Update top metrics
  const statPracEl = document.getElementById('gradingStatPracticalCount');
  if (statPracEl) statPracEl.textContent = `${practicalGradedCount}/${students.length}`;
  const statWsEl = document.getElementById('gradingStatWorksheetCount');
  if (statWsEl) statWsEl.textContent = `${worksheetGradedCount}/${students.length}`;
  const statSubmittedEl = document.getElementById('gradingStatSubmittedCount');
  if (statSubmittedEl) statSubmittedEl.textContent = `${submittedCount}/${students.length}`;
  const legacyGradedEl = document.getElementById('gradingStatGradedCount');
  if (legacyGradedEl) legacyGradedEl.textContent = `${practicalGradedCount}/${students.length}`;

  // Filter items
  let filtered = items;
  if (currentRosterFilter === 'pending_practical') {
    filtered = filtered.filter(it => it.subPractical && !it.practicalGrade);
  } else if (currentRosterFilter === 'pending_worksheet') {
    filtered = filtered.filter(it => it.subWorksheet && !it.worksheetGrade);
  } else if (currentRosterFilter === 'pending') {
    filtered = filtered.filter(it => (it.subPractical && !it.practicalGrade) || (it.subWorksheet && !it.worksheetGrade));
  } else if (currentRosterFilter === 'graded') {
    filtered = filtered.filter(it => it.practicalGrade || it.worksheetGrade);
  }

  if (search) {
    filtered = filtered.filter(it => {
      const matchId = (it.student.student_id || '').toLowerCase().includes(search);
      const matchName = (it.student.name || '').toLowerCase().includes(search);
      return matchId || matchName;
    });
  }

  const countBadge = document.getElementById('rosterFilterCount');
  if (countBadge) countBadge.textContent = `${filtered.length} คน`;

  if (filtered.length === 0) {
    rosterContainer.innerHTML = `
      <div class="p-6 text-center text-xs text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200">
        <i class="fa-solid fa-filter-circle-xmark text-slate-300 text-lg mb-1 block"></i>
        ไม่พบนักเรียนตามเงื่อนไขที่เลือก
      </div>
    `;
    return;
  }

  rosterContainer.innerHTML = filtered.map(it => {
    const s = it.student;
    const isSelected = s.student_id === currentStdId;

    let pracPill = '';
    if (it.practicalGrade) {
      pracPill = `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300 flex items-center gap-1 shrink-0" title="คะแนนโจทย์ปฏิบัติ"><i class="fa-solid fa-microchip text-[9px] text-amber-600"></i> ปฏิบัติ: ${it.practicalGrade.score}/10</span>`;
    } else if (it.subPractical) {
      pracPill = `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200 flex items-center gap-1 shrink-0"><i class="fa-solid fa-bolt text-[9px] text-amber-600"></i> รอตรวจปฏิบัติ</span>`;
    } else {
      pracPill = `<span class="px-1.5 py-0.5 rounded text-[10px] text-slate-400 bg-slate-50 border border-slate-200 shrink-0">ปฏิบัติ: ยังไม่ส่ง</span>`;
    }

    let wsPill = '';
    if (it.worksheetGrade) {
      wsPill = `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-900 border border-indigo-300 flex items-center gap-1 shrink-0" title="คะแนนใบงาน"><i class="fa-solid fa-file-lines text-[9px] text-indigo-600"></i> ใบงาน: ${it.worksheetGrade.score}/10</span>`;
    } else if (it.subWorksheet) {
      wsPill = `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-indigo-50 text-indigo-800 border border-indigo-200 flex items-center gap-1 shrink-0"><i class="fa-solid fa-bolt text-[9px] text-indigo-600"></i> รอตรวจใบงาน</span>`;
    } else {
      wsPill = `<span class="px-1.5 py-0.5 rounded text-[10px] text-slate-400 bg-slate-50 border border-slate-200 shrink-0">ใบงาน: ยังไม่ส่ง</span>`;
    }

    const cardClasses = isSelected
      ? "p-2.5 rounded-xl border-2 border-[#173b6b] bg-blue-50/70 shadow-sm flex items-center justify-between cursor-pointer transition transform scale-[1.01]"
      : "p-2.5 rounded-xl border border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50/80 flex items-center justify-between cursor-pointer transition";

    return `
      <div onclick="selectStudentForGrading('${s.student_id}')" class="${cardClasses}" data-student-id="${s.student_id}">
        <div class="min-w-0 pr-2">
          <div class="flex items-center gap-1.5">
            <span class="font-mono text-xs font-bold ${isSelected ? 'text-[#173b6b]' : 'text-slate-600'}">${s.student_id}</span>
            <span class="text-xs font-bold text-slate-800 truncate">${escapeHtml(s.name)}</span>
          </div>
          <div class="text-[10px] text-slate-400 mt-0.5">${escapeHtml(s.class_room || 'ม.5/12')}</div>
        </div>
        <div class="flex flex-col items-end gap-1 shrink-0">
          ${pracPill}
          ${wsPill}
        </div>
      </div>
    `;
  }).join('');
}

function selectStudentForGrading(studentId) {
  const stdSelect = document.getElementById('gradeStudentSelect');
  if (stdSelect) {
    stdSelect.value = studentId;
  }
  onGradeStudentChange();
  renderGradingStudentRoster();
}

function onGradeStudentChange() {
  const stdId = document.getElementById('gradeStudentSelect')?.value;
  const pId = document.getElementById('gradeUnitSelect')?.value;
  const practical = (state.practicalExams || []).find(p => p.id === pId);
  const chapterId = practical ? practical.chapter_id : null;
  const ws = (state.worksheets || []).find(w => w.chapter_id === chapterId || w.chapter_number === practical?.unit_number);
  const wsId = ws ? ws.id : (chapterId ? `ws_${chapterId}` : null);
  const student = (state.students || []).find(s => s.student_id === stdId);

  if (!student) return;

  // 1. Update Active Student Banner
  const idLabel = document.getElementById('activeStudentIdLabel');
  if (idLabel) idLabel.textContent = student.student_id;
  const nameLabel = document.getElementById('activeStudentNameLabel');
  if (nameLabel) nameLabel.textContent = student.name;

  const practicalGrade = (state.scores || []).find(sc => sc.student_id === stdId && sc.target_id === pId && sc.exam_category === 'practical');
  const worksheetGrade = (state.scores || []).find(sc => sc.student_id === stdId && (sc.target_id === wsId || sc.chapter_id === chapterId || sc.target_id === chapterId) && sc.exam_category === 'worksheet');
  const subPractical = (state.submissions || []).find(s => s.student_id === stdId && s.chapter_id === chapterId && (s.task_type || 'practical') === 'practical');
  const subWorksheet = (state.submissions || []).find(s => s.student_id === stdId && s.chapter_id === chapterId && s.task_type === 'worksheet');

  // Update Status Badges in Mode Switcher
  const deskPracBadge = document.getElementById('deskStatusBadge-practical');
  if (deskPracBadge) {
    if (practicalGrade) {
      deskPracBadge.className = "text-[10px] px-2 py-0.5 rounded-full bg-emerald-500 text-white font-mono font-bold";
      deskPracBadge.textContent = `${practicalGrade.score}/10`;
    } else if (subPractical) {
      deskPracBadge.className = "text-[10px] px-2 py-0.5 rounded-full bg-amber-400 text-slate-900 font-mono font-bold";
      deskPracBadge.textContent = "รอตรวจ";
    } else {
      deskPracBadge.className = "text-[10px] px-2 py-0.5 rounded-full bg-slate-200 text-slate-600 font-mono";
      deskPracBadge.textContent = "ยังไม่ส่ง";
    }
  }

  const deskWsBadge = document.getElementById('deskStatusBadge-worksheet');
  if (deskWsBadge) {
    if (worksheetGrade) {
      deskWsBadge.className = "text-[10px] px-2 py-0.5 rounded-full bg-emerald-500 text-white font-mono font-bold";
      deskWsBadge.textContent = `${worksheetGrade.score}/10`;
    } else if (subWorksheet) {
      deskWsBadge.className = "text-[10px] px-2 py-0.5 rounded-full bg-amber-400 text-slate-900 font-mono font-bold";
      deskWsBadge.textContent = "รอตรวจ";
    } else {
      deskWsBadge.className = "text-[10px] px-2 py-0.5 rounded-full bg-slate-200 text-slate-600 font-mono";
      deskWsBadge.textContent = "ยังไม่ส่ง";
    }
  }

  // Active student banner status badge
  const statusBadge = document.getElementById('activeStudentStatusBadge');
  if (statusBadge) {
    if (practicalGrade && worksheetGrade) {
      statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500 text-white shadow-sm flex items-center gap-1";
      statusBadge.innerHTML = `<i class="fa-solid fa-circle-check"></i> ตรวจครบทั้ง 2 ชิ้นแล้ว (ป: ${practicalGrade.score}/10 | บ: ${worksheetGrade.score}/10)`;
    } else if (practicalGrade) {
      statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500 text-white shadow-sm flex items-center gap-1";
      statusBadge.innerHTML = `<i class="fa-solid fa-check"></i> ตรวจโจทย์ปฏิบัติแล้ว (${practicalGrade.score}/10) • รอตรวจใบงาน`;
    } else if (worksheetGrade) {
      statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500 text-white shadow-sm flex items-center gap-1";
      statusBadge.innerHTML = `<i class="fa-solid fa-check"></i> ตรวจใบงานแล้ว (${worksheetGrade.score}/10) • รอตรวจโจทย์ปฏิบัติ`;
    } else if (subPractical || subWorksheet) {
      statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-400 text-slate-900 shadow-sm flex items-center gap-1";
      statusBadge.innerHTML = `<i class="fa-solid fa-bolt"></i> ส่งงานแล้ว (รอตรวจให้คะแนน)`;
    } else {
      statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-white/20 text-white";
      statusBadge.innerHTML = `<i class="fa-solid fa-clock"></i> ยังไม่ได้ตรวจ`;
    }
  }

  // 2. Update Submission Freshness Badge
  const freshBadge = document.getElementById('submissionFreshnessBadge');
  if (freshBadge) {
    if (subPractical && subWorksheet) {
      freshBadge.innerHTML = `<span class="text-emerald-600 font-bold"><i class="fa-solid fa-circle-check mr-1"></i>ส่งครบ 2 ชิ้น (โจทย์ + ใบงาน)</span>`;
    } else if (subPractical) {
      freshBadge.innerHTML = `<span class="text-blue-600 font-bold"><i class="fa-solid fa-microchip mr-1"></i>ส่งเฉพาะโจทย์ข้อสอบปฏิบัติ</span>`;
    } else if (subWorksheet) {
      freshBadge.innerHTML = `<span class="text-indigo-600 font-bold"><i class="fa-solid fa-file-lines mr-1"></i>ส่งเฉพาะใบงานประจำบท</span>`;
    } else {
      freshBadge.innerHTML = `<span class="text-slate-400"><i class="fa-solid fa-circle-info mr-1"></i>ยังไม่ส่งผ่านเว็บ</span>`;
    }
  }

  // 3. Update Submission Preview Box
  updateSubmissionPreview();

  // 4. Load Practical Rubrics & Scores
  const defaultRubrics = parseRubrics(practical ? practical.rubrics : null);

  if (practicalGrade) {
    if (Array.isArray(practicalGrade.rubrics_breakdown) && practicalGrade.rubrics_breakdown.length > 0) {
      currentRubricsState = defaultRubrics.map((r, i) => {
        const saved = practicalGrade.rubrics_breakdown[i];
        const pts = saved && saved.currentPoints !== undefined ? parseFloat(saved.currentPoints) : r.maxPoints;
        return { ...r, currentPoints: pts };
      });
    } else {
      const ratio = (parseFloat(practicalGrade.score) || 0) / 10;
      currentRubricsState = defaultRubrics.map(r => ({
        ...r,
        currentPoints: Math.round(r.maxPoints * ratio * 2) / 2
      }));
    }

    const scoreInput = document.getElementById('gradeScoreInput');
    if (scoreInput) scoreInput.value = practicalGrade.score;

    const notesInput = document.getElementById('gradeNotesInput');
    if (notesInput) notesInput.value = practicalGrade.notes || '';
  } else {
    currentRubricsState = defaultRubrics.map(r => ({ ...r, currentPoints: r.maxPoints }));
    const scoreInput = document.getElementById('gradeScoreInput');
    if (scoreInput) scoreInput.value = 10;

    const notesInput = document.getElementById('gradeNotesInput');
    if (notesInput) notesInput.value = '';
  }

  renderRubricCriteriaInputs();

  // 5. Load Worksheet Score & Notes
  const wsScoreInput = document.getElementById('gradeWorksheetScoreInput');
  const wsNotesInput = document.getElementById('gradeWorksheetNotesInput');
  const wsIndicator = document.getElementById('worksheetStatusIndicator');

  if (worksheetGrade) {
    if (wsScoreInput) wsScoreInput.value = worksheetGrade.score;
    if (wsNotesInput) wsNotesInput.value = worksheetGrade.notes || '';
    if (wsIndicator) {
      wsIndicator.className = "px-2.5 py-1 rounded-full font-bold text-xs bg-emerald-100 text-emerald-800 border border-emerald-300";
      wsIndicator.innerHTML = `<i class="fa-solid fa-check mr-1"></i>ตรวจแล้ว (${worksheetGrade.score}/10)`;
    }
  } else {
    if (wsScoreInput) wsScoreInput.value = 10;
    if (wsNotesInput) wsNotesInput.value = '';
    if (wsIndicator) {
      if (subWorksheet) {
        wsIndicator.className = "px-2.5 py-1 rounded-full font-bold text-xs bg-amber-100 text-amber-800 border border-amber-300";
        wsIndicator.innerHTML = `<i class="fa-solid fa-bolt text-amber-600 mr-1"></i>ส่งใบงานแล้ว (รอตรวจ)`;
      } else {
        wsIndicator.className = "px-2.5 py-1 rounded-full font-bold text-xs bg-slate-100 text-slate-500 border border-slate-200";
        wsIndicator.textContent = "ยังไม่ส่งใบงาน";
      }
    }
  }

  renderWorksheetLevelPills();
  recalculateWorksheetTotal();
}

function updateSubmissionPreview() {
  const preview = document.getElementById('studentSubmissionPreview');
  if (!preview) return;

  const stdId = document.getElementById('gradeStudentSelect')?.value;
  const pId = document.getElementById('gradeUnitSelect')?.value;
  const practical = (state.practicalExams || []).find(p => p.id === pId);
  const chapterId = practical ? practical.chapter_id : null;

  if (!stdId || !chapterId) {
    preview.innerHTML = `<span class="text-slate-400"><i class="fa-solid fa-circle-info mr-1"></i> กรุณาเลือกนักเรียนและบทเรียนเพื่อตรวจสอบรายงานที่ส่ง</span>`;
    return;
  }

  const subPractical = (state.submissions || []).find(s => s.student_id === stdId && s.chapter_id === chapterId && (s.task_type || 'practical') === 'practical');
  const subWorksheet = (state.submissions || []).find(s => s.student_id === stdId && s.chapter_id === chapterId && s.task_type === 'worksheet');

  if (subPractical || subWorksheet) {
    preview.className = "p-3.5 bg-blue-50/90 border border-blue-300 rounded-xl text-xs space-y-3 shadow-sm";
    let html = `
      <div class="flex items-center justify-between">
        <span class="font-bold text-[#173b6b] flex items-center gap-1.5">
          <i class="fa-solid fa-folder-open text-blue-600"></i> ลิงก์ผลงานและเอกสารที่นักเรียนส่งเข้ามา
        </span>
        <span class="text-[11px] text-slate-500 font-mono">สถานะ: มีข้อมูลส่งงาน</span>
      </div>
      <div class="space-y-2">
    `;

    // 1. Practical task report
    if (subPractical) {
      const pDate = new Date(subPractical.submitted_at).toLocaleString('th-TH');
      html += `
        <div class="bg-white p-2.5 rounded-lg border border-amber-200 space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-bold text-amber-800 flex items-center gap-1.5">
              <i class="fa-solid fa-microchip text-amber-600"></i> โจทย์ข้อสอบปฏิบัติ:
            </span>
            <span class="text-[10px] text-slate-400 font-mono">${pDate}</span>
          </div>
          <div class="flex items-center gap-2 pl-4">
            <strong class="text-slate-700 whitespace-nowrap text-[11px]">ลิงก์:</strong>
            <a href="${escapeHtml(subPractical.report_url)}" target="_blank" class="text-blue-600 hover:text-blue-800 underline font-mono break-all flex items-center gap-1 font-bold text-[11px]">
              <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i> ${escapeHtml(subPractical.report_url)}
            </a>
          </div>
          ${subPractical.notes ? `
          <div class="text-[11px] pl-4 text-slate-600">
            <strong class="text-slate-700">บันทึก:</strong> ${escapeHtml(subPractical.notes)}
          </div>
          ` : ''}
        </div>
      `;
    } else {
      html += `
        <div class="bg-amber-50/50 p-2 rounded-lg border border-dashed border-amber-200 text-[11px] text-amber-700 flex items-center gap-1.5">
          <i class="fa-solid fa-circle-exclamation text-amber-500"></i> ยังไม่ส่งรายงานโจทย์ข้อสอบปฏิบัติ
        </div>
      `;
    }

    // 2. Lab worksheet
    if (subWorksheet) {
      const wDate = new Date(subWorksheet.submitted_at).toLocaleString('th-TH');
      html += `
        <div class="bg-white p-2.5 rounded-lg border border-indigo-200 space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-bold text-indigo-800 flex items-center gap-1.5">
              <i class="fa-solid fa-file-lines text-indigo-600"></i> ใบงานปฏิบัติการประจำบท:
            </span>
            <span class="text-[10px] text-slate-400 font-mono">${wDate}</span>
          </div>
          <div class="flex items-center gap-2 pl-4">
            <strong class="text-slate-700 whitespace-nowrap text-[11px]">ลิงก์:</strong>
            <a href="${escapeHtml(subWorksheet.report_url)}" target="_blank" class="text-indigo-600 hover:text-indigo-800 underline font-mono break-all flex items-center gap-1 font-bold text-[11px]">
              <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i> ${escapeHtml(subWorksheet.report_url)}
            </a>
          </div>
          ${subWorksheet.notes ? `
          <div class="text-[11px] pl-4 text-slate-600">
            <strong class="text-slate-700">บันทึก:</strong> ${escapeHtml(subWorksheet.notes)}
          </div>
          ` : ''}
        </div>
      `;
    } else {
      html += `
        <div class="bg-indigo-50/50 p-2 rounded-lg border border-dashed border-indigo-200 text-[11px] text-indigo-700 flex items-center gap-1.5">
          <i class="fa-solid fa-circle-exclamation text-indigo-500"></i> ยังไม่ส่งใบงานปฏิบัติการประจำบท
        </div>
      `;
    }

    html += `</div>`;
    preview.innerHTML = html;
  } else {
    preview.className = "p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-500";
    preview.innerHTML = `
      <div class="flex items-center gap-2">
        <i class="fa-solid fa-circle-info text-slate-400"></i>
        <span>นักเรียนยังไม่ได้ส่งรายงานหรือใบงานผ่านลิงก์ดิจิทัล (สามารถตรวจประเมินผลการปฏิบัติจริงในห้องเรียนได้ทันที)</span>
      </div>
    `;
  }
}

function onGradeUnitChange() {
  const unitSelect = document.getElementById('gradeUnitSelect');
  if (!unitSelect) return;
  const pId = unitSelect.value;
  const practical = (state.practicalExams || []).find(p => p.id === pId);
  if (!practical) return;

  currentRubricsState = parseRubrics(practical.rubrics);
  renderGradingStudentRoster();
  onGradeStudentChange();
}

function renderRubricCriteriaInputs() {
  const container = document.getElementById('rubricCriteriaContainer');
  if (!container) return;

  container.innerHTML = currentRubricsState.map((r, idx) => {
    let pillValues = [];
    if (r.maxPoints === 3) {
      pillValues = [0, 1, 1.5, 2, 2.5, 3];
    } else if (r.maxPoints === 4) {
      pillValues = [0, 1, 2, 2.5, 3, 3.5, 4];
    } else if (r.maxPoints <= 2) {
      pillValues = [0, 0.5, 1, 1.5, 2].filter(v => v <= r.maxPoints);
    } else {
      pillValues = [0, Math.round(r.maxPoints * 0.4 * 2) / 2, Math.round(r.maxPoints * 0.6 * 2) / 2, Math.round(r.maxPoints * 0.8 * 2) / 2, r.maxPoints];
      pillValues = [...new Set(pillValues)].sort((a, b) => a - b);
    }

    const currentVal = r.currentPoints !== undefined ? r.currentPoints : r.maxPoints;

    const pillsHtml = pillValues.map(val => {
      const isSelected = Math.abs(currentVal - val) < 0.05;
      const isFull = val === r.maxPoints;
      const pillClass = isSelected
        ? "bg-[#173b6b] text-white border-[#173b6b] shadow font-black scale-105 ring-2 ring-blue-300"
        : "bg-white text-slate-700 hover:bg-blue-50 border-slate-300 font-bold hover:border-blue-400";

      return `
        <button type="button" onclick="setRubricCriterionScore(${idx}, ${val})" class="px-3 py-1 rounded-xl text-xs border transition duration-150 flex items-center gap-1 ${pillClass}">
          ${val}${isFull ? ' <span class="text-[9px] opacity-80">(เต็ม)</span>' : ''}
        </button>
      `;
    }).join('');

    return `
      <div class="bg-white p-3.5 rounded-xl border border-yellow-300/80 shadow-sm space-y-2">
        <div class="flex items-start justify-between gap-2">
          <div class="font-bold text-xs text-slate-800 leading-snug flex items-center gap-1.5">
            <span class="w-5 h-5 rounded-full bg-blue-100 text-[#173b6b] font-extrabold text-[11px] flex items-center justify-center shrink-0">${idx + 1}</span>
            <span>${escapeHtml(r.title)}</span>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <span class="font-black text-[#173b6b] font-mono text-sm px-2.5 py-0.5 rounded-lg bg-blue-50 border border-blue-200" id="rubricScoreDisplay_${idx}">${currentVal}/${r.maxPoints} คะแนน</span>
            <input type="number" min="0" max="${r.maxPoints}" step="0.5" value="${currentVal}" onchange="setRubricCriterionScore(${idx}, this.value)" class="w-14 text-center text-xs font-bold border border-slate-200 rounded-lg p-1 bg-slate-50 focus:bg-white focus:outline-none focus:border-[#173b6b]" title="กรอกตัวเลขแบบละเอียด">
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-1.5 pt-1">
          <span class="text-[10px] text-slate-400 font-bold mr-1">ระดับ:</span>
          ${pillsHtml}
        </div>
      </div>
    `;
  }).join('');

  recalculateRubricTotal();
}

function setRubricCriterionScore(idx, score) {
  if (currentRubricsState[idx]) {
    const max = currentRubricsState[idx].maxPoints;
    let num = parseFloat(score);
    if (isNaN(num)) num = 0;
    if (num < 0) num = 0;
    if (num > max) num = max;

    currentRubricsState[idx].currentPoints = num;
    renderRubricCriteriaInputs();
  }
}

function recalculateRubricTotal() {
  const total = currentRubricsState.reduce((sum, r) => sum + (r.currentPoints || 0), 0);
  const rounded = Math.round(total * 10) / 10;

  const scoreInput = document.getElementById('gradeScoreInput');
  if (scoreInput) scoreInput.value = rounded;

  const dispTotal = document.getElementById('rubricScoreDisplayTotal');
  if (dispTotal) {
    dispTotal.textContent = rounded.toFixed(1);
    dispTotal.className = rounded >= 8
      ? "text-lg font-black text-emerald-600 ml-1"
      : rounded >= 6
        ? "text-lg font-black text-blue-600 ml-1"
        : "text-lg font-black text-amber-600 ml-1";
  }

  const sumLabel = document.getElementById('rubricAutoSumLabel');
  if (sumLabel) sumLabel.textContent = `รวม ${rounded} / 10 คะแนน`;
}

function applyRubricPreset(totalScore) {
  if (currentRubricsState.length === 3 && currentRubricsState[0].maxPoints === 3 && currentRubricsState[1].maxPoints === 4 && currentRubricsState[2].maxPoints === 3) {
    const presets = {
      10: [3, 4, 3],
      9: [2.5, 4, 2.5],
      8: [2.5, 3, 2.5],
      7: [2, 3, 2],
      5: [1.5, 2, 1.5]
    };
    const arr = presets[totalScore] || [Math.round(3 * totalScore / 10 * 2) / 2, Math.round(4 * totalScore / 10 * 2) / 2, Math.round(3 * totalScore / 10 * 2) / 2];
    currentRubricsState[0].currentPoints = arr[0];
    currentRubricsState[1].currentPoints = arr[1];
    currentRubricsState[2].currentPoints = arr[2];
  } else {
    const totalMax = currentRubricsState.reduce((s, r) => s + r.maxPoints, 0) || 10;
    const ratio = totalScore / totalMax;
    currentRubricsState.forEach(r => {
      r.currentPoints = Math.round(r.maxPoints * ratio * 2) / 2;
    });
  }

  renderRubricCriteriaInputs();
  showToast(`ปรับชุดคะแนนรูบริกเป็น ${totalScore} คะแนนเรียบร้อย`, 'info');
}

function appendQuickFeedback(text) {
  const input = document.getElementById('gradeNotesInput');
  if (!input) return;

  const current = input.value.trim();
  if (!current) {
    input.value = text;
  } else if (!current.includes(text)) {
    input.value = `${current}, ${text}`;
  }
  input.focus();
}

// ==============================================================
// WORKSHEET GRADING FUNCTIONS
// ==============================================================
function renderWorksheetLevelPills() {
  const container = document.getElementById('worksheetLevelPillsContainer');
  if (!container) return;

  const scoreInput = document.getElementById('gradeWorksheetScoreInput');
  const currentVal = parseFloat(scoreInput?.value || 10);
  const levels = [0, 5, 6, 7, 8, 8.5, 9, 9.5, 10];

  container.innerHTML = levels.map(val => {
    const isSelected = Math.abs(currentVal - val) < 0.05;
    const isFull = val === 10;
    const pillClass = isSelected
      ? "bg-indigo-700 text-white border-indigo-700 shadow font-black scale-105 ring-2 ring-indigo-300"
      : "bg-white text-slate-700 hover:bg-indigo-50 border-slate-300 font-bold hover:border-indigo-400";

    return `
      <button type="button" onclick="setWorksheetScore(${val})" class="px-3 py-1 rounded-xl text-xs border transition duration-150 flex items-center gap-1 ${pillClass}">
        ${val}${isFull ? ' <span class="text-[9px] opacity-80">(เต็ม)</span>' : ''}
      </button>
    `;
  }).join('');
}

function setWorksheetScore(val) {
  let num = parseFloat(val);
  if (isNaN(num)) num = 0;
  if (num < 0) num = 0;
  if (num > 10) num = 10;

  const input = document.getElementById('gradeWorksheetScoreInput');
  if (input) input.value = num;

  renderWorksheetLevelPills();
  recalculateWorksheetTotal();
}

function onWorksheetScoreInputChange(val) {
  renderWorksheetLevelPills();
  recalculateWorksheetTotal();
}

function recalculateWorksheetTotal() {
  const scoreInput = document.getElementById('gradeWorksheetScoreInput');
  const num = parseFloat(scoreInput?.value || 0);
  const dispTotal = document.getElementById('worksheetScoreDisplayTotal');
  if (dispTotal) {
    dispTotal.textContent = num.toFixed(1);
    dispTotal.className = num >= 8
      ? "text-lg font-black text-emerald-600 ml-1"
      : num >= 6
        ? "text-lg font-black text-indigo-700 ml-1"
        : "text-lg font-black text-amber-600 ml-1";
  }
}

function applyWorksheetPreset(score) {
  setWorksheetScore(score);
  showToast(`ปรับคะแนนใบงานเป็น ${score} คะแนนเรียบร้อย`, 'info');
}

function appendWorksheetFeedback(text) {
  const input = document.getElementById('gradeWorksheetNotesInput');
  if (!input) return;
  const cur = input.value.trim();
  if (!cur) input.value = text;
  else if (!cur.includes(text)) input.value = `${cur}, ${text}`;
  input.focus();
}

async function handleGradeWorksheet(e) {
  e.preventDefault();
  const student_id = document.getElementById('gradeStudentSelect')?.value;
  const practical_id = document.getElementById('gradeUnitSelect')?.value;
  const practical = (state.practicalExams || []).find(p => p.id === practical_id);
  const chapter_id = practical ? practical.chapter_id : 'ch01';
  const ws = (state.worksheets || []).find(w => w.chapter_id === chapter_id);
  const worksheet_id = ws ? ws.id : `ws_${chapter_id}`;

  const score = document.getElementById('gradeWorksheetScoreInput')?.value;
  const notes = document.getElementById('gradeWorksheetNotesInput') ? document.getElementById('gradeWorksheetNotesInput').value : '';

  if (!student_id || !chapter_id) {
    showToast('กรุณาเลือกนักเรียนและบทเรียนที่ต้องการประเมิน', 'error');
    return;
  }

  const std = (state.students || []).find(s => s.student_id === student_id);
  const student_name = std ? std.name : 'นักเรียน';

  try {
    const res = await fetch('/api/worksheets/grade', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        student_id,
        student_name,
        chapter_id,
        worksheet_id,
        score,
        notes
      })
    });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(`บันทึกคะแนนใบงานของ ${student_name} สำเร็จ (${score}/10 คะแนน) พร้อมซิงค์เข้าชีต worksheet แล้ว`, 'success');
      await fetchAllData();
      renderScores();
      renderWorksheets();
      renderGradingStudentRoster();

      const autoNext = document.getElementById('gradeWorksheetAutoNextCheckbox')?.checked;
      if (autoNext) {
        nextUngradedStudent(false);
      } else {
        onGradeStudentChange();
      }
    } else {
      showToast(json.message || 'บันทึกไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการบันทึกคะแนนใบงาน', 'error');
  }
}

// Navigation helpers
function prevStudentToGrade() {
  const students = state.students || [];
  if (students.length === 0) return;
  const currentStdId = document.getElementById('gradeStudentSelect')?.value;
  const idx = students.findIndex(s => s.student_id === currentStdId);

  if (idx > 0) {
    selectStudentForGrading(students[idx - 1].student_id);
  } else {
    showToast('นี่คือนักเรียนคนแรกของห้องแล้ว', 'info');
  }
}

function nextStudentToGrade() {
  const students = state.students || [];
  if (students.length === 0) return;
  const currentStdId = document.getElementById('gradeStudentSelect')?.value;
  const idx = students.findIndex(s => s.student_id === currentStdId);

  if (idx >= 0 && idx < students.length - 1) {
    selectStudentForGrading(students[idx + 1].student_id);
  } else {
    showToast('นี่คือนักเรียนคนสุดท้ายของห้องแล้ว', 'info');
  }
}

function nextUngradedStudent(showToastMsg = true) {
  const students = state.students || [];
  if (students.length === 0) return;

  const pId = document.getElementById('gradeUnitSelect')?.value;
  const practical = (state.practicalExams || []).find(p => p.id === pId);
  const chapterId = practical ? practical.chapter_id : null;
  const ws = (state.worksheets || []).find(w => w.chapter_id === chapterId);
  const wsId = ws ? ws.id : (chapterId ? `ws_${chapterId}` : null);
  const currentStdId = document.getElementById('gradeStudentSelect')?.value;
  const curIdx = students.findIndex(s => s.student_id === currentStdId);

  // Check 1: In current grading mode, find student who has submission AND not graded
  for (let step = 1; step <= students.length; step++) {
    const checkIdx = (curIdx + step) % students.length;
    const s = students[checkIdx];

    if (currentGradingMode === 'worksheet') {
      const gradeRecord = (state.scores || []).find(sc => sc.student_id === s.student_id && (sc.target_id === wsId || sc.chapter_id === chapterId || sc.target_id === chapterId) && sc.exam_category === 'worksheet');
      const sub = (state.submissions || []).find(sub => sub.student_id === s.student_id && sub.chapter_id === chapterId && sub.task_type === 'worksheet');
      if (!gradeRecord && sub) {
        selectStudentForGrading(s.student_id);
        if (showToastMsg) showToast(`ข้ามไปยัง ${s.name} (มีใบงานส่งรอตรวจ)`, 'info');
        return;
      }
    } else {
      const gradeRecord = (state.scores || []).find(sc => sc.student_id === s.student_id && sc.target_id === pId && sc.exam_category === 'practical');
      const sub = (state.submissions || []).find(sub => sub.student_id === s.student_id && sub.chapter_id === chapterId && (sub.task_type || 'practical') === 'practical');
      if (!gradeRecord && sub) {
        selectStudentForGrading(s.student_id);
        if (showToastMsg) showToast(`ข้ามไปยัง ${s.name} (มีโจทย์ปฏิบัติส่งรอตรวจ)`, 'info');
        return;
      }
    }
  }

  // Check 2: find any student not graded yet in current mode
  for (let step = 1; step <= students.length; step++) {
    const checkIdx = (curIdx + step) % students.length;
    const s = students[checkIdx];
    const isWs = currentGradingMode === 'worksheet';
    const gradeRecord = isWs
      ? (state.scores || []).find(sc => sc.student_id === s.student_id && (sc.target_id === wsId || sc.chapter_id === chapterId || sc.target_id === chapterId) && sc.exam_category === 'worksheet')
      : (state.scores || []).find(sc => sc.student_id === s.student_id && sc.target_id === pId && sc.exam_category === 'practical');

    if (!gradeRecord) {
      selectStudentForGrading(s.student_id);
      if (showToastMsg) showToast(`ข้ามไปยัง ${s.name} (ยังไม่ได้รับการตรวจ${isWs ? 'ใบงาน' : 'โจทย์ปฏิบัติ'})`, 'info');
      return;
    }
  }

  // All graded in current mode
  if (showToastMsg) {
    showToast(`🎉 นักเรียนทุกคนได้รับการประเมิน${currentGradingMode === 'worksheet' ? 'ใบงาน' : 'โจทย์ปฏิบัติ'}ครบ 100% แล้ว!`, 'success');
  }
}

async function handleGradePractical(e) {
  e.preventDefault();
  const student_id = document.getElementById('gradeStudentSelect')?.value;
  const practical_id = document.getElementById('gradeUnitSelect')?.value;
  const score = document.getElementById('gradeScoreInput')?.value;
  const notes = document.getElementById('gradeNotesInput') ? document.getElementById('gradeNotesInput').value : '';

  if (!student_id || !practical_id) {
    showToast('กรุณาเลือกนักเรียนและบทเรียนที่ต้องการประเมิน', 'error');
    return;
  }

  const std = (state.students || []).find(s => s.student_id === student_id);
  const student_name = std ? std.name : 'นักเรียน';

  try {
    const res = await fetch('/api/practical/grade', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        student_id,
        student_name,
        practical_id,
        score,
        notes,
        rubrics_breakdown: currentRubricsState
      })
    });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(`บันทึกคะแนนโจทย์ปฏิบัติของ ${student_name} สำเร็จ (${score}/10 คะแนน) พร้อมซิงค์เข้าชีต practical แล้ว`, 'success');
      await fetchAllData();
      renderScores();
      renderPracticalTasks();
      renderGradingStudentRoster();

      const autoNext = document.getElementById('gradeAutoNextCheckbox')?.checked;
      if (autoNext) {
        nextUngradedStudent(false);
      } else {
        onGradeStudentChange();
      }
    } else {
      showToast(json.message || 'บันทึกไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการบันทึกคะแนนโจทย์ปฏิบัติ', 'error');
  }
}


// ==============================================================
// 6. ONLINE EXAMINATION ENGINE (QUIZZES)
// ==============================================================
function startChapterExam() {
  if (!isLoggedIn()) {
    showToast('กรุณาเข้าสู่ระบบนักเรียนก่อนเริ่มทำข้อสอบเพื่อบันทึกคะแนน', 'warning');
    openStudentLoginModal();
    return;
  }

  const chId = document.getElementById('examChapterSelect').value;
  const questions = state.quizzes.filter(q => q.chapter_id === chId && q.category === 'chapter_quiz');
  if (questions.length === 0) {
    showToast('ไม่พบข้อสอบในบทเรียนนี้', 'error');
    return;
  }

  const lesson = state.lessons.find(l => l.id === chId);
  initExamRunner({
    title: `แบบทดสอบท้ายบทเรียนที่ ${lesson ? lesson.chapter_number : ''}: ${lesson ? lesson.title : ''}`,
    subtitle: `ข้อสอบปรนัย 4 ตัวเลือก จำนวน ${questions.length} ข้อ (คะแนนเต็ม ${questions.length} คะแนน)`,
    category: 'chapter_quiz',
    target_id: chId,
    questions: questions
  });
}

function startStandardExam(category) {
  if (!isLoggedIn()) {
    showToast('กรุณาเข้าสู่ระบบนักเรียนก่อนเริ่มทำข้อสอบวัดผลเพื่อบันทึกคะแนน', 'warning');
    openStudentLoginModal();
    return;
  }

  const questions = state.quizzes.filter(q => q.category === category);
  if (questions.length === 0) {
    showToast(`ไม่พบข้อสอบหมวด ${category}`, 'error');
    return;
  }

  const isMid = category === 'midterm';
  initExamRunner({
    title: isMid ? 'แบบทดสอบวัดผลกลางภาคเรียน (Midterm Examination)' : 'แบบทดสอบวัดผลปลายภาคเรียน (Final Examination)',
    subtitle: isMid ? 'ครอบคลุมบทที่ 1–6 (20 ข้อ 20 คะแนน เวลา 40 นาที)' : 'ครอบคลุมบทที่ 7–12 (20 ข้อ 20 คะแนน เวลา 40 นาที)',
    category: category,
    target_id: category,
    questions: questions
  });
}

function initExamRunner(examConfig) {
  state.activeExam = {
    ...examConfig,
    answers: {}
  };

  document.getElementById('activeExamTitle').textContent = examConfig.title;
  document.getElementById('activeExamSubtitle').textContent = examConfig.subtitle;
  document.getElementById('examProgressCount').textContent = `0 / ${examConfig.questions.length}`;

  const body = document.getElementById('examQuestionsBody');
  body.innerHTML = examConfig.questions.map((q, idx) => {
    return `
      <div class="p-6 rounded-2xl border border-slate-200 bg-white" id="q_card_${q.id}">
        <div class="flex items-start space-x-3 mb-4">
          <span class="w-8 h-8 rounded-full bg-[#173b6b] text-[#fff200] flex items-center justify-center font-bold text-xs flex-shrink-0 shadow">
            ${idx + 1}
          </span>
          <div class="text-sm font-bold text-slate-900 leading-relaxed pt-1">
            ${q.question_text}
          </div>
        </div>

        <div class="space-y-2.5 pl-11">
          ${q.options.map((opt, optIdx) => {
            const letters = ['ก', 'ข', 'ค', 'ง'];
            return `
              <label class="exam-option-label flex items-center p-3.5 rounded-xl border border-slate-200 text-xs">
                <input type="radio" name="ans_${q.id}" value="${optIdx}" onchange="recordAnswer('${q.id}', ${optIdx})" class="mr-3 text-[#173b6b] focus:ring-[#173b6b]">
                <span class="font-bold mr-2 text-[#173b6b]">${letters[optIdx]}.</span>
                <span class="text-slate-800">${opt}</span>
              </label>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }).join('');

  document.getElementById('examRunnerContainer').classList.remove('hidden');
  document.getElementById('examResultContainer').classList.add('hidden');
  document.getElementById('examRunnerContainer').scrollIntoView({ behavior: 'smooth' });
}

function recordAnswer(questionId, optionIndex) {
  if (!state.activeExam) return;
  state.activeExam.answers[questionId] = optionIndex;
  
  const answeredCount = Object.keys(state.activeExam.answers).length;
  const total = state.activeExam.questions.length;
  document.getElementById('examProgressCount').textContent = `${answeredCount} / ${total}`;

  // Highlight answered question card
  const card = document.getElementById(`q_card_${questionId}`);
  if (card) {
    card.classList.add('border-[#173b6b]', 'bg-blue-50/20');
  }
}

function cancelExam() {
  if (confirm('คุณต้องการยกเลิกการทำข้อสอบชุดนี้หรือไม่? คำตอบที่ทำไว้จะไม่ได้รับการบันทึก')) {
    state.activeExam = null;
    document.getElementById('examRunnerContainer').classList.add('hidden');
  }
}

async function submitActiveExam() {
  if (!state.activeExam) return;

  if (!state.currentUser || !state.currentUser.id) {
    showToast('กรุณาเข้าสู่ระบบนักเรียนก่อนทำการส่งข้อสอบ', 'warning');
    openStudentLoginModal();
    return;
  }

  const total = state.activeExam.questions.length;
  const answered = Object.keys(state.activeExam.answers).length;

  if (answered < total) {
    if (!confirm(`คุณยังตอบข้อสอบไม่ครบ (${answered}/${total} ข้อ) ยืนยันที่จะส่งข้อสอบเพื่อคิดคะแนนหรือไม่?`)) {
      return;
    }
  }

  try {
    const res = await fetch('/api/quizzes/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: state.currentUser.id,
        student_name: state.currentUser.name,
        category: state.activeExam.category,
        target_id: state.activeExam.target_id,
        answers: state.activeExam.answers
      })
    });

    const json = await res.json();
    if (json.status === 'success') {
      displayExamResult(json.result);
      await fetchAllData();
      renderScores();
    } else {
      showToast(json.message || 'ส่งข้อสอบไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการส่งคำตอบ', 'error');
  }
}

function displayExamResult(result) {
  document.getElementById('examRunnerContainer').classList.add('hidden');
  const resContainer = document.getElementById('examResultContainer');
  resContainer.classList.remove('hidden');

  document.getElementById('resultExamTitle').textContent = state.activeExam.title;
  document.getElementById('resultScore').textContent = result.score;
  document.getElementById('resultMaxScore').textContent = `/ ${result.max_score}`;
  document.getElementById('resultPercentage').textContent = `(${result.percentage}%)`;

  const reviewBody = document.getElementById('examReviewBody');
  const letters = ['ก', 'ข', 'ค', 'ง'];

  reviewBody.innerHTML = result.review.map((item, idx) => {
    return `
      <div class="p-5 rounded-2xl border ${item.is_correct ? 'border-emerald-200 bg-emerald-50/30' : 'border-red-200 bg-red-50/30'}">
        <div class="flex items-start justify-between gap-3 mb-2">
          <div class="flex items-start space-x-2">
            <span class="w-6 h-6 rounded-full ${item.is_correct ? 'bg-emerald-600' : 'bg-red-600'} text-white flex items-center justify-center font-bold text-xs flex-shrink-0">
              ${idx + 1}
            </span>
            <div class="text-xs sm:text-sm font-bold text-slate-900">${item.question_text}</div>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-full font-bold ${item.is_correct ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}">
            ${item.is_correct ? 'ถูกต้อง (+1)' : 'ไม่ถูกต้อง (0)'}
          </span>
        </div>

        <div class="text-xs space-y-1.5 pl-8 text-slate-700 mt-2">
          <div>
            <strong>คำตอบของคุณ:</strong> 
            ${item.student_answer !== null ? `${letters[item.student_answer]}. ${item.options[item.student_answer]}` : '<span class="text-red-500 font-bold">ไม่ได้ตอบ</span>'}
          </div>
          <div class="text-emerald-800 font-bold">
            <strong>คำตอบที่ถูกต้อง:</strong> 
            ${letters[item.correct_answer]}. ${item.options[item.correct_answer]}
          </div>
          <div class="p-3 bg-white/90 rounded-xl border border-slate-200 text-slate-700 mt-2 leading-relaxed">
            <i class="fa-solid fa-lightbulb text-yellow-500 mr-1"></i>
            <strong>เฉลยละเอียดเชิงวิชาการ:</strong> ${item.explanation || 'เฉลยตามเอกสารรายวิชา'}
          </div>
        </div>
      </div>
    `;
  }).join('');

  resContainer.scrollIntoView({ behavior: 'smooth' });
}

function closeExamResult() {
  document.getElementById('examResultContainer').classList.add('hidden');
  state.activeExam = null;
}

// ==============================================================
// 7. CODE SANDBOX & COPY FUNCTION
// ==============================================================
function renderCodeCards() {
  const container = document.getElementById('codeCardsGrid');
  if (!container) return;

  const codeSnippets = [
    { ch: 0, file: 'pc_webcam_simulator.py', desc: 'โปรแกรมจำลอง Edge AI บนกล้องเว็บแคม PC/โน้ตบุ๊ก (โหมดสำรองกรณีไม่มีบอร์ด)' },
    { ch: 1, file: 'check_env.py', desc: 'ตรวจสอบสถานะ Linux aarch64 และไดเรกทอรี /ei-models' },
    { ch: 2, file: 'brick_runner.py', desc: 'สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุม GPIO/LED' },
    { ch: 3, file: 'db_logger.py', desc: 'Database-SQL Brick บันทึกผลการตรวจจับ AI ลง SQLite' },
    { ch: 4, file: 'data_pipeline_check.py', desc: 'การเชื่อมต่อกล้องและจัดสัดส่วน Train/Test 80:20 บน Edge Impulse' },
    { ch: 5, file: 'vad_test.py', desc: 'การอ่านค่าคะแนน Anomaly Score และ Anomaly Max Score' },
    { ch: 6, file: 'fix_app_yaml.py', desc: 'การแก้ไขข้อผิดพลาดไฟล์การกำหนดค่า app.yaml ด้วยวงเล็บปีกกา {...} ตามมาตรฐานล่าสุด' },
    { ch: 7, file: 'test_vad_live.py', desc: 'การประมวลผลภาพสดผ่านกล้อง UVC ตรวจจับความผิดปกติ และบันทึกข้อมูลลง SQL Brick' },
    { ch: 8, file: 'fomo_eval.py', desc: 'การประเมินโมเดล FOMO Object Detection บน Confusion Matrix' },
    { ch: 9, file: 'fomo_live.py', desc: 'การคำนวณพิกัดกึ่งกลาง X, Y และควบคุมอุปกรณ์ขับเคลื่อน (Actuator) ในการคัดแยก' },
    { ch: 10, file: 'classification_train.py', desc: 'การจำแนกภาพแบบ Live Stream ผ่านกล้องเว็บแคม' },
    { ch: 11, file: 'kws_features.py', desc: 'การแปลงเสียงเป็น MFCC Spectrogram รู้จำคำสั่งเสียงภาษาไทย' },
    { ch: 12, file: 'multi_ai_live.py', desc: 'การประมวลผลระบบปัญญาประดิษฐ์พหุโมดอล (ภาพและเสียง) และการสร้างรายงานสถิติผ่านคำสั่ง SQL' }
  ];

  container.innerHTML = codeSnippets.map(c => {
    return `
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex flex-col justify-between hover:border-[#173b6b] transition">
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold px-2.5 py-0.5 rounded bg-slate-100 text-slate-700">${c.ch === 0 ? 'โหมดจำลอง (PC)' : `บทที่ ${c.ch}`}</span>
            <span class="text-[11px] font-mono text-[#173b6b] bg-blue-50 px-2 py-0.5 rounded font-bold">${c.file}</span>
          </div>
          <h3 class="text-sm font-bold text-slate-900">${c.desc}</h3>
          <div class="mt-3 bg-[#0d2342] text-yellow-300 p-3 rounded-xl text-xs font-mono overflow-x-auto border border-slate-700">
            <pre><code># KT-Edu Edge AI Pipeline
import sqlite3, os, sys
${c.ch === 0 ? 'import cv2\nprint("PC Edge AI Webcam Simulator Ready")' : (c.ch === 3 ? 'conn = sqlite3.connect("edgeai_records.db")\nprint("Database-SQL Brick Ready")' : 'import edge_impulse_linux\nprint("Edge AI Inference Pipeline Ready")')}</code></pre>
          </div>
        </div>
        <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
          <span class="text-[11px] text-slate-400 font-mono">${c.ch === 0 ? 'code_examples/chapter00_simulation' : `code_examples/chapter${String(c.ch).padStart(2, '0')}`}</span>
          <button onclick="copyCodeSnippet('${c.file}', ${c.ch})" class="text-xs btn-depa-blue px-3 py-1.5 rounded-lg flex items-center gap-1.5 font-bold shadow-sm">
            <i class="fa-regular fa-copy text-[#fff200]"></i> คัดลอกโค้ด
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function copyCodeSnippet(fileName, chNum) {
  let snippet = `# ชุดคำสั่งรายวิชา ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว\n# ไฟล์: ${fileName}\nimport os, sys\nsys.stdout.reconfigure(encoding='utf-8')\nprint("KT-Edu Edge AI Execution")\n`;
  if (chNum === 0) {
    snippet += `# PC Webcam Simulator Mode\nimport cv2, sqlite3\nprint("Running Edge AI Simulation on Laptop/PC Webcam...")\ncap = cv2.VideoCapture(0)\n`;
  } else if (chNum === 3) {
    snippet += `# Database-SQL Brick\nimport sqlite3\nconn = sqlite3.connect('/home/arduino/.arduino-bricks/data/edgeai_records.db')\ncursor = conn.cursor()\ncursor.execute("CREATE TABLE IF NOT EXISTS ai_logs (id INTEGER PRIMARY KEY, status TEXT, score REAL)")\nconn.commit()\n`;
  }
  navigator.clipboard.writeText(snippet).then(() => {
    showToast(`คัดลอกชุดคำสั่ง ${fileName} ลงคลิปบอร์ดแล้ว`, 'success');
  });
}

// ==============================================================
// 8. MATERIALS & DATASETS
// ==============================================================
function renderMaterials() {
  const container = document.getElementById('materialsGrid');
  if (!container) return;

  const typeIconMap = {
    slide: '<i class="fa-solid fa-file-pdf text-red-600"></i>',
    dataset: '<i class="fa-solid fa-images text-[#173b6b]"></i>',
    code: '<i class="fa-solid fa-code text-indigo-600"></i>',
    doc: '<i class="fa-solid fa-book text-amber-600"></i>'
  };

  container.innerHTML = state.materials.map(m => {
    return `
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex flex-col justify-between hover:border-[#173b6b] transition">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="text-2xl">${typeIconMap[m.type] || '<i class="fa-solid fa-file"></i>'}</span>
            <span class="text-[11px] uppercase tracking-wider font-bold text-[#173b6b] bg-blue-50 px-2 py-0.5 rounded">${m.type}</span>
          </div>
          <h3 class="text-sm font-bold text-slate-900 leading-snug">${m.title}</h3>
          <p class="text-xs text-slate-500 mt-2 font-mono break-all">${m.chapter_id}</p>
        </div>
        <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
          <a href="${m.url}" target="_blank" class="text-xs btn-depa-blue px-3 py-1.5 rounded-lg flex items-center gap-1.5 font-bold shadow-sm">
            <i class="fa-solid fa-cloud-arrow-down text-[#fff200]"></i> เปิดเอกสาร / ดาวน์โหลด
          </a>
          ${state.currentRole === 'admin' ? `
            <button onclick="deleteMaterial('${m.id}')" class="text-xs text-red-600 hover:bg-red-50 p-1.5 rounded" title="ลบสื่อ">
              <i class="fa-solid fa-trash"></i>
            </button>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

async function handleSaveMaterial(e) {
  e.preventDefault();
  const payload = {
    chapter_id: document.getElementById('materialFormChapter').value,
    type: document.getElementById('materialFormType').value,
    title: document.getElementById('materialFormTitle').value.trim(),
    url: document.getElementById('materialFormUrl').value.trim()
  };

  try {
    const res = await fetch('/api/materials', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload)
    });
    const json = await res.json();
    if (json.status === 'success') {
      showToast('เพิ่มสื่อการสอนเรียบร้อยแล้ว', 'success');
      closeModal('materialModal');
      await fetchAllData();
      renderMaterials();
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการบันทึกสื่อ', 'error');
  }
}

async function deleteMaterial(id) {
  if (!confirm('ยืนยันลบสื่อการสอนนี้หรือไม่?')) return;
  try {
    const res = await fetch(`/api/materials/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    const json = await res.json();
    if (json.status === 'success') {
      showToast('ลบสื่อเรียบร้อยแล้ว', 'success');
      await fetchAllData();
      renderMaterials();
    }
  } catch (err) {
    showToast('ลบไม่สำเร็จ', 'error');
  }
}

// ==============================================================
// 9. SCORES & GRADEBOOK (สมุดบันทึกคะแนน & ประวัติการส่งงาน)
// ==============================================================
let currentScoresSubTab = 'scores'; // 'scores' or 'submissions'
let scoresSearchQuery = '';
let scoresCategoryFilter = 'all';

function switchScoresSubTab(tab) {
  currentScoresSubTab = tab;
  const btnScores = document.getElementById('scoresSubTabBtn-scores');
  const btnSubs = document.getElementById('scoresSubTabBtn-submissions');
  const panelScores = document.getElementById('scoresViewPanel-scores');
  const panelSubs = document.getElementById('scoresViewPanel-submissions');

  if (tab === 'scores') {
    if (btnScores) {
      btnScores.className = 'px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-[#173b6b] text-white shadow-sm';
    }
    if (btnSubs) {
      btnSubs.className = 'px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 text-slate-600 hover:text-slate-900';
    }
    if (panelScores) panelScores.classList.remove('hidden');
    if (panelSubs) panelSubs.classList.add('hidden');
  } else {
    if (btnScores) {
      btnScores.className = 'px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 text-slate-600 hover:text-slate-900';
    }
    if (btnSubs) {
      btnSubs.className = 'px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-[#173b6b] text-white shadow-sm';
    }
    if (panelScores) panelScores.classList.add('hidden');
    if (panelSubs) panelSubs.classList.remove('hidden');
  }
  renderScores();
}

function onAdminScoresSearch(val) {
  scoresSearchQuery = (val || '').trim().toLowerCase();
  renderScores();
}

function onAdminScoresCategoryFilter(val) {
  scoresCategoryFilter = val || 'all';
  renderScores();
}

function renderScores() {
  const gatekeeper = document.getElementById('scoresGatekeeperLock');
  const scoresContent = document.getElementById('scoresContentArea');
  const tbodyScores = document.getElementById('scoresTableBody');
  const tbodySubs = document.getElementById('submissionsTableBody');

  // If not logged in (neither student nor admin), enforce privacy gatekeeper
  if (!isLoggedIn()) {
    if (gatekeeper) gatekeeper.classList.remove('hidden');
    if (scoresContent) scoresContent.classList.add('hidden');
    return;
  }

  if (gatekeeper) gatekeeper.classList.add('hidden');
  if (scoresContent) scoresContent.classList.remove('hidden');

  const currentStudentId = state.currentUser ? state.currentUser.student_id : null;
  const isAdmin = (state.currentRole === 'admin' && !!sessionStorage.getItem('edgeai_admin_token'));

  // 1. Update Title, Subtitle, and Privacy Badge
  const titleEl = document.getElementById('scoresSectionTitle');
  const subtitleEl = document.getElementById('scoresSectionSubtitle');
  const privacyBadge = document.getElementById('scoresPrivacyBadge');
  const adminFilterControls = document.getElementById('adminScoresFilterControls');

  if (titleEl && subtitleEl) {
    if (isAdmin) {
      titleEl.textContent = 'สมุดบันทึกคะแนนรวมทั้งห้องเรียน (Class Gradebook - ม.5/12)';
      subtitleEl.textContent = 'ผลคะแนนสอบปรนัย กลางภาค ปลายภาค และผลการประเมินภาคปฏิบัติของนักเรียนทุกคน (30 คน)';
      if (privacyBadge) privacyBadge.classList.add('hidden');
      if (adminFilterControls) adminFilterControls.classList.remove('hidden');
    } else {
      titleEl.textContent = 'สมุดบันทึกผลการเรียนและการส่งงานส่วนบุคคล';
      subtitleEl.textContent = `🔒 ระบบแสดงเฉพาะข้อมูลผลการเรียนและการส่งงานของคุณ (${escapeHtml(state.currentUser?.name || '')} - ${escapeHtml(currentStudentId || '')}) ตามมาตรฐาน PDPA`;
      if (privacyBadge) {
        privacyBadge.classList.remove('hidden');
        privacyBadge.style.display = 'inline-flex';
      }
      if (adminFilterControls) adminFilterControls.classList.add('hidden');
    }
  }

  // 2. Render personalized Student Scorecard if logged in as student
  const studentSummaryContainer = document.getElementById('studentPersonalScorecard');
  if (studentSummaryContainer) {
    if (currentStudentId && !isAdmin) {
      const myScores = (state.scores || []).filter(s => s.student_id === currentStudentId);
      const totalScore = myScores.reduce((acc, curr) => acc + (parseFloat(curr.score) || 0), 0);
      const mySubs = (state.submissions || []).filter(s => s.student_id === currentStudentId);
      
      studentSummaryContainer.classList.remove('hidden');
      studentSummaryContainer.innerHTML = `
        <div class="bg-gradient-to-r from-[#173b6b] to-[#0d2342] text-white p-6 rounded-2xl shadow-md border-b-4 border-[#fff200]">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3.5">
              <div class="w-12 h-12 rounded-2xl bg-[#fff200] text-[#173b6b] flex items-center justify-center text-xl font-black shadow">
                <i class="fa-solid fa-user-graduate"></i>
              </div>
              <div>
                <div class="text-xs text-yellow-300 font-mono font-bold">${escapeHtml(state.currentUser.student_id)} • ห้อง ${escapeHtml(state.currentUser.class_room || 'ม.5/12')}</div>
                <h3 class="text-lg font-black text-white">${escapeHtml(state.currentUser.name)}</h3>
                <div class="text-xs text-slate-300">สมุดบันทึกคะแนนสะสมและผลการประเมินส่วนบุคคล (เฉพาะตนเอง)</div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <div class="bg-white/10 px-4 py-2 rounded-xl border border-white/15 text-center">
                <div class="text-[11px] text-slate-300">ข้อสอบที่ทำแล้ว</div>
                <div class="text-base font-black text-yellow-300">${myScores.length} ชุด</div>
              </div>
              <div class="bg-white/10 px-4 py-2 rounded-xl border border-white/15 text-center">
                <div class="text-[11px] text-slate-300">ใบงานที่ส่งแล้ว</div>
                <div class="text-base font-black text-emerald-400">${mySubs.length} งาน</div>
              </div>
              <div class="bg-white/10 px-4 py-2 rounded-xl border border-white/15 text-center">
                <div class="text-[11px] text-slate-300">คะแนนสะสมรวม</div>
                <div class="text-base font-black text-white">${totalScore.toFixed(1)} <span class="text-xs font-normal text-yellow-200">คะแนน</span></div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else {
      studentSummaryContainer.classList.add('hidden');
      studentSummaryContainer.innerHTML = '';
    }
  }

  const categoryMap = {
    chapter_quiz: '<span class="px-2.5 py-0.5 rounded text-[11px] bg-yellow-100 text-[#173b6b] font-bold border border-yellow-300">ข้อสอบท้ายบท</span>',
    midterm: '<span class="px-2.5 py-0.5 rounded text-[11px] bg-blue-100 text-[#173b6b] font-bold border border-blue-300">กลางภาคเรียน</span>',
    final: '<span class="px-2.5 py-0.5 rounded text-[11px] bg-indigo-100 text-indigo-800 font-bold border border-indigo-300">ปลายภาคเรียน</span>',
    practical: '<span class="px-2.5 py-0.5 rounded text-[11px] bg-emerald-100 text-emerald-800 font-bold border border-emerald-300">ข้อสอบปฏิบัติ</span>',
    worksheet: '<span class="px-2.5 py-0.5 rounded text-[11px] bg-indigo-100 text-indigo-800 font-bold border border-indigo-300">ใบงานปฏิบัติการ</span>'
  };

  // 3. Render Table Header dynamically based on role
  const tableHeaderRow = document.getElementById('scoresTableHeaderRow');
  if (tableHeaderRow) {
    if (isAdmin) {
      tableHeaderRow.innerHTML = `
        <th class="px-4 py-3.5">รหัสนักเรียน</th>
        <th class="px-4 py-3.5">ชื่อ-นามสกุล</th>
        <th class="px-4 py-3.5">ประเภทการสอบ</th>
        <th class="px-4 py-3.5">ชุดข้อสอบ / บท</th>
        <th class="px-4 py-3.5 text-center">คะแนนที่ได้</th>
        <th class="px-4 py-3.5 text-center">ร้อยละ</th>
        <th class="px-4 py-3.5 text-right">วันเวลาที่บันทึก</th>
      `;
    } else {
      tableHeaderRow.innerHTML = `
        <th class="px-4 py-3.5">ประเภทการสอบ</th>
        <th class="px-4 py-3.5">ชุดข้อสอบ / บทเรียน</th>
        <th class="px-4 py-3.5 text-center">คะแนนที่ได้</th>
        <th class="px-4 py-3.5 text-center">ร้อยละ</th>
        <th class="px-4 py-3.5">ข้อเสนอแนะ / เกณฑ์</th>
        <th class="px-4 py-3.5 text-right">วันเวลาที่บันทึก</th>
      `;
    }
  }

  // 4. Render Scores Table (STRICT PDPA FILTER: นักเรียนดูได้เฉพาะของตนเองเท่านั้น)
  if (tbodyScores) {
    let list = (state.scores || []);
    if (!isAdmin) {
      list = list.filter(s => s.student_id === currentStudentId);
    } else {
      if (scoresSearchQuery) {
        list = list.filter(s => 
          (s.student_id && s.student_id.toLowerCase().includes(scoresSearchQuery)) ||
          (s.student_name && s.student_name.toLowerCase().includes(scoresSearchQuery)) ||
          (s.target_id && s.target_id.toLowerCase().includes(scoresSearchQuery))
        );
      }
      if (scoresCategoryFilter && scoresCategoryFilter !== 'all') {
        list = list.filter(s => s.exam_category === scoresCategoryFilter);
      }
    }

    if (list.length === 0) {
      const colSpan = isAdmin ? 7 : 6;
      tbodyScores.innerHTML = `
        <tr>
          <td colspan="${colSpan}" class="px-6 py-12 text-center text-slate-400">
            <i class="fa-solid fa-clipboard-list text-3xl mb-2 text-slate-300 block"></i>
            <span class="text-xs font-bold">${isAdmin ? 'ไม่พบข้อมูลคะแนนตามเงื่อนไขที่ค้นหา' : 'ยังไม่มีบันทึกคะแนนในระบบ (ทำแบบทดสอบหรือส่งงานเพื่อรับคะแนนประเมิน)'}</span>
          </td>
        </tr>
      `;
    } else {
      tbodyScores.innerHTML = list.map(s => {
        const d = new Date(s.submitted_at || Date.now());
        const dateStr = d.toLocaleDateString('th-TH') + ' ' + d.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
        const isMe = currentStudentId && s.student_id === currentStudentId;
        const rowClass = isMe ? 'bg-yellow-50/60 font-semibold' : 'hover:bg-slate-50/50';

        if (isAdmin) {
          return `
            <tr class="${rowClass} transition">
              <td class="px-4 py-3.5 font-mono font-bold text-[#173b6b]">${escapeHtml(s.student_id)}</td>
              <td class="px-4 py-3.5 font-medium text-slate-900">${escapeHtml(s.student_name)}</td>
              <td class="px-4 py-3.5">${categoryMap[s.exam_category] || escapeHtml(s.exam_category)}</td>
              <td class="px-4 py-3.5 font-mono text-xs text-slate-600">${escapeHtml(s.target_id)}</td>
              <td class="px-4 py-3.5 text-center font-bold text-slate-900">${s.score} / ${s.max_score}</td>
              <td class="px-4 py-3.5 text-center font-extrabold ${s.percentage >= 80 ? 'text-emerald-700' : 'text-[#173b6b]'}">${s.percentage}%</td>
              <td class="px-4 py-3.5 text-right text-xs text-slate-400 font-mono">${dateStr}</td>
            </tr>
          `;
        } else {
          return `
            <tr class="hover:bg-slate-50/50 transition">
              <td class="px-4 py-3.5">${categoryMap[s.exam_category] || escapeHtml(s.exam_category)}</td>
              <td class="px-4 py-3.5 font-mono text-xs font-bold text-[#173b6b]">${escapeHtml(s.target_id)}</td>
              <td class="px-4 py-3.5 text-center font-bold text-slate-900 text-sm">${s.score} / ${s.max_score}</td>
              <td class="px-4 py-3.5 text-center font-extrabold ${s.percentage >= 80 ? 'text-emerald-700' : 'text-[#173b6b]'}">${s.percentage}%</td>
              <td class="px-4 py-3.5 text-xs text-slate-600">${escapeHtml(s.notes || '-')}</td>
              <td class="px-4 py-3.5 text-right text-xs text-slate-400 font-mono">${dateStr}</td>
            </tr>
          `;
        }
      }).join('');
    }
  }

  // 5. Render Submissions Table (STRICT PDPA FILTER: นักเรียนดูได้เฉพาะของตนเองเท่านั้น)
  if (tbodySubs) {
    let subList = (state.submissions || []);
    if (!isAdmin) {
      subList = subList.filter(s => s.student_id === currentStudentId);
    } else {
      if (scoresSearchQuery) {
        subList = subList.filter(s =>
          (s.student_id && s.student_id.toLowerCase().includes(scoresSearchQuery)) ||
          (s.student_name && s.student_name.toLowerCase().includes(scoresSearchQuery)) ||
          (s.chapter_id && s.chapter_id.toLowerCase().includes(scoresSearchQuery))
        );
      }
    }

    if (subList.length === 0) {
      tbodySubs.innerHTML = `
        <tr>
          <td colspan="6" class="px-6 py-12 text-center text-slate-400">
            <i class="fa-solid fa-folder-open text-3xl mb-2 text-slate-300 block"></i>
            <span class="text-xs font-bold">${isAdmin ? 'ไม่พบข้อมูลการส่งงานตามเงื่อนไข' : 'ยังไม่มีประวัติการส่งรายงานหรือใบงานของคุณ (สามารถส่งงานได้ที่แท็บ "ใบงาน & ข้อสอบปฏิบัติ")'}</span>
          </td>
        </tr>
      `;
    } else {
      tbodySubs.innerHTML = subList.map(sub => {
        const d = new Date(sub.submitted_at || Date.now());
        const dateStr = d.toLocaleDateString('th-TH') + ' ' + d.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
        const isWorksheet = sub.task_type === 'worksheet';
        const taskTypeBadge = isWorksheet
          ? '<span class="px-2.5 py-0.5 rounded text-[11px] bg-indigo-100 text-indigo-800 font-bold border border-indigo-300"><i class="fa-solid fa-file-lines mr-1 text-indigo-600"></i>ใบงานประจำบท</span>'
          : '<span class="px-2.5 py-0.5 rounded text-[11px] bg-amber-100 text-amber-800 font-bold border border-amber-300"><i class="fa-solid fa-microchip mr-1 text-amber-600"></i>โจทย์ข้อสอบปฏิบัติ</span>';

        // Check if graded
        const category = isWorksheet ? 'worksheet' : 'practical';
        const matchedScore = (state.scores || []).find(sc => sc.student_id === sub.student_id && (sc.chapter_id === sub.chapter_id || sc.target_id === sub.chapter_id || sc.target_id?.includes(sub.chapter_id)) && sc.exam_category === category);

        const statusBadge = matchedScore
          ? `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 inline-flex items-center gap-1"><i class="fa-solid fa-circle-check text-emerald-600"></i>ตรวจแล้ว (${matchedScore.score}/10)</span>`
          : `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300 inline-flex items-center gap-1"><i class="fa-solid fa-clock text-amber-600"></i>รอตรวจให้คะแนน</span>`;

        return `
          <tr class="hover:bg-slate-50/50 transition">
            <td class="px-4 py-3.5 font-bold text-[#173b6b]">${escapeHtml(sub.chapter_id)}</td>
            <td class="px-4 py-3.5">${taskTypeBadge}</td>
            <td class="px-4 py-3.5 font-mono text-xs">
              <a href="${escapeHtml(sub.report_url)}" target="_blank" class="text-blue-600 hover:text-blue-800 underline font-bold inline-flex items-center gap-1 max-w-xs truncate" title="${escapeHtml(sub.report_url)}">
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> ${escapeHtml(sub.report_url)}
              </a>
            </td>
            <td class="px-4 py-3.5 text-xs text-slate-500 font-mono">${dateStr}</td>
            <td class="px-4 py-3.5 text-center">${statusBadge}</td>
            <td class="px-4 py-3.5 text-right text-xs text-slate-600">${escapeHtml(matchedScore?.notes || sub.notes || '-')}</td>
          </tr>
        `;
      }).join('');
    }
  }
}

function exportScoresCSV() {
  const currentStudentId = state.currentUser ? state.currentUser.student_id : null;
  const isAdmin = (state.currentRole === 'admin' && !!sessionStorage.getItem('edgeai_admin_token'));

  // Strict PDPA: นักเรียนส่งออกได้เฉพาะข้อมูลคะแนนของตนเองเท่านั้น
  const list = isAdmin
    ? (state.scores || [])
    : (state.scores || []).filter(s => s.student_id === currentStudentId);

  if (list.length === 0) {
    showToast('ไม่มีข้อมูลคะแนนสำหรับส่งออก', 'error');
    return;
  }

  let csv = '\uFEFFรหัสนักเรียน,ชื่อ-นามสกุล,ประเภทการสอบ,ชุดข้อสอบ,คะแนนที่ได้,คะแนนเต็ม,ร้อยละ,วันเวลาที่บันทึก\n';
  list.forEach(s => {
    csv += `"${s.student_id}","${s.student_name}","${s.exam_category}","${s.target_id}",${s.score},${s.max_score},${s.percentage},"${s.submitted_at}"\n`;
  });

  const filename = isAdmin
    ? `KT_Edu_EdgeAI_Scorebook_Class_All_${new Date().toISOString().slice(0, 10)}.csv`
    : `KT_Edu_EdgeAI_Scorebook_${currentStudentId}_${new Date().toISOString().slice(0, 10)}.csv`;

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  showToast(isAdmin ? 'ส่งออกรายงานคะแนนรวมทั้งห้องสำเร็จ' : 'ส่งออกรายงานคะแนนส่วนบุคคลสำเร็จ', 'success');
}

// ==============================================================
// 10. ADMIN CMS MANAGEMENT (CRUD บทเรียน & ข้อสอบ)
// ==============================================================
let currentAdminSubTab = 'grading';
let adminSubFilter = 'all'; // 'all', 'practical', 'worksheet'
let adminSubSearch = '';

function switchAdminSubTab(subTabName) {
  const tabs = ['grading', 'submissions', 'practical', 'worksheets', 'lessons', 'quizzes', 'overview', 'settings'];
  if (!tabs.includes(subTabName)) subTabName = 'grading';
  currentAdminSubTab = subTabName;

  // Toggle content visibility and button styles
  tabs.forEach(tab => {
    const content = document.getElementById(`adminSubContent-${tab}`);
    const btn = document.getElementById(`adminSubBtn-${tab}`);
    if (content) {
      if (tab === subTabName) {
        content.classList.remove('hidden');
      } else {
        content.classList.add('hidden');
      }
    }
    if (btn) {
      if (tab === subTabName) {
        btn.className = "admin-sub-tab px-3.5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-[#173b6b] text-white shadow-sm";
      } else {
        btn.className = "admin-sub-tab px-3.5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-700 hover:bg-white/60";
      }
    }
  });

  // Sub-tab specific actions
  if (subTabName === 'grading') {
    renderGradingStudentRoster();
    onGradeStudentChange();
    triggerLiveSheetSync(false);
  } else if (subTabName === 'practical') {
    renderAdminPractical();
  } else if (subTabName === 'worksheets') {
    renderAdminWorksheets();
  } else if (subTabName === 'submissions') {
    renderAdminSubmissions();
    triggerLiveSheetSync(false);
  } else if (subTabName === 'quizzes') {
    renderAdminQuizzes();
  } else if (subTabName === 'settings') {
    loadGoogleSheetConfig();
  }
}

function filterAdminSubmissions(type) {
  adminSubFilter = type;
  const pills = {
    all: document.getElementById('subFilterBtn-all'),
    practical: document.getElementById('subFilterBtn-practical'),
    worksheet: document.getElementById('subFilterBtn-worksheet')
  };

  Object.entries(pills).forEach(([key, el]) => {
    if (!el) return;
    if (key === type) {
      el.className = "sub-filter-pill active text-xs font-bold px-3 py-1.5 rounded-lg bg-[#173b6b] text-white shadow-sm transition";
    } else {
      el.className = "sub-filter-pill text-xs font-bold px-3 py-1.5 rounded-lg bg-white text-slate-700 hover:bg-slate-100 border border-slate-200 transition";
    }
  });

  renderAdminSubmissions();
}

function searchAdminSubmissions(query) {
  adminSubSearch = (query || '').trim().toLowerCase();
  renderAdminSubmissions();
}

function renderAdminCMS() {
  if (state.stats) {
    const lCount = document.getElementById('statLessonsCount');
    if (lCount) lCount.textContent = state.lessons.length;
    const qCount = document.getElementById('statQuizzesCount');
    if (qCount) qCount.textContent = state.quizzes.length;
    const pCount = document.getElementById('statPracticalCount');
    if (pCount) pCount.textContent = state.practicalExams.length;
    const avg = document.getElementById('statAvgScore');
    if (avg) avg.textContent = `${state.stats.avgPercentage || 0}%`;
  }

  // Admin Pill Badges
  const pBadge = document.getElementById('adminPracticalCount');
  if (pBadge) pBadge.textContent = `${state.practicalExams.length} บท`;
  const wBadge = document.getElementById('adminWorksheetsCount');
  if (wBadge) wBadge.textContent = `${state.worksheets.length} บท`;

  // Admin Lessons List
  const adminLessonsEl = document.getElementById('adminLessonsList');
  if (adminLessonsEl) {
    adminLessonsEl.innerHTML = state.lessons.map(l => `
      <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between text-xs hover:border-[#173b6b] transition">
        <div>
          <span class="font-bold text-slate-800">บทที่ ${l.chapter_number}: ${l.title}</span>
          <div class="text-[11px] text-slate-400 font-mono">${l.id} | ${l.duration_hours} คาบ</div>
        </div>
        <div class="flex space-x-1.5">
          <button onclick="prepareEditLesson('${l.id}')" class="px-2.5 py-1 bg-blue-100 text-[#173b6b] hover:bg-blue-200 rounded font-bold">แก้ไข</button>
          <button onclick="deleteLesson('${l.id}')" class="px-2.5 py-1 bg-red-100 text-red-700 hover:bg-red-200 rounded font-bold">ลบ</button>
        </div>
      </div>
    `).join('');
  }

  renderAdminPractical();
  renderAdminWorksheets();
  renderAdminQuizzes();
  renderAdminSubmissions();
  loadGoogleSheetConfig();
  switchAdminSubTab(currentAdminSubTab);
}

function renderAdminPractical() {
  const container = document.getElementById('adminPracticalList');
  const countBadge = document.getElementById('adminPracticalTotalCount');
  if (!container) return;

  const search = (document.getElementById('adminPracticalSearchInput')?.value || '').trim().toLowerCase();
  let list = state.practicalExams || [];

  if (countBadge) countBadge.textContent = `${list.length} บท`;

  if (search) {
    list = list.filter(p => {
      const rubricsText = formatRubricsText(p.rubrics);
      const str = `${p.title || ''} ${p.scenario || p.description || ''} ${rubricsText} ${p.chapter_id || ''} ${p.unit_number || ''}`.toLowerCase();
      return str.includes(search);
    });
  }

  if (list.length === 0) {
    container.innerHTML = `
      <div class="p-8 bg-slate-50 rounded-2xl border border-slate-200 text-center text-slate-400">
        <i class="fa-solid fa-microchip text-3xl mb-2 text-slate-300"></i>
        <div class="text-xs font-bold">ไม่พบข้อมูลโจทย์ข้อสอบปฏิบัติ</div>
        <button onclick="prepareCreatePractical()" class="mt-3 btn-depa-blue text-xs font-bold px-3 py-1.5 rounded-lg inline-flex items-center gap-1">
          <i class="fa-solid fa-plus text-[#fff200]"></i> เพิ่มโจทย์ใหม่
        </button>
      </div>
    `;
    return;
  }

  const sorted = [...list].sort((a, b) => (parseInt(a.unit_number) || 0) - (parseInt(b.unit_number) || 0));

  container.innerHTML = sorted.map(p => {
    const rubricsText = formatRubricsText(p.rubrics);
    const rubricsLines = rubricsText.split('\n').filter(line => line.trim()).map(line => {
      return `<li class="text-[11px] text-slate-600 list-disc list-inside leading-snug">${escapeHtml(line.replace(/^\*\s*/, ''))}</li>`;
    }).join('');

    return `
      <div class="p-4 bg-slate-50 hover:bg-white rounded-2xl border border-slate-200 hover:border-amber-400 hover:shadow-md transition space-y-3">
        <div class="flex flex-wrap items-start justify-between gap-2">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-amber-100 text-amber-800 border border-amber-300">
                บทที่ ${p.unit_number}
              </span>
              <span class="text-xs font-bold text-slate-500 font-mono">(${p.id} | ${p.chapter_id})</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-yellow-100 text-yellow-800">
                เต็ม ${p.max_score || 10} คะแนน
              </span>
            </div>
            <h4 class="text-sm font-bold text-[#173b6b] leading-snug">${escapeHtml(p.title)}</h4>
          </div>
          <div class="flex items-center space-x-1.5 flex-shrink-0">
            <button onclick="quickGradePractical('${p.id}')" class="px-2.5 py-1 bg-emerald-100 text-emerald-800 hover:bg-emerald-200 rounded-lg font-bold text-xs flex items-center gap-1 shadow-sm transition" title="ตรวจให้คะแนนนักเรียนในบทนี้">
              <i class="fa-solid fa-clipboard-check"></i> ตรวจงาน
            </button>
            <button onclick="prepareEditPractical('${p.id}')" class="px-2.5 py-1 bg-blue-100 text-[#173b6b] hover:bg-blue-200 rounded-lg font-bold text-xs flex items-center gap-1 transition">
              <i class="fa-solid fa-pen-to-square"></i> แก้ไข
            </button>
            <button onclick="deletePractical('${p.id}')" class="px-2.5 py-1 bg-red-100 text-red-700 hover:bg-red-200 rounded-lg font-bold text-xs flex items-center gap-1 transition">
              <i class="fa-solid fa-trash"></i> ลบ
            </button>
          </div>
        </div>

        ${p.scenario ? `
          <div class="bg-white p-3 rounded-xl border border-slate-200 text-xs text-slate-700 leading-relaxed space-y-1">
            <span class="font-bold text-[#173b6b] flex items-center gap-1">
              <i class="fa-solid fa-bullseye text-amber-600"></i> สถานการณ์ / ภารกิจ:
            </span>
            <p class="whitespace-pre-line text-slate-600 text-[11px]">${escapeHtml(p.scenario)}</p>
          </div>
        ` : ''}

        ${rubricsLines ? `
          <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-200 text-xs space-y-1">
            <span class="font-bold text-amber-900 flex items-center gap-1">
              <i class="fa-solid fa-list-check text-amber-700"></i> เกณฑ์การประเมินรูบริก 10 คะแนน:
            </span>
            <ul class="space-y-0.5 pt-0.5">
              ${rubricsLines}
            </ul>
          </div>
        ` : ''}

        ${p.code_reference ? `
          <div class="text-[11px] text-slate-500 font-mono flex items-center gap-1.5">
            <i class="fa-solid fa-code text-slate-400"></i>
            <span>โค้ดอ้างอิง:</span>
            <code class="bg-slate-200/70 text-slate-800 px-1.5 py-0.5 rounded text-[10px]">${escapeHtml(p.code_reference)}</code>
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function renderAdminWorksheets() {
  const container = document.getElementById('adminWorksheetsList');
  const countBadge = document.getElementById('adminWorksheetsTotalCount');
  if (!container) return;

  const search = (document.getElementById('adminWorksheetSearchInput')?.value || '').trim().toLowerCase();
  let list = state.worksheets || [];

  if (countBadge) countBadge.textContent = `${list.length} บท`;

  if (search) {
    list = list.filter(w => {
      const str = `${w.title || ''} ${w.instructions || ''} ${w.chapter_id || ''} ${w.chapter_number || ''}`.toLowerCase();
      return str.includes(search);
    });
  }

  if (list.length === 0) {
    container.innerHTML = `
      <div class="p-8 bg-slate-50 rounded-2xl border border-slate-200 text-center text-slate-400">
        <i class="fa-solid fa-file-lines text-3xl mb-2 text-slate-300"></i>
        <div class="text-xs font-bold">ไม่พบข้อมูลใบงานปฏิบัติการ</div>
        <button onclick="prepareCreateWorksheet()" class="mt-3 btn-depa-blue text-xs font-bold px-3 py-1.5 rounded-lg inline-flex items-center gap-1">
          <i class="fa-solid fa-plus text-[#fff200]"></i> เพิ่มใบงานใหม่
        </button>
      </div>
    `;
    return;
  }

  const sorted = [...list].sort((a, b) => (parseInt(a.chapter_number) || 0) - (parseInt(b.chapter_number) || 0));

  container.innerHTML = sorted.map(w => {
    const isActive = (w.status || 'active') === 'active';
    const statusBadge = isActive
      ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">เปิดใช้งาน (Active)</span>'
      : '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-200 text-slate-600">ฉบับร่าง (Draft)</span>';

    return `
      <div class="p-4 bg-slate-50 hover:bg-white rounded-2xl border border-slate-200 hover:border-indigo-400 hover:shadow-md transition space-y-3">
        <div class="flex flex-wrap items-start justify-between gap-2">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-indigo-100 text-indigo-800 border border-indigo-300">
                ใบงานที่ ${w.chapter_number}
              </span>
              <span class="text-xs font-bold text-slate-500 font-mono">(${w.id} | ${w.chapter_id})</span>
              <span class="text-xs text-slate-500 flex items-center gap-1 font-mono">
                <i class="fa-regular fa-clock"></i> ${w.time_minutes || 60} นาที
              </span>
              ${statusBadge}
            </div>
            <h4 class="text-sm font-bold text-[#173b6b] leading-snug">${escapeHtml(w.title)}</h4>
          </div>
          <div class="flex items-center space-x-1.5 flex-shrink-0">
            <button onclick="quickGradeWorksheetByChapter('${w.chapter_id}')" class="px-2.5 py-1 bg-amber-100 text-amber-900 hover:bg-amber-200 rounded-lg font-bold text-xs flex items-center gap-1 transition" title="ไปที่ห้องตรวจให้คะแนนใบงานนี้">
              <i class="fa-solid fa-file-signature text-amber-700"></i> ตรวจคะแนน
            </button>
            ${w.view_url || w.file_url ? `
              <a href="${escapeHtml(w.view_url || w.file_url)}" target="_blank" class="px-2.5 py-1 bg-indigo-100 text-indigo-800 hover:bg-indigo-200 rounded-lg font-bold text-xs flex items-center gap-1 shadow-sm transition">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> เปิดดูใบงาน
              </a>
            ` : ''}
            <button onclick="prepareEditWorksheet('${w.id}')" class="px-2.5 py-1 bg-blue-100 text-[#173b6b] hover:bg-blue-200 rounded-lg font-bold text-xs flex items-center gap-1 transition">
              <i class="fa-solid fa-pen-to-square"></i> แก้ไข
            </button>
            <button onclick="deleteWorksheet('${w.id}')" class="px-2.5 py-1 bg-red-100 text-red-700 hover:bg-red-200 rounded-lg font-bold text-xs flex items-center gap-1 transition">
              <i class="fa-solid fa-trash"></i> ลบ
            </button>
          </div>
        </div>

        ${w.instructions ? `
          <div class="bg-white p-3 rounded-xl border border-slate-200 text-xs text-slate-700 leading-relaxed space-y-1">
            <span class="font-bold text-indigo-900 flex items-center gap-1">
              <i class="fa-solid fa-clipboard-list text-indigo-600"></i> คำชี้แจง / ขั้นตอนกิจกรรม:
            </span>
            <p class="whitespace-pre-line text-slate-600 text-[11px]">${escapeHtml(w.instructions)}</p>
          </div>
        ` : ''}

        <div class="flex flex-wrap items-center gap-3 text-[11px] text-slate-500 pt-1">
          ${w.file_name ? `
            <span class="flex items-center gap-1 font-mono">
              <i class="fa-solid fa-file-pdf text-red-500"></i> ${escapeHtml(w.file_name)}
            </span>
          ` : ''}
          ${w.code_reference ? `
            <span class="flex items-center gap-1 font-mono">
              <i class="fa-solid fa-code text-slate-400"></i>
              <code class="bg-slate-200/70 text-slate-800 px-1.5 py-0.5 rounded text-[10px]">${escapeHtml(w.code_reference)}</code>
            </span>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function renderAdminQuizzes() {
  const container = document.getElementById('adminQuizzesList');
  if (!container) return;

  const catFilter = document.getElementById('adminQuizFilterCategory')?.value || 'all';
  let filtered = state.quizzes;
  if (catFilter !== 'all') {
    filtered = filtered.filter(q => q.category === catFilter);
  }

  container.innerHTML = filtered.slice(0, 30).map((q, idx) => {
    return `
      <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1.5">
        <div class="flex items-start justify-between gap-2">
          <span class="font-bold text-slate-800 leading-snug line-clamp-1">#${idx + 1} (${q.chapter_id}): ${q.question_text}</span>
          <div class="flex space-x-1 flex-shrink-0">
            <button onclick="prepareEditQuiz('${q.id}')" class="px-2.5 py-0.5 bg-blue-100 text-[#173b6b] rounded font-bold text-[11px]">แก้ไข</button>
            <button onclick="deleteQuiz('${q.id}')" class="px-2.5 py-0.5 bg-red-100 text-red-700 rounded font-bold text-[11px]">ลบ</button>
          </div>
        </div>
        <div class="text-[11px] text-emerald-800 font-bold">
          เฉลย: ข้อ ${q.correct_letter || 'ก'}. (${q.options ? q.options[q.correct_index] : ''})
        </div>
      </div>
    `;
  }).join('') + (filtered.length > 30 ? `<div class="text-center text-xs text-slate-400 py-2">แสดง 30 จากทั้งหมด ${filtered.length} ข้อ</div>` : '');
}

function renderAdminSubmissions() {
  const tbody = document.getElementById('adminSubmissionsTableBody');
  const countBadge = document.getElementById('adminSubmissionCount');
  if (!tbody) return;

  const rawList = state.submissions || [];

  // 1. Filter by type
  let filtered = rawList;
  if (adminSubFilter === 'practical') {
    filtered = filtered.filter(s => (s.task_type || 'practical') === 'practical');
  } else if (adminSubFilter === 'worksheet') {
    filtered = filtered.filter(s => s.task_type === 'worksheet');
  }

  // 2. Filter by search query
  if (adminSubSearch) {
    filtered = filtered.filter(s => {
      const practical = (state.practicalExams || []).find(p => p.chapter_id === s.chapter_id);
      const unitTitle = practical ? `บทที่ ${practical.unit_number}: ${practical.title}` : (s.chapter_id || '');
      const str = `${s.student_id || ''} ${s.student_name || ''} ${s.chapter_id || ''} ${unitTitle} ${s.notes || ''}`.toLowerCase();
      return str.includes(adminSubSearch);
    });
  }

  // Update badge counter
  if (countBadge) {
    if (filtered.length === rawList.length) {
      countBadge.textContent = `${rawList.length} งาน`;
    } else {
      countBadge.textContent = `${filtered.length} / ${rawList.length} งาน`;
    }
  }

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="p-6 text-center text-slate-400">
          <i class="fa-solid fa-inbox text-2xl mb-1 text-slate-300"></i><br>
          ${rawList.length === 0 ? 'ยังไม่มีข้อมูลการส่งรายงานหรือใบงานจากนักเรียน' : 'ไม่พบข้อมูลที่ตรงกับตัวกรองหรือคำค้นหา'}
        </td>
      </tr>
    `;
    return;
  }

  const sorted = [...filtered].sort((a, b) => new Date(b.submitted_at || 0) - new Date(a.submitted_at || 0));

  tbody.innerHTML = sorted.map(s => {
    const dStr = s.submitted_at ? new Date(s.submitted_at).toLocaleString('th-TH') : '-';
    const practical = (state.practicalExams || []).find(p => p.chapter_id === s.chapter_id);
    const unitTitle = practical ? `บทที่ ${practical.unit_number}: ${practical.title}` : s.chapter_id;
    const isWorksheet = s.task_type === 'worksheet';
    const typeBadge = isWorksheet
      ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800 border border-indigo-200 whitespace-nowrap"><i class="fa-solid fa-file-lines mr-1 text-indigo-600"></i>ใบงานประจำบท</span>'
      : '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-200 whitespace-nowrap"><i class="fa-solid fa-microchip mr-1 text-amber-600"></i>โจทย์ปฏิบัติ</span>';

    return `
      <tr class="hover:bg-slate-50 transition">
        <td class="p-3 text-slate-500 font-mono text-[11px] whitespace-nowrap">${dStr}</td>
        <td class="p-3 font-bold text-[#173b6b] font-mono">${escapeHtml(s.student_id)}</td>
        <td class="p-3 font-medium text-slate-800 whitespace-nowrap">${escapeHtml(s.student_name)}</td>
        <td class="p-3 text-slate-700 max-w-[180px] truncate" title="${escapeHtml(unitTitle)}">${escapeHtml(unitTitle)}</td>
        <td class="p-3 whitespace-nowrap">${typeBadge}</td>
        <td class="p-3 max-w-[200px]">
          ${s.report_url ? `
            <a href="${escapeHtml(s.report_url)}" target="_blank" class="text-blue-600 hover:text-blue-800 underline font-mono flex items-center gap-1 font-bold truncate">
              <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> ${escapeHtml(s.report_url)}
            </a>
          ` : '<span class="text-slate-400">-</span>'}
        </td>
        <td class="p-3 text-slate-600 max-w-[180px] truncate" title="${escapeHtml(s.notes || '')}">${escapeHtml(s.notes || '-')}</td>
        <td class="p-3 text-right whitespace-nowrap">
          <button onclick="loadSubmissionToGrading('${s.student_id}', '${s.chapter_id}', '${s.task_type || 'practical'}')" class="btn-depa-blue text-[11px] font-bold px-2.5 py-1 rounded-lg shadow-sm">
            <i class="fa-solid fa-clipboard-check mr-1"></i> ตรวจ${s.task_type === 'worksheet' ? 'ใบงาน' : 'ปฏิบัติ'}
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function loadSubmissionToGrading(studentId, chapterId, taskType = 'practical') {
  switchTab('admin');
  switchAdminSubTab('grading');

  const practical = (state.practicalExams || []).find(p => p.chapter_id === chapterId);
  const unitSelect = document.getElementById('gradeUnitSelect');
  if (practical && unitSelect) {
    unitSelect.value = practical.id;
    onGradeUnitChange();
  }

  selectStudentForGrading(studentId);
  setGradingMode(taskType === 'worksheet' ? 'worksheet' : 'practical');

  setTimeout(() => {
    document.getElementById('activeStudentNameLabel')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 100);

  const taskTitle = taskType === 'worksheet' ? 'ใบงานปฏิบัติการ' : 'โจทย์ข้อสอบปฏิบัติ';
  showToast(`โหลดงาน ${taskTitle} ของ ${studentId} เข้าฟอร์มประเมินเรียบร้อย`, 'info');
}

function quickGradePractical(practicalId) {
  switchTab('admin');
  switchAdminSubTab('grading');
  setGradingMode('practical');
  const unitSelect = document.getElementById('gradeUnitSelect');
  if (unitSelect) {
    unitSelect.value = practicalId;
    onGradeUnitChange();
  }
  document.getElementById('activeStudentNameLabel')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  showToast('เข้าสู่แบบฟอร์มประเมินรูบริกข้อสอบปฏิบัติสำหรับบทเรียนนี้แล้ว', 'info');
}

function quickGradePracticalByChapter(chapterId) {
  const practical = (state.practicalExams || []).find(p => p.chapter_id === chapterId);
  if (practical) {
    quickGradePractical(practical.id);
  } else {
    switchTab('admin');
    switchAdminSubTab('grading');
    setGradingMode('practical');
  }
}

function quickGradeWorksheetByChapter(chapterId) {
  switchTab('admin');
  switchAdminSubTab('grading');
  setGradingMode('worksheet');
  const unitSelect = document.getElementById('gradeUnitSelect');
  const practical = (state.practicalExams || []).find(p => p.chapter_id === chapterId);
  if (practical && unitSelect) {
    unitSelect.value = practical.id;
    onGradeUnitChange();
  }
  document.getElementById('activeStudentNameLabel')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  showToast('เข้าสู่แบบฟอร์มตรวจให้คะแนนใบงานปฏิบัติการสำหรับบทเรียนนี้แล้ว', 'info');
}

async function loadGoogleSheetConfig() {
  try {
    const res = await fetch('/api/admin/google-sheet-config');
    const json = await res.json();
    if (json.status === 'success' && json.data) {
      const input = document.getElementById('googleSheetWebhookInput');
      if (input && json.data.webhook_url) {
        input.value = json.data.webhook_url;
      }
    }
  } catch (err) {
    console.warn('Load sheet config failed:', err.message);
  }
}

async function handleSaveGoogleSheetWebhook() {
  const input = document.getElementById('googleSheetWebhookInput');
  if (!input) return;
  const webhook_url = input.value.trim();

  try {
    const res = await fetch('/api/admin/google-sheet-config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-token': state.token || ''
      },
      body: JSON.stringify({ webhook_url })
    });
    const json = await res.json();
    if (json.status === 'success') {
      showToast('บันทึกการตั้งค่า Google Sheet Webhook สำเร็จแล้ว!', 'success');
    } else {
      showToast(json.message || 'เกิดข้อผิดพลาดในการบันทึก', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์', 'error');
  }
}

async function handleSyncAllToGoogleSheet() {
  try {
    showToast('กำลังส่งข้อมูลงานทั้งหมดไปยัง Google Sheet...', 'info');
    const res = await fetch('/api/admin/sync-all-submissions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-token': state.token || ''
      }
    });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
    } else {
      showToast(json.message || 'ซิงค์ไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการเชื่อมต่อ', 'error');
  }
}

function prepareCreateQuiz() {
  document.getElementById('quizModalTitle').textContent = 'เพิ่มข้อสอบใหม่เข้าสู่คลัง';
  document.getElementById('quizFormId').value = '';
  document.getElementById('quizFormCategory').value = 'chapter_quiz';
  document.getElementById('quizFormText').value = '';
  document.getElementById('quizFormOpt0').value = '';
  document.getElementById('quizFormOpt1').value = '';
  document.getElementById('quizFormOpt2').value = '';
  document.getElementById('quizFormOpt3').value = '';
  document.getElementById('quizFormCorrectIndex').value = '0';
  document.getElementById('quizFormPoints').value = '1';
  document.getElementById('quizFormExplanation').value = '';
  openModal('quizModal');
}

function prepareEditQuiz(id) {
  const quiz = state.quizzes.find(q => q.id === id);
  if (!quiz) return;

  document.getElementById('quizModalTitle').textContent = 'แก้ไขข้อสอบ';
  document.getElementById('quizFormId').value = quiz.id;
  document.getElementById('quizFormCategory').value = quiz.category || 'chapter_quiz';
  document.getElementById('quizFormChapter').value = quiz.chapter_id || 'ch01';
  document.getElementById('quizFormText').value = quiz.question_text;
  document.getElementById('quizFormOpt0').value = quiz.options[0] || '';
  document.getElementById('quizFormOpt1').value = quiz.options[1] || '';
  document.getElementById('quizFormOpt2').value = quiz.options[2] || '';
  document.getElementById('quizFormOpt3').value = quiz.options[3] || '';
  document.getElementById('quizFormCorrectIndex').value = quiz.correct_index !== undefined ? quiz.correct_index : 0;
  document.getElementById('quizFormPoints').value = quiz.points || 1;
  document.getElementById('quizFormExplanation').value = quiz.explanation || '';

  openModal('quizModal');
}

async function handleSaveQuiz(e) {
  e.preventDefault();
  const id = document.getElementById('quizFormId').value;
  const payload = {
    category: document.getElementById('quizFormCategory').value,
    chapter_id: document.getElementById('quizFormChapter').value,
    question_text: document.getElementById('quizFormText').value.trim(),
    options: [
      document.getElementById('quizFormOpt0').value.trim(),
      document.getElementById('quizFormOpt1').value.trim(),
      document.getElementById('quizFormOpt2').value.trim(),
      document.getElementById('quizFormOpt3').value.trim()
    ],
    correct_index: parseInt(document.getElementById('quizFormCorrectIndex').value, 10),
    points: parseInt(document.getElementById('quizFormPoints').value, 10),
    explanation: document.getElementById('quizFormExplanation').value.trim()
  };

  try {
    let res;
    if (id) {
      res = await fetch(`/api/quizzes/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    } else {
      res = await fetch('/api/quizzes', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    }

    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      closeModal('quizModal');
      await fetchAllData();
      renderAdminCMS();
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการบันทึกข้อสอบ', 'error');
  }
}

async function deleteQuiz(id) {
  if (!confirm('ยืนยันที่จะลบข้อสอบนี้ออกจากคลังหรือไม่?')) return;
  try {
    const res = await fetch(`/api/quizzes/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    const json = await res.json();
    if (json.status === 'success') {
      showToast('ลบข้อสอบออกจากคลังสำเร็จ', 'success');
      await fetchAllData();
      renderAdminCMS();
    }
  } catch (err) {
    showToast('ลบไม่สำเร็จ', 'error');
  }
}

// -------------------------------------------------------------
// 10.1 PRACTICAL EXAMS CRUD CONTROLLERS (โจทย์ข้อสอบปฏิบัติ)
// -------------------------------------------------------------
function prepareCreatePractical() {
  const nextUnit = state.practicalExams.length + 1;
  document.getElementById('practicalModalTitle').innerHTML = '<i class="fa-solid fa-microchip text-amber-300"></i> เพิ่มโจทย์ข้อสอบปฏิบัติใหม่';
  document.getElementById('practicalFormId').value = '';
  document.getElementById('practicalFormUnit').value = nextUnit;
  document.getElementById('practicalFormTitle').value = '';
  document.getElementById('practicalFormScenario').value = '';
  document.getElementById('practicalFormRubrics').value = '* การตรวจสอบและเตรียมสภาพแวดล้อมระบบ (3 คะแนน):\n* การเขียนโปรแกรมและการรันสคริปต์คำสั่ง (4 คะแนน):\n* การวิเคราะห์ผลลัพธ์และการเชื่อมโยง Edge AI (3 คะแนน):';
  document.getElementById('practicalFormCodeRef').value = `code_examples/chapter${String(nextUnit).padStart(2, '0')}/`;
  document.getElementById('practicalFormMaxScore').value = 10;

  const chSelect = document.getElementById('practicalFormChapter');
  if (chSelect && state.lessons.length > 0) {
    chSelect.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
    const targetCh = `ch${String(nextUnit).padStart(2, '0')}`;
    if (state.lessons.some(l => l.id === targetCh)) {
      chSelect.value = targetCh;
    }
  }

  openModal('practicalModal');
}

function prepareEditPractical(id) {
  const practical = state.practicalExams.find(p => p.id === id);
  if (!practical) return;

  document.getElementById('practicalModalTitle').innerHTML = '<i class="fa-solid fa-microchip text-amber-300"></i> แก้ไขโจทย์ข้อสอบปฏิบัติ';
  document.getElementById('practicalFormId').value = practical.id;
  document.getElementById('practicalFormUnit').value = practical.unit_number;
  document.getElementById('practicalFormTitle').value = practical.title;
  document.getElementById('practicalFormScenario').value = practical.scenario || practical.description || '';
  document.getElementById('practicalFormRubrics').value = formatRubricsText(practical.rubrics);
  document.getElementById('practicalFormCodeRef').value = practical.code_reference || '';
  document.getElementById('practicalFormMaxScore').value = practical.max_score || 10;

  const chSelect = document.getElementById('practicalFormChapter');
  if (chSelect && state.lessons.length > 0) {
    chSelect.innerHTML = state.lessons.map(l => `
      <option value="${l.id}" ${l.id === practical.chapter_id ? 'selected' : ''}>บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
  }

  openModal('practicalModal');
}

async function handleSavePractical(e) {
  e.preventDefault();
  const id = document.getElementById('practicalFormId').value;
  const payload = {
    unit_number: parseInt(document.getElementById('practicalFormUnit').value, 10),
    chapter_id: document.getElementById('practicalFormChapter').value,
    title: document.getElementById('practicalFormTitle').value.trim(),
    scenario: document.getElementById('practicalFormScenario').value.trim(),
    rubrics: document.getElementById('practicalFormRubrics').value.trim(),
    code_reference: document.getElementById('practicalFormCodeRef').value.trim(),
    max_score: parseInt(document.getElementById('practicalFormMaxScore').value, 10) || 10
  };

  try {
    let res;
    if (id) {
      res = await fetch(`/api/practical/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    } else {
      res = await fetch('/api/practical', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    }

    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      closeModal('practicalModal');
      await fetchAllData();
      populateDropdowns();
      renderAllViews();
    } else {
      showToast(json.message || 'บันทึกไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการบันทึกโจทย์ข้อสอบปฏิบัติ', 'error');
  }
}

async function deletePractical(id) {
  if (!confirm('ยืนยันที่จะลบโจทย์ข้อสอบปฏิบัตินี้หรือไม่? ข้อมูลเกณฑ์รูบริกที่เกี่ยวข้องจะถูกนำออก')) return;
  try {
    const res = await fetch(`/api/practical/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      await fetchAllData();
      populateDropdowns();
      renderAllViews();
    } else {
      showToast(json.message || 'ลบไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการลบโจทย์ปฏิบัติ', 'error');
  }
}

// -------------------------------------------------------------
// 10.2 LAB WORKSHEETS CRUD CONTROLLERS (ใบงานปฏิบัติการประจำบท)
// -------------------------------------------------------------
function prepareCreateWorksheet() {
  const nextNum = state.worksheets.length + 1;
  document.getElementById('worksheetModalTitle').innerHTML = '<i class="fa-solid fa-file-lines text-indigo-300"></i> เพิ่มใบงานปฏิบัติการใหม่';
  document.getElementById('worksheetFormId').value = '';
  document.getElementById('worksheetFormChapterNum').value = nextNum;
  document.getElementById('worksheetFormTitle').value = `ใบงานปฏิบัติการที่ ${nextNum}: `;
  document.getElementById('worksheetFormTime').value = 60;
  document.getElementById('worksheetFormInstructions').value = '';
  document.getElementById('worksheetFormFileName').value = `Lab_Worksheet_${String(nextNum).padStart(2, '0')}.pdf`;
  document.getElementById('worksheetFormFileUrl').value = `/worksheets/Lab_Worksheet_${String(nextNum).padStart(2, '0')}.pdf`;
  document.getElementById('worksheetFormViewUrl').value = `/worksheets/worksheet${String(nextNum).padStart(2, '0')}.html`;
  document.getElementById('worksheetFormCodeRef').value = `code_examples/chapter${String(nextNum).padStart(2, '0')}/`;
  document.getElementById('worksheetFormStatus').value = 'active';

  const chSelect = document.getElementById('worksheetFormChapter');
  if (chSelect && state.lessons.length > 0) {
    chSelect.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
    const targetCh = `ch${String(nextNum).padStart(2, '0')}`;
    if (state.lessons.some(l => l.id === targetCh)) {
      chSelect.value = targetCh;
    }
  }

  openModal('worksheetModal');
}

function prepareEditWorksheet(id) {
  const ws = state.worksheets.find(w => w.id === id);
  if (!ws) return;

  document.getElementById('worksheetModalTitle').innerHTML = '<i class="fa-solid fa-file-lines text-indigo-300"></i> แก้ไขใบงานปฏิบัติการ';
  document.getElementById('worksheetFormId').value = ws.id;
  document.getElementById('worksheetFormChapterNum').value = ws.chapter_number;
  document.getElementById('worksheetFormTitle').value = ws.title;
  document.getElementById('worksheetFormTime').value = ws.time_minutes || 60;
  document.getElementById('worksheetFormInstructions').value = ws.instructions || '';
  document.getElementById('worksheetFormFileName').value = ws.file_name || '';
  document.getElementById('worksheetFormFileUrl').value = ws.file_url || '';
  document.getElementById('worksheetFormViewUrl').value = ws.view_url || '';
  document.getElementById('worksheetFormCodeRef').value = ws.code_reference || '';
  document.getElementById('worksheetFormStatus').value = ws.status || 'active';

  const chSelect = document.getElementById('worksheetFormChapter');
  if (chSelect && state.lessons.length > 0) {
    chSelect.innerHTML = state.lessons.map(l => `
      <option value="${l.id}" ${l.id === ws.chapter_id ? 'selected' : ''}>บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
  }

  openModal('worksheetModal');
}

async function handleSaveWorksheet(e) {
  e.preventDefault();
  const id = document.getElementById('worksheetFormId').value;
  const payload = {
    chapter_number: parseInt(document.getElementById('worksheetFormChapterNum').value, 10),
    chapter_id: document.getElementById('worksheetFormChapter').value,
    title: document.getElementById('worksheetFormTitle').value.trim(),
    time_minutes: parseInt(document.getElementById('worksheetFormTime').value, 10) || 60,
    instructions: document.getElementById('worksheetFormInstructions').value.trim(),
    file_name: document.getElementById('worksheetFormFileName').value.trim(),
    file_url: document.getElementById('worksheetFormFileUrl').value.trim(),
    view_url: document.getElementById('worksheetFormViewUrl').value.trim(),
    code_reference: document.getElementById('worksheetFormCodeRef').value.trim(),
    status: document.getElementById('worksheetFormStatus').value
  };

  try {
    let res;
    if (id) {
      res = await fetch(`/api/worksheets/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    } else {
      res = await fetch('/api/worksheets', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      });
    }

    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      closeModal('worksheetModal');
      await fetchAllData();
      populateDropdowns();
      renderAllViews();
    } else {
      showToast(json.message || 'บันทึกไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการบันทึกใบงานปฏิบัติการ', 'error');
  }
}

async function deleteWorksheet(id) {
  if (!confirm('ยืนยันที่จะลบใบงานปฏิบัติการนี้หรือไม่?')) return;
  try {
    const res = await fetch(`/api/worksheets/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      await fetchAllData();
      populateDropdowns();
      renderAllViews();
    } else {
      showToast(json.message || 'ลบไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการลบใบงาน', 'error');
  }
}

async function confirmResetDatabase() {
  if (!confirm('คำเตือน: คุณต้องการคืนค่าฐานข้อมูลสู่ค่าเริ่มต้นมาตรฐานหรือไม่? ข้อมูลที่เพิ่มใหม่จะถูกแทนที่ด้วยข้อมูลตั้งต้นบทเรียนและข้อสอบ')) return;

  try {
    const res = await fetch('/api/reset-database', { method: 'POST', headers: getAuthHeaders() });
    const json = await res.json();
    if (json.status === 'success') {
      showToast(json.message, 'success');
      await fetchAllData();
      renderAllViews();
    } else {
      showToast(json.message || 'รีเซ็ตไม่สำเร็จ', 'error');
    }
  } catch (err) {
    showToast('เกิดข้อผิดพลาดในการรีเซ็ตข้อมูล', 'error');
  }
}

// ==============================================================
// 11. HELPERS & UTILITIES
// ==============================================================
function populateDropdowns() {
  // Populate Exam Chapter Select
  const examSelect = document.getElementById('examChapterSelect');
  if (examSelect && state.lessons.length > 0) {
    examSelect.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
  }

  // Populate Quiz Form Chapter Select
  const quizFormCh = document.getElementById('quizFormChapter');
  if (quizFormCh && state.lessons.length > 0) {
    quizFormCh.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('') + `
      <option value="midterm">ข้อสอบกลางภาคเรียน</option>
      <option value="final">ข้อสอบปลายภาคเรียน</option>
    `;
  }

  // Populate Practical Form Chapter Select
  const pracFormCh = document.getElementById('practicalFormChapter');
  if (pracFormCh && state.lessons.length > 0) {
    pracFormCh.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
  }

  // Populate Worksheet Form Chapter Select
  const wsFormCh = document.getElementById('worksheetFormChapter');
  if (wsFormCh && state.lessons.length > 0) {
    wsFormCh.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
  }

  // Populate Practical Unit Select
  const gradeUnitSelect = document.getElementById('gradeUnitSelect');
  if (gradeUnitSelect && state.practicalExams.length > 0) {
    gradeUnitSelect.innerHTML = state.practicalExams.map(p => `
      <option value="${p.id}">บทที่ ${p.unit_number}: ${p.title}</option>
    `).join('');
  }

  // Populate Student Select for Practical Grading
  const gradeStudentSelect = document.getElementById('gradeStudentSelect');
  if (gradeStudentSelect && state.students.length > 0) {
    gradeStudentSelect.innerHTML = state.students.map(s => `
      <option value="${s.student_id}">${s.student_id} - ${s.name} (${s.class_room || 'ม.5/12'})</option>
    `).join('');
  }

  if (gradeUnitSelect && gradeStudentSelect && state.practicalExams.length > 0 && state.students.length > 0) {
    try {
      renderGradingStudentRoster();
      onGradeStudentChange();
    } catch (e) {
      console.warn('Auto-init grading error:', e);
    }
  }

  // Populate Material Form Chapter
  const matFormCh = document.getElementById('materialFormChapter');
  if (matFormCh && state.lessons.length > 0) {
    matFormCh.innerHTML = state.lessons.map(l => `
      <option value="${l.id}">บทที่ ${l.chapter_number}: ${l.title}</option>
    `).join('');
  }
}

function handleUrlDeepLinking() {
  const urlParams = new URLSearchParams(window.location.search);
  const chapterParam = urlParams.get('chapter');
  const hash = window.location.hash;

  if (hash) {
    const tabName = hash.replace('#section-', '');
    const validTabs = ['lessons', 'quizzes', 'worksheets', 'practical', 'code', 'scores'];
    if (tabName === 'admin' && state.currentRole === 'admin') {
      switchTab('admin');
    } else if (validTabs.includes(tabName)) {
      switchTab(tabName);
    } else if (tabName === 'admin') {
      switchTab('lessons');
    }
  }

  if (chapterParam) {
    const chNum = parseInt(chapterParam, 10);
    const targetLesson = state.lessons.find(l => l.chapter_number === chNum);
    const targetChId = targetLesson ? targetLesson.id : `ch${String(chNum).padStart(2, '0')}`;

    // 1. Quizzes Tab Dropdown Auto-Select
    const examSelect = document.getElementById('examChapterSelect');
    if (examSelect) {
      examSelect.value = targetChId;
    }

    // 2. Worksheet Filter Auto-Select
    const wsFilter = document.getElementById('worksheetChapterFilter');
    if (wsFilter) {
      wsFilter.value = targetChId;
      if (typeof filterWorksheets === 'function') filterWorksheets();
    }

    // 3. Code Filter Auto-Select
    const codeFilter = document.getElementById('codeChapterFilter');
    if (codeFilter) {
      codeFilter.value = targetChId;
      if (typeof filterCodeCards === 'function') filterCodeCards();
    }

    // If navigated to quizzes, auto scroll smoothly to exam selection card
    if (hash === '#section-quizzes') {
      setTimeout(() => {
        const quizCard = document.getElementById('examChapterSelect');
        quizCard?.closest('.bg-white')?.scrollIntoView({ behavior: 'smooth' });
      }, 350);
    }
  }
}

function renderAllViews() {
  renderLessons();
  renderPracticalTasks();
  renderWorksheets();
  renderCodeCards();
  renderMaterials();
  renderScores();
  renderAdminCMS();
}

function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.remove('hidden');
}

function closeModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.add('hidden');
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  const colors = {
    success: 'bg-[#173b6b] text-white border-2 border-[#fff200]',
    error: 'bg-red-800 text-white border-2 border-red-400',
    info: 'bg-[#0d2342] text-white border border-slate-600'
  };

  toast.className = `toast px-4 py-3 rounded-xl shadow-2xl text-xs font-bold flex items-center space-x-2 border ${colors[type] || colors.info}`;
  toast.innerHTML = `
    <span class="text-[#fff200] font-black">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3500);
}


// Accessible Modal UX: ESC key listener and backdrop click listener
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const openModals = document.querySelectorAll('[id$="Modal"]:not(.hidden)');
    openModals.forEach(m => m.classList.add('hidden'));
  }
});

document.addEventListener('click', (e) => {
  if (e.target && e.target.id && e.target.id.endsWith('Modal') && !e.target.classList.contains('hidden')) {
    e.target.classList.add('hidden');
  }
});
