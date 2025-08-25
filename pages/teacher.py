import streamlit as st
import sqlite3
from backend.user import get_first_name_by_email, update_user_info, get_user_profile_by_email

st.set_page_config(page_title="Teacher Dashboard", page_icon="👨‍🏫", layout="wide")

# Enhanced CSS for better styling
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem;
        color: #39AB3D;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f2f6;
    }
    
    /* Card styling */
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #39AB3D;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #39AB3D;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-icon {
        font-size: 1.8rem;
        color: #39AB3D;
        margin-bottom: 0.5rem;
    }
    
    /* Action button styling */
    .action-button {
        background-color: #39AB3D;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 5px;
        text-align: center;
        margin: 0.5rem 0;
        cursor: pointer;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s;
        width: 100%;
    }
    .action-button:hover {
        background-color: #303F9F;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.5rem;
        color: #39AB3D;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #ddd;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    /* Status messages */
    .success-message {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-message {
        background-color: #fff8e1;
        color: #f57f17;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Recent activity styling */
    .activity-item {
        padding: 0.8rem;
        border-left: 3px solid #39AB3D;
        background-color: #f5f7ff;
        margin-bottom: 0.5rem;
        border-radius: 0 5px 5px 0;
    }
    .activity-time {
        font-size: 0.8rem;
        color: #666;
    }
    
    /* Input fields */
    .stTextInput input {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    
    /* Custom button styling */
    div.stButton > button {
        background-color: #39AB3D;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    div.stButton > button:hover {
        background-color: #349F30;
    }
</style>
""", unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("style.css")
except:
    pass  # If the file doesn't exist, continue without it

email = st.session_state.get("email", None)
if email:
    name = get_first_name_by_email(email) 
    user = get_user_profile_by_email(email)

    if user:
        user_id, last_name, other_names, user_type, _, title = user

        if "user_id" not in st.session_state:
            st.session_state["user_id"] = user_id
        
        if user_type == "teacher":
            # Main header with custom styling
            st.markdown(f"<h1 class='main-header'>Welcome, {title if title else ''} {name}</h1>", unsafe_allow_html=True)
            
            # Sidebar with improved styling
            with st.sidebar:
                st.markdown("<h2 class='sidebar-header'>Manage Account</h2>", unsafe_allow_html=True)
                st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
                new_last_name = st.text_input("Last Name", last_name)
                new_other_names = st.text_input("Other Names", other_names)
                new_title = st.text_input("Title", title)
                new_password = st.text_input("New Password (leave blank to keep current)", type="password")

                if st.button("Update Profile"):
                    success = update_user_info(user_id=user_id, last_name=new_last_name, other_names=new_other_names, title=new_title, password=new_password)
                    if success:
                        st.markdown("<div class='success-message'>✅ Profile updated successfully! Refresh to see the new update.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("Logout"):
                    st.session_state.email = None
            
            # Dashboard metrics section
            st.markdown("<h2 style='margin-top: 1.5rem; margin-bottom: 1rem;'>Dashboard Overview</h2>", unsafe_allow_html=True)
            
            # Metrics cards in a 4-column layout
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon">📚</div>
                    <div class="metric-value">24</div>
                    <div class="metric-label">Total Exams</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon">👨‍🎓</div>
                    <div class="metric-value">156</div>
                    <div class="metric-label">Total Students</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-value">78%</div>
                    <div class="metric-label">Average Score</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-icon">🔍</div>
                    <div class="metric-value">12</div>
                    <div class="metric-label">Pending Reviews</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick actions section
            st.markdown("<h2 style='margin-top: 2rem; margin-bottom: 1rem;'>Quick Actions</h2>", unsafe_allow_html=True)
            
            # Action buttons in a 2-column layout
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                if st.button("Create New Exam", key="create_exam"):
                    st.switch_page("pages/create_exam.py")
                    
            with action_col2:
                if st.button("View Results", key="view_results"):
                    st.switch_page("pages/results.py")
            
            # Recent activity section
            st.markdown("<h2 style='margin-top: 2rem; margin-bottom: 1rem;'>Recent Activity</h2>", unsafe_allow_html=True)
            
            # Recent activity in a card layout
            st.markdown("""
            <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div class="activity-item">
                    <strong>Physics 101 Exam</strong> was completed by 18 students
                    <div class="activity-time">Today, 10:45 AM</div>
                </div>
                <div class="activity-item">
                    <strong>Chemistry Final</strong> was created
                    <div class="activity-time">Yesterday, 3:20 PM</div>
                </div>
                <div class="activity-item">
                    <strong>Math Quiz #3</strong> average score: 82%
                    <div class="activity-time">2 days ago, 11:15 AM</div>
                </div>
                <div class="activity-item">
                    <strong>Biology Midterm</strong> was updated
                    <div class="activity-time">3 days ago, 2:30 PM</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Upcoming exams section
            st.markdown("<h2 style='margin-top: 2rem; margin-bottom: 1rem;'>Upcoming Exams</h2>", unsafe_allow_html=True)
            
            upcoming_col1, upcoming_col2 = st.columns(2)
            
            with upcoming_col1:
                st.markdown("""
                <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #349F30; margin-top: 0;">This Week</h3>
                    <ul style="padding-left: 1.5rem;">
                        <li><strong>Computer Science 101</strong> - Tuesday, 10:00 AM</li>
                        <li><strong>Advanced Mathematics</strong> - Wednesday, 2:30 PM</li>
                        <li><strong>Physics Lab Exam</strong> - Friday, 9:00 AM</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            with upcoming_col2:
                st.markdown("""
                <div style="background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #349F30; margin-top: 0;">Next Week</h3>
                    <ul style="padding-left: 1.5rem;">
                        <li><strong>Biology Final</strong> - Monday, 11:00 AM</li>
                        <li><strong>Chemistry Quiz</strong> - Tuesday, 3:00 PM</li>
                        <li><strong>Literature Review</strong> - Thursday, 1:30 PM</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

else:
    st.markdown("<h1 class='main-header'>Teacher Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div class='warning-message'>⚠️ Log in to access your dashboard</div>", unsafe_allow_html=True)
    
    # Center the login button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login"):
            st.switch_page("pages/login.py")