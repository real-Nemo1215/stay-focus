import streamlit as st
import os
import datetime
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv(".env.local")
load_dotenv(".env")

# Page Configuration
st.set_page_config(
    page_title="Focus 🎯 - Shared Daily & Monthly Focus Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Maroon Theme CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #FAF4F6 0%, #F5E6E9 50%, #EED6DC 100%);
        color: #331118;
    }
    
    /* Header Card */
    .focus-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.25rem 1.75rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(128, 0, 32, 0.15);
        box-shadow: 0 4px 20px rgba(128, 0, 32, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .focus-title {
        font-size: 1.75rem;
        font-weight: 900;
        color: #800020;
        margin: 0;
        line-height: 1.2;
    }
    
    .focus-subtitle {
        font-size: 0.8rem;
        color: #733844;
        font-weight: 600;
        margin: 0;
    }
    
    /* Date Banner */
    .date-banner {
        background: #FAF0F3;
        border: 1px solid #E5BEC5;
        color: #800020;
        padding: 0.4rem 1rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        display: inline-block;
    }
    
    /* Column Cards */
    .focus-card {
        background: #FFFFFF;
        border: 1px solid rgba(128, 0, 32, 0.15);
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(128, 0, 32, 0.04);
        margin-bottom: 1.5rem;
    }
    
    .column-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #800020;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    .partner-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #5C0A19;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #800020 0%, #8B1E3F 50%, #5C0A19 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        font-weight: 700;
        padding: 0.5rem 1.25rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6B001A 0%, #751532 50%, #470613 100%);
        box-shadow: 0 4px 12px rgba(128, 0, 32, 0.25);
        color: white;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background-color: #800020;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 6px;
        border-radius: 9999px;
        border: 1px solid rgba(128, 0, 32, 0.15);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px;
        padding: 8px 18px;
        font-weight: 700;
        color: #662B37;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #800020 0%, #8B1E3F 100%) !important;
        color: white !important;
    }
    
    /* Input Fields */
    .stTextInput input {
        border-radius: 0.75rem;
        border: 1px solid #DFC0C7;
        background-color: #FAF5F6;
    }
    
    .stTextInput input:focus {
        border-color: #800020;
        box-shadow: 0 0 0 2px rgba(128, 0, 32, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helper to get Supabase Client
@st.cache_resource
def init_supabase():
    url = (
        st.secrets.get("SUPABASE_URL")
        or st.secrets.get("NEXT_PUBLIC_SUPABASE_URL")
        or os.environ.get("SUPABASE_URL")
        or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    )
    key = (
        st.secrets.get("SUPABASE_ANON_KEY")
        or st.secrets.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
        or os.environ.get("SUPABASE_ANON_KEY")
        or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    )

    if not url or not key:
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error initializing Supabase client: {e}")
        return None

supabase = init_supabase()

# Allowed Accounts definition
ACCOUNTS = {
    "Nemo": {
        "name": "Nemo",
        "email": "nemo@focus.app",
        "avatar": "🐠",
        "partner": "pikachu",
    },
    "pikachu": {
        "name": "pikachu",
        "email": "pikachu@focus.app",
        "avatar": "⚡",
        "partner": "Nemo",
    },
}

# Date Helpers
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
today_iso = today.strftime("%Y-%m-%d")
yesterday_iso = yesterday.strftime("%Y-%m-%d")
today_formatted = today.strftime("%A, %B %d, %Y")
yesterday_formatted = yesterday.strftime("%A, %B %d, %Y")
month_formatted = today.strftime("%B %Y")

# Session state initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# If Supabase not configured in secrets
if not supabase:
    st.markdown(
        """
        <div style="text-align: center; padding: 3rem 1rem;">
            <span style="font-size: 3rem;">🎯</span>
            <h1 style="color: #800020; font-weight: 900;">Focus</h1>
            <p style="color: #733844;">Please set your Supabase credentials in Streamlit Secrets or .env.local file.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("⚙️ Configure Supabase Credentials"):
        cfg_url = st.text_input("Supabase URL", placeholder="https://your-project.supabase.co")
        cfg_key = st.text_input("Supabase Anon Key", type="password", placeholder="your-anon-key")
        if st.button("Connect"):
            if cfg_url and cfg_key:
                os.environ["SUPABASE_URL"] = cfg_url
                os.environ["SUPABASE_ANON_KEY"] = cfg_key
                st.cache_resource.clear()
                st.rerun()
    st.stop()


# ------------------------------------------------------------------------------
# AUTHENTICATION SCREEN
# ------------------------------------------------------------------------------
if not st.session_state.user:
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 2rem; margin-bottom: 1.5rem;">
                <div style="display: inline-flex; width: 64px; height: 64px; border-radius: 16px; background: #F7E7EA; align-items: center; justify-content: center; font-size: 32px; border: 1px solid #E5BEC5;">
                    🎯
                </div>
                <h1 style="color: #800020; font-size: 2.2rem; font-weight: 900; margin-top: 0.75rem; margin-bottom: 0;">Focus</h1>
                <p style="color: #733844; font-size: 0.9rem; font-weight: 600; margin-top: 0.25rem;">Sign in to your shared Focus workspace</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown(
                '<div style="background: white; padding: 2rem; border-radius: 1.5rem; border: 1px solid rgba(128, 0, 32, 0.15); box-shadow: 0 10px 30px rgba(128, 0, 32, 0.08);">',
                unsafe_allow_html=True,
            )

            selected_account_name = st.radio(
                "Select Account",
                options=["Nemo", "pikachu"],
                format_func=lambda x: f"🐠 {x}" if x == "Nemo" else f"⚡ {x}",
                horizontal=True,
            )

            password = st.text_input(f"Password for {selected_account_name}", type="password")

            if st.button(f"Log In as {selected_account_name} 🎯", use_container_width=True):
                account = ACCOUNTS[selected_account_name]
                try:
                    res = supabase.auth.sign_in_with_password(
                        {"email": account["email"], "password": password}
                    )
                    if res.user:
                        st.session_state.user = res.user
                        st.session_state.profile = {
                            "id": res.user.id,
                            "name": account["name"],
                            "email": account["email"],
                            "partner_name": account["partner"],
                        }
                        st.rerun()
                except Exception as e:
                    err_msg = str(e)
                    # Attempt auto-signup fallback if account not created yet
                    if "invalid login credentials" in err_msg.lower() or "user not found" in err_msg.lower():
                        try:
                            signup_res = supabase.auth.sign_up(
                                {
                                    "email": account["email"],
                                    "password": password,
                                    "options": {"data": {"full_name": account["name"]}},
                                }
                            )
                            if signup_res.user:
                                # Sign in again
                                retry_res = supabase.auth.sign_in_with_password(
                                    {"email": account["email"], "password": password}
                                )
                                if retry_res.user:
                                    st.session_state.user = retry_res.user
                                    st.session_state.profile = {
                                        "id": retry_res.user.id,
                                        "name": account["name"],
                                        "email": account["email"],
                                        "partner_name": account["partner"],
                                    }
                                    st.rerun()
                        except Exception as e2:
                            err_msg = str(e2)

                    if "email not confirmed" in err_msg.lower():
                        st.error("Email confirmation required. Please run supabase/schema.sql in Supabase SQL Editor to auto-confirm accounts.")
                    else:
                        st.error(f"Login failed: {err_msg}")

            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ------------------------------------------------------------------------------
# MAIN FOCUS DASHBOARD
# ------------------------------------------------------------------------------
current_user = st.session_state.user
profile = st.session_state.profile or {"name": "User", "partner_name": "Partner", "id": current_user.id}
my_name = profile.get("name", "User")
partner_name = profile.get("partner_name", "Partner")
my_avatar = "🐠" if my_name == "Nemo" else "⚡"
partner_avatar = "⚡" if my_name == "Nemo" else "🐠"

# Top Navigation Bar
st.markdown(
    f"""
    <div class="focus-header">
        <div style="display: flex; align-items: center; gap: 0.85rem;">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: #F7E7EA; display: flex; align-items: center; justify-content: center; font-size: 24px; border: 1px solid #E5BEC5;">
                🎯
            </div>
            <div>
                <h1 class="focus-title">Focus</h1>
                <p class="focus-subtitle">{my_name} & {partner_name} • Shared Focus Space</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="background: #FAF0F3; color: #800020; border: 1px solid #E2B7C1; border-radius: 10px; padding: 0.35rem 0.85rem; font-size: 0.8rem; font-weight: 700;">
                {my_avatar} {my_name}
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sign Out button in a compact row
h_col1, h_col2 = st.columns([8, 2])
with h_col2:
    if st.button("Sign Out", key="sign_out_btn"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.profile = None
        st.rerun()

# Tabs for Today, Yesterday, and Monthly
tab_today, tab_yesterday, tab_monthly = st.tabs(
    ["☀️ Today's Focus", "⏳ Yesterday's Focus", "🌙 Monthly Focus"]
)

# Fetch all goals from Supabase
try:
    goals_res = supabase.table("goals").select("*").order("created_at", desc=False).execute()
    all_goals = goals_res.data or []
except Exception as e:
    st.warning(f"Error fetching goals: {e}")
    all_goals = []

# Fetch Partner ID if available
partner_id = None
try:
    partner_prof = supabase.table("profiles").select("id").ilike("name", partner_name).maybe_single().execute()
    if partner_prof.data:
        partner_id = partner_prof.data.get("id")
except Exception:
    pass


def get_goal_date(g):
    if g.get("target_date"):
        return g["target_date"]
    if g.get("created_at"):
        return g["created_at"][:10]
    return today_iso


def render_tab_content(tab_type, date_text):
    st.markdown(
        f'<div style="text-align: center;"><span class="date-banner">📅 {date_text}</span></div>',
        unsafe_allow_html=True,
    )

    # Filter goals for this tab
    if tab_type == "monthly":
        my_list = [g for g in all_goals if g.get("user_id") == current_user.id and g.get("type") == "monthly"]
        part_list = [g for g in all_goals if partner_id and g.get("user_id") == partner_id and g.get("type") == "monthly"]
    elif tab_type == "yesterday":
        my_list = [g for g in all_goals if g.get("user_id") == current_user.id and g.get("type") == "daily" and get_goal_date(g) == yesterday_iso]
        part_list = [g for g in all_goals if partner_id and g.get("user_id") == partner_id and g.get("type") == "daily" and get_goal_date(g) == yesterday_iso]
    else:  # today
        my_list = [g for g in all_goals if g.get("user_id") == current_user.id and g.get("type") == "daily" and (get_goal_date(g) == today_iso or not g.get("created_at"))]
        part_list = [g for g in all_goals if partner_id and g.get("user_id") == partner_id and g.get("type") == "daily" and (get_goal_date(g) == today_iso or not g.get("created_at"))]

    col_left, col_right = st.columns(2)

    # --- LEFT COLUMN: My Focus ---
    with col_left:
        st.markdown(
            f"""
            <div class="focus-card">
                <div class="column-title">
                    <span>{my_avatar}</span> {my_name}'s Focus
                </div>
            """,
            unsafe_allow_html=True,
        )

        my_completed = len([g for g in my_list if g.get("is_completed")])
        my_total = len(my_list)
        my_pct = (my_completed / my_total) if my_total > 0 else 0.0

        st.caption(f"**{my_completed}/{my_total} Done**")
        st.progress(my_pct)

        # Add Goal Form (Only for Today and Monthly)
        if tab_type != "yesterday":
            with st.form(key=f"add_form_{tab_type}", clear_on_submit=True):
                new_title = st.text_input(
                    "Add Focus",
                    placeholder="Add a focus item..." if tab_type == "today" else "Add a monthly focus item...",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button("Add")
                if submitted and new_title.strip():
                    g_type = "monthly" if tab_type == "monthly" else "daily"
                    try:
                        # Try insert with target_date
                        supabase.table("goals").insert({
                            "user_id": current_user.id,
                            "title": new_title.strip(),
                            "type": g_type,
                            "target_date": today_iso,
                            "is_completed": False,
                        }).execute()
                    except Exception:
                        # Fallback without target_date
                        supabase.table("goals").insert({
                            "user_id": current_user.id,
                            "title": new_title.strip(),
                            "type": g_type,
                            "is_completed": False,
                        }).execute()
                    st.rerun()
        else:
            st.info("🔒 Yesterday's list is archived. You can check off items or copy unfinished tasks to Today.")

        # Goal Items list
        if not my_list:
            st.markdown(
                '<p style="color: #9E6772; font-style: italic; text-align: center; padding: 1.5rem;">No focus items found.</p>',
                unsafe_allow_html=True,
            )
        else:
            for g in my_list:
                g_id = g["id"]
                g_done = g.get("is_completed", False)
                g_title = g.get("title", "")

                c_check, c_btn = st.columns([8, 2])
                with c_check:
                    new_val = st.checkbox(
                        g_title,
                        value=g_done,
                        key=f"chk_{tab_type}_{g_id}",
                    )
                    if new_val != g_done:
                        supabase.table("goals").update({"is_completed": new_val}).eq("id", g_id).execute()
                        st.rerun()

                with c_btn:
                    # If in yesterday and not completed, provide 1-click + Today button
                    if tab_type == "yesterday" and not g_done:
                        if st.button("➕ Today", key=f"cpy_{g_id}", help="Carry over to Today"):
                            supabase.table("goals").insert({
                                "user_id": current_user.id,
                                "title": g_title,
                                "type": "daily",
                                "target_date": today_iso,
                                "is_completed": False,
                            }).execute()
                            st.toast("Carried over to Today's Focus! 🎯")
                            st.rerun()
                    else:
                        if st.button("✕", key=f"del_{tab_type}_{g_id}", help="Delete item"):
                            supabase.table("goals").delete().eq("id", g_id).execute()
                            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: Partner's Focus ---
    with col_right:
        st.markdown(
            f"""
            <div class="focus-card">
                <div class="partner-title">
                    <span>{partner_avatar}</span> {partner_name}'s Focus
                </div>
            """,
            unsafe_allow_html=True,
        )

        part_completed = len([g for g in part_list if g.get("is_completed")])
        part_total = len(part_list)
        part_pct = (part_completed / part_total) if part_total > 0 else 0.0

        st.caption(f"**{part_completed}/{part_total} Done**")
        st.progress(part_pct)

        if not part_list:
            st.markdown(
                f'<p style="color: #9E6772; font-style: italic; text-align: center; padding: 2rem;">{partner_name} hasn\'t added any items here yet. 🎯</p>',
                unsafe_allow_html=True,
            )
        else:
            for g in part_list:
                g_done = g.get("is_completed", False)
                g_title = g.get("title", "")
                st.checkbox(
                    g_title,
                    value=g_done,
                    disabled=True,
                    key=f"part_chk_{tab_type}_{g['id']}",
                )

        st.markdown(
            f'<div style="text-align: center; font-size: 0.75rem; color: rgba(128, 0, 32, 0.6); margin-top: 1.5rem;">⚡ Synced with {partner_name}\'s Focus</div></div>',
            unsafe_allow_html=True,
        )


with tab_today:
    render_tab_content("today", f"Today: {today_formatted}")

with tab_yesterday:
    render_tab_content("yesterday", f"Yesterday: {yesterday_formatted} (Archived)")

with tab_monthly:
    render_tab_content("monthly", f"Monthly Focus for {month_formatted}")
