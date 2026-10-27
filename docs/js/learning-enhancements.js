/**
 * KT-Edu Digital Learning Platform - Learning Enhancements
 * รวมฟังก์ชันยกระดับประสบการณ์การเรียนรู้:
 * 1. In-Page YouTube Video Player Modal พร้อมระบบสลับตอน (Multi-Episode Switcher)
 * 2. Code Block Syntax Enhancement & One-Click Copy Button
 * 3. Deep-Linking Context Synchronization
 * 4. Facebook Profile Link & Social Integration
 */

// ==============================================================
// 1. DATA MAPPING: YOUTUBE VIDEOS ประจำบทเรียน (อ.ธนา)
// ==============================================================
const CHAPTER_VIDEOS = {
  1: {
    title: 'การเตรียมความพร้อมระบบและบอร์ดพัฒนา Arduino UNO Q',
    pdfUrl: 'https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434',
    defaultEp: 'Ep.01',
    episodes: [
      { id: 'oVg57hOrU4s', ep: 'Ep.01', label: 'ติดตั้ง App Lab', title: 'การติดตั้ง Arduino App Lab บนคอมพิวเตอร์', desc: 'ดาวน์โหลดและติดตั้ง Arduino App Lab, ติดตั้ง Qualcomm USB Driver, ตั้งค่าสิทธิ์ Firewall' },
      { id: 'IUrO0bfUvc0', ep: 'Ep.02', label: 'ติดตั้ง Debian Linux', title: 'การติดตั้งและตรวจสอบ Debian Linux OS บน UNO Q', desc: 'สถาปัตยกรรม Dual-Core Qualcomm Dragonwing QRB2210 และระบบปฏิบัติการ Debian 12 AArch64' },
      { id: 'cRO5jjGtE_k', ep: 'Ep.03', label: 'Initial Setup บอร์ด', title: 'การตั้งค่าเริ่มต้นบอร์ด Arduino UNO Q เพื่อใช้ App Lab', desc: 'การเชื่อมต่อสาย USB-C Data, mDNS discovery และการเชื่อมต่อเครือข่าย Wi-Fi/LAN' },
      { id: 'nO3FicIusQs', ep: 'Ep.04', label: 'สร้าง App บน App Lab', title: 'เริ่มต้นสร้างแอปพลิเคชันใช้งานร่วมกับ Arduino UNO Q', desc: 'การสร้างโปรเจกต์ใหม่, สถาปัตยกรรม Modular Brick และการรันแอปพลิเคชันทดสอบระบบ' },
      { id: '-X8y_aeMAFY', ep: 'Ep.29', label: 'เริ่มต้น Edge Impulse', title: 'เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI', desc: 'การเชื่อมต่อ Edge Impulse Studio, Data Acquisition และภาพรวม Data Pipeline' }
    ]
  },
  2: {
    title: 'สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุมฮาร์ดแวร์พื้นฐาน',
    pdfUrl: 'https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434',
    defaultEp: 'Ep.05',
    episodes: [
      { id: 'g4sF5nnsSeY', ep: 'Ep.05', label: 'การทำงาน App.run()', title: 'การทำงานของวงรอบประมวลผล App.run()', desc: 'โครงสร้างสถาปัตยกรรม Modular Brick และการทำงานของฟังก์ชัน App.run()' },
      { id: 'DVCrb6t5dls', ep: 'Ep.06', label: 'Single-Board & Linux', title: 'การโปรแกรมบอร์ด Single-Board Mode & Desktop Linux', desc: 'การโปรแกรมบอร์ดในโหมด Single-board Computer และ การเยี่ยมชมเดสก์ท็อป Linux' },
      { id: 'zu6CBc-GZpM', ep: 'Ep.07', label: 'Network Mode & CLI', title: 'การโปรแกรมบอร์ดในโหมดเครือข่ายไร้สาย (Network Mode)', desc: 'Network Mode และการสั่งงานผ่าน Command Line Interface' },
      { id: 'pcw_iF02Ros', ep: 'Ep.08', label: 'สร้าง App บน Console', title: 'เริ่มต้นสร้าง App เพื่อใช้งานแสดงข้อความบนคอนโซล', desc: 'การสร้างแอปพลิเคชันและการแสดงผลข้อความสถานะระบบ' },
      { id: '7JBtwM5m-YI', ep: 'Ep.09', label: 'ควบคุม LED Matrix (ตอน 1)', title: 'สร้าง App เพื่อใช้ควบคุมบอร์ด LED บนบอร์ด Arduino UNO Q ตอนที่ 1', desc: 'การควบคุม Digital I/O และการแสดงผลแผงไฟ LED Matrix เบื้องต้น' },
      { id: '36Z_RYn6pQI', ep: 'Ep.10', label: 'ควบคุม LED Matrix (ตอน 2)', title: 'สร้าง App เพื่อใช้ควบคุมบอร์ด LED บนบอร์ด Arduino UNO Q ตอนที่ 2', desc: 'การเขียนโค้ดแสดงผลแอนิเมชันและรูปภาพบน LED Matrix' },
      { id: 'PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU', ep: 'Playlist', label: 'เพลย์ลิสต์ฉบับเต็ม', isPlaylist: true, title: 'Modular Brick & Hardware I/O (Playlist Ep.05–12)', desc: 'เพลย์ลิสต์รวมทุกคลิปของบทเรียนสถาปัตยกรรม Modular Brick และ Hardware I/O' }
    ]
  },
  3: {
    title: 'การจัดการระบบฐานข้อมูลบนอุปกรณ์ด้วย Database-SQL Brick',
    pdfUrl: 'https://app.box.com/s/jk0x5i37qc670f0kmwuisougd3kj8j4p',
    defaultEp: 'Ep.16',
    episodes: [
      { id: 'N-tZirbAWCE', ep: 'Ep.16', label: 'Database-SQL Brick', title: 'รู้จักกับ "Database-SQL Brick" บน Arduino App Lab', desc: 'การใช้งาน SQLite Database Brick และการสร้างตารางบันทึกข้อมูล' },
      { id: 'MekwqhTuTzc', ep: 'Ep.17', label: 'Time Series Brick', title: 'รู้จักกับ "Database-Time Series Brick" บน Arduino App Lab', desc: 'การจัดการข้อมูลอนุกรมเวลาและการจัดเก็บบันทึกข้อมูลเชิงเวลา' }
    ]
  },
  4: {
    title: 'การจัดเตรียมชุดข้อมูลและการออกแบบขั้นตอนการประมวลผล (Data Pipeline) บน Edge Impulse',
    pdfUrl: 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
    defaultEp: 'Ep.29',
    episodes: [
      { id: '-X8y_aeMAFY', ep: 'Ep.29', label: 'Data Pipeline บน Studio', title: 'การออกแบบ Data Pipeline บน Edge Impulse Studio', desc: 'Data Acquisition, การแบ่ง Train/Test 80:20, Image Preprocessing 96x96' }
    ]
  },
  5: {
    title: 'การฝึกสอนโมเดลตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection)',
    pdfUrl: 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
    defaultEp: 'Ep.30',
    episodes: [
      { id: '1yEMEJnsrUY', ep: 'Ep.30', label: 'Visual Anomaly (FOMO-AD)', title: 'การฝึกสอนโมเดล Visual Anomaly Detection (FOMO-AD)', desc: 'หลักการ One-Class Learning และการคำนวณ Anomaly Score' }
    ]
  },
  6: {
    title: 'การนำโมเดล .eim ไปใช้งานและการกำหนดค่าไฟล์ app.yaml บนบอร์ดพัฒนา Arduino UNO Q',
    pdfUrl: 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
    defaultEp: 'Ep.33',
    episodes: [
      { id: '3mAwLsQjv6U', ep: 'Ep.33', label: 'Deploy ไฟล์ .eim', title: 'การนำโมเดล (.eim) สู่บอร์ด Arduino UNO Q', desc: 'การคอมไพล์ไบนารี AArch64 .eim และการคัดลอกลงไดเรกทอรี ei-models' },
      { id: '0g2F-s-7O2U', ep: 'Ep.35', label: 'ถ่ายซ่อมแก้ app.yaml', title: 'ถ่ายซ่อมการแก้ไขไฟล์ app.yaml', desc: 'การกำหนดค่า app.yaml ไวยากรณ์ตัวแปร variables ให้ถูกต้อง' }
    ]
  },
  7: {
    title: 'การประมวลผลโมเดลตรวจจับความผิดปกติจากภาพ และการบันทึกข้อมูลลง Database-SQL Brick',
    pdfUrl: 'https://app.box.com/s/5fc91neqpantexqez8yr9vjfv9fc5s6b',
    defaultEp: 'Ep.34',
    episodes: [
      { id: '5Xiz_W53yU0', ep: 'Ep.34', label: 'VAD Brick & Database-SQL', title: 'รู้จักกับ Visual Anomaly Detection Brick บน Arduino App Lab', desc: 'การรันโมเดล VAD แบบเรียลไทม์ และบันทึกผลลง Database-SQL' }
    ]
  },
  8: {
    title: 'การฝึกสอนโมเดลตรวจจับวัตถุด้วยสถาปัตยกรรม FOMO (Object Detection)',
    pdfUrl: 'https://app.box.com/s/13lyv179wa2fo0igkep1i977e13dv6kd',
    defaultEp: 'Ep.31',
    episodes: [
      { id: 'glQx9GTLEUI', ep: 'Ep.31', label: 'FOMO Object Detection', title: 'การฝึกสอนโมเดล AI ให้ใช้กับงาน Object Detection (FOMO)', desc: 'การกำหนด Bounding Box, โมเดล MobileNetV2 0.35 และ F1-Score' },
      { id: 'mkmYqMgfaUw', ep: 'Ep.18', label: 'Object Detection Brick', title: 'รู้จักกับ Object Detection Brick บน Arduino App Lab', desc: 'การประยุกต์ใช้งาน Object Detection Brick ร่วมกับกล้องบน UNO Q' }
    ]
  },
  9: {
    title: 'การนำโมเดล FOMO ไปใช้งานและการควบคุมอุปกรณ์ขับเคลื่อน (Actuator)',
    pdfUrl: 'https://app.box.com/s/13lyv179wa2fo0igkep1i977e13dv6kd',
    defaultEp: 'Ep.42',
    episodes: [
      { id: '6DlVYQzgrEw', ep: 'Ep.42', label: 'FOMO เว็บแคม & Actuator', title: 'Object Detection ผ่านกล้องเว็บแคม และคุม Actuator', desc: 'การสกัด Centroid X,Y และสั่งงานเซอร์โวมอเตอร์คัดแยกชิ้นงาน' },
      { id: 'glQx9GTLEUI', ep: 'Ep.31', label: 'ฝึกสอน FOMO Model', title: 'การฝึกสอนโมเดล Object Detection (FOMO)', desc: 'ทบทวนสถาปัตยกรรม FOMO สำหรับการระบุตำแหน่งวัตถุ' }
    ]
  },
  10: {
    title: 'การพัฒนาและประมวลผลโมเดลจำแนกประเภทภาพ (Image Classification)',
    pdfUrl: 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
    defaultEp: 'Ep.32',
    episodes: [
      { id: '3EmkC1QBZK0', ep: 'Ep.32', label: 'Image Classification Brick', title: 'การฝึกสอนโมเดล Image Classification (Brick)', desc: 'การเรียนรู้แบบถ่ายโอน Transfer Learning และคลาส Background' },
      { id: 'bLw9BH5RrFo', ep: 'Ep.43', label: 'ทดสอบผ่านเว็บแคม', title: 'Image Classification ผ่านกล้องเว็บแคม', desc: 'การทดสอบ Inference สดผ่านกล้องเว็บแคม' },
      { id: 'Hwm797kDhbE', ep: 'Ep.22', label: 'Classify Brick เบื้องต้น', title: 'รู้จักกับ Image Classification Brick บน Arduino App Lab', desc: 'การทำงานของ Image Classification Brick' }
    ]
  },
  11: {
    title: 'การประมวลผลสัญญาณเสียงและการฝึกสอนโมเดลรู้จำคำสั่งเสียง (Keyword Spotting: KWS)',
    pdfUrl: 'https://app.box.com/s/hh6m3noroe5dz932y7f6e0hklb6iuj21',
    defaultEp: 'Ep.44',
    episodes: [
      { id: 'CRpBHlDRh60', ep: 'Ep.44', label: 'KWS ไมโครโฟน คำสั่งไทย', title: 'Keyword Spotting ผ่านไมโครโฟน (คำสั่งไทย)', desc: 'การฝึกสอนและรู้จำคำสั่งเสียงภาษาไทยแบบเรียลไทม์' },
      { id: 'Lt5RQeWXZBA', ep: 'Ep.36', label: 'Keyword Spotting Brick', title: 'การฝึกสอนโมเดล Keyword Spotting (Brick)', desc: 'การสกัดสเปกโทรแกรม MFCC และการเทรนโมเดลเสียง' },
      { id: 'Ty9b9Zs9h-o', ep: 'Ep.37', label: 'KWS Brick ตอน 1', title: 'รู้จักกับ Keyword Spotting Brick ตอนที่ 1/2', desc: 'การกำหนดค่าไมโครโฟนและการสร้าง Brick' }
    ]
  },
  12: {
    title: 'การจำแนกเสียงเฉพาะทางและการบูรณาการระบบ Edge AI เชิงวิศวกรรม',
    pdfUrl: 'https://app.box.com/s/m1zd2ahqm8xb20ozfig7h4gow6rhjmi1',
    defaultEp: 'Ep.45',
    episodes: [
      { id: 'OSzculUyvaY', ep: 'Ep.45', label: 'Audio Class ไมโครโฟน', title: 'Audio Classification ผ่านไมโครโฟน', desc: 'การจำแนกเสียงเฉพาะทางในงานวิศวกรรม' },
      { id: '9R-vpS6F4jA', ep: 'Ep.39', label: 'Audio Classification Brick', title: 'การฝึกสอนโมเดล Audio Classification (Brick)', desc: 'การสร้างโมเดลจำแนกเสียงและระบบบำรุงรักษาเชิงคาดการณ์' },
      { id: '6xLtYZOkvfA', ep: 'Ep.40', label: 'Audio Class ตอน 1', title: 'รู้จักกับ Audio Classification Brick ตอนที่ 1/2', desc: 'การตั้งค่า Brick สำหรับเสียง Acoustic' }
    ]
  }
};

// ==============================================================
// 2. VIDEO MODAL IN-PAGE PLAYER WITH MULTI-EPISODE SWITCHER
// ==============================================================
function initVideoModal() {
  if (document.getElementById('inpageVideoModal')) return;

  const modalHtml = `
    <div id="inpageVideoModal" class="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-sm flex items-center justify-center p-3 sm:p-6 hidden transition-opacity duration-300">
      <div class="relative w-full max-w-4xl bg-slate-900 rounded-2xl shadow-2xl overflow-hidden border border-slate-700 flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-3.5 bg-[#0d2342] border-b border-white/10 text-white flex-wrap gap-2">
          <div class="flex items-center space-x-2.5">
            <span class="w-8 h-8 rounded-lg bg-red-600 text-white flex items-center justify-center font-bold text-xs shadow shrink-0">
              <i class="fa-brands fa-youtube"></i>
            </span>
            <div>
              <h4 id="inpageVideoTitle" class="text-xs sm:text-sm font-bold text-white line-clamp-1">คลิปการสอน อ.ธนา</h4>
              <div class="flex items-center gap-2 flex-wrap mt-0.5">
                <p id="inpageVideoSubtitle" class="text-[11px] text-yellow-300 font-mono">Arduino UNO Q & Edge AI Learning</p>
                <!-- Inline Episode badges (matching user requested + [ ] + [ ]) -->
                <div id="inpageVideoEpisodeInline" class="flex items-center gap-1"></div>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2 shrink-0">
            <a id="inpageVideoPdfLink" href="https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-lg bg-blue-600/80 hover:bg-blue-600 text-white text-xs font-semibold transition inline-flex items-center gap-1.5 shadow" title="ดาวน์โหลด/ดูเอกสารประกอบการบรรยาย (PDF)">
              <i class="fa-solid fa-file-pdf"></i> <span class="hidden sm:inline">เอกสาร</span> (PDF)
            </a>
            <a id="inpageVideoExternalLink" href="#" target="_blank" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-slate-200 text-xs font-semibold transition hidden sm:inline-flex items-center gap-1.5">
              <i class="fa-solid fa-arrow-up-right-from-square"></i> เปิดแท็บใหม่
            </a>
            <button onclick="closeVideoModal()" class="w-8 h-8 rounded-lg bg-white/10 hover:bg-red-600 text-slate-200 hover:text-white flex items-center justify-center transition" title="ปิดหน้าต่าง (Esc)">
              <i class="fa-solid fa-xmark text-sm"></i>
            </button>
          </div>
        </div>

        <!-- Episode Selector Bar (shown when multiple episodes exist) -->
        <div id="inpageVideoEpisodeBar" class="px-5 py-2.5 bg-[#09182d] border-b border-white/10 flex items-center gap-2 overflow-x-auto text-xs hidden">
          <span class="text-yellow-300 font-bold shrink-0 flex items-center gap-1 text-[11px]">
            <i class="fa-solid fa-film"></i> ตอนที่เกี่ยวข้อง:
          </span>
          <div id="inpageVideoEpisodes" class="flex items-center gap-1.5 overflow-x-auto py-0.5"></div>
        </div>

        <!-- 16:9 Video Player Container -->
        <div class="relative w-full aspect-video bg-black flex items-center justify-center">
          <iframe id="inpageVideoIframe" class="w-full h-full border-0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>

        <!-- Footer Bar -->
        <div class="px-5 py-2.5 bg-slate-950 text-slate-400 text-[11px] flex items-center justify-between">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-circle-info text-yellow-400"></i> วิทยากร: ผศ.ดร.ธนา อุดมศรีไพบูลย์ (depa & KT-Edu)
          </span>
          <span class="text-slate-500">กดปุ่ม Esc หรือคลิกพื้นที่ด้านนอกเพื่อปิด</span>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);

  // Close on Backdrop Click
  const modal = document.getElementById('inpageVideoModal');
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeVideoModal();
  });

  // Close on Escape Key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeVideoModal();
  });
}

function openVideoModal(param1, title = '', subtitle = '') {
  initVideoModal();

  // If param1 is a chapter number (1-12)
  if (typeof param1 === 'number' || (typeof param1 === 'string' && /^\d+$/.test(param1))) {
    const chNum = parseInt(param1, 10);
    return openChapterVideoModal(chNum);
  }

  // If param1 is a string, check if it matches a chapter or episode in CHAPTER_VIDEOS
  if (typeof param1 === 'string') {
    for (const [chKey, chData] of Object.entries(CHAPTER_VIDEOS)) {
      const eps = chData.episodes || [];
      const found = eps.find(e => e.id === param1 || (param1.includes(e.id) && e.id.length > 5));
      if (found) {
        return openChapterVideoModal(parseInt(chKey, 10), found.id);
      }
    }
  }

  // Fallback for custom standalone video ID/URL
  playSingleVideo(param1, title, subtitle);
}

function openChapterVideoModal(chNum, targetVideoIdOrEp = null) {
  initVideoModal();
  const chData = CHAPTER_VIDEOS[chNum];
  if (!chData) return;

  const episodes = chData.episodes || [];
  let currentEp = episodes[0];

  if (targetVideoIdOrEp) {
    currentEp = episodes.find(e => e.id === targetVideoIdOrEp || e.ep === targetVideoIdOrEp) || episodes[0];
  } else if (chData.defaultEp) {
    currentEp = episodes.find(e => e.ep === chData.defaultEp) || episodes[0];
  }

  renderAndPlayEpisode(chNum, currentEp, episodes);
}

function renderAndPlayEpisode(chNum, ep, episodes) {
  const modal = document.getElementById('inpageVideoModal');
  const iframe = document.getElementById('inpageVideoIframe');
  const titleEl = document.getElementById('inpageVideoTitle');
  const subEl = document.getElementById('inpageVideoSubtitle');
  const extLink = document.getElementById('inpageVideoExternalLink');
  const epBar = document.getElementById('inpageVideoEpisodeBar');
  const epContainer = document.getElementById('inpageVideoEpisodes');
  const inlineEpContainer = document.getElementById('inpageVideoEpisodeInline');

  // Set Embed URL
  let embedUrl = '';
  let externalUrl = '';
  if (ep.isPlaylist || ep.id.includes('playlist') || ep.id.startsWith('PL_')) {
    const listId = ep.id.replace(/.*list=/, '');
    embedUrl = `https://www.youtube-nocookie.com/embed/videoseries?list=${listId}&autoplay=1`;
    externalUrl = `https://youtube.com/playlist?list=${listId}`;
  } else {
    let id = ep.id;
    if (id.includes('v=')) id = id.split('v=')[1].split('&')[0];
    else if (id.includes('youtu.be/')) id = id.split('youtu.be/')[1].split('?')[0];

    embedUrl = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    externalUrl = `https://www.youtube.com/watch?v=${id}`;
  }

  iframe.src = embedUrl;
  titleEl.textContent = `บทที่ ${chNum}: ${ep.title}`;
  extLink.href = externalUrl;
  const pdfLink = document.getElementById('inpageVideoPdfLink');
  if (pdfLink) {
    const chData = CHAPTER_VIDEOS[chNum] || {};
    pdfLink.href = chData.pdfUrl || (chNum === 1 ? 'https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434' : 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu');
  }

  // Render Episode Selectors if more than 1 episode exists
  if (episodes && episodes.length > 1) {
    epBar.classList.remove('hidden');
    epBar.classList.add('flex');
    epContainer.innerHTML = '';
    if (inlineEpContainer) inlineEpContainer.innerHTML = '';

    episodes.forEach(item => {
      const isCurrent = (item.id === ep.id && item.ep === ep.ep);

      // 1. Episode Bar Button
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `px-3 py-1.5 rounded-lg text-xs font-semibold transition shrink-0 flex items-center gap-1.5 ${
        isCurrent
          ? 'bg-[#fff200] text-[#173b6b] font-black shadow-md ring-2 ring-yellow-300'
          : 'bg-white/10 hover:bg-white/20 text-slate-200 hover:text-white border border-white/10'
      }`;
      btn.innerHTML = `<i class="fa-solid ${isCurrent ? 'fa-play text-red-600' : 'fa-circle-play text-slate-400'} text-[11px]"></i> <span><strong>${item.ep}</strong>: ${item.label || item.title}</span>`;
      btn.title = item.title;
      btn.onclick = () => renderAndPlayEpisode(chNum, item, episodes);
      epContainer.appendChild(btn);

      // 2. Inline badge next to subtitle (matching user requested + [ ] + [ ])
      if (inlineEpContainer) {
        const badge = document.createElement('button');
        badge.type = 'button';
        badge.className = `px-2 py-0.5 rounded text-[11px] font-mono font-bold transition flex items-center gap-1 ${
          isCurrent
            ? 'bg-[#fff200] text-[#173b6b] shadow-sm'
            : 'bg-white/20 text-slate-200 hover:text-white hover:bg-white/30 border border-white/20'
        }`;
        badge.innerHTML = `<span class="opacity-70 text-[9px]">+</span> ${item.ep}`;
        badge.title = `${item.ep}: ${item.title}`;
        badge.onclick = () => renderAndPlayEpisode(chNum, item, episodes);
        inlineEpContainer.appendChild(badge);
      }
    });
  } else {
    epBar.classList.add('hidden');
    epBar.classList.remove('flex');
    if (inlineEpContainer) inlineEpContainer.innerHTML = '';
  }

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function playSingleVideo(videoIdOrUrl, title = '', subtitle = '') {
  const modal = document.getElementById('inpageVideoModal');
  const iframe = document.getElementById('inpageVideoIframe');
  const titleEl = document.getElementById('inpageVideoTitle');
  const subEl = document.getElementById('inpageVideoSubtitle');
  const extLink = document.getElementById('inpageVideoExternalLink');
  const epBar = document.getElementById('inpageVideoEpisodeBar');
  const inlineEpContainer = document.getElementById('inpageVideoEpisodeInline');

  if (epBar) { epBar.classList.add('hidden'); epBar.classList.remove('flex'); }
  if (inlineEpContainer) inlineEpContainer.innerHTML = '';

  let embedUrl = '';
  let externalUrl = '';

  if (videoIdOrUrl.includes('playlist') || videoIdOrUrl.startsWith('PL_')) {
    const listId = videoIdOrUrl.replace(/.*list=/, '');
    embedUrl = `https://www.youtube-nocookie.com/embed/videoseries?list=${listId}&autoplay=1`;
    externalUrl = `https://youtube.com/playlist?list=${listId}`;
  } else {
    let id = videoIdOrUrl;
    if (id.includes('v=')) id = id.split('v=')[1].split('&')[0];
    else if (id.includes('youtu.be/')) id = id.split('youtu.be/')[1].split('?')[0];

    embedUrl = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    externalUrl = `https://www.youtube.com/watch?v=${id}`;
  }

  iframe.src = embedUrl;
  if (title) titleEl.textContent = title;
  if (subtitle) subEl.textContent = subtitle;
  extLink.href = externalUrl;

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function openVideoByEpisode(chNum, epName) {
  openChapterVideoModal(chNum, epName);
}

function closeVideoModal() {
  const modal = document.getElementById('inpageVideoModal');
  const iframe = document.getElementById('inpageVideoIframe');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
  if (iframe) {
    iframe.src = ''; // Stop video playback
  }
}

// ==============================================================
// 3. SYNTAX HIGHLIGHTING & ONE-CLICK COPY CODE BUTTON
// ==============================================================
function injectPrismLibraries() {
  if (window.Prism) return;

  // Inject Prism CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css';
  document.head.appendChild(link);

  // Inject Local Custom Syntax CSS
  const localCss = document.createElement('link');
  localCss.rel = 'stylesheet';
  localCss.href = 'css/syntax-highlight.css';
  document.head.appendChild(localCss);

  // Inject Prism JS
  const script = document.createElement('script');
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js';
  script.onload = () => {
    // Load Python, Bash, YAML components
    ['python', 'bash', 'yaml', 'json'].forEach(lang => {
      const langScript = document.createElement('script');
      langScript.src = `https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-${lang}.min.js`;
      langScript.onload = () => {
        if (window.Prism) Prism.highlightAll();
      };
      document.head.appendChild(langScript);
    });
  };
  document.head.appendChild(script);
}

function initCodeCopyAndHighlight() {
  injectPrismLibraries();

  // Add Copy button to all code blocks
  const codeBlocks = document.querySelectorAll('pre');
  codeBlocks.forEach((pre) => {
    // Add language class if missing
    let codeEl = pre.querySelector('code');
    if (!codeEl) {
      pre.innerHTML = `<code>${pre.innerHTML}</code>`;
      codeEl = pre.querySelector('code');
    }

    if (codeEl && !codeEl.className.includes('language-')) {
      const text = codeEl.innerText.trim();
      if (text.startsWith('$') || text.startsWith('curl') || text.startsWith('sudo') || text.startsWith('npm') || text.startsWith('source')) {
        codeEl.classList.add('language-bash');
      } else if (text.includes('version:') || text.includes('project:') || text.includes('inputs:')) {
        codeEl.classList.add('language-yaml');
      } else {
        codeEl.classList.add('language-python');
      }
    }

    // Skip if already initialized
    if (pre.getAttribute('data-copy-init') === 'true') return;
    pre.setAttribute('data-copy-init', 'true');

    pre.classList.add('relative', 'group');

    // Create Copy Button
    const copyBtn = document.createElement('button');
    copyBtn.type = 'button';
    copyBtn.className = 'absolute top-2.5 right-2.5 z-20 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white border border-white/20 backdrop-blur-sm shadow transition flex items-center gap-1.5 opacity-90 group-hover:opacity-100';
    copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i> <span>คัดลอกโค้ด</span>';
    copyBtn.title = 'คลิกเพื่อคัดลอกโค้ดทั้งหมดลงในคลิปบอร์ด';

    copyBtn.addEventListener('click', async () => {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      try {
        await navigator.clipboard.writeText(code);
        copyBtn.className = 'absolute top-2.5 right-2.5 z-20 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-600 text-white border border-emerald-400 shadow transition flex items-center gap-1.5';
        copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> <span>คัดลอกสำเร็จ!</span>';
        setTimeout(() => {
          copyBtn.className = 'absolute top-2.5 right-2.5 z-20 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white border border-white/20 backdrop-blur-sm shadow transition flex items-center gap-1.5 opacity-90 group-hover:opacity-100';
          copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i> <span>คัดลอกโค้ด</span>';
        }, 2200);
      } catch (err) {
        console.error('Clipboard copy failed:', err);
      }
    });

    pre.appendChild(copyBtn);
  });
}

// ==============================================================
// 4. ATTACH VIDEO MODAL TRIGGERS TO CHAPTER HEADER & HERO
// ==============================================================
function attachChapterVideoTriggers() {
  // Detect current chapter from URL
  const match = window.location.pathname.match(/chapter(\d+)\.html/);
  if (!match) return;
  const chNum = parseInt(match[1], 10);
  const videoData = CHAPTER_VIDEOS[chNum];
  if (!videoData) return;

  // Find existing YouTube links in Hero and add an In-Page Watch button
  const heroYoutubeLinks = document.querySelectorAll('header a[href*="youtube.com"], section a[href*="youtube.com"]');
  heroYoutubeLinks.forEach(link => {
    // If it's a primary button in Hero or Header, make it open modal
    if (!link.hasAttribute('data-video-modal-attached')) {
      link.setAttribute('data-video-modal-attached', 'true');
      link.addEventListener('click', (e) => {
        // Only open modal if left clicked without Ctrl/Meta
        if (!e.ctrlKey && !e.metaKey && !e.shiftKey) {
          e.preventDefault();
          const href = link.getAttribute('href') || '';
          let matchedEp = null;
          if (videoData.episodes) {
            matchedEp = videoData.episodes.find(ep => href.includes(ep.id));
          }
          openChapterVideoModal(chNum, matchedEp ? matchedEp.id : null);
        }
      });
      link.title = 'คลิกเพื่อเปิดดูคลิปในหน้านี้ (In-Page Player)';
    }
  });

  // Update Hero Meta card "code_examples" to be a clickable link
  const codeCardSpan = document.querySelector('span.font-mono.text-yellow-300.font-bold');
  if (codeCardSpan && codeCardSpan.textContent.includes('code_examples/chapter')) {
    const chStr = String(chNum).padStart(2, '0');
    codeCardSpan.innerHTML = `
      <a href="/code_examples/chapter${chStr}/" target="_blank" class="hover:text-white underline decoration-yellow-400 underline-offset-2 flex items-center gap-1.5" title="เปิดดูโฟลเดอร์ไฟล์โค้ดของบทเรียนนี้">
        <span>code_examples/chapter${chStr}</span>
        <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
      </a>
    `;
  }
}

// ==============================================================
// 5. AUTO INITIALIZATION ON DOM READY
// ==============================================================
document.addEventListener('DOMContentLoaded', () => {
  initVideoModal();
  initCodeCopyAndHighlight();
  attachChapterVideoTriggers();
});

// Export functions to window
window.openVideoModal = openVideoModal;
window.openChapterVideoModal = openChapterVideoModal;
window.openVideoByEpisode = openVideoByEpisode;
window.closeVideoModal = closeVideoModal;
window.initCodeCopyAndHighlight = initCodeCopyAndHighlight;
window.CHAPTER_VIDEOS = CHAPTER_VIDEOS;
