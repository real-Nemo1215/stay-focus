import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()
load_dotenv("couple-goals/.env.local")

# Page Configuration
st.set_page_config(
    page_title="Focus 🎯 - Shared Daily & Monthly Focus Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Maroon Theme CSS mirroring Next.js
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(180deg, #FAF4F6 0%, #F5E6E9 50%, #EED6DC 100%) !important;
    }

    /* Main Container max-width for desktop elegance */
    .block-container {
        max-width: 1080px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* Primary Maroon Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #800020 0%, #8B1E3F 50%, #5C0A19 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.6rem 1.3rem !important;
        box-shadow: 0 4px 14px rgba(128, 0, 32, 0.22) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(128, 0, 32, 0.32) !important;
        color: #ffffff !important;
    }

    /* Secondary / Action Buttons */
    button[kind="secondary"] {
        background: #ffffff !important;
        color: #800020 !important;
        border: 1px solid #E2B7C1 !important;
        box-shadow: 0 2px 6px rgba(128, 0, 32, 0.05) !important;
    }

    /* Cards */
    .focus-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 0, 32, 0.14);
        border-radius: 26px;
        padding: 1.75rem;
        box-shadow: 0 10px 30px rgba(128, 0, 32, 0.04);
        margin-bottom: 1.5rem;
    }

    .focus-header-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 0, 32, 0.14);
        border-radius: 22px;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 16px rgba(128, 0, 32, 0.03);
        margin-bottom: 1.5rem;
    }

    /* Date Banner */
    .date-banner-pill {
        background: #FAF0F3;
        border: 1px solid #E5BEC5;
        color: #800020;
        border-radius: 16px;
        padding: 0.4rem 1.2rem;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 6px rgba(128, 0, 32, 0.03);
    }

    /* Badge Counter */
    .done-badge {
        background: #FAF0F3;
        color: #800020;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 800;
        border: 1px solid #E5BEC5;
    }

    /* Custom Goal List Items */
    .goal-row {
        background: #FAF3F5;
        border: 1px solid #E9CAD1;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.55rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: background 0.15s ease;
    }
    .goal-row:hover {
        background: #F7EAEF;
    }

    /* Input styling */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #DFC0C7 !important;
        background-color: #FAF5F6 !important;
        color: #111827 !important;
        font-weight: 500 !important;
    }
    .stTextInput input:focus {
        background-color: #ffffff !important;
        border-color: #800020 !important;
        box-shadow: 0 0 0 2px rgba(128, 0, 32, 0.2) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(128, 0, 32, 0.18);
        padding: 6px;
        border-radius: 9999px;
        box-shadow: 0 4px 16px rgba(128, 0, 32, 0.04);
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        padding: 8px 22px !important;
        color: #662B37 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #800020 0%, #8B1E3F 50%, #5C0A19 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(128, 0, 32, 0.25) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #800020 0%, #9C1B33 100%) !important;
        border-radius: 9999px !important;
    }
    .stProgress > div > div {
        background-color: #FAF0F3 !important;
        border: 1px solid #F0D5DA !important;
        border-radius: 9999px !important;
        height: 10px !important;
    }

    /* Checkbox custom accent */
    .stCheckbox label span {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #111827 !important;
    }
</style>
""", unsafe_allow_html=True)

# Supabase Initialization
SUPABASE_URL = (
    st.secrets.get("SUPABASE_URL")
    or os.environ.get("SUPABASE_URL")
    or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    or "https://rsrtvdvwkqjzqbovlwje.supabase.co"
)
SUPABASE_KEY = (
    st.secrets.get("SUPABASE_ANON_KEY")
    or os.environ.get("SUPABASE_ANON_KEY")
    or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    or "sb_publishable_OMWZDBRZyeN1XnPZMKDzbQ_-4zlh87N"
)

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_supabase()
except Exception as e:
    st.error(f"Failed to connect to Supabase: {e}")
    st.stop()

# Allowed Accounts Configuration
ACCOUNTS = {
    "Nemo": {
        "email": "nemo@focus.app",
        "avatar": "🐠",
        "partner": "pikachu",
        "partner_avatar": "⚡"
    },
    "pikachu": {
        "email": "pikachu@focus.app",
        "avatar": "⚡",
        "partner": "Nemo",
        "partner_avatar": "🐠"
    }
}

# Session State Initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "username" not in st.session_state:
    st.session_state.username = "Nemo"
if "profile" not in st.session_state:
    st.session_state.profile = None
if "partner_profile" not in st.session_state:
    st.session_state.partner_profile = None

# Date Calculations
now = datetime.date.today()
yesterday = now - datetime.timedelta(days=1)
today_iso = now.isoformat()
yesterday_iso = yesterday.isoformat()
today_formatted = now.strftime("%A, %B %d, %Y")
yesterday_formatted = yesterday.strftime("%A, %B %d, %Y")
month_formatted = now.strftime("%B %Y")


def load_profile_and_partner(user_id, username):
    account_meta = ACCOUNTS.get(username, {})
    partner_name = account_meta.get("partner", "Partner")
    try:
        res = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if res.data and len(res.data) > 0:
            st.session_state.profile = res.data[0]
        else:
            ins = supabase.table("profiles").upsert({
                "id": user_id,
                "name": username,
                "email": account_meta.get("email"),
                "username": username.lower()
            }).execute()
            st.session_state.profile = ins.data[0] if ins.data else {"id": user_id, "name": username}

        part_res = supabase.table("profiles").select("*").ilike("name", partner_name).execute()
        if part_res.data and len(part_res.data) > 0:
            st.session_state.partner_profile = part_res.data[0]
        else:
            st.session_state.partner_profile = {"id": f"pending-{partner_name}", "name": partner_name}
    except Exception:
        st.session_state.profile = {"id": user_id, "name": username}
        st.session_state.partner_profile = {"id": f"pending-{partner_name}", "name": partner_name}


# ==========================================
# 1. LOGIN SCREEN (Clean & Secure)
# ==========================================
if not st.session_state.user:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1])

    with c2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='display: inline-flex; width: 64px; height: 64px; background: #F7E7EA; border-radius: 20px; align-items: center; justify-content: center; font-size: 32px; border: 1px solid #E5BEC5; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 0.75rem;'>
                🎯
            </div>
            <h1 style='color: #800020; font-weight: 900; margin: 0; font-size: 2.2rem; tracking-tight;'>Focus</h1>
            <p style='color: #733844; font-size: 0.9rem; font-weight: 600; margin-top: 4px;'>Sign in to your shared Focus workspace</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='focus-card'>", unsafe_allow_html=True)

            selected_acc = st.radio(
                "Select Account",
                options=["Nemo", "pikachu"],
                format_func=lambda x: f"{ACCOUNTS[x]['avatar']} {x}",
                horizontal=True
            )

            acc_info = ACCOUNTS[selected_acc]
            password = st.text_input(
                f"Password for {selected_acc}",
                placeholder="Enter your password",
                type="password"
            )

            if st.button(f"Log In as {selected_acc} 🎯", use_container_width=True):
                with st.spinner("Signing in..."):
                    try:
                        auth_res = supabase.auth.sign_in_with_password({
                            "email": acc_info["email"],
                            "password": password
                        })
                        if auth_res.user:
                            st.session_state.user = auth_res.user
                            st.session_state.username = selected_acc
                            load_profile_and_partner(auth_res.user.id, selected_acc)
                            st.rerun()
                    except Exception as err:
                        try:
                            sign_up = supabase.auth.sign_up({
                                "email": acc_info["email"],
                                "password": password,
                                "options": {"data": {"full_name": selected_acc}}
                            })
                            if sign_up.user:
                                retry = supabase.auth.sign_in_with_password({
                                    "email": acc_info["email"],
                                    "password": password
                                })
                                if retry.user:
                                    st.session_state.user = retry.user
                                    st.session_state.username = selected_acc
                                    load_profile_and_partner(retry.user.id, selected_acc)
                                    st.rerun()
                        except Exception:
                            st.error(f"Login failed: {err}")

            st.markdown("<div style='text-align: center; margin-top: 1.5rem; font-size: 0.75rem; color: #800020; opacity: 0.6; font-weight: 600;'>Focus &bull; Shared Goal Tracker</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ==========================================
# 2. MAIN DASHBOARD
# ==========================================
current_user = st.session_state.user
current_username = st.session_state.username
user_info = ACCOUNTS.get(current_username, {})
partner_name = user_info.get("partner", "Partner")
partner_avatar = user_info.get("partner_avatar", "💫")
user_avatar = user_info.get("avatar", "👤")

# Header Bar (Matching Next.js layout)
st.markdown("<div class='focus-header-box'>", unsafe_allow_html=True)
h1, h2, h3 = st.columns([3.5, 1.2, 1])

with h1:
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 14px;'>
        <div style='width: 48px; height: 48px; background: #F7E7EA; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 24px; border: 1px solid #E5BEC5; box-shadow: inset 0 1px 3px rgba(0,0,0,0.04);'>
            🎯
        </div>
        <div>
            <h2 style='color: #800020; font-weight: 900; margin: 0; line-height: 1.1; font-size: 1.6rem;'>Focus</h2>
            <span style='color: #733844; font-size: 0.8rem; font-weight: 700;'>{current_username} & {partner_name} &bull; Shared Focus Space</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div style='display: flex; justify-content: flex-end; align-items: center; height: 100%;'>
        <span style='background: #FAF0F3; color: #800020; padding: 6px 14px; border-radius: 12px; border: 1px solid #E2B7C1; font-weight: 800; font-size: 0.82rem; box-shadow: 0 1px 4px rgba(0,0,0,0.03);'>
            {user_avatar} {current_username}
        </span>
    </div>
    """, unsafe_allow_html=True)

with h3:
    if st.button("Sign Out", use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state.user = None
        st.session_state.profile = None
        st.session_state.partner_profile = None
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_today, tab_yesterday, tab_monthly = st.tabs([
    "☀️ Today's Focus",
    "⏳ Yesterday's Focus",
    "🌙 Monthly Focus"
])

# Fetch all goals for both partners
profile_id = st.session_state.profile.get("id") if st.session_state.profile else current_user.id
partner_id = st.session_state.partner_profile.get("id") if st.session_state.partner_profile else None

try:
    my_goals_res = supabase.table("goals").select("*").eq("user_id", profile_id).order("created_at").execute()
    my_goals = my_goals_res.data or []
except Exception:
    my_goals = []

partner_goals = []
if partner_id and not str(partner_id).startswith("pending-"):
    try:
        part_goals_res = supabase.table("goals").select("*").eq("user_id", partner_id).order("created_at").execute()
        partner_goals = part_goals_res.data or []
    except Exception:
        partner_goals = []


def filter_goals(goals_list, tab_type):
    filtered = []
    for g in goals_list:
        g_type = g.get("type", "daily")
        g_date = g.get("target_date")
        if not g_date and g.get("created_at"):
            g_date = str(g["created_at"])[:10]

        if tab_type == "monthly":
            if g_type == "monthly":
                filtered.append(g)
        elif tab_type == "today":
            if g_type == "daily" and (g_date == today_iso or not g_date):
                filtered.append(g)
        elif tab_type == "yesterday":
            if g_type == "daily" and g_date == yesterday_iso:
                filtered.append(g)
    return filtered


def render_focus_tab(tab_type, banner_html, allow_add=True):
    # Prominent Date Banner
    st.markdown(f"<div style='text-align: center; margin-top: 0.5rem; margin-bottom: 1.25rem;'><span class='date-banner-pill'>{banner_html}</span></div>", unsafe_allow_html=True)

    col_my, col_part = st.columns(2, gap="large")

    active_my = filter_goals(my_goals, tab_type)
    active_part = filter_goals(partner_goals, tab_type)

    my_done = sum(1 for g in active_my if g.get("is_completed"))
    part_done = sum(1 for g in active_part if g.get("is_completed"))

    my_pct = int((my_done / len(active_my) * 100)) if len(active_my) > 0 else 0
    part_pct = int((part_done / len(active_part) * 100)) if len(active_part) > 0 else 0

    # 1. User Column (Left)
    with col_my:
        st.markdown("<div class='focus-card'>", unsafe_allow_html=True)
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown(f"<h3 style='color: #800020; font-weight: 900; margin:0; font-size: 1.25rem;'>{user_avatar} {current_username}'s Focus</h3>", unsafe_allow_html=True)
        with h_col2:
            st.markdown(f"<div style='text-align: right;'><span class='done-badge'>{my_done}/{len(active_my)} Done</span></div>", unsafe_allow_html=True)

        st.progress(my_pct / 100.0)

        # Add Goal Form (Today and Monthly)
        if allow_add:
            with st.form(key=f"add_form_{tab_type}", clear_on_submit=True):
                c_in, c_btn = st.columns([4, 1])
                with c_in:
                    placeholder_text = "Add a monthly focus item..." if tab_type == "monthly" else "Add today's focus item..."
                    new_title = st.text_input(
                        "Add item",
                        placeholder=placeholder_text,
                        label_visibility="collapsed"
                    )
                with c_btn:
                    submitted = st.form_submit_button("Add")
                if submitted and new_title.strip():
                    g_type = "monthly" if tab_type == "monthly" else "daily"
                    try:
                        supabase.table("goals").insert({
                            "user_id": profile_id,
                            "title": new_title.strip(),
                            "type": g_type,
                            "target_date": today_iso,
                            "is_completed": False
                        }).execute()
                    except Exception:
                        supabase.table("goals").insert({
                            "user_id": profile_id,
                            "title": new_title.strip(),
                            "type": g_type,
                            "is_completed": False
                        }).execute()
                    st.rerun()
        else:
            st.markdown("""
            <div style='background: #FAF3F5; border: 1px solid #E9CAD1; border-radius: 14px; padding: 10px 14px; font-size: 0.8rem; color: #7A3341; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;'>
                <span>🔒 <b>Yesterday's list is archived.</b></span>
                <span style='color: #800020; font-weight: 800;'>Use '+ Today' to carry over</span>
            </div>
            """, unsafe_allow_html=True)

        # Goal Items List
        if not active_my:
            msg = "No focus items recorded for yesterday. ⏳" if tab_type == "yesterday" else "No focus items yet. Add one above! ✨"
            st.markdown(f"<div style='text-align: center; padding: 2.5rem; color: #9E6772; font-style: italic; background: #FAF5F6; border-radius: 16px; border: 1px dashed #E5CBD1;'>{msg}</div>", unsafe_allow_html=True)
        else:
            for g in active_my:
                g_id = g.get("id")
                g_title = g.get("title", "")
                is_done = g.get("is_completed", False)

                row1, row2, row3 = st.columns([6, 2, 1])
                with row1:
                    checked = st.checkbox(
                        g_title,
                        value=is_done,
                        key=f"check_{tab_type}_{g_id}"
                    )
                    if checked != is_done:
                        supabase.table("goals").update({"is_completed": checked}).eq("id", g_id).execute()
                        st.rerun()

                with row2:
                    if tab_type == "yesterday" and not is_done:
                        if st.button("+ Today", key=f"copy_{g_id}", help="Copy to today's list"):
                            try:
                                supabase.table("goals").insert({
                                    "user_id": profile_id,
                                    "title": g_title,
                                    "type": "daily",
                                    "target_date": today_iso,
                                    "is_completed": False
                                }).execute()
                            except Exception:
                                supabase.table("goals").insert({
                                    "user_id": profile_id,
                                    "title": g_title,
                                    "type": "daily",
                                    "is_completed": False
                                }).execute()
                            st.rerun()

                with row3:
                    if st.button("✕", key=f"del_{tab_type}_{g_id}", help="Delete item"):
                        supabase.table("goals").delete().eq("id", g_id).execute()
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Partner Column (Right)
    with col_part:
        st.markdown("<div class='focus-card'>", unsafe_allow_html=True)
        ph_col1, ph_col2 = st.columns([3, 1])
        with ph_col1:
            st.markdown(f"<h3 style='color: #5C0A19; font-weight: 900; margin:0; font-size: 1.25rem;'>{partner_avatar} {partner_name}'s Focus</h3>", unsafe_allow_html=True)
        with ph_col2:
            st.markdown(f"<div style='text-align: right;'><span class='done-badge'>{part_done}/{len(active_part)} Done</span></div>", unsafe_allow_html=True)

        st.progress(part_pct / 100.0)

        if not active_part:
            st.markdown(f"<div style='text-align: center; padding: 3rem; color: #9E6772; font-style: italic; background: #FAF5F6; border-radius: 16px; border: 1px dashed #E5CBD1;'>{partner_name} hasn't added any focus items. 🎯</div>", unsafe_allow_html=True)
        else:
            for pg in active_part:
                p_done = pg.get("is_completed", False)
                p_title = pg.get("title", "")
                icon = "✅" if p_done else "⬜"
                style_line = "text-decoration: line-through; color: #9E6772;" if p_done else "color: #111827; font-weight: 700;"

                st.markdown(f"""
                <div class='goal-row'>
                    <span style='font-size: 0.88rem; {style_line}'>{icon} {p_title}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"<div style='text-align: center; margin-top: 1.75rem; font-size: 0.75rem; color: rgba(128,0,32,0.65); font-weight: 700;'>⚡ Real-time synced with {partner_name}'s Focus</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


with tab_today:
    render_focus_tab("today", f"📅 Today: <strong>{today_formatted}</strong>", allow_add=True)

with tab_yesterday:
    render_focus_tab("yesterday", f"📅 Yesterday: <strong>{yesterday_formatted}</strong> (Read-Only)", allow_add=False)

with tab_monthly:
    render_focus_tab("monthly", f"🗓️ Monthly Focus for <strong>{month_formatted}</strong>", allow_add=True)
