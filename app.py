import streamlit as st
import os
from groq import Groq
from datetime import datetime
import json
import re
import logging
from typing import Dict, List, Optional

# Import our custom modules
try:
    from config import Config
    from youtube_collector import YouTubeRecipeCollector
    from recipe_processor import RecipeProcessor
    YOUTUBE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"YouTube features not available: {e}")
    YOUTUBE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)

# AI Shopping List App
st.set_page_config(
    page_title="AI Shopping List Generator",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛒 AI-Powered Grocery List Generator")
st.markdown("### *With YouTube Recipe Integration*")
st.write("Generate personalized shopping lists based on your favorite dishes, enhanced with AI and YouTube recipe data!")

# --- Configuration ---
try:
    config = Config.validate()
    client = Groq(api_key=config.GROQ_API_KEY)
except ValueError as e:
    st.error(f"Configuration error: {e}")
    st.stop()

# Initialize components
if YOUTUBE_AVAILABLE:
    youtube_collector = YouTubeRecipeCollector()
    recipe_processor = RecipeProcessor()
else:
    youtube_collector = None
    recipe_processor = None

# Initialize session state
if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = {}
if "recipe_data" not in st.session_state:
    st.session_state.recipe_data = {}
if "video_tutorials" not in st.session_state:
    st.session_state.video_tutorials = []
if "cooking_instructions" not in st.session_state:
    st.session_state.cooking_instructions = []

# --- Enhanced Functions ---
def generate_shopping_list_with_ai(dishes: List[str], use_youtube: bool = True) -> Dict:
    """
    Enhanced shopping list generation with optional YouTube integration
    """
    result = {
        "shopping_list": {},
        "video_tutorials": [],
        "cooking_instructions": [],
        "recipe_data": {}
    }
    
    # If YouTube is available and enabled, collect recipe data
    if use_youtube and YOUTUBE_AVAILABLE and youtube_collector.youtube:
        st.info("🔍 Searching YouTube for recipe videos...")
        
        all_ingredients = []
        for dish in dishes:
            with st.spinner(f"Analyzing recipes for {dish}..."):
                recipe_data = youtube_collector.get_recipe_data(dish)
                if recipe_data:
                    summary = recipe_processor.generate_recipe_summary(recipe_data)
                    result["recipe_data"][dish] = summary
                    all_ingredients.extend(recipe_data.get("ingredients", []))
                    result["video_tutorials"].extend(summary.get("video_tutorials", []))
                    result["cooking_instructions"].extend(summary.get("cooking_instructions", []))
        
        # Process and categorize ingredients
        if all_ingredients:
            result["shopping_list"] = recipe_processor.process_ingredients_list(all_ingredients)
    
    # Fallback to AI-only generation or enhance AI with YouTube data
    ai_list = generate_ai_shopping_list(dishes, result["shopping_list"])
    
    # Merge AI results with YouTube data
    if result["shopping_list"]:
        result["shopping_list"] = recipe_processor.merge_shopping_lists(
            result["shopping_list"], ai_list
        )
    else:
        result["shopping_list"] = ai_list
    
    return result

def generate_ai_shopping_list(dishes: List[str], existing_list: Dict = None) -> Dict:
    """
    Generate shopping list using AI with optional existing ingredients context
    """
    dishes_text = ", ".join(dishes)
    
    context = ""
    if existing_list:
        context = f"\nExisting ingredients found from recipe analysis: {json.dumps(existing_list, indent=2)}\n"
    
    prompt = f"""
    You are an expert chef and shopping list assistant.
    A user wants to cook the following dish(es): "{dishes_text}".
    {context}
    Please generate a comprehensive shopping list for these dishes.
    Include specific quantities and consider serving sizes for 4 people.
    
    The output should be a clean JSON object where keys are categories and values are lists of ingredients.
    Categories should include: "Produce", "Meat & Seafood", "Dairy & Eggs", "Pantry Staples", "Bakery", "Condiments", "Frozen"
    
    For each ingredient, include quantity when possible (e.g., "2 large onions", "1 lb ground beef", "1 cup milk").
    
    Generate the shopping list now.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model=config.GROQ_MODEL,
            temperature=config.TEMPERATURE,
            response_format={"type": "json_object"},
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Clean JSON response
        json_match = re.search(r"```json\n(.*)\n```", response_text, re.S)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response_text
            
        return json.loads(json_str)

    except Exception as e:
        st.error(f"Error generating AI shopping list: {e}")
        return {}

def display_enhanced_shopping_list():
    """
    Display the shopping list with enhanced features
    """
    if not st.session_state.shopping_list:
        st.info("Your shopping list is currently empty.")
        return

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🛍️ Your Shopping List")
        
        all_items = []
        for category, items in st.session_state.shopping_list.items():
            if items:  # Only show categories with items
                st.markdown(f"**{category}**")
                for i, item in enumerate(items):
                    key = f"{category}-{i}-{item}"
                    checked = st.checkbox(item, key=key)
                    if not checked:
                        all_items.append(item)
                st.markdown("---")
        
        # Download options
        if all_items:
            list_text = "\n".join([f"• {item}" for item in all_items])
            st.download_button(
                label="📄 Download Shopping List",
                data=list_text,
                file_name=f"shopping_list_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    with col2:
        st.subheader("📊 List Summary")
        total_items = sum(len(items) for items in st.session_state.shopping_list.values())
        st.metric("Total Items", total_items)
        
        categories = len([cat for cat, items in st.session_state.shopping_list.items() if items])
        st.metric("Categories", categories)

def display_video_tutorials():
    """
    Display YouTube video tutorials
    """
    if not st.session_state.video_tutorials:
        return
        
    st.subheader("📺 Cooking Tutorials")
    
    for i, video in enumerate(st.session_state.video_tutorials[:6]):  # Show max 6 videos
        with st.expander(f"🎥 {video['title'][:50]}..." if len(video['title']) > 50 else f"🎥 {video['title']}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(f"**Channel:** {video['channel']}")
                st.link_button("Watch on YouTube", video['url'])
            
            with col2:
                # Embed YouTube video
                if video['video_id']:
                    st.video(f"https://www.youtube.com/watch?v={video['video_id']}")

def display_cooking_instructions():
    """
    Display extracted cooking instructions
    """
    if not st.session_state.cooking_instructions:
        return
        
    st.subheader("👨‍🍳 Cooking Instructions")
    
    instructions = list(set(st.session_state.cooking_instructions))[:10]  # Remove duplicates, max 10
    
    for i, instruction in enumerate(instructions, 1):
        st.write(f"{i}. {instruction}")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key status
    st.subheader("🔑 API Status")
    if config.GROQ_API_KEY:
        st.success("✅ Groq API Connected")
    else:
        st.error("❌ Groq API Key Missing")
    
    if YOUTUBE_AVAILABLE:
        if config.YOUTUBE_API_KEY:
            st.success("✅ YouTube API Connected")
            use_youtube = st.checkbox("Use YouTube Recipe Data", value=True)
        else:
            st.warning("⚠️ YouTube API Key Missing")
            st.info("Add YOUTUBE_API_KEY to environment variables for enhanced features")
            use_youtube = False
    else:
        st.warning("⚠️ YouTube Features Unavailable")
        st.info("Install required packages: youtube-transcript-api, google-api-python-client")
        use_youtube = False
    
    st.subheader("🎯 Preferences")
    serving_size = st.slider("Serving Size", 1, 10, 4)
    dietary_restrictions = st.multiselect(
        "Dietary Restrictions",
        ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto"]
    )
    
    st.subheader("📊 Statistics")
    total_lists = len(st.session_state.get("shopping_list", {}))
    st.metric("Lists Generated", total_lists)
    
    if st.button("🗑️ Clear All Data"):
        st.session_state.shopping_list = {}
        st.session_state.recipe_data = {}
        st.session_state.video_tutorials = []
        st.session_state.cooking_instructions = []
        st.rerun()

# --- Main UI Layout ---
st.header("🎯 Generate Your Shopping List")

# Recipe input section
with st.form("recipe_form"):
    st.write("What dishes do you want to cook? (Enter each dish on a separate line)")
    
    # Text area for multiple dishes
    dishes_input = st.text_area(
        "Dishes to cook:",
        placeholder="Spaghetti Carbonara\nCaesar Salad\nChocolate Chip Cookies",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("🚀 Generate Shopping List", type="primary")
    with col2:
        if YOUTUBE_AVAILABLE and config.YOUTUBE_API_KEY:
            use_youtube_form = st.checkbox("Include YouTube Recipe Data", value=use_youtube if 'use_youtube' in locals() else True)
        else:
            use_youtube_form = False

# Process form submission
if submitted and dishes_input.strip():
    dishes = [dish.strip() for dish in dishes_input.strip().split('\n') if dish.strip()]
    
    if dishes:
        with st.spinner("🧠 Generating your personalized shopping list..."):
            result = generate_shopping_list_with_ai(dishes, use_youtube_form)
            
            # Update session state
            st.session_state.shopping_list = result["shopping_list"]
            st.session_state.video_tutorials = result["video_tutorials"]
            st.session_state.cooking_instructions = result["cooking_instructions"]
            st.session_state.recipe_data = result["recipe_data"]
            
            if result["shopping_list"]:
                st.success(f"✅ Generated shopping list for {len(dishes)} dish(es)!")
                if result["video_tutorials"]:
                    st.info(f"🎥 Found {len(result['video_tutorials'])} video tutorials!")
            else:
                st.error("❌ Failed to generate shopping list. Please try again.")

# Display sections
st.divider()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["🛍️ Shopping List", "📺 Video Tutorials", "👨‍🍳 Cooking Instructions"])

with tab1:
    display_enhanced_shopping_list()

with tab2:
    display_video_tutorials()

with tab3:
    display_cooking_instructions()

# --- Additional Features ---
st.divider()
st.subheader("🔧 Additional Tools")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Export to PDF"):
        st.info("PDF export feature coming soon!")

with col2:
    if st.button("📱 Send to Phone"):
        st.info("Mobile sharing feature coming soon!")

with col3:
    if st.button("🔄 Refresh Data"):
        st.rerun()

# --- Footer ---
st.divider()
st.markdown("""
### 🌟 About This App
This AI-Powered Grocery List Generator uses advanced AI and YouTube recipe data to create personalized shopping lists. 
Features include:
- 🤖 AI-powered ingredient analysis
- 📺 YouTube recipe integration
- 🎯 Smart categorization
- 📋 Downloadable lists
- 🍳 Cooking tutorials

**Need API Keys?**
- [Get Groq API Key](https://console.groq.com/keys) (Required)
- [Get YouTube API Key](https://console.cloud.google.com/) (Optional, for enhanced features)

Made with ❤️ using Streamlit and Groq AI
""")

# --- Debug Information (only in development) ---
if st.checkbox("🔍 Show Debug Info"):
    st.subheader("Debug Information")
    st.write("Session State:", st.session_state)
    st.write("YOUTUBE_AVAILABLE:", YOUTUBE_AVAILABLE)
    st.write("Config:", {
        "GROQ_API_KEY": "Set" if config.GROQ_API_KEY else "Not Set",
        "YOUTUBE_API_KEY": "Set" if config.YOUTUBE_API_KEY else "Not Set"
    })
