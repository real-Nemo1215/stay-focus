# Focus 🎯

A sleek, real-time shared daily and monthly focus tracker designed for couples, built with **Next.js (App Router)**, **Tailwind CSS**, and **Supabase**.

---

## ✨ Features

- **Exclusive Shared Space**: Dedicated login for **Nemo** 🐠 and **pikachu** ⚡ with automatic account linking.
- **Rich Maroon Aesthetics**: Cohesive burgundy and maroon palette (`#800020`, `#8B1E3F`, `#FAF4F6`).
- **Date & Day Indicators**: Dynamic dates and days of the week for all tasks.
- **Today & Yesterday Focus**:
  - ☀️ **Today's Focus**: Create and manage today's goals with live completion tracking.
  - ⏳ **Yesterday's Focus**: Archived past view with a 1-click `+ Today` button to carry over unfinished tasks.
- **Monthly Focus**: Manage broader long-term goals.
- **Real-Time Sync**: Instant two-way synchronization between devices using Supabase Realtime.
- **Live Progress Bars**: Visual progress indicators for both partners.

---

## 🚀 Deploy to Vercel (1-Click)

1. Import this repository into **[Vercel](https://vercel.com)**:
   - Click **"Add New..."** > **"Project"** > Select `real-Nemo1215/stay-focus`.
2. Configure **Environment Variables** in Vercel:
   - `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL (`https://your-project.supabase.co`)
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anon key
3. Click **Deploy**.

---

## 🗄️ Database Setup (Supabase)

Copy and run the contents of [`supabase/schema.sql`](supabase/schema.sql) in your **Supabase Dashboard > SQL Editor**. This script will:
- Create `profiles` and `goals` tables
- Enable Row Level Security (RLS)
- Enable Realtime subscriptions
- Pre-seed and auto-confirm the **Nemo** and **pikachu** accounts

---

## 💻 Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/real-Nemo1215/stay-focus.git
   cd stay-focus
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. Start dev server:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000).
