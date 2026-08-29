# Focus 🎯

A real-time couple focus & goal tracking web app built with Next.js (App Router), Tailwind CSS, and Supabase.

## ✨ Features

- **Exclusive Shared Space**: Dedicated login for **Nemo** 🐠 and **pikachu** ⚡ with automatic account linking.
- **Rich Maroon Aesthetics**: Elegant, cohesive burgundy and maroon UI.
- **Daily & Yesterday Focus Tracker**:
  - **Today's Focus**: Manage and track active tasks with dynamic Date & Day indicators.
  - **Yesterday's Focus**: Archived view of yesterday's tasks with 1-click `+ Today` carry-over for unfinished items.
- **Monthly Focus**: Manage broader long-term couple goals.
- **Live Real-time Sync**: Goal additions, completion toggles, and deletions synchronize instantly across devices via Supabase Realtime.
- **Progress Bars**: Visual progress indicator reflecting completion percentage for both partners.

## 🚀 Getting Started

### 1. Database Setup
Copy and run the SQL script in [`supabase/schema.sql`](supabase/schema.sql) in your **Supabase Dashboard > SQL Editor**.

### 2. Environment Variables
Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### 3. Install & Run
```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.
