-- ==============================================================
-- EdgeAI Learning Platform - Supabase Security Hardening & RLS Policies
-- ==============================================================

-- 1. ลบ Policy เดิมที่เปิดสิทธิ์กว้างเกินไป (Drop overly permissive policies)
drop policy if exists "Allow all on students" on public.students;
drop policy if exists "Allow all on submissions" on public.submissions;
drop policy if exists "Allow all on scores" on public.scores;
drop policy if exists "Allow all on lessons" on public.lessons;
drop policy if exists "Allow all on quizzes" on public.quizzes;
drop policy if exists "Allow all on practical_exams" on public.practical_exams;
drop policy if exists "Allow all on worksheets" on public.worksheets;

-- 2. เปิดใช้งาน Row Level Security (RLS) บนทุกตาราง
alter table public.students enable row level security;
alter table public.submissions enable row level security;
alter table public.scores enable row level security;
alter table public.lessons enable row level security;
alter table public.quizzes enable row level security;
alter table public.practical_exams enable row level security;
alter table public.worksheets enable row level security;

-- 3. นโยบายสำหรับ Public / Anon Key (ผู้ใช้ทั่วไป & นักเรียน):
--    อนุญาตเฉพาะการอ่าน (SELECT) เท่านั้น ไม่อนุญาตให้ INSERT / UPDATE / DELETE โดยตรงผ่านหน้าบ้าน
--    (เพื่อป้องกันไม่ให้นักเรียนแฮกแก้คะแนนหรือลบคะแนนเพื่อนผ่าน DevTools)

-- 3.1 นักเรียน & ข้อมูลบทเรียน: อ่านได้ทุกคน
create policy "Anon Read Only on students" on public.students
    for select to anon using (true);

create policy "Anon Read Only on lessons" on public.lessons
    for select to anon using (true);

create policy "Anon Read Only on quizzes" on public.quizzes
    for select to anon using (true);

create policy "Anon Read Only on practical_exams" on public.practical_exams
    for select to anon using (true);

create policy "Anon Read Only on worksheets" on public.worksheets
    for select to anon using (true);

-- 3.2 การส่งงาน & คะแนน: หน้าบ้านอ่านได้เพื่อแสดงผลสดผ่าน Realtime
create policy "Anon Read Only on submissions" on public.submissions
    for select to anon using (true);

create policy "Anon Read Only on scores" on public.scores
    for select to anon using (true);

-- 4. นโยบายสำหรับ Service Role (Backend Server ของเรา):
--    มีสิทธิ์ CRUD เต็ม 100% (SELECT, INSERT, UPDATE, DELETE)
--    เพราะผ่านการตรวจสิทธิ์และคัดกรองความปลอดภัยจาก Node.js แล้ว
create policy "Service Role Full Access on students" on public.students
    for all to service_role using (true) with check (true);

create policy "Service Role Full Access on submissions" on public.submissions
    for all to service_role using (true) with check (true);

create policy "Service Role Full Access on scores" on public.scores
    for all to service_role using (true) with check (true);

create policy "Service Role Full Access on lessons" on public.lessons
    for all to service_role using (true) with check (true);

create policy "Service Role Full Access on quizzes" on public.quizzes
    for all to service_role using (true) with check (true);

create policy "Service Role Full Access on practical_exams" on public.practical_exams
    for all to service_role using (true) with check (true);

create policy "Service Role Full Access on worksheets" on public.worksheets
    for all to service_role using (true) with check (true);

-- 5. ตรวจสอบ Realtime Publication ให้ครอบคลุม
do $$
begin
    if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and tablename = 'submissions') then
        alter publication supabase_realtime add table public.submissions;
    end if;
    if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and tablename = 'scores') then
        alter publication supabase_realtime add table public.scores;
    end if;
    if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and tablename = 'students') then
        alter publication supabase_realtime add table public.students;
    end if;
end $$;
