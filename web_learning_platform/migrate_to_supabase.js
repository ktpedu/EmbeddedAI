const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'data', 'db.json');
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

const SUPABASE_URL = process.env.SUPABASE_URL || process.argv[2];
const SUPABASE_KEY = process.env.SUPABASE_KEY || process.argv[3];

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('Usage: node migrate_to_supabase.js <SUPABASE_URL> <SUPABASE_KEY>');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function migrate() {
  console.log('🚀 Starting migration to Supabase:', SUPABASE_URL);

  // 1. Students
  if (db.students && db.students.length > 0) {
    const studentRecords = db.students.map(s => ({
      id: s.id || `std_${s.student_id}`,
      student_id: s.student_id,
      username: s.username || s.student_id,
      name: s.name,
      full_name: s.full_name || s.name,
      class_room: s.class_room || 'ม.5/12',
      role: s.role || 'student'
    }));
    const { error } = await supabase.from('students').upsert(studentRecords, { onConflict: 'student_id' });
    if (error) console.error('❌ Students migration error:', error.message);
    else console.log(`✅ Synced ${studentRecords.length} students.`);
  }

  // 2. Submissions
  if (db.submissions && db.submissions.length > 0) {
    const subRecords = db.submissions.map(s => ({
      id: s.id,
      student_id: s.student_id,
      student_name: s.student_name,
      chapter_id: s.chapter_id,
      task_type: s.task_type || 'practical',
      report_url: s.report_url || '',
      notes: s.notes || '',
      status: s.status || 'submitted',
      score: s.score !== undefined ? s.score : null,
      submitted_at: s.submitted_at || new Date().toISOString()
    }));
    const { error } = await supabase.from('submissions').upsert(subRecords, { onConflict: 'id' });
    if (error) console.error('❌ Submissions migration error:', error.message);
    else console.log(`✅ Synced ${subRecords.length} submissions.`);
  }

  // 3. Scores
  if (db.scores && db.scores.length > 0) {
    const scoreRecords = db.scores.map(s => ({
      id: s.id,
      student_id: s.student_id,
      student_name: s.student_name,
      exam_category: s.exam_category,
      target_id: s.target_id,
      chapter_id: s.chapter_id || '',
      score: s.score,
      max_score: s.max_score || 10,
      percentage: s.percentage,
      notes: s.notes || '',
      rubrics_breakdown: s.rubrics_breakdown || null,
      submitted_at: s.submitted_at || new Date().toISOString()
    }));
    const { error } = await supabase.from('scores').upsert(scoreRecords, { onConflict: 'id' });
    if (error) console.error('❌ Scores migration error:', error.message);
    else console.log(`✅ Synced ${scoreRecords.length} scores.`);
  }

  // 4. Lessons
  if (db.lessons && db.lessons.length > 0) {
    const { error } = await supabase.from('lessons').upsert(db.lessons, { onConflict: 'id' });
    if (error) console.error('❌ Lessons migration error:', error.message);
    else console.log(`✅ Synced ${db.lessons.length} lessons.`);
  }

  // 5. Quizzes
  if (db.quizzes && db.quizzes.length > 0) {
    const { error } = await supabase.from('quizzes').upsert(db.quizzes, { onConflict: 'id' });
    if (error) console.error('❌ Quizzes migration error:', error.message);
    else console.log(`✅ Synced ${db.quizzes.length} quizzes.`);
  }

  // 6. Practical Exams
  if (db.practical_exams && db.practical_exams.length > 0) {
    const { error } = await supabase.from('practical_exams').upsert(db.practical_exams, { onConflict: 'id' });
    if (error) console.error('❌ Practical exams migration error:', error.message);
    else console.log(`✅ Synced ${db.practical_exams.length} practical exams.`);
  }

  // 7. Worksheets
  if (db.worksheets && db.worksheets.length > 0) {
    const { error } = await supabase.from('worksheets').upsert(db.worksheets, { onConflict: 'id' });
    if (error) console.error('❌ Worksheets migration error:', error.message);
    else console.log(`✅ Synced ${db.worksheets.length} worksheets.`);
  }

  console.log('🎉 Migration completed successfully!');
}

migrate();
