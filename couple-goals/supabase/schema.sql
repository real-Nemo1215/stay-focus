-- ==============================================================================
-- Focus Database Schema & Setup Script
-- Paste this script into your Supabase Dashboard > SQL Editor and click "Run"
-- ==============================================================================

-- Enable pgcrypto for password hashing
create extension if not exists pgcrypto;

-- 1. Create Profiles Table (stores name, username/email, and partner link)
create table if not exists public.profiles (
  id uuid references auth.users on delete cascade primary key,
  name text not null,
  email text,
  username text,
  partner_id uuid references public.profiles(id)
);

-- 2. Create Goals / Focus Table
create table if not exists public.goals (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  title text not null,
  type text check (type in ('daily', 'monthly')) not null,
  is_completed boolean default false,
  created_at timestamp with time zone default now()
);

-- 3. Enable Row Level Security (RLS)
alter table public.profiles enable row level security;
alter table public.goals enable row level security;

-- 4. Profiles RLS Policies
drop policy if exists "Allow public read of profiles" on public.profiles;
create policy "Allow public read of profiles" on public.profiles 
  for select using (true);

drop policy if exists "Allow authenticated insert of profiles" on public.profiles;
create policy "Allow authenticated insert of profiles" on public.profiles 
  for insert with check (true);

drop policy if exists "Allow users to update own profile" on public.profiles;
create policy "Allow users to update own profile" on public.profiles 
  for update using (auth.uid() = id);

-- 5. Goals RLS Policies
drop policy if exists "Select own or partner goals" on public.goals;
create policy "Select own or partner goals" on public.goals 
  for select using (
    user_id = auth.uid() or 
    user_id in (select partner_id from public.profiles where id = auth.uid()) or
    auth.role() = 'authenticated'
  );

drop policy if exists "Insert own goals" on public.goals;
create policy "Insert own goals" on public.goals 
  for insert with check (user_id = auth.uid());

drop policy if exists "Update own goals" on public.goals;
create policy "Update own goals" on public.goals 
  for update using (user_id = auth.uid());

drop policy if exists "Delete own goals" on public.goals;
create policy "Delete own goals" on public.goals 
  for delete using (user_id = auth.uid());

-- 6. Enable Realtime for Goals
alter publication supabase_realtime add table public.goals;

-- 7. Auto-create Profile on Signup Trigger
create or replace function public.handle_new_user() 
returns trigger as $$
declare
  v_name text;
  v_username text;
begin
  v_name := coalesce(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1));
  v_username := lower(v_name);

  insert into public.profiles (id, name, email, username) 
  values (
    new.id, 
    v_name, 
    new.email,
    v_username
  )
  on conflict (id) do update set
    name = excluded.name,
    email = excluded.email,
    username = excluded.username;

  -- Auto link Nemo and pikachu to each other if both exist
  if lower(v_name) = 'nemo' then
    update public.profiles set partner_id = (select id from public.profiles where lower(name) = 'pikachu' limit 1) where id = new.id;
    update public.profiles set partner_id = new.id where lower(name) = 'pikachu';
  elsif lower(v_name) = 'pikachu' then
    update public.profiles set partner_id = (select id from public.profiles where lower(name) = 'nemo' limit 1) where id = new.id;
    update public.profiles set partner_id = new.id where lower(name) = 'nemo';
  end if;

  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- ==============================================================================
-- 8. AUTO-CONFIRM & PRE-SEED Nemo AND pikachu ACCOUNTS
-- This fixes the "Email not confirmed" error instantly!
-- ==============================================================================
-- Confirm any existing accounts
update auth.users 
set email_confirmed_at = now() 
where email in ('nemo@focus.app', 'pikachu@focus.app') and email_confirmed_at is null;

-- Pre-seed Nemo (Password: Nemo1215!!!)
do $$
declare
  nemo_id uuid := 'a0000000-0000-0000-0000-000000000001';
  pikachu_id uuid := 'a0000000-0000-0000-0000-000000000002';
begin
  if not exists (select 1 from auth.users where email = 'nemo@focus.app') then
    insert into auth.users (
      instance_id, id, aud, role, email, encrypted_password, email_confirmed_at,
      raw_app_meta_data, raw_user_meta_data, created_at, updated_at, confirmation_token, email_change, email_change_token_new, recovery_token
    ) values (
      '00000000-0000-0000-0000-000000000000',
      nemo_id,
      'authenticated',
      'authenticated',
      'nemo@focus.app',
      crypt('Nemo1215!!!', gen_salt('bf')),
      now(),
      '{"provider":"email","providers":["email"]}',
      '{"full_name":"Nemo"}',
      now(), now(), '', '', '', ''
    );
  else
    update auth.users 
    set encrypted_password = crypt('Nemo1215!!!', gen_salt('bf')), email_confirmed_at = now()
    where email = 'nemo@focus.app';
  end if;

  -- Pre-seed pikachu (Password: pikachu2108!!!)
  if not exists (select 1 from auth.users where email = 'pikachu@focus.app') then
    insert into auth.users (
      instance_id, id, aud, role, email, encrypted_password, email_confirmed_at,
      raw_app_meta_data, raw_user_meta_data, created_at, updated_at, confirmation_token, email_change, email_change_token_new, recovery_token
    ) values (
      '00000000-0000-0000-0000-000000000000',
      pikachu_id,
      'authenticated',
      'authenticated',
      'pikachu@focus.app',
      crypt('pikachu2108!!!', gen_salt('bf')),
      now(),
      '{"provider":"email","providers":["email"]}',
      '{"full_name":"pikachu"}',
      now(), now(), '', '', '', ''
    );
  else
    update auth.users 
    set encrypted_password = crypt('pikachu2108!!!', gen_salt('bf')), email_confirmed_at = now()
    where email = 'pikachu@focus.app';
  end if;

  -- Ensure both profiles exist and are linked
  insert into public.profiles (id, name, email, username)
  select id, 'Nemo', 'nemo@focus.app', 'nemo' from auth.users where email = 'nemo@focus.app'
  on conflict (id) do nothing;

  insert into public.profiles (id, name, email, username)
  select id, 'pikachu', 'pikachu@focus.app', 'pikachu' from auth.users where email = 'pikachu@focus.app'
  on conflict (id) do nothing;

  -- Link them
  update public.profiles 
  set partner_id = (select id from public.profiles where lower(name) = 'pikachu' limit 1)
  where lower(name) = 'nemo';

  update public.profiles 
  set partner_id = (select id from public.profiles where lower(name) = 'nemo' limit 1)
  where lower(name) = 'pikachu';
end $$;
