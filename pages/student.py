import streamlit as st
from backend.user import get_first_name_by_email, update_user_info, get_user_profile_by_email

st.set_page_config(page_title="Student Dashboard", page_icon="📖", layout="wide")

def load_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Custom CSS for better styling - keeping it minimal and focused
st.markdown("""
<style>
    /* Simple, clean styling */
    .main-header {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .welcome-text {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .action-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1f1f1f;
    }
    .sidebar-form {
        background-color: white;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
    /* Overriding Streamlit styles */
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

email = st.session_state.get("email", None)

if email:
    name = get_first_name_by_email(email)
    user = get_user_profile_by_email(email)

    if user:
        student_id, last_name, other_names, user_type, matric_number, _ = user

        if "user_id" not in st.session_state:
            st.session_state["user_id"] = student_id

    # Simple welcome header
    st.markdown(f"""
    <div class="main-header">
        <div class="welcome-text">Welcome, {name}</div>
        <p>Access your exams and results from this dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Main content - keeping it focused on exam actions
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Exam Actions</div>', unsafe_allow_html=True)
        
        # Hidden buttons for functionality
        if st.button("Take exam", key="take_exam"):
            st.switch_page("pages/take_exam.py")
            
        if st.button("View Results", key="view_result"):
            st.switch_page("pages/result.py")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Simple instructions
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Quick Guide</div>', unsafe_allow_html=True)
        st.markdown("""
        <p><strong>Taking an Exam:</strong> Click the "Take an Exam" button to start a new exam. You'll need an exam code from your instructor.</p>
        <p><strong>Viewing Results:</strong> Click "View Your Results" to see scores from your previous exams.</p>
        <p><strong>Profile Updates:</strong> Use the sidebar to update your personal information if needed.</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced sidebar - keeping the existing functionality
    with st.sidebar:
        st.header("Student Profile")
        st.markdown(f"**Name:** {name}")
        st.markdown(f"**Matric Number:** {matric_number if matric_number else 'Not set'}")
        
        st.markdown("### Update Your Information")
        
        st.markdown('<div class="sidebar-form">', unsafe_allow_html=True)
        with st.form("update_profile"):
            new_last_name = st.text_input("Last Name", last_name)
            new_other_names = st.text_input("Other Names", other_names)
            new_matric_number = st.text_input("Matric Number", matric_number)
            new_password = st.text_input("New Password (leave blank to keep current)", type="password")

            if st.form_submit_button("Update Profile"):
                success = update_user_info(user_id=student_id, last_name=new_last_name, other_names=new_other_names, matric_number=new_matric_number, password=new_password)
                
                if success:
                    st.success("Profile updated successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Logout button
        if st.button("Log Out", type="primary"):
            st.session_state.clear()
else:
    # Login page styling - simple and focused
    st.title("Student Dashboard")
    st.warning("Log in to access your dashboard")
    if st.link_button("Login", "pages/login"):
        st.switch_page("pages/login.py")