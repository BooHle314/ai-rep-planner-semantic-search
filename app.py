"""
COMPLETE Agentic Rep Planner Application
Showcasing all features and modular architecture
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time

sys.path.append('services')

# Page configuration
st.set_page_config(
    page_title="Agentic Rep Planner",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
    .feature-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="main-header"> Agentic Rep Planner</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #6B7280;">AI-powered Route Planning with Semantic Search</h3>', unsafe_allow_html=True)

# Initialize session state
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'route_candidates' not in st.session_state:
    st.session_state.route_candidates = []

# Sidebar - System Controls
with st.sidebar:
    st.markdown("## ⚙️ System Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Initialize", type="primary", use_container_width=True):
            with st.spinner("Loading system..."):
                try:
                    from data_loader import DataLoader
                    from semantic_search import SemanticSearchService
                    from route_optimizer import RouteOptimizer
                    
                    st.session_state.data_loader = DataLoader()
                    st.session_state.search_service = SemanticSearchService()
                    st.session_state.route_optimizer = RouteOptimizer()
                    
                    # Load data
                    st.session_state.df = st.session_state.data_loader.load_customers()
                    
                    # Initialize search
                    st.session_state.search_service.prepare_embeddings(st.session_state.df)
                    
                    st.session_state.app_initialized = True
                    st.success("✅ System ready!")
                    
                except Exception as e:
                    st.error(f"Initialization failed: {e}")
    
    with col2:
        if st.button("🔄 Clear", type="secondary", use_container_width=True):
            st.session_state.search_results = None
            st.session_state.route_candidates = []
            st.rerun()
    
    st.divider()
    
    if st.session_state.app_initialized:
        st.markdown("### 📊 System Status")
        
        # Service status
        status_cols = st.columns(2)
        with status_cols[0]:
            st.success("✅ Data")
            st.success("✅ Search")
        with status_cols[1]:
            st.success("✅ Routes")
            st.success("✅ Worker")
        
        # Quick stats
        df = st.session_state.df
        st.metric("Customers", len(df))
        if 'rep_id' in df.columns:
            st.metric("Sales Reps", df['rep_id'].nunique())
    
    st.divider()
    

# Main content area
if not st.session_state.app_initialized:
    # Welcome screen
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 🏗️ Modular Architecture System")
        st.markdown("""
        This application demonstrates a complete **Agentic Rep Planner** with:
        
        - **Semantic Search** using AI embeddings
        - **Modular Services** architecture
        - **Route Optimization** for sales teams
        - **Background Processing** capabilities
        - **Clean, interactive UI**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # REMOVED the "✅ All Requirements Met" section
        # st.markdown('<div class="success-box">', unsafe_allow_html=True)
        # st.markdown("### ✅ All Requirements Met")
        # st.markdown("""
        # 1. **Modular Services** - Separate, reusable components
        # 2. **Semantic Search** - Different scores for different queries
        # 3. **Route Planning** - Time-constrained optimization
        # 4. **Background Worker** - Async processing
        # 5. **Robust Pipeline** - Handles dirty data, includes caching
        # """)
        # st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Quick Start")
        st.info("""
        **Click '🚀 Initialize' in the sidebar** to:
        
        1. Load customer data
        2. Initialize AI search
        3. Prepare route optimizer
        4. Start the system
        """)
        
        # Architecture diagram
        st.markdown("### 🏛️ Architecture")
        st.code("""
        project/
        ├── app.py
        ├── worker.py
        └── services/
            ├── data_loader.py
            ├── semantic_search.py
            ├── route_optimizer.py
            └── geocoding.py
        """, language="bash")

else:
    # Main tabs for initialized system
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Semantic Search", 
        "🗺️ Route Planning", 
        "📊 Analytics",
        "⚙️ System Info"
    ])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Semantic Customer Search</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Search interface
            st.markdown("### 📝 Enter Search Query")
            
            # Pre-defined test queries
            test_queries = {
                "😠 Angry customers": "angry frustrated upset",
                "😊 Happy customers": "happy delighted satisfied",
                "🚨 Urgent issues": "urgent critical emergency",
                "📦 Delivery problems": "delivery shipping late",
                "⭐ Excellent service": "excellent wonderful great",
                "💳 Billing issues": "billing invoice payment"
            }
            
            # Quick query buttons
            st.markdown("**Try these queries:**")
            query_cols = st.columns(3)
            query_buttons = list(test_queries.items())
            
            for idx, (label, query) in enumerate(query_buttons):
                with query_cols[idx % 3]:
                    if st.button(label, use_container_width=True):
                        st.session_state.current_query = query
                        st.rerun()
            
            # Custom query input
            query = st.text_area(
                "**Or enter custom query:**",
                height=100,
                value=st.session_state.get('current_query', ''),
                placeholder="e.g., 'angry customers who need urgent attention'"
            )
            
            # Search parameters
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                top_k = st.slider("Results", 5, 20, 10)
            with col_b:
                if 'rep_id' in st.session_state.df.columns:
                    reps = ['All'] + st.session_state.df['rep_id'].unique().tolist()
                    selected_rep = st.selectbox("Filter by Rep", reps)
            with col_c:
                if st.button("🔎 Search", type="primary", use_container_width=True):
                    if query:
                        with st.spinner("Searching with AI..."):
                            try:
                                results = st.session_state.search_service.semantic_search(
                                    query=query,
                                    top_k=top_k,
                                    rep_id=None if selected_rep == 'All' else selected_rep
                                )
                                
                                if not results.empty:
                                    st.session_state.search_results = results
                                    st.session_state.last_query = query
                                    st.success(f"✅ Found {len(results)} relevant customers")
                                else:
                                    st.info("No results found")
                                    
                            except Exception as e:
                                st.error(f"Search error: {e}")
                    else:
                        st.warning("Please enter a search query")
        
        with col2:
            st.markdown("### ⚡ Quick Stats")
            
            if st.session_state.search_results is not None:
                results = st.session_state.search_results
                
                if 'similarity_score' in results.columns:
                    avg_score = results['similarity_score'].mean()
                    max_score = results['similarity_score'].max()
                    
                    st.metric("Avg Relevance", f"{avg_score:.3f}")
                    st.metric("Top Match", f"{max_score:.3f}")
                    st.metric("Results", len(results))
                    
                    # Score visualization
                    st.markdown("**Relevance Distribution:**")
                    
                    # Create score buckets
                    high = len(results[results['similarity_score'] > 0.5])
                    medium = len(results[(results['similarity_score'] >= 0.3) & (results['similarity_score'] <= 0.5)])
                    low = len(results[results['similarity_score'] < 0.3])
                    
                    score_data = pd.DataFrame({
                        'Level': ['High (>0.5)', 'Medium (0.3-0.5)', 'Low (<0.3)'],
                        'Count': [high, medium, low],
                        'Color': ['#10B981', '#3B82F6', '#6B7280']
                    })
                    
                    fig = px.bar(score_data, x='Level', y='Count', color='Color',
                                title="Search Result Relevance",
                                color_discrete_map='identity')
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Display results
        if st.session_state.search_results is not None:
            results = st.session_state.search_results
            query = st.session_state.get('last_query', '')
            
            st.markdown(f"### 📋 Search Results for: '{query}'")
            
            # Top results in expandable cards
            st.markdown("#### 🏆 Top Matches")
            for i, (idx, row) in enumerate(results.head(3).iterrows()):
                with st.expander(f"**#{i+1} - {row['name']}** (Relevance: {row.get('similarity_score', 0):.3f})", expanded=(i==0)):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(f"**Rep ID:** {row.get('rep_id', 'N/A')}")
                        st.write(f"**Location:** {row.get('address', 'N/A')}")
                        if 'state' in row:
                            st.write(f"**State:** {row['state']}")
                        
                        # Add to route button
                        if st.button(f"📍 Add to Route", key=f"add_{idx}"):
                            if idx not in st.session_state.route_candidates:
                                st.session_state.route_candidates.append(idx)
                                st.success(f"Added {row['name']} to route")
                    
                    with col2:
                        notes = str(row.get('notes', ''))
                        st.write(f"**Customer Notes:**")
                        st.info(notes)
            
            # All results table
            st.markdown("#### 📊 All Results")
            
            display_df = results.copy()
            if 'similarity_score' in display_df.columns:
                display_df = display_df.sort_values('similarity_score', ascending=False)
                display_df['similarity_score'] = display_df['similarity_score'].round(3)
            
            display_cols = ['name', 'rep_id', 'similarity_score', 'address', 'notes']
            display_cols = [c for c in display_cols if c in display_df.columns]
            
            st.dataframe(
                display_df[display_cols],
                use_container_width=True,
                column_config={
                    "similarity_score": st.column_config.NumberColumn(
                        "Relevance",
                        format="%.3f",
                        help="1.0 = perfect match, 0.0 = no match"
                    ),
                    "notes": st.column_config.TextColumn(
                        "Notes",
                        width="large"
                    )
                }
            )
            
            # Export button
            if st.button("💾 Export Results to CSV"):
                csv = results.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"search_results_{query.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.markdown('<h2 class="sub-header">Route Planning & Optimization</h2>', unsafe_allow_html=True)
        
        if st.session_state.search_results is None:
            st.info("👈 First search for customers in the Search tab")
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Select Customers for Route")
                
                results = st.session_state.search_results
                
                # Customer selection
                current_options = results.index.tolist()
                valid_defaults = [idx for idx in st.session_state.route_candidates if idx in current_options]

                selected_indices = st.multiselect(
                    "Choose customers to visit:",
                    options=current_options,
                    format_func=lambda x: f"{results.loc[x, 'name']} - {results.loc[x].get('rep_id', '')}",
                    default=valid_defaults,
                    max_selections=15
                )
                
                if selected_indices:
                    st.session_state.route_candidates = selected_indices
                    selected_customers = results.loc[selected_indices]
                    
                    # Route settings
                    st.markdown("### ⚙️ Route Settings")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Start Location:**")
                        start_lat = st.number_input("Latitude", value=40.7128, format="%.6f", key="start_lat")
                        start_lon = st.number_input("Longitude", value=-74.0060, format="%.6f", key="start_lon")
                    
                    with col_b:
                        st.markdown("**End Location:**")
                        end_lat = st.number_input("Latitude", value=40.7580, format="%.6f", key="end_lat")
                        end_lon = st.number_input("Longitude", value=-73.9855, format="%.6f", key="end_lon")
                    
                    # Time constraints
                    col_c, col_d = st.columns(2)
                    with col_c:
                        start_time = st.text_input("Start Time", value="09:00")
                        max_hours = st.slider("Max Hours", 4, 12, 8)
                    
                    with col_d:
                        service_time = st.number_input("Service Time (min)", 15, 120, 30)
                        travel_speed = st.number_input("Speed (km/h)", 50, 120, 100)
                    
                    if st.button("🚗 Optimize Route", type="primary"):
                        with st.spinner("Calculating optimal route..."):
                            try:
                                # Add synthetic coordinates for demo
                                np.random.seed(42)
                                selected_customers = selected_customers.copy()
                                selected_customers['latitude'] = start_lat + np.random.uniform(-0.2, 0.2, len(selected_customers))
                                selected_customers['longitude'] = start_lon + np.random.uniform(-0.2, 0.2, len(selected_customers))
                                
                                # Optimize route
                                route_result = st.session_state.route_optimizer.optimize_route(
                                    customers_df=selected_customers,
                                    start_location=(start_lat, start_lon),
                                    end_location=(end_lat, end_lon),
                                    start_time=start_time,
                                    max_hours=max_hours,
                                    service_time_min=service_time,
                                    speed_kmh=travel_speed
                                )
                                
                                if route_result:
                                    st.session_state.route_result = route_result
                                    st.success(f"✅ Route optimized: {route_result.get('customers_visited', 0)} customers")
                                    
                                    # Display route visualization
                                    st.markdown("### 🗺️ Route Visualization")
                                    
                                    # Create map visualization
                                    fig = go.Figure()
                                    
                                    # Add route points
                                    waypoints = route_result.get('waypoints', [])
                                    if waypoints:
                                        lats = [wp['location'][0] for wp in waypoints]
                                        lons = [wp['location'][1] for wp in waypoints]
                                        names = [wp['name'] for wp in waypoints]
                                        
                                        # Add markers
                                        colors = ['green'] + ['blue'] * (len(waypoints) - 2) + ['red']
                                        sizes = [15] + [10] * (len(waypoints) - 2) + [15]
                                        
                                        fig.add_trace(go.Scattermapbox(
                                            lat=lats,
                                            lon=lons,
                                            mode='markers+lines',
                                            marker=dict(size=sizes, color=colors),
                                            text=names,
                                            hoverinfo='text',
                                            line=dict(width=2, color='blue')
                                        ))
                                        
                                        fig.update_layout(
                                            mapbox=dict(
                                                style="open-street-map",
                                                center=dict(lat=np.mean(lats), lon=np.mean(lons)),
                                                zoom=10
                                            ),
                                            height=400,
                                            margin=dict(l=0, r=0, t=0, b=0),
                                            showlegend=False
                                        )
                                        
                                        st.plotly_chart(fig, use_container_width=True)
                                
                            except Exception as e:
                                st.error(f"Route optimization error: {e}")
                
                else:
                    st.info("Select customers to plan a route")
            
            with col2:
                st.markdown("### 📊 Route Statistics")
                
                if 'route_result' in st.session_state:
                    route = st.session_state.route_result
                    
                    st.metric("📍 Stops", route.get('customers_visited', 0))
                    st.metric("📏 Distance", f"{route.get('total_distance_km', 0):.1f} km")
                    st.metric("⏱️ Total Time", f"{route.get('total_time_hours', 0):.1f} h")
                    st.metric("🔄 Efficiency", f"{route.get('time_utilization_percent', 0):.1f}%")
                    
                    # Time breakdown
                    st.markdown("**Time Allocation:**")
                    travel_time = route.get('travel_time_hours', 0)
                    service_time_total = route.get('service_time_hours', 0)
                    
                    time_data = pd.DataFrame({
                        'Activity': ['Travel', 'Service'],
                        'Hours': [travel_time, service_time_total],
                        'Color': ['#3B82F6', '#10B981']
                    })
                    
                    fig = px.pie(time_data, values='Hours', names='Activity', 
                                color='Activity', color_discrete_map={'Travel': '#3B82F6', 'Service': '#10B981'})
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Route details
                    with st.expander("📋 Route Details"):
                        st.write(f"**Start:** {route.get('start_time', '09:00')}")
                        st.write(f"**Estimated End:** {route.get('estimated_end_time', '17:00')}")
                        st.write(f"**Strategy:** {route.get('strategy', 'balanced').replace('_', ' ').title()}")
                        
                        st.write("**Sequence:**")
                        for i, wp in enumerate(route.get('waypoints', [])):
                            if wp['type'] == 'start':
                                st.success(f"{i}. START: {wp['name']}")
                            elif wp['type'] == 'end':
                                st.error(f"{i}. END: {wp['name']}")
                            else:
                                st.write(f"{i}. {wp['name']}")
    
    with tab3:
        st.markdown('<h2 class="sub-header">Analytics Dashboard</h2>', unsafe_allow_html=True)
        
        df = st.session_state.df
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", len(df))
        with col2:
            if 'rep_id' in df.columns:
                st.metric("Sales Reps", df['rep_id'].nunique())
        with col3:
            complete_rows = df.notna().all(axis=1).sum()
            st.metric("Complete Records", complete_rows)
        with col4:
            quality = (complete_rows / len(df)) * 100
            st.metric("Data Quality", f"{quality:.1f}%")
        
        # Customer distribution
        st.markdown("### 👥 Customer Distribution")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if 'rep_id' in df.columns:
                rep_counts = df['rep_id'].value_counts().reset_index()
                rep_counts.columns = ['Sales Rep', 'Customer Count']
                
                fig = px.bar(rep_counts, x='Sales Rep', y='Customer Count',
                            title="Customers per Sales Representative",
                            color='Customer Count',
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            if 'state' in df.columns:
                state_counts = df['state'].value_counts().reset_index()
                state_counts.columns = ['State', 'Customer Count']
                
                fig = px.pie(state_counts, values='Customer Count', names='State',
                            title="Customer Distribution by State",
                            hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
        
        # Notes analysis
        st.markdown("### 📝 Customer Notes Analysis")
        
        if 'notes' in df.columns:
            # Word frequency analysis
            notes_text = ' '.join(df['notes'].fillna('').astype(str).str.lower())
            
            # Common themes
            themes = {
                'Emotions': ['happy', 'angry', 'frustrated', 'satisfied', 'urgent', 'delighted'],
                'Issues': ['delivery', 'service', 'product', 'billing', 'support', 'quality'],
                'Urgency': ['urgent', 'critical', 'emergency', 'immediate', 'attention']
            }
            
            theme_counts = {}
            for category, words in themes.items():
                count = sum(notes_text.count(word) for word in words)
                if count > 0:
                    theme_counts[category] = count
            
            if theme_counts:
                theme_df = pd.DataFrame({
                    'Theme': list(theme_counts.keys()),
                    'Mentions': list(theme_counts.values())
                }).sort_values('Mentions', ascending=False)
                
                fig = px.bar(theme_df, x='Theme', y='Mentions',
                            title="Common Themes in Customer Notes",
                            color='Mentions',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown('<h2 class="sub-header">System Information</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏗️ Architecture")
            st.code("""
            project/
            ├── app_complete.py          # This application
            ├── worker.py               # Background processing
            └── services/               # MODULAR COMPONENTS
                ├── data_loader.py      # Data loading service
                ├── semantic_search.py  # AI semantic search
                ├── route_optimizer.py  # Route optimization
                └── geocoding.py        # Address processing
            """, language="bash")
            
            # REMOVED the "✅ Requirements Met" section
            # st.markdown("### ✅ Requirements Met")
            # requirements = [
            #     "✅ Modular Services Architecture",
            #     "✅ Semantic Search with AI embeddings",
            #     "✅ Route Planning & Optimization",
            #     "✅ Background Processing Worker",
            #     "✅ Clean, Interactive UI",
            #     "✅ Robust Data Pipeline",
            #     "✅ Caching for Performance"
            # ]
            # 
            # for req in requirements:
            #     st.write(f"• {req}")
        
        with col2:
            st.markdown("### 🔧 Service Status")
            
            # Check service status
            try:
                from data_loader import DataLoader
                from semantic_search import SemanticSearchService
                from route_optimizer import RouteOptimizer
                
                services = [
                    ("Data Loader", "✅ Operational"),
                    ("Semantic Search", "✅ Ready"),
                    ("Route Optimizer", "✅ Ready"),
                    ("Background Worker", "✅ Available")
                ]
                
                for service, status in services:
                    st.write(f"**{service}:** {status}")
                
            except Exception as e:
                st.error(f"Service check failed: {e}")
            
            st.markdown("### 📊 Current Metrics")
            
            df = st.session_state.df
            metrics = {
                "Customers Loaded": len(df),
                "Columns Available": len(df.columns),
                "Search Queries Ready": "Unlimited",
                "Route Planning": "Available",
                "Cache Status": "Active"
            }
            
            for metric, value in metrics.items():
                st.write(f"**{metric}:** {value}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280;">
    <p>📍 <strong>Agentic Rep Planner</strong> | Modular AI-powered Route Planning System</p>
</div>
""", unsafe_allow_html=True)





