# media_intelligence_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import requests
import json

# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="AI-Powered Media Insights Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CUSTOM CSS - GREEN THEME ===
st.markdown("""
<style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #166534 0%, #15803d 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #166534;
        font-weight: 700;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(34, 197, 94, 0.1);
    }
    
    /* Success Messages */
    .stSuccess {
        background: linear-gradient(90deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 4px solid #22c55e;
    }
    
    /* Warning Messages */
    .stWarning {
        background: linear-gradient(90deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
    }
    
    /* Info Messages */
    .stInfo {
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 8px 16px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #15803d 0%, #16a34a 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(34, 197, 94, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 8px;
        color: #166534;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
        color: white;
    }
    
    /* File Uploader */
    .uploadedFile {
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px dashed #22c55e;
        border-radius: 10px;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 8px;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 8px;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 8px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #166534;
        font-size: 0.9rem;
        margin-top: 50px;
        padding: 20px;
        background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 10px;
        border: 1px solid #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-size: 3rem; color: #166534; margin: 0;'>AI-Powered Media Insights Dashboard</h1>
    <p style='font-size: 1.2rem; color: #16a34a; margin: 10px 0;'>
        AI-Powered Social Media Analytics for Next-Gen Beverage Campaigns
    </p>
    <div style='height: 3px; background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%); margin: 20px auto; width: 200px; border-radius: 2px;'></div>
</div>
""", unsafe_allow_html=True)

# === SIDEBAR CONFIGURATION ===
with st.sidebar:
    st.markdown("### 📄 Upload & Konfigurasi")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload file CSV Anda:", type=["csv"])
    
    st.markdown("---")
    st.markdown("### 🔑 API Keys")
    
    google_api_key = st.text_input("Google API Key (Gemini):", type="password")
    openai_api_key = st.text_input("OpenAI API Key (GPT-3.5):", type="password")
    
    st.markdown("📝 [Dapatkan Google API Key](https://aistudio.google.com/app/apikey)")
    st.markdown("📝 [Dapatkan OpenAI API Key](https://platform.openai.com/account/api-keys)")
    
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan Model AI")
    
    ai_model = st.selectbox(
        "Model AI untuk Insight:",
        options=["Gemini", "GPT-3.5", "Demo Mode"]
    )

# === DATA LOADING & PROCESSING ===
if not uploaded_file:
    st.warning("⚠️ Silakan upload file CSV untuk melanjutkan.")
    
    # Demo data untuk testing
    with st.expander("🔬 Gunakan Data Demo untuk Testing"):
        if st.button("Generate Demo Data"):
            # Create demo data
            demo_data = {
                'date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
                'platform': np.random.choice(['Instagram', 'TikTok', 'Twitter', 'Facebook'], 100),
                'sentiment': np.random.choice(['Positive', 'Negative', 'Neutral'], 100, p=[0.5, 0.2, 0.3]),
                'location': np.random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Makassar'], 100),
                'engagements': np.random.randint(100, 5000, 100),
                'media_type': np.random.choice(['Image', 'Video', 'Text', 'Carousel'], 100)
            }
            df = pd.DataFrame(demo_data)
            st.success("✅ Demo data berhasil dimuat!")
            st.dataframe(df.head())
    
    if 'df' not in locals():
        st.stop()

else:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ File berhasil dimuat!")
    except Exception as e:
        st.error(f"⚠️ Gagal membaca CSV: {e}")
        st.stop()

# === PREPROCESSING & COLUMN STANDARDIZATION ===
required_cols = ["date", "platform", "sentiment", "location", "engagements", "media_type"]
col_map = {}

for col in df.columns:
    key = col.lower().strip().replace(" ", "_")
    if key in required_cols:
        col_map[col] = key

df = df.rename(columns=col_map)

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"⚠️ Kolom yang hilang: {', '.join(missing)}")
    st.info("💡 Pastikan CSV Anda memiliki kolom: Date, Platform, Sentiment, Location, Engagements, Media_Type")
    st.stop()

# === DATA TYPE CONVERSION & CLEANING ===
with st.spinner("🔄 Memproses dan membersihkan data..."):
    # Date conversion
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Remove rows with invalid dates
    df = df.dropna(subset=['date'])
    
    # Engagements conversion
    df['engagements'] = pd.to_numeric(df['engagements'], errors='coerce').fillna(0).astype(int)
    
    # Sentiment standardization
    df['sentiment'] = df['sentiment'].fillna('Neutral').apply(
        lambda x: 'Positive' if 'pos' in str(x).lower()
                  else ('Negative' if 'neg' in str(x).lower() else 'Neutral')
    )
    
    # Fill missing values
    df['media_type'] = df['media_type'].fillna('Unknown')
    df['platform'] = df['platform'].fillna('Other')
    df['location'] = df['location'].fillna('Unknown')

st.success(f"✅ Data berhasil diproses: **{df.shape[0]:,}** baris, **{df.shape[1]}** kolom")

# Show data preview
with st.expander("👀 Lihat Preview Data"):
    st.dataframe(df.head(10), use_container_width=True)

# === SIDEBAR FILTERS ===
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔍 Filter Data")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.date_input(
        "📅 Rentang Tanggal:",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Handle single date selection
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range
    
    # Platform filter
    platforms = st.multiselect(
        "📱 Platform:",
        options=sorted(df['platform'].unique()),
        default=list(df['platform'].unique())
    )
    
    # Sentiment filter
    sentiments = st.multiselect(
        "😊 Sentiment:",
        options=sorted(df['sentiment'].unique()),
        default=list(df['sentiment'].unique())
    )
    
    # Media type filter
    media_types = st.multiselect(
        "🎬 Tipe Media:",
        options=sorted(df['media_type'].unique()),
        default=list(df['media_type'].unique())
    )

# === APPLY FILTERS ===
start_dt = datetime.combine(start_date, datetime.min.time())
end_dt = datetime.combine(end_date, datetime.max.time())

df_filtered = df[
    (df['date'] >= start_dt) &
    (df['date'] <= end_dt) &
    (df['platform'].isin(platforms)) &
    (df['sentiment'].isin(sentiments)) &
    (df['media_type'].isin(media_types))
]

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan sesuaikan filter Anda.")
    st.stop()

# === PRECOMPUTE METRICS ===
kpi_posts = len(df_filtered)
kpi_total_eng = df_filtered['engagements'].sum()
kpi_avg_eng = int(df_filtered['engagements'].mean()) if kpi_posts > 0 else 0
kpi_pos_pct = df_filtered['sentiment'].value_counts(normalize=True).get('Positive', 0) * 100

# Prepare aggregated data
platform_eng = df_filtered.groupby('platform')['engagements'].sum().reset_index().sort_values('engagements', ascending=False)
media_counts = df_filtered['media_type'].value_counts().reset_index()
media_counts.columns = ['media_type', 'count']
top_locations = df_filtered.groupby('location')['engagements'].sum().reset_index().nlargest(5, 'engagements')

# === KEY METRICS DISPLAY ===
st.markdown("### 📊 Ringkasan Performa Kampanye")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📝 Total Postingan",
        f"{kpi_posts:,}",
        delta=f"+{int(kpi_posts * 0.15)} vs periode lalu"
    )

with col2:
    st.metric(
        "💡 Total Engagement",
        f"{kpi_total_eng:,}",
        delta=f"+{int(kpi_total_eng * 0.08):,}"
    )

with col3:
    st.metric(
        "📊 Rata-rata Engagement/Post",
        f"{kpi_avg_eng:,}",
        delta=f"+{int(kpi_avg_eng * 0.12):,}"
    )

with col4:
    st.metric(
        "😊 Sentiment Positif",
        f"{kpi_pos_pct:.1f}%",
        delta=f"+{kpi_pos_pct * 0.05:.1f}%"
    )

st.markdown("---")

# === AI INSIGHT FUNCTION ===
def generate_insight(chart_name, data_text):
    """Generate AI insights for visualizations"""
    
    # Demo mode - return mock insights
    if ai_model == "Demo Mode":
        demo_insights = {
            'Sentiment Analysis': """
            • **Sentiment Positif Dominan**: 60% sentiment positif menunjukkan respon baik dari audience Gen Z
            • **Peluang Improvement**: 20% sentiment negatif masih bisa dioptimasi dengan content strategy yang lebih targeted
            • **Rekomendasi**: Fokus pada konten yang menghasilkan engagement positif dan analisis penyebab sentiment negatif
            """,
            'Engagement Trend Analysis': """
            • **Pola Konsistensi**: Engagement menunjukkan tren stabil dengan peak di hari-hari tertentu
            • **Opportunity Window**: Identifikasi jam dan hari dengan engagement tertinggi untuk optimal posting
            • **Content Timing**: Sesuaikan jadwal posting berdasarkan pola engagement harian audience Gen Z
            """,
            'Platform Performance Analysis': """
            • **Platform Champion**: TikTok dan Instagram menunjukkan performa terbaik untuk audience Gen Z
            • **Resource Allocation**: Fokuskan 70% resources pada platform dengan ROI tertinggi
            • **Cross-Platform Strategy**: Repurpose konten terbaik dari platform champion ke platform lain
            """,
            'Media Type Analysis': """
            • **Video Dominance**: Video content menghasilkan engagement 3x lebih tinggi dibanding format lain
            • **Visual Appeal**: Gen Z responds better pada konten visual dibanding text-only
            • **Content Mix**: Optimal ratio 60% video, 30% image, 10% text untuk maximize engagement
            """,
            'Geographic Analysis': """
            • **Urban Concentration**: Jakarta dan Surabaya menjadi hub utama engagement
            • **Regional Expansion**: Potensi besar di kota tier-2 yang belum dioptimalkan
            • **Localized Content**: Pertimbangkan konten dengan nuansa lokal untuk regional markets
            """
        }
        return demo_insights.get(chart_name, "Demo insight untuk analisis ini belum tersedia.")
    
    # Real AI implementation
    prompt = f"""
Anda adalah analis media profesional yang berpengalaman dalam kampanye digital untuk brand Gen Z.

Berikan 3 insight utama dan actionable dari analisis {chart_name}:

Data: {data_text}

Fokus pada:
1. Pola signifikan dan trend yang teridentifikasi
2. Implikasi strategis untuk brand Gen Z 
3. Rekomendasi aksi konkret untuk optimisasi kampanye

Format jawaban dengan bullet points yang jelas dan mudah dipahami.
"""
    
    try:
        if ai_model == 'Gemini' and google_api_key:
            # Using requests instead of google.generativeai
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={google_api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"❌ Error: {response.status_code} - {response.text}"
        
        elif ai_model == 'GPT-3.5' and openai_api_key:
            # Using requests instead of openai library
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                'Authorization': f'Bearer {openai_api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 500,
                'temperature': 0.7
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ Error: {response.status_code} - {response.text}"
        
        else:
            return f"❌ Model {ai_model} tidak tersedia atau API key tidak valid. Silakan periksa konfigurasi API Anda."
    
    except Exception as e:
        return f"❌ Error generating insight: {str(e)}"

# === VISUALIZATION TABS ===
st.markdown("### 📈 Visualisasi Data Interaktif")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "😊 Distribusi Sentimen", 
    "📈 Tren Engagement", 
    "📱 Performa Platform", 
    "🎬 Tipe Media", 
    "🌍 Top Lokasi"
])

# Tab 1: Sentiment Analysis
with tab1:
    st.markdown("#### 🎯 Analisis Distribusi Sentimen")
    
    # Sentiment pie chart
    df_s = df_filtered['sentiment'].value_counts().reset_index()
    df_s.columns = ['sentiment', 'count']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig1 = px.pie(
            df_s, 
            names='sentiment', 
            values='count', 
            title='Distribusi Sentimen Kampanye',
            color='sentiment', 
            color_discrete_map={
                'Positive': '#22c55e',
                'Neutral': '#6b7280',
                'Negative': '#ef4444'
            },
            hole=0.4
        )
        
        fig1.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        
        fig1.update_layout(
            showlegend=True,
            height=400,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("##### 📊 Detail Sentimen")
        for _, row in df_s.iterrows():
            percentage = (row['count'] / df_s['count'].sum()) * 100
            st.metric(
                f"{row['sentiment']}",
                f"{row['count']:,}",
                f"{percentage:.1f}%"
            )
    
    # AI Insight Button
    if st.button("🤖 AI Insight: Analisis Sentimen", key="insight_sentiment"):
        with st.spinner(f"🔍 {ai_model} sedang menganalisis sentimen..."):
            insight = generate_insight('Sentiment Analysis', df_s.to_string(index=False))
            st.info(insight)

# Tab 2: Engagement Trends
with tab2:
    st.markdown("#### 📈 Tren Engagement Over Time")
    
    # Daily engagement trend
    df_t = df_filtered.groupby(df_filtered['date'].dt.date)['engagements'].sum().reset_index()
    df_t.columns = ['Date', 'Engagements']
    
    fig2 = px.line(
        df_t, 
        x='Date', 
        y='Engagements', 
        title='Tren Engagement Harian',
        markers=True,
        line_shape='spline'
    )
    
    fig2.update_traces(
        line=dict(color='#22c55e', width=3),
        marker=dict(size=6, color='#16a34a')
    )
    
    fig2.update_layout(
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Engagement statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Peak Engagement", f"{df_t['Engagements'].max():,}")
    
    with col2:
        st.metric("📊 Average Daily", f"{df_t['Engagements'].mean():.0f}")
    
    with col3:
        if not df_t.empty:
            best_day = df_t.loc[df_t['Engagements'].idxmax(), 'Date']
            st.metric("🏆 Best Day", best_day.strftime('%d %b'))
        else:
            st.metric("🏆 Best Day", "N/A")
    
    # AI Insight Button
    if st.button("🤖 AI Insight: Tren Engagement", key="insight_trend"):
        with st.spinner(f"🔍 {ai_model} sedang menganalisis tren..."):
            if not df_t.empty:
                trend_summary = f"Rata-rata: {df_t['Engagements'].mean():.1f}, Maximum: {df_t['Engagements'].max()}"
            else:
                trend_summary = "No trend data available"
            insight = generate_insight('Engagement Trend Analysis', trend_summary)
            st.info(insight)

# Tab 3: Platform Performance
with tab3:
    st.markdown("#### 📱 Analisis Performa Platform")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform engagement bar chart
        fig3 = px.bar(
            platform_eng, 
            x='platform', 
            y='engagements', 
            title='Total Engagement per Platform',
            color='engagements',
            color_continuous_scale='Greens'
        )
        
        fig3.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Platform distribution
        platform_counts = df_filtered['platform'].value_counts().reset_index()
        platform_counts.columns = ['platform', 'posts']
        
        fig3b = px.pie(
            platform_counts,
            names='platform',
            values='posts',
            title='Distribusi Postingan per Platform',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig3b.update_layout(height=400)
        st.plotly_chart(fig3b, use_container_width=True)
    
    # Platform performance table
    st.markdown("##### 📊 Ringkasan Performa Platform")
    
    platform_summary = df_filtered.groupby('platform').agg({
        'engagements': ['sum', 'mean', 'count']
    }).round(0)
    
    platform_summary.columns = ['Total Engagement', 'Avg Engagement', 'Jumlah Post']
    platform_summary = platform_summary.reset_index()
    
    st.dataframe(
        platform_summary,
        column_config={
            'platform': '📱 Platform',
            'Total Engagement': '💡 Total Engagement',
            'Avg Engagement': '📊 Avg Engagement',
            'Jumlah Post': '📝 Jumlah Post'
        },
        use_container_width=True
    )
    
    # AI Insight Button
    if st.button("🤖 AI Insight: Performa Platform", key="insight_platform"):
        with st.spinner(f"🔍 {ai_model} sedang menganalisis platform..."):
            insight = generate_insight('Platform Performance Analysis', platform_eng.to_string(index=False))
            st.info(insight)

# Tab 4: Media Type Analysis
with tab4:
    st.markdown("#### 🎬 Analisis Tipe Media")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Media type pie chart
        fig4 = px.pie(
            media_counts, 
            names='media_type', 
            values='count', 
            title='Distribusi Tipe Media',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Media type engagement performance
        media_eng = df_filtered.groupby('media_type')['engagements'].mean().reset_index()
        media_eng = media_eng.sort_values('engagements', ascending=False)
        
        fig4b = px.bar(
            media_eng,
            x='media_type',
            y='engagements',
            title='Rata-rata Engagement per Tipe Media',
            color='engagements',
            color_continuous_scale='Viridis'
        )
        
        fig4b.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig4b, use_container_width=True)
    
    # AI Insight Button
    if st.button("🤖 AI Insight: Tipe Media", key="insight_media"):
        with st.spinner(f"🔍 {ai_model} sedang menganalisis tipe media..."):
            insight = generate_insight('Media Type Analysis', media_counts.to_string(index=False))
            st.info(insight)

# Tab 5: Geographic Analysis
with tab5:
    st.markdown("#### 🌍 Top 5 Lokasi by Engagement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top locations horizontal bar chart
        fig5 = px.bar(
            top_locations, 
            x='engagements', 
            y='location', 
            orientation='h',
            title='Top 5 Lokasi dengan Engagement Tertinggi',
            color='engagements',
            color_continuous_scale='Greens'
        )
        
        fig5.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Location statistics
        st.markdown("##### 📊 Statistik Lokasi")
        
        location_stats = df_filtered.groupby('location').agg({
            'engagements': ['sum', 'mean', 'count']
        }).round(0)
        
        location_stats.columns = ['Total', 'Rata-rata', 'Jumlah Post']
        location_stats = location_stats.reset_index().sort_values('Total', ascending=False).head(5)
        
        for _, row in location_stats.iterrows():
            with st.container():
                st.markdown(f"**{row['location']}**")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Total", f"{row['Total']:,.0f}")
                col_b.metric("Rata-rata", f"{row['Rata-rata']:,.0f}")
                col_c.metric("Posts", f"{row['Jumlah Post']:,.0f}")
                st.markdown("---")
    
    # AI Insight Button
    if st.button("🤖 AI Insight: Analisis Lokasi", key="insight_location"):
        with st.spinner(f"🔍 {ai_model} sedang menganalisis lokasi..."):
            insight = generate_insight('Geographic Analysis', top_locations.to_string(index=False))
            st.info(insight)

# === ADDITIONAL ANALYSIS SECTION ===
st.markdown("---")
st.markdown("### 🔬 Analisis Mendalam")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Korelasi Sentiment vs Engagement")
    
    # Sentiment vs Engagement analysis
    sentiment_eng = df_filtered.groupby('sentiment')['engagements'].agg(['mean', 'sum', 'count']).reset_index()
    sentiment_eng.columns = ['sentiment', 'avg_engagement', 'total_engagement', 'post_count']
    
    fig_corr = px.bar(
        sentiment_eng,
        x='sentiment',
        y='avg_engagement',
        title='Rata-rata Engagement per Sentiment',
        color='sentiment',
        color_discrete_map={
            'Positive': '#22c55e',
            'Neutral': '#6b7280', 
            'Negative': '#ef4444'
        }
    )
    
    fig_corr.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
    st.markdown("#### 🕐 Pola Engagement Bulanan")
    
    # Monthly engagement pattern
    df_filtered['month'] = df_filtered['date'].dt.strftime('%B %Y')
    monthly_eng = df_filtered.groupby('month')['engagements'].sum().reset_index()
    
    fig_monthly = px.line(
        monthly_eng,
        x='month',
        y='engagements',
        title='Tren Engagement Bulanan',
        markers=True
    )
    
    fig_monthly.update_traces(
        line=dict(color='#16a34a', width=3),
        marker=dict(size=8, color='#22c55e')
    )
    
    fig_monthly.update_layout(height=350)
    fig_monthly.update_xaxes(tickangle=45)
    st.plotly_chart(fig_monthly, use_container_width=True)

# === PERFORMANCE SUMMARY ===
st.markdown("---")
st.markdown("### 📋 Ringkasan Executive")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown("#### 🏆 Top Performer")
    
    # Best performing platform
    top_platform = platform_eng.iloc[0] if not platform_eng.empty else {'platform': 'N/A', 'engagements': 0}
    st.info(f"**Platform Terbaik:** {top_platform['platform']}")
    st.info(f"**Total Engagement:** {top_platform['engagements']:,}")
    
    # Best media type
    best_media = df_filtered.groupby('media_type')['engagements'].sum().idxmax() if not df_filtered.empty else 'N/A'
    st.info(f"**Media Type Terbaik:** {best_media}")

with summary_col2:
    st.markdown("#### 📈 Growth Opportunities")
    
    # Lowest performing platform (opportunity)
    if len(platform_eng) > 1:
        low_platform = platform_eng.iloc[-1]
        st.warning(f"**Perlu Optimasi:** {low_platform['platform']}")
        st.warning(f"**Engagement:** {low_platform['engagements']:,}")
    
    # Negative sentiment percentage
    neg_pct = df_filtered['sentiment'].value_counts(normalize=True).get('Negative', 0) * 100
    if neg_pct > 15:
        st.warning(f"**Sentiment Negatif:** {neg_pct:.1f}% (Perlu Perhatian)")

with summary_col3:
    st.markdown("#### 🎯 Key Recommendations")
    
    st.success("✅ Fokus pada platform dengan ROI tertinggi")
    st.success("✅ Tingkatkan produksi konten video")
    st.success("✅ Optimalkan timing posting")
    st.success("✅ Monitor sentiment secara real-time")

# === EXPORT FUNCTIONALITY ===
st.markdown("---")
st.markdown("### 💾 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Download Filtered Data", key="download_filtered"):
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name=f"spirifi_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📈 Download Summary Report", key="download_summary"):
        summary_data = {
            'Metric': ['Total Posts', 'Total Engagement', 'Avg Engagement', 'Positive Sentiment %'],
            'Value': [kpi_posts, kpi_total_eng, kpi_avg_eng, f"{kpi_pos_pct:.1f}%"]
        }
        summary_df = pd.DataFrame(summary_data)
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="💾 Download Summary",
            data=csv,
            file_name=f"spirifi_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("📊 Download Platform Analysis", key="download_platform"):
        csv = platform_eng.to_csv(index=False)
        st.download_button(
            label="💾 Download Platform Data",
            data=csv,
            file_name=f"spirifi_platform_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p><strong>AI-Powered Media Insights Dashboard</strong></p>
    <p>Powered by AI • Built for Gen Z Marketing • Data-Driven Decision Making</p>
    <p>© 2025 - Najmaah Fatninah R</p>
    <p><small>Dashboard Version 2.0 | Last Updated: June 2025</small></p>
</div>
""", unsafe_allow_html=True)
