import streamlit as st
import utils
import time

# Page Configuration
st.set_page_config(
    page_title="Lesson Plan Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Feel
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #F63366;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Inputs
with st.sidebar:
    st.title("📚 Lesson Planner")
    st.markdown("Generate comprehensive lesson plans in seconds.")
    
    st.header("Class Details")
    grade = st.selectbox("Class/Grade", ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])
    subject = st.text_input("Subject", placeholder="e.g. Science, Math, History")
    topic = st.text_input("Chapter/Topic", placeholder="e.g. Photosynthesis, WWII")
    duration = st.selectbox("Duration", ["30 mins", "40 mins", "45 mins", "60 mins", "90 mins"])
    
    st.markdown("---")
    
    # Try to get key from secrets
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = st.text_input("Gemini API Key", type="password", help="Get your key from Google AI Studio")
    
    generate_btn = st.button("Generate Lesson Plan")
    
    st.markdown("---")
    st.markdown("Made by **Gunjankumar**")

# Main Content
if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not subject or not topic:
        st.error("Please fill in all fields (Subject and Topic are required).")
    else:
        with st.spinner("Creating your lesson plan..."):
            # Call the Gemini generation function
            plan = utils.generate_lesson_plan(grade, subject, topic, duration, api_key)
            
        if "error" in plan:
            st.error(f"Error: {plan['error']}")
        else:
            # Display Results
            st.title(f"Lesson Plan: {plan['topic']}")
        st.caption(f"{plan['grade']} | {plan['subject']} | {plan['duration']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📘 Learning Objectives")
            for obj in plan.get('objectives', []):
                st.markdown(f"- {obj}")
            
            if 'introduction' in plan:
                st.subheader("🧠 Introduction")
                st.info(plan['introduction'])
                
            if 'explanation_steps' in plan:
                st.subheader("📚 Explanation Steps")
                for step in plan['explanation_steps']:
                    st.markdown(f"- {step}")
            
            st.subheader("🎲 Activities")
            for activity in plan.get('activities', []):
                with st.expander(f"{activity['title']} ({activity['time']})", expanded=True):
                    st.write(activity['description'])
            
            st.subheader("💡 Real-Life Examples")
            for example in plan.get('real_life_examples', []):
                st.markdown(f"- {example}")
                
        with col2:
            st.subheader("🖤 Blackboard Summary")
            st.markdown("""
            <div style="background-color: #262730; color: white; padding: 15px; border-radius: 10px; border: 1px solid #444;">
            """, unsafe_allow_html=True)
            for item in plan.get('blackboard_summary', []):
                st.markdown(f"• {item}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.subheader("🏠 Homework")
            for hw in plan.get('homework', []):
                st.markdown(f"- {hw}")
                
            if 'assessment' in plan:
                st.subheader("📘 Assessment")
                for q in plan['assessment']:
                    st.markdown(f"- {q}")
                
            st.markdown("---")
            st.subheader("🖼️ Topic Images")
            if 'image_keywords' in plan and plan['image_keywords']:
                # Limit to max 4 images
                keywords = plan['image_keywords'][:4]
                cols = st.columns(len(keywords))
                
                import requests
                
                for idx, keyword in enumerate(keywords):
                    with cols[idx]:
                        image_url = f"https://image.pollinations.ai/prompt/{keyword}?width=400&height=300&nologo=true"
                        try:
                            # Fast check if image is reachable
                            response = requests.head(image_url, timeout=3)
                            if response.status_code == 200:
                                st.image(image_url, caption=keyword.capitalize(), use_container_width=True)
                            else:
                                st.warning("Not images available right now")
                        except:
                             st.warning("Not images available right now")
            else:
                st.info("Not images available right now")

else:
    # Empty State
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1>Welcome to the AI Lesson Planner</h1>
        <p style="font-size: 1.2em; color: #888;">
            Enter your class details in the sidebar to generate a structured lesson plan instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)
