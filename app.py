

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

# Import your custom modules
try:
    from exercise_recommender import ExerciseRecommender
    from visualizations import GymDataVisualizer
    from data_processor import GymDataProcessor
    from config import VALID_MUSCLES
except ImportError:
    st.error("Required modules not found. Make sure all the refactored files are in the same directory.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="💪 Gym Exercise Recommender",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .exercise-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .muscle-tag {
        background-color: #ff4b4b;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        margin: 2px;
        display: inline-block;
        font-weight: 500;
    }
    .difficulty-badge {
        background-color: #28a745;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .search-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommender' not in st.session_state:
    st.session_state.recommender = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

@st.cache_resource
def load_recommender():
    """Load and cache the recommender system"""
    try:
        with st.spinner("🔄 Initializing Exercise Recommender..."):
            recommender = ExerciseRecommender()
            recommender.initialize()
            # Verify the vectorstore is properly loaded
            if recommender.vectorstore is None:
                st.error("❌ Failed to initialize vectorstore. Please check your data files.")
                return None
            return recommender
    except Exception as e:
        st.error(f"❌ Error initializing recommender: {str(e)}")
        st.info("💡 Make sure you have run the data processing steps and have all required files.")
        return None

@st.cache_data
def load_gym_data():
    """Load and cache gym data for analysis"""
    processor = GymDataProcessor()
    return processor.generate_exercise_descriptions()

def parse_exercise_details(exercise_text):
    """Parse exercise text into structured data"""
    details = {}
    lines = exercise_text.strip().split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            details[key.strip()] = value.strip()
    return details

def display_exercise_card(exercise_text, index):
    """Display an exercise in a styled card format"""
    details = parse_exercise_details(exercise_text)
    
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    
    # Header with exercise name and key info
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 🏋️‍♂️ {details.get('Exercise Name', 'Unknown Exercise')}")
        
        # Tags for main muscle and difficulty
        main_muscle = details.get('Main Muscle', 'N/A')
        difficulty = details.get('Difficulty (1-5)', 'N/A')
        
        if main_muscle != 'N/A':
            st.markdown(f'<span class="muscle-tag">{main_muscle}</span>', unsafe_allow_html=True)
        
        if difficulty != 'N/A':
            st.markdown(f'<span class="difficulty-badge">Level {difficulty}/5</span>', unsafe_allow_html=True)
    
    with col2:
        equipment = details.get('Equipment', 'N/A')
        mechanics = details.get('Mechanics', 'N/A')
        st.markdown(f"**Equipment:** {equipment}")
        st.markdown(f"**Type:** {mechanics}")
    
    # Key exercise information
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        preparation = details.get('Preparation', 'N/A')
        if preparation != 'N/A':
            st.markdown(f"**🎯 Preparation:**")
            st.markdown(f"{preparation}")
    
    with col_b:
        execution = details.get('Execution', 'N/A')
        if execution != 'N/A':
            st.markdown(f"**⚡ Execution:**")
            st.markdown(f"{execution}")
    
    # Additional details in expandable section
    with st.expander("📋 Additional Details"):
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.markdown(f"**Force:** {details.get('Force', 'N/A')}")
            st.markdown(f"**Utility:** {details.get('Utility', 'N/A')}")
            st.markdown(f"**Variation:** {details.get('Variation', 'N/A')}")
        
        with detail_col2:
            st.markdown(f"**Synergist Muscles:** {details.get('Synergist Muscles', 'N/A')}")
            st.markdown(f"**Secondary Muscles:** {details.get('Secondary Muscles', 'N/A')}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">💪 Gym Exercise Recommender</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🔍 Exercise Search", "📊 Data Analytics", "📈 Search History"]
        )
        
        st.markdown("---")
        st.header("💡 Search Examples")
        st.info("""
        **Try these searches:**
        • "5 chest exercises"
        • "back and shoulder workout"
        • "10 leg exercises"
        • "beginner arm exercises"
        • "core strengthening"
        """)
        
        st.markdown("---")
        st.header("🎯 Available Muscle Groups")
        muscles_text = " • ".join(VALID_MUSCLES)
        st.markdown(f"**{muscles_text}**")
        
        st.markdown("---")
        st.header("ℹ️ How it Works")
        st.markdown("""
        1. **Enter your request** in natural language
        2. **AI understands** your needs
        3. **Get personalized** exercise recommendations
        4. **View detailed** instructions and tips
        """)
    
    # Load recommender
    if st.session_state.recommender is None:
        st.session_state.recommender = load_recommender()
        
    
    # Page routing
    if page == "🔍 Exercise Search":
        exercise_search_page()
    elif page == "📊 Data Analytics":
        analytics_page()
    elif page == "📈 Search History":
        search_history_page()

def exercise_search_page():
    st.header("🔍 Find Your Perfect Workout")
    
    
    # Search interface in a styled container
    # st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "What exercises are you looking for?",
            placeholder="e.g., '5 chest exercises', 'back workout', 'beginner shoulder exercises'",
            help="Describe the exercises you want - include muscle groups, difficulty, or number of exercises",
            label_visibility="collapsed"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search execution
    if search_button and query:
        # Check if recommender is properly initialized
        if st.session_state.recommender is None or st.session_state.recommender.vectorstore is None:
            st.error("❌ Recommender not properly initialized. Please refresh the page.")
            return
            
        with st.spinner("🔍 Finding the perfect exercises for you..."):
            try:
                start_time = time.time()
                exercises = st.session_state.recommender.get_exercises(query)
                search_time = time.time() - start_time
                
                # Add to search history
                st.session_state.search_history.append({
                    'query': query,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'results_count': len(exercises),
                    'search_time': round(search_time, 2)
                })
            except Exception as e:
                st.error(f"❌ Error during search: {str(e)}")
                return
        
        # Display results
        if exercises and not exercises[0].startswith("No valid muscles"):
            st.success(f"✅ Found {len(exercises)} perfect exercises for you!")
            
            # Results summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Results Found", len(exercises))
            with col2:
                st.metric("⚡ Search Time", f"{search_time:.2f}s")
            with col3:
                st.metric("🔍 Your Query", f'"{query}"')
            
            st.markdown("---")
            st.subheader("📋 Your Recommended Exercises")
            
            # Display exercises
            for i, exercise in enumerate(exercises):
                display_exercise_card(exercise, i)
                
        else:
            st.error("❌ No exercises found. Try using different muscle group names or check your spelling!")
            st.info("💡 **Tip:** Try searches like 'chest exercises', 'back workout', or 'arm strengthening'")
    
    elif query and not search_button:
        st.info("👆 Click the Search button to find exercises!")
    
    # Quick search buttons
    if not query:
        # st.markdown("### 🚀 Quick Start - Try These Popular Searches:")
        
        # quick_searches = [
        #     "5 chest exercises",
        #     "back and shoulder workout", 
        #     "10 leg exercises",
        #     "beginner arm exercises",
        #     "core strengthening exercises"
        # ]
        
        # cols = st.columns(len(quick_searches))
        # for i, search_term in enumerate(quick_searches):
        #     with cols[i]:
        #         if st.button(search_term, key=f"quick_{i}", use_container_width=True):
        #             st.session_state.temp_query = search_term
        #             st.rerun()
        
        # Handle quick search selection
        if 'temp_query' in st.session_state:
            query = st.session_state.temp_query
            del st.session_state.temp_query
            
            # Check if recommender is properly initialized
            if st.session_state.recommender is None or st.session_state.recommender.vectorstore is None:
                st.error("❌ Recommender not properly initialized. Please refresh the page.")
                return
            
            with st.spinner("🔍 Finding exercises..."):
                try:
                    start_time = time.time()
                    exercises = st.session_state.recommender.get_exercises(query)
                    search_time = time.time() - start_time
                    
                    # Add to search history
                    st.session_state.search_history.append({
                        'query': query,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'results_count': len(exercises),
                        'search_time': round(search_time, 2)
                    })
                except Exception as e:
                    st.error(f"❌ Error during search: {str(e)}")
                    return
            
            # Display results (same as above)
            if exercises and not exercises[0].startswith("No valid muscles"):
                st.success(f"✅ Found {len(exercises)} exercises for: **{query}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🎯 Results Found", len(exercises))
                with col2:
                    st.metric("⚡ Search Time", f"{search_time:.2f}s")
                with col3:
                    st.metric("🔍 Search", f'"{query}"')
                
                st.markdown("---")
                st.subheader("📋 Your Recommended Exercises")
                
                for i, exercise in enumerate(exercises):
                    display_exercise_card(exercise, i)

def analytics_page():
    st.header("📊 Exercise Database Analytics")
    st.markdown("Explore insights about our comprehensive exercise database")
    
    try:
        # Load data
        gym_data = load_gym_data()
        
        # Overview metrics
        st.subheader("📈 Database Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💪 Total Exercises", len(gym_data))
        with col2:
            st.metric("🎯 Muscle Groups", gym_data['Main_muscle'].nunique())
        with col3:
            st.metric("🛠️ Equipment Types", gym_data['Equipment'].nunique())
        with col4:
            avg_difficulty = gym_data['Difficulty (1-5)'].mean()
            st.metric("📊 Avg Difficulty", f"{avg_difficulty:.1f}/5")
        
        st.markdown("---")
        
        # Main charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Exercises by Muscle Group")
            muscle_counts = gym_data['Main_muscle'].value_counts()
            fig_muscle = px.bar(
                x=muscle_counts.values,
                y=muscle_counts.index,
                orientation='h',
                title="Exercise Distribution by Target Muscle",
                color=muscle_counts.values,
                color_continuous_scale="Reds",
                text=muscle_counts.values
            )
            fig_muscle.update_traces(texttemplate='%{text}', textposition='outside')
            fig_muscle.update_layout(
                showlegend=False, 
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Number of Exercises",
                yaxis_title="Muscle Group"
            )
            st.plotly_chart(fig_muscle, use_container_width=True)
        
        with col2:
            st.subheader("⚖️ Difficulty Distribution")
            difficulty_counts = gym_data['Difficulty (1-5)'].value_counts().sort_index()
            fig_diff = px.pie(
                values=difficulty_counts.values,
                names=[f"Level {x}" for x in difficulty_counts.index],
                title="Exercise Difficulty Breakdown",
                color_discrete_sequence=px.colors.sequential.Reds_r,
                hole=0.4
            )
            fig_diff.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_diff, use_container_width=True)
        
        # Equipment analysis
        st.subheader("🛠️ Most Popular Equipment")
        equipment_counts = gym_data['Equipment'].value_counts().head(12)
        fig_equipment = px.bar(
            x=equipment_counts.index,
            y=equipment_counts.values,
            title="Top Equipment Types Used in Exercises",
            color=equipment_counts.values,
            color_continuous_scale="Reds",
            text=equipment_counts.values
        )
        fig_equipment.update_traces(texttemplate='%{text}', textposition='outside')
        fig_equipment.update_xaxes(tickangle=45)
        fig_equipment.update_layout(
            showlegend=False,
            xaxis_title="Equipment Type",
            yaxis_title="Number of Exercises",
            height=500
        )
        st.plotly_chart(fig_equipment, use_container_width=True)
        
        # Exercise mechanics
        st.subheader("⚙️ Exercise Mechanics Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            mechanics_counts = gym_data['Mechanics'].value_counts()
            fig_mechanics = px.pie(
                values=mechanics_counts.values,
                names=mechanics_counts.index,
                title="Exercise Mechanics Distribution"
            )
            st.plotly_chart(fig_mechanics, use_container_width=True)
        
        with col2:
            utility_counts = gym_data['Utility'].value_counts()
            fig_utility = px.bar(
                x=utility_counts.values,
                y=utility_counts.index,
                orientation='h',
                title="Exercise Utility Types",
                color=utility_counts.values,
                color_continuous_scale="Blues"
            )
            fig_utility.update_layout(showlegend=False)
            st.plotly_chart(fig_utility, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading analytics data: {str(e)}")
        st.info("Make sure your data files are properly loaded and the recommender is initialized.")

def search_history_page():
    st.header("📈 Your Search History")
    st.markdown("Track your workout planning journey and search patterns")
    
    if not st.session_state.search_history:
        st.info("🔍 No search history yet! Start searching for exercises to see your activity here.")
        
        # Show some example searches to get started
        st.markdown("### 🚀 Get Started with These Searches:")
        example_searches = [
            "Try searching for 'chest exercises'",
            "Look up 'back and shoulder workout'", 
            "Find 'beginner leg exercises'",
            "Search for 'core strengthening'"
        ]
        
        for search in example_searches:
            st.markdown(f"• {search}")
        
        return
    
    # Summary metrics
    total_searches = len(st.session_state.search_history)
    total_results = sum(h['results_count'] for h in st.session_state.search_history)
    avg_results = total_results / total_searches
    avg_time = sum(h['search_time'] for h in st.session_state.search_history) / total_searches
    
    st.subheader("📊 Search Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔍 Total Searches", total_searches)
    with col2:
        st.metric("💪 Total Results", total_results)
    with col3:
        st.metric("📈 Avg Results/Search", f"{avg_results:.1f}")
    with col4:
        st.metric("⚡ Avg Search Time", f"{avg_time:.2f}s")
    
    # Clear history button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.search_history = []
            st.rerun()
    
    st.markdown("---")
    
    # Recent searches
    st.subheader("📋 Recent Searches")
    history_df = pd.DataFrame(st.session_state.search_history)
    history_df = history_df.sort_values('timestamp', ascending=False)
    
    # Style the dataframe
    styled_df = history_df.rename(columns={
        "query": "🔍 Search Query",
        "timestamp": "📅 Date & Time", 
        "results_count": "💪 Results Found",
        "search_time": "⚡ Time (seconds)"
    })
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Search performance trends
    if len(st.session_state.search_history) > 2:
        st.subheader("📊 Search Performance Trends")
        
        # Convert timestamps to datetime for plotting
        history_df['datetime'] = pd.to_datetime(history_df['timestamp'])
        history_df = history_df.sort_values('datetime')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Search time trend
            fig_time = px.line(
                history_df,
                x='datetime',
                y='search_time',
                title='Search Response Time Trend',
                markers=True,
                color_discrete_sequence=['#ff4b4b']
            )
            fig_time.update_layout(
                xaxis_title="Time",
                yaxis_title="Search Time (seconds)"
            )
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            # Results count trend
            fig_results = px.line(
                history_df,
                x='datetime',
                y='results_count',
                title='Results Found per Search',
                markers=True,
                color_discrete_sequence=['#28a745']
            )
            fig_results.update_layout(
                xaxis_title="Time",
                yaxis_title="Number of Results"
            )
            st.plotly_chart(fig_results, use_container_width=True)
        
        # Most searched terms
        st.subheader("🏆 Your Most Popular Searches")
        query_counts = history_df['query'].value_counts().head(5)
        
        if len(query_counts) > 0:
            fig_popular = px.bar(
                x=query_counts.values,
                y=query_counts.index,
                orientation='h',
                title="Top 5 Most Repeated Searches",
                color=query_counts.values,
                color_continuous_scale="Reds"
            )
            fig_popular.update_layout(
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Number of Times Searched",
                yaxis_title="Search Query"
            )
            st.plotly_chart(fig_popular, use_container_width=True)

if __name__ == "__main__":
    main()


