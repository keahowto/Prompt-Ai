# ==============================================================================
# Complete and Correct Code for Prompt.py (v2.1 - Renamed)
# Using "Focused Studio" UI
# ==============================================================================
import streamlit as st
import time
from openai import OpenAI, RateLimitError

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    layout="wide",
    page_title="LDK Prompt", # <-- UPDATED NAME
    page_icon="✨"
)

# --- Custom CSS (Applied for a modern look) ---
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Poppins', sans-serif;
        }
        .stButton > button {
            border-radius: 20px;
            border: 1px solid #33C4FF;
            color: #33C4FF;
            background-color: transparent;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #33C4FF;
            color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# NOTE: This section is for local testing. In production on Streamlit Cloud,
# you should remove these lines and use Secrets management.
# AI_API_KEY = "sk-e0b24d8af1fe456a875f3d95186e11b7"
# AI_BASE_URL = "https://api.deepseek.com/v1"
# AI_MODEL_NAME = "deepseek-chat"

# --- API Configuration & Helper Functions ---
try:
    # Initialize OpenAI Client using Streamlit Secrets
    client = OpenAI(
        api_key=st.secrets["AI_API_KEY"],
        base_url=st.secrets["AI_BASE_URL"],
    )
except (FileNotFoundError, KeyError):
    st.sidebar.error("⚠️ AI_API_KEY or AI_BASE_URL not found in secrets.")

# --- ✨ REWRITTEN FUNCTION FOR OPENAI COMPATIBLE APIS ---
def call_openai_compatible_api(character, setting, lighting, action_emotion, camera, style):
    """Takes simple user inputs and asks the AI to expand them into a structured, cinematic format."""
    
    system_prompt = """
    Act as a creative film director and script enhancer.
    Based on the user's simple inputs, expand on each category to make it more vivid, detailed, and cinematic.
    Your response MUST strictly follow this format, filling in each category. Do not add any other text before or after the formatted response.

    **Your enhanced output:**
    Character: 
    Setting: 
    Lighting: 
    Action & Emotion: 
    Camera: 
    """
    user_prompt = f"""
    **User's simple inputs:**
    - Character: {character}
    - Setting: {setting}
    - Action & Emotion: {action_emotion}
    - Lighting: {lighting}
    - Camera: {camera}
    - Style: {style}
    """
    
    # --- Start of Retry Logic ---
    retries = 3
    delay = 5
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model=st.secrets["AI_MODEL_NAME"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            if i < retries - 1:
                st.warning(f"Rate limit hit. Retrying in {delay} seconds... ({i+1}/{retries})")
                time.sleep(delay)
                delay *= 2
            else:
                st.error(f"An error occurred after multiple retries: {e}")
                return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None
    # --- End of Retry Logic ---

# --- SIDEBAR (Control Panel for "Focused Studio" UI) ---
with st.sidebar:
    st.title("✨ LDK Prompt") # <-- UPDATED NAME
    st.caption("v2.1 - OpenAI Compatible") 
    
    with st.form("control_panel_form"):
        st.header("1. Your Simple Ideas")
        character = st.text_input("Character", placeholder="e.g., a young woman")
        setting = st.text_input("Setting", placeholder="e.g., in a library")
        action_emotion = st.text_input("Action & Emotion", placeholder="e.g., reading a book, feeling happy")
        khmer_dialogue = st.text_area("Dialogue", "ការស្វែងរកចំណេះដឹង គឺពិតជាអស្ចារ្យណាស់។")

        st.divider()

        st.header("2. Technical Style")
        style = st.selectbox("Video Style", ("Cinematic, Photorealistic, 4K", "Documentary Style", "Vlog Style, Handheld", "Anime, Vibrant Colors", "Sci-Fi, Futuristic", "Epic Fantasy, Grand Scale", "Horror, Tense Atmosphere", "Vintage Film Look (8mm/16mm)", "Black and White, Film Noir"))
        camera = st.selectbox("Camera Angle", ("Medium Close-up Shot", "Close-up Shot", "Extreme Close-up", "Wide Shot / Long Shot", "Establishing Shot", "Full Shot", "Low Angle Shot (Looking up)", "High Angle Shot (Looking down)", "Dutch Angle (Tilted)", "Panning Shot (Side to side)", "Tilting Shot (Up and down)", "Dolly Zoom (Vertigo effect)"))
        lighting = st.selectbox("Lighting", ("Golden Hour (Sunrise/Sunset)", "Midday Sun (Harsh shadows)", "Overcast (Soft, diffused light)", "Three-Point Lighting (Key, Fill, Backlight)", "High-Key (Bright, few shadows)", "Low-Key (Dark, high contrast)", "Backlight (Creates a silhouette)", "Neon Lighting (Cyberpunk feel)", "Candlelight (Warm and intimate)"))
        
        st.divider()
        submit_button = st.form_submit_button("✨ Enhance My Ideas", use_container_width=True)

    st.sidebar.divider()
    st.sidebar.markdown("©️ Credit by Kongkea - គង្គា")


# --- MAIN CONTENT AREA (Output Zone) ---
st.header("🎬 LDK Enhanced Prompt") # <-- UPDATED NAME

if submit_button:
    if not all([character, setting, action_emotion]):
        st.error("Please fill in at least the 'Character', 'Setting', and 'Action & Emotion' fields.")
    else:
        # Check if secrets are loaded
        if "AI_API_KEY" not in st.secrets or "AI_BASE_URL" not in st.secrets or "AI_MODEL_NAME" not in st.secrets:
             st.error("Please configure your API Key, Base URL, and Model Name in Streamlit Secrets.")
        else:
            with st.spinner('✨ The AI is enhancing your ideas...'):
                enhanced_output = call_openai_compatible_api(character, setting, lighting, action_emotion, camera, style)

            if enhanced_output:
                st.subheader("✅ AI Generation Complete!")
                final_prompt_text = f"{enhanced_output.strip()}\nDialogue: {khmer_dialogue}"
                with st.container(border=True):
                    st.text(final_prompt_text)
                st.balloons()
            else:
                st.error("Failed to generate an enhanced prompt from the AI.")
else:
    st.info("Fill in your simple ideas on the left, then click 'Enhance My Ideas' to let the AI expand on them.")
