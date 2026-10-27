const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://savyelqzzyzbipucdksn.supabase.co';
// Load .env configuration if present
const envFilePath = path.join(__dirname, '.env');
if (fs.existsSync(envFilePath)) {
  try {
    fs.readFileSync(envFilePath, 'utf8').split(/\r?\n/).forEach(l => {
      const trimmed = l.trim();
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const eqIdx = trimmed.indexOf('=');
        const k = trimmed.substring(0, eqIdx).trim();
        const v = trimmed.substring(eqIdx + 1).trim();
        if (!process.env[k]) process.env[k] = v;
      }
    });
  } catch(e) {}
}
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || '';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function uploadQuizzes() {
  const dbPath = path.join(__dirname, 'data', 'db.json');
  const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
  const quizzes = db.quizzes || [];

  console.log(`🚀 Uploading ${quizzes.length} quizzes to Supabase...`);

  // Batch insert in chunks of 50 to avoid payload limits
  const chunkSize = 50;
  let successCount = 0;

  for (let i = 0; i < quizzes.length; i += chunkSize) {
    const chunk = quizzes.slice(i, i + chunkSize);
    const { data, error } = await supabase.from('quizzes').upsert(chunk, { onConflict: 'id' });
    if (error) {
      console.error(`❌ Batch ${i} - ${i + chunk.length} failed:`, error.message);
    } else {
      successCount += chunk.length;
      console.log(`✅ Uploaded batch ${i + 1} - ${Math.min(i + chunkSize, quizzes.length)}`);
    }
  }

  console.log(`🎉 Finished! Successfully uploaded ${successCount}/${quizzes.length} questions to Supabase.`);
}

uploadQuizzes().catch(err => console.error('Migration failed:', err.message));
