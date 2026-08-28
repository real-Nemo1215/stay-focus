# Focus 🎯 - Shared Goal & Focus Tracker

A couple focus and goal-tracking application built with **Streamlit** (Python) and **Next.js** (App Router & Tailwind CSS), powered by **Supabase** real-time database.

---

## 🌟 Key Features

- **Maroon & Wine Luxury Theme**: Elegant aesthetic tailored for shared focus and productivity.
- **Dedicated 2-Account Login**: Pre-configured accounts for **Nemo** 🐠 and **pikachu** ⚡.
- **Today's Focus**: Daily checklist with dynamic **Date & Day** headers.
- **Yesterday's Focus (Archived)**: Review completed/uncompleted goals from yesterday with **`+ Today`** 1-click migration.
- **Monthly Focus**: Manage broader targets for the current month.
- **Live Real-time Partner Sync**: Mutual visibility into partner goals and progress percentages.

---

## 📱 Quick Run with Streamlit (Mobile & Desktop)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run App
```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deploy on Streamlit Community Cloud (Free 24/7 Access)

1. Fork or push this repository to GitHub.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and connect your GitHub account.
3. Click **New app**, select this repository, and set `streamlit_app.py` as the Main file path.
4. Under **Advanced Settings > Secrets**, add your Supabase credentials:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_ANON_KEY = "your-anon-key"
   ```
5. Click **Deploy**!

---

## 💻 Next.js Web Application

If you prefer running the Next.js React application:

```bash
cd couple-goals
npm install
npm run dev
```

---

## 🗄️ Database Setup (Supabase)

Copy and execute [`couple-goals/supabase/schema.sql`](couple-goals/supabase/schema.sql) in your **Supabase Dashboard > SQL Editor** to automatically set up the tables, RLS security policies, and user accounts.
