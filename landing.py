import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import pathlib

# Page configuration
st.set_page_config(
    page_title="AI Grading System For Computer Based Theory Tests",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: #01AA12;
        line-height: 1.2;
    }
    .subtitle {
        font-size: 1.5rem !important;
        color: #002D05;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
    }
    .logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2E8A1E;
    }
    .section-header {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #2E8A1E;
        margin-top: 2rem !important;
    }
    .feature-card {
        background-color: #F0FCE9;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .feature-title {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #2E8A1E;
    }
    .feature-text {
        color: #384C35;
    }
    .cta-container {
        background-color: #EFFFF1;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
        text-align: center;
    }
    .footer {
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        color: #64748B;
    }
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1E8A2E;
    }
    .metric-label {
        font-size: 1rem !important;
        color: #475569;
    }

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="logo-text">📝 AI Grading System for <br> Computer Based Theory Test</div>
    <div>
        <p style="color: #1E8A1E; display: inline; cursor: pointer;" 
        onmouseover="this.style.textDecoration='underline'" 
        onmouseout="this.style.textDecoration='none'">Features</p> &nbsp;&nbsp;
        <p style="color: #1E8A1E; display: inline; cursor: pointer;" 
        onmouseover="this.style.textDecoration='underline'" 
        onmouseout="this.style.textDecoration='none'">How It Works</p> &nbsp;&nbsp;
        <p style="color: #1E8A1E; display: inline; cursor: pointer;" 
        onmouseover="this.style.textDecoration='underline'" 
        onmouseout="this.style.textDecoration='none'">Pricing</p> &nbsp;&nbsp;
        <p style="color: #1E8A1E; display: inline; cursor: pointer;" 
        onmouseover="this.style.textDecoration='underline'" 
        onmouseout="this.style.textDecoration='none'">Contact</p>
    </div>

</div>
""", unsafe_allow_html=True)

# Hero Section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<p class="title">Spend Less Time Grading, More Time Inspiring</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Cut Grading Time from Hours to Minutes with AI-Driven Theory Assessment</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn3, col_btn2 = st.columns([1, 1, 2])
    with col_btn1:
        if st.button("Sign Up", use_container_width=True, key="get_started"):
            st.switch_page("pages/signup.py")
    with col_btn3:
        if st.button("Log in", use_container_width=True):
            st.switch_page("pages/login.py")
    with col_btn2:
        st.button("Watch Demo", use_container_width=False, type="secondary")
    

with col2:
    # Placeholder for hero image
    st.image("teachers/20.png", use_container_width=True)

# Metrics Section
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<p class="metric-value">87%</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Time Saved on Grading</p>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="metric-value">99%</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Grading Accuracy</p>', unsafe_allow_html=True)

with col3:
    st.markdown('<p class="metric-value">5k+</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Educators Using GradeGenius</p>', unsafe_allow_html=True)

# Features Section
st.markdown('<h2 class="section-header" id="features">Key Features</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <p class="feature-title">AI-Powered Grading</p>
        <p class="feature-text">Our advanced AI algorithms grade assignments with human-like understanding, providing consistent and fair evaluations.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <p class="feature-title">Detailed Feedback</p>
        <p class="feature-text">Generate personalized feedback for each student, highlighting strengths and areas for improvement.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <p class="feature-title">Multiple Format Support</p>
        <p class="feature-text">Grade essays, multiple choice, short answers, math problems, and code assignments all in one platform.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <p class="feature-title">Plagiarism Detection</p>
        <p class="feature-text">Automatically detect potential plagiarism and similar submissions across your class.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <p class="feature-title">LMS Integration</p>
        <p class="feature-text">Seamlessly integrate with popular learning management systems like Canvas, Blackboard, and Moodle.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <p class="feature-title">Analytics Dashboard</p>
        <p class="feature-text">Gain insights into student performance with comprehensive analytics and reporting tools.</p>
    </div>
    """, unsafe_allow_html=True)

# How It Works Section
st.markdown('<h2 class="section-header" id="how-it-works">How It Works</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("teachers/18.png", use_container_width=True)
    st.markdown("<p style='text-align: center; font-weight: 600;'>1. Create Exams </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>You can create an exam by uploading your lecture material.</p>", unsafe_allow_html=True)

with col2:
    st.image("teachers/17.png", use_container_width=True)
    st.markdown("<p style='text-align: center; font-weight: 600;'>2. AI Grading</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Our AI analyzes and grades your student submissions based on your marking guide.</p>", unsafe_allow_html=True)

with col3:
    st.image("teachers/19.png", use_container_width=True)
    st.markdown("<p style='text-align: center; font-weight: 600;'>3. Review & Export</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Review AI-generated grades, make adjustments if needed, and export the result.</p>", unsafe_allow_html=True)

# Demo Section
st.markdown('<h2 class="section-header">See GradeGenius in Action</h2>', unsafe_allow_html=True)

# Sample grading dashboard
st.markdown("### Sample Grading Dashboard")

# Create sample data
data = {
    'Student': ['Alex Johnson', 'Maria Garcia', 'James Smith', 'Aisha Patel', 'David Kim'],
    'Test': ['Essay #1', 'Essay #1', 'Essay #1', 'Essay #1', 'Essay #1'],
    'Score': [92, 88, 76, 95, 84],
    'Feedback': [
        'Excellent thesis and supporting arguments. Consider adding more examples.',
        'Well-structured essay. Work on transitions between paragraphs.',
        'Good ideas but needs better organization. Several grammar errors.',
        'Outstanding analysis and writing style. Very thorough research.',
        'Solid work overall. Could improve conclusion and citation format.'
    ]
}

df = pd.DataFrame(data)

# Add a color gradient based on scores
def color_score(val):
    if val >= 90:
        color = 'background-color: #DCFCE7'  # light green
    elif val >= 80:
        color = 'background-color: #E0F2FE'  # light blue
    elif val >= 70:
        color = 'background-color: #FEF9C3'  # light yellow
    else:
        color = 'background-color: #FEE2E2'  # light red
    return f'{color}'

# Apply the styling
styled_df = df.style.applymap(color_score, subset=['Score'])

# Display the dataframe
st.dataframe(styled_df, use_container_width=True)

# Sample visualization
st.markdown("### Class Performance Analytics")

# Generate sample data for visualization
categories = ['Content', 'Organization', 'Grammar', 'Citations', 'Creativity']
class_avg = [85, 78, 82, 75, 88]
top_student = [95, 92, 88, 90, 96]

# Create a chart
chart_data = pd.DataFrame({
    'Category': categories,
    'Class Average': class_avg,
    'Top Performer': top_student
})

chart_data = pd.melt(chart_data, id_vars=['Category'], var_name='Metric', value_name='Score')
st.bar_chart(chart_data.pivot(index='Category', columns='Metric', values='Score'))

# Testimonials
st.markdown('<h2 class="section-header">What Educators Say</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #F8FAFC; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <p style="font-style: italic;">"GradeGenius has revolutionized my teaching workflow. I now spend more time providing personalized guidance to students instead of basic grading."</p>
        <p style="font-weight: 600;">Dr. Sarah Johnson</p>
        <p>Professor of English, Stanford University</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #F8FAFC; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <p style="font-style: italic;">"The accuracy of GradeGenius is impressive. It catches nuances in student responses that I would, and provides consistent grading across all submissions."</p>
        <p style="font-weight: 600;">Prof. Michael Chen</p>
        <p>Computer Science Department, MIT</p>
    </div>
    """, unsafe_allow_html=True)

# Pricing Section
st.markdown('<h2 class="section-header" id="pricing">Pricing Plans</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #F8FAFC; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); height: 100%;">
        <p style="font-size: 1.25rem; font-weight: 600; color: #1E8A23;">Starter</p>
        <p style="font-size: 2rem; font-weight: 700; color: #1E8A23;">$49<span style="font-size: 1rem; font-weight: 400; color: #475569;">/month</span></p>
        <p>Perfect for individual teachers</p>
        <ul>
            <li>Up to 100 assignments per month</li>
            <li>Basic analytics</li>
            <li>Email support</li>
            <li>1 course integration</li>
        </ul>
        <div style="margin-top: 1rem;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Choose Starter", key="starter_btn", use_container_width=True)

with col2:
    st.markdown("""
    <div style="background-color: #E8FFE3; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 2px solid #1E8A23; height: 100%;">
        <p style="font-size: 1.25rem; font-weight: 600; color: #1E8A23;">Professional</p>
        <p style="font-size: 2rem; font-weight: 700; color: #1E8A23;">$99<span style="font-size: 1rem; font-weight: 400; color: #475569;">/month</span></p>
        <p>Ideal for department use</p>
        <ul>
            <li>Unlimited assignments</li>
            <li>Advanced analytics</li>
            <li>Priority support</li>
            <li>5 course integrations</li>
            <li>Plagiarism detection</li>
        </ul>
        <div style="margin-top: 1rem;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Choose Professional", key="pro_btn", type="primary", use_container_width=True)

with col3:
    st.markdown("""
    <div style="background-color: #F8FAFC; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); height: 100%;">
        <p style="font-size: 1.25rem; font-weight: 600; color: #1E8A23;">Enterprise</p>
        <p style="font-size: 2rem; font-weight: 700; color: #1E8A23;">Custom</p>
        <p>For institutions and universities</p>
        <ul>
            <li>Unlimited everything</li>
            <li>Custom integrations</li>
            <li>24/7 dedicated support</li>
            <li>Custom AI training</li>
            <li>On-premise deployment option</li>
            <li>SLA guarantees</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.button("Contact Sales", key="enterprise_btn", use_container_width=True)

# Call to Action
st.markdown("""
<div class="cta-container">
    <h2 style="font-size: 2rem; font-weight: 600; color: #2B8A1E;">Ready to transform your grading process?</h2>
    <p style="font-size: 1.25rem; color: #47694C; margin-bottom: 1.5rem;">Join thousands of educators saving time and providing better feedback.</p>
</div>
""", unsafe_allow_html=True)

cta_col1, cta_col2, cta_col3 = st.columns([2, 1, 2])

with cta_col2:
    st.button("Start Free Trial", type="primary", use_container_width=True)

# Contact Section
st.markdown('<h2 class="section-header" id="contact">Contact Us</h2>', unsafe_allow_html=True)

contact_col1, contact_col2 = st.columns(2)

with contact_col1:
    st.text_input("Name")
    st.text_input("Email")
    st.text_area("Message")
    st.button("Send Message")

with contact_col2:
    st.markdown("""
    <div style="padding: 1rem;">
        <p style="font-weight: 600; font-size: 1.25rem;">Get in Touch</p>
        <p>Have questions about GradeGenius? Our team is here to help.</p>
        <p style="margin-top: 1rem;"><strong>Email:</strong> info@gradegenius.com</p>
        <p><strong>Phone:</strong> (555) 123-4567</p>
        <p><strong>Hours:</strong> Monday-Friday, 9am-5pm EST</p>
    </div>
    """, unsafe_allow_html=True)

# FAQ Section
st.markdown('<h2 class="section-header">Frequently Asked Questions</h2>', unsafe_allow_html=True)

with st.expander("How accurate is the AI grading?"):
    st.write("Our AI grading system has been trained on millions of assignments and achieves an accuracy rate of over 95% compared to human graders. The system continues to learn and improve with each use.")

with st.expander("Can I customize the grading rubric?"):
    st.write("Yes! GradeGenius allows you to create custom rubrics with specific criteria and point values. You can save multiple rubrics for different assignment types.")

with st.expander("How does the integration with LMS work?"):
    st.write("GradeGenius offers seamless integration with popular LMS platforms through API connections and LTI standards. Once connected, you can import assignments directly and push grades back to your LMS gradebook.")

with st.expander("Is my data secure?"):
    st.write("Absolutely. GradeGenius employs enterprise-grade security measures including encryption, secure authentication, and regular security audits. We are FERPA compliant and never share your data with third parties.")

with st.expander("Can I try before I buy?"):
    st.write("Yes, we offer a 14-day free trial with full access to all features. No credit card required to start your trial.")

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 GradeGenius. All rights reserved.</p>
    <p>Privacy Policy | Terms of Service | Support</p>
</div>
""", unsafe_allow_html=True)