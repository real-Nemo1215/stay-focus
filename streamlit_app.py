import streamlit as st
import os
import datetime
from dotenv import load_dotenv

# Load local environment variables
load_dotenv(".env.local")
load_dotenv(".env")

# Page Configuration
st.set_page_config(
    page_title="Focus 🎯 - Shared Daily & Monthly Focus Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom High-Fidelity CSS matching Next.js Tailwind design exactly
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Hide standard Streamlit header, toolbar, and footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1050px !important;
    }

    html, body, [class*="css"] {
        font-family: 'Geist', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #FAF4F6 0%, #F5E6E9 50%, #EED6DC 100%) !important;
        color: #1f2937;
    }

    /* Top Header Bar */
    .app-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 0, 32, 0.15);
        border-radius: 1.5rem;
        padding: 1rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .app-logo-box {
        width: 48px;
        height: 48px;
        border-radius: 1rem;
        background: #F7E7EA;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        border: 1px solid #E5BEC5;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    .app-title {
        font-size: 1.5rem;
        font-weight: 900;
        color: #800020;
        letter-spacing: -0.025em;
        line-height: 1.2;
        margin: 0;
    }
    .app-subtitle {
        font-size: 0.75rem;
        color: #733844;
        font-weight: 600;
        margin: 0;
    }
    .user-badge {
        background: #FAF0F3;
        color: #800020;
        border: 1px solid #E2B7C1;
        border-radius: 0.75rem;
        padding: 0.35rem 0.85rem;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }

    /* Date Banner */
    .date-banner-wrap {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    .date-banner {
        background: #FAF0F3;
        border: 1px solid #E5BEC5;
        color: #800020;
        padding: 0.35rem 1.25rem;
        border-radius: 1rem;
        font-size: 0.825rem;
        font-weight: 700;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* Two Column Cards */
    .focus-panel {
        background: #FFFFFF;
        border: 1px solid rgba(128, 0, 32, 0.15);
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
    }
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .panel-title {
        font-size: 1.15rem;
        font-weight: 900;
        color: #800020;
        margin: 0;
    }
    .partner-panel-title {
        font-size: 1.15rem;
        font-weight: 900;
        color: #5C0A19;
        margin: 0;
    }
    .status-badge {
        background: #FAF0F3;
        color: #800020;
        border: 1px solid #E5BEC5;
        border-radius: 9999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #800020, #9C1B33) !important;
        border-radius: 9999px !important;
    }
    .stProgress > div > div > div {
        background: #FAF0F3 !important;
        border: 1px solid #F0D5DA !important;
        border-radius: 9999px !important;
        height: 10px !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #800020 0%, #8B1E3F 50%, #5C0A19 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: 0 2px 6px rgba(128, 0, 32, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #6B001A 0%, #751532 50%, #470613 100%) !important;
        box-shadow: 0 4px 12px rgba(128, 0, 32, 0.3) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(128, 0, 32, 0.2) !important;
        border-radius: 9999px !important;
        padding: 4px !important;
        box-shadow: 0 2px 8px rgba(128, 0, 32, 0.05) !important;
        margin-bottom: 0.75rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px !important;
        padding: 8px 20px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #662B37 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #800020 0%, #8B1E3F 50%, #5C0A19 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 6px rgba(128, 0, 32, 0.25) !important;
    }

    /* Input text box */
    .stTextInput input {
        border-radius: 0.75rem !important;
        border: 1px solid #DFC0C7 !important;
        background-color: #FAF5F6 !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.875rem !important;
    }
    .stTextInput input:focus {
        border-color: #800020 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(128, 0, 32, 0.15) !important;
    }

    /* Task Item Rows */
    .task-row {
        background: #FAF3F5;
        border: 1px solid #E9CAD1;
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
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
        st.error(f"Error connecting to Supabase: {e}")
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

# Date Computations
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

# If Supabase credentials are missing
if not supabase:
    st.markdown(
        """
        <div style="text-align: center; padding: 3rem 1rem;">
            <span style="font-size: 3rem;">🎯</span>
            <h1 style="color: #800020; font-weight: 900;">Focus</h1>
            <p style="color: #733844;">Please provide your Supabase credentials to launch Focus.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("⚙️ Connect Supabase"):
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
# AUTHENTICATION SCREEN (Maroon Card without Credential Mentions)
# ------------------------------------------------------------------------------
if not st.session_state.user:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 2.5rem; margin-bottom: 1.5rem;">
                <div style="display: inline-flex; width: 64px; height: 64px; border-radius: 16px; background: #F7E7EA; align-items: center; justify-content: center; font-size: 32px; border: 1px solid #E5BEC5; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);">
                    🎯
                </div>
                <h1 style="color: #800020; font-size: 2.25rem; font-weight: 900; margin-top: 0.75rem; margin-bottom: 0; letter-spacing: -0.025em;">Focus</h1>
                <p style="color: #733844; font-size: 0.9rem; font-weight: 600; margin-top: 0.25rem;">Sign in to your shared Focus workspace</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown(
                '<div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); padding: 2rem; border-radius: 1.5rem; border: 1px solid rgba(128, 0, 32, 0.15); box-shadow: 0 10px 30px rgba(128, 0, 32, 0.08);">',
                unsafe_allow_html=True,
            )

            st.markdown('<p style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #9E5765; text-align: center; margin-bottom: 0.5rem;">Select Account</p>', unsafe_allow_html=True)
            selected_account_name = st.radio(
                "Account",
                options=["Nemo", "pikachu"],
                format_func=lambda x: f"🐠 {x}" if x == "Nemo" else f"⚡ {x}",
                horizontal=True,
                label_visibility="collapsed",
            )

            st.markdown(f'<p style="font-size: 12px; font-weight: 600; color: #541622; margin-top: 1rem; margin-bottom: 0.25rem;">Password for <strong style="color: #800020;">{selected_account_name}</strong></p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

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
                        st.error("Email confirmation is required. Please run supabase/schema.sql in Supabase SQL Editor.")
                    else:
                        st.error("Incorrect password or login failed.")

            st.markdown(
                '<div style="margin-top: 1.5rem; text-align: center; font-size: 12px; color: rgba(128, 0, 32, 0.5); font-weight: 500;">Focus &bull; Shared Goal Tracker</div></div>',
                unsafe_allow_html=True,
            )
    st.stop()


# ------------------------------------------------------------------------------
# MAIN FOCUS DASHBOARD (Maroon Theme, Today/Yesterday/Monthly Tabs)
# ------------------------------------------------------------------------------
current_user = st.session_state.user
profile = st.session_state.profile or {"name": "User", "partner_name": "Partner", "id": current_user.id}
my_name = profile.get("name", "User")
partner_name = profile.get("partner_name", "Partner")
my_avatar = "🐠" if my_name == "Nemo" else "⚡"
partner_avatar = "⚡" if my_name == "Nemo" else "🐠"

# Header Row
head_col, out_col = st.columns([8.5, 1.5])
with head_col:
    st.markdown(
        f"""
        <div class="app-header">
            <div style="display: flex; align-items: center; gap: 0.875rem;">
                <div class="app-logo-box">🎯</div>
                <div>
                    <h1 class="app-title">Focus</h1>
                    <p class="app-subtitle">{my_name} & {partner_name} &bull; Shared Focus Space</p>
                </div>
            </div>
            <div>
                <span class="user-badge">{my_avatar} {my_name}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with out_col:
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    if st.button("Sign Out", key="dash_sign_out", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.profile = None
        st.rerun()

# 3 Main Tabs
tab_today, tab_yesterday, tab_monthly = st.tabs(
    ["☀️ Today's Focus", "⏳ Yesterday's Focus", "🌙 Monthly Focus"]
)

# Fetch all goals from Supabase
try:
    goals_res = supabase.table("goals").select("*").order("created_at", desc=False).execute()
    all_goals = goals_res.data or []
except Exception as e:
    st.warning(f"Error loading goals: {e}")
    all_goals = []

# Fetch Partner ID
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


def render_tab_view(tab_type, banner_label):
    st.markdown(
        f'<div class="date-banner-wrap"><span class="date-banner">📅 {banner_label}</span></div>',
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

    # --- LEFT COLUMN: User's Focus ---
    with col_left:
        my_completed = len([g for g in my_list if g.get("is_completed")])
        my_total = len(my_list)
        my_pct = (my_completed / my_total) if my_total > 0 else 0.0

        st.markdown(
            f"""
            <div class="focus-panel">
                <div class="panel-header">
                    <h2 class="panel-title"><span>{my_avatar}</span> {my_name}'s Focus</h2>
                    <span class="status-badge">{my_completed}/{my_total} Done</span>
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(my_pct)

        # Add form only on Today & Monthly (Locked on Yesterday)
        if tab_type != "yesterday":
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            with st.form(key=f"add_form_{tab_type}", clear_on_submit=True):
                in_col, btn_col = st.columns([8, 2])
                with in_col:
                    new_title = st.text_input(
                        "Add Focus",
                        placeholder="Add today's focus item..." if tab_type == "today" else "Add a monthly focus item...",
                        label_visibility="collapsed",
                    )
                with btn_col:
                    submitted = st.form_submit_button("Add", use_container_width=True)

                if submitted and new_title.strip():
                    g_type = "monthly" if tab_type == "monthly" else "daily"
                    try:
                        supabase.table("goals").insert({
                            "user_id": current_user.id,
                            "title": new_title.strip(),
                            "type": g_type,
                            "target_date": today_iso,
                            "is_completed": False,
                        }).execute()
                    except Exception:
                        supabase.table("goals").insert({
                            "user_id": current_user.id,
                            "title": new_title.strip(),
                            "type": g_type,
                            "is_completed": False,
                        }).execute()
                    st.rerun()
        else:
            st.markdown(
                """
                <div style="background: #FAF3F5; border: 1px solid #E9CAD1; border-radius: 0.75rem; padding: 0.75rem 1rem; font-size: 0.75rem; color: #7A3341; font-weight: 600; display: flex; justify-content: space-between; align-items: center; margin: 0.75rem 0;">
                    <span>🔒 Yesterday's list is archived.</span>
                    <span style="color: #800020; font-weight: 700;">Use '+ Today' to carry over</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # List items
        if not my_list:
            st.markdown(
                """
                <div style="text-align: center; padding: 2.5rem 1rem; color: #9E6772; font-style: italic; font-size: 0.875rem; background: #FAF5F6; border-radius: 1rem; border: 1px dashed #E5CBD1; margin-top: 0.75rem;">
                    No focus items found. ✨
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            for g in my_list:
                g_id = g["id"]
                g_done = g.get("is_completed", False)
                g_title = g.get("title", "")

                row_col1, row_col2 = st.columns([8, 2])
                with row_col1:
                    new_val = st.checkbox(
                        g_title,
                        value=g_done,
                        key=f"item_{tab_type}_{g_id}",
                    )
                    if new_val != g_done:
                        supabase.table("goals").update({"is_completed": new_val}).eq("id", g_id).execute()
                        st.rerun()

                with row_col2:
                    if tab_type == "yesterday" and not g_done:
                        if st.button("+ Today", key=f"carry_{g_id}", help="Copy to Today's Focus"):
                            supabase.table("goals").insert({
                                "user_id": current_user.id,
                                "title": g_title,
                                "type": "daily",
                                "target_date": today_iso,
                                "is_completed": False,
                            }).execute()
                            st.toast("Carried over to Today! 🎯")
                            st.rerun()
                    else:
                        if st.button("✕", key=f"del_{tab_type}_{g_id}", help="Delete item"):
                            supabase.table("goals").delete().eq("id", g_id).execute()
                            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: Partner's Focus ---
    with col_right:
        part_completed = len([g for g in part_list if g.get("is_completed")])
        part_total = len(part_list)
        part_pct = (part_completed / part_total) if part_total > 0 else 0.0

        st.markdown(
            f"""
            <div class="focus-panel">
                <div class="panel-header">
                    <h2 class="partner-panel-title"><span>{partner_avatar}</span> {partner_name}'s Focus</h2>
                    <span class="status-badge">{part_completed}/{part_total} Done</span>
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(part_pct)

        if not part_list:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 3rem 1rem; color: #9E6772; font-style: italic; font-size: 0.875rem; background: #FAF5F6; border-radius: 1rem; border: 1px dashed #E5CBD1; margin-top: 0.75rem;">
                    {partner_name} hasn't added any items here yet. 🎯
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            for g in part_list:
                g_done = g.get("is_completed", False)
                g_title = g.get("title", "")
                st.checkbox(
                    g_title,
                    value=g_done,
                    disabled=True,
                    key=f"partner_item_{tab_type}_{g['id']}",
                )

        st.markdown(
            f"""
            <div style="text-align: center; font-size: 0.75rem; color: rgba(128, 0, 32, 0.6); font-weight: 600; margin-top: 1.5rem;">
                ⚡ Real-time synced with {partner_name}'s Focus
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


with tab_today:
    render_tab_view("today", f"Today: {today_formatted}")

with tab_yesterday:
    render_tab_view("yesterday", f"Yesterday: {yesterday_formatted} (Archived)")

with tab_monthly:
    render_tab_view("monthly", f"Monthly Focus for {month_formatted}")
