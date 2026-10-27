-- ==============================================================
-- EdgeAI Learning Platform - Supabase PostgreSQL Schema
-- ==============================================================

-- 1. Table: students (รายชื่อนักเรียน ม.5/12)
create table if not exists public.students (
    id text primary key,
    student_id text unique not null,
    username text,
    name text not null,
    full_name text,
    class_room text default 'ม.5/12',
    role text default 'student',
    created_at timestamp with time zone default now()
);

-- 2. Table: submissions (การส่งงาน แยกโจทย์ปฏิบัติ และ ใบงาน)
create table if not exists public.submissions (
    id text primary key,
    student_id text not null,
    student_name text,
    chapter_id text not null,
    task_type text not null check (task_type in ('practical', 'worksheet')),
    report_url text,
    notes text,
    status text default 'submitted' check (status in ('submitted', 'graded')),
    score numeric,
    submitted_at text,
    created_at timestamp with time zone default now()
);

-- 3. Table: scores (สมุดบันทึกคะแนน รูบริก และใบงาน)
create table if not exists public.scores (
    id text primary key,
    student_id text not null,
    student_name text,
    exam_category text not null, -- 'practical', 'worksheet', 'chapter_quiz', 'midterm', 'final'
    target_id text not null,
    chapter_id text,
    score numeric not null,
    max_score numeric default 10,
    percentage numeric,
    notes text,
    rubrics_breakdown jsonb,
    submitted_at text,
    created_at timestamp with time zone default now()
);

-- 4. Table: lessons (บทเรียนออนไลน์ 12 บท)
create table if not exists public.lessons (
    id text primary key,
    chapter_number integer not null,
    title text not null,
    duration_hours integer default 2,
    objectives jsonb,
    sections jsonb,
    summary text,
    code_example text,
    created_at timestamp with time zone default now()
);

-- 5. Table: quizzes (แบบทดสอบออนไลน์)
create table if not exists public.quizzes (
    id text primary key,
    chapter_id text,
    title text not null,
    category text default 'chapter_quiz',
    time_limit_minutes integer default 15,
    questions jsonb,
    created_at timestamp with time zone default now()
);

-- 6. Table: practical_exams (โจทย์ข้อสอบปฏิบัติและเกณฑ์รูบริก)
create table if not exists public.practical_exams (
    id text primary key,
    unit_number integer not null,
    chapter_id text not null,
    title text not null,
    description text,
    rubrics jsonb,
    code_reference text,
    created_at timestamp with time zone default now()
);

-- 7. Table: worksheets (ใบงานปฏิบัติการประจำบท)
create table if not exists public.worksheets (
    id text primary key,
    chapter_number integer not null,
    chapter_id text not null,
    title text not null,
    time_minutes integer default 60,
    instructions text,
    file_url text,
    view_url text,
    file_name text,
    code_reference text,
    status text default 'active',
    created_at timestamp with time zone default now()
);

-- ==============================================================
-- Row Level Security (RLS) Policies
-- ==============================================================
alter table public.students enable row level security;
alter table public.submissions enable row level security;
alter table public.scores enable row level security;
alter table public.lessons enable row level security;
alter table public.quizzes enable row level security;
alter table public.practical_exams enable row level security;
alter table public.worksheets enable row level security;

create policy "Allow all on students" on public.students for all using (true) with check (true);
create policy "Allow all on submissions" on public.submissions for all using (true) with check (true);
create policy "Allow all on scores" on public.scores for all using (true) with check (true);
create policy "Allow all on lessons" on public.lessons for all using (true) with check (true);
create policy "Allow all on quizzes" on public.quizzes for all using (true) with check (true);
create policy "Allow all on practical_exams" on public.practical_exams for all using (true) with check (true);
create policy "Allow all on worksheets" on public.worksheets for all using (true) with check (true);

-- ==============================================================
-- Enable Realtime for Submissions, Scores, and Students
-- ==============================================================
alter publication supabase_realtime add table public.submissions;
alter publication supabase_realtime add table public.scores;
alter publication supabase_realtime add table public.students;
