import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random


st.set_page_config(page_title="COVID Memory Archive", layout="wide")
@st.cache_data
def load_data():
    events_file = 'eventscopy.csv' 
    posts_file = 'covid_instagramcopy.csv'
    
    try:
        events_df = pd.read_csv(events_file)
        events_df['start_date'] = pd.to_datetime(events_df['start_date'])
        events_df['end_date'] = pd.to_datetime(events_df['end_date'])
        posts_df = pd.read_csv(posts_file)
        posts_df['Date'] = pd.to_datetime(posts_df['Date'])
        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        posts_df['sentiment_score'] = posts_df['Sentiment'].str.strip().str.lower().map(sentiment_map)
        lang_to_region = {
             "English": "Global/USA/UK", "Spanish": "Spanish speaking", 
             "Turkish": "Turkey", "Indonesian": "Indonesia", 
             "French": "French speaking", "Hindi": "India",
             "Portuguese": "Portuguese speaking"
        }
        posts_df['Region_Simple'] = posts_df['Full Language'].map(lambda x: lang_to_region.get(x, x))

        return events_df, posts_df
    except Exception as e:
        st.error(f"Помилка даних: {e}")
        st.stop()

df_events, df_posts = load_data()
min_date = df_posts['Date'].min().date()
max_date = df_posts['Date'].max().date()
st.title("🦠 COVID Memory Archive")
st.markdown("### Інтерактивна хроніка пандемії через призму соцмереж")

st.divider()
st.markdown("""
    <style>
    .big-date-label {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #00CC96 !important; 
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stDateInput"] > div {
        border: 2px solid #00CC96 !important; 
        border-radius: 12px !important;      
        background-color: transparent !important; 
        padding: 5px;
        box-shadow: 0px 4px 10px rgba(0, 204, 150, 0.2); /* Тінь */
        transition: all 0.3s ease;
        cursor: pointer !important;          
        position: relative;                  
    }

  
    div[data-testid="stDateInput"]:hover > div {
        box-shadow: 0px 6px 15px rgba(0, 204, 150, 0.4);
        transform: translateY(-2px); 
    }
    
    div[data-testid="stDateInput"] input {
        font-size: 18px !important;
        font-weight: bold !important;
        color: white !important; 
        cursor: pointer !important;
        padding-right: 30px !important;
    }

    div[data-testid="stDateInput"] > div::after {
        content: "▼";
        font-size: 12px;
        color: white; /* Колір трикутника */
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        pointer-events: none;
    }
    
    /* Прибираємо стандартну іконку календаря, якщо вона заважає (опціонально) */
    div[data-testid="stDateInput"] svg {
        display: none !important;
    }
    </style>
    
    <!-- Власний HTML заголовок замість стандартного label -->
    <div class="big-date-label">📅 Натисніть тут, щоб обрати дату 👇</div>
""", unsafe_allow_html=True)


selected_date = st.date_input(
    "Оберіть дату", 
    min_value=min_date,
    max_value=max_date,
    value=pd.to_datetime("2021-07-14").date(),
    label_visibility="collapsed" 
)

st.info(f"Ви переглядаєте архів за **{selected_date.strftime('%d %B %Y')}**. Гортайте вниз, щоб побачити пости та події цього дня.")
st.sidebar.header("⚙️ Глобальні фільтри")

st.sidebar.subheader("🌐 Мовний фільтр")
main_languages = ["English", "Spanish", "Tamil", "Hindi"]

lang_mode = st.sidebar.radio(
    "Які мови показувати на графіку?",
    options=["Основні (Eng/Esp/Tam/Hin)", "Всі мови (All)", "Обрати вручну"],
    index=0
)

if lang_mode == "Основні (Eng/Esp/Tam/Hin)":
    selected_langs = main_languages
elif lang_mode == "Обрати вручну":
    all_languages = sorted(df_posts['Full Language'].dropna().unique().tolist())
    selected_langs = st.sidebar.multiselect("Оберіть мови:", options=all_languages, default=["English"])
else:
    selected_langs = df_posts['Full Language'].unique().tolist()

if selected_langs:
    filtered_df_posts = df_posts[df_posts['Full Language'].isin(selected_langs)]
else:
    filtered_df_posts = df_posts

st.header("📈 Хронологія Світу та Емоцій")

if not filtered_df_posts.empty:
    daily_sentiment = filtered_df_posts.groupby('Date')['sentiment_score'].mean().reset_index()

    fig = px.line(daily_sentiment, x='Date', y='sentiment_score', 
                  title="Середній сентимент постів у часі",
                  labels={'sentiment_score': 'Сентимент', 'Date': 'Дата'},
                  height=500) 
    
    fig.update_traces(line_color='#00CC96', line_width=2)
    fig.update_yaxes(range=[-1.1, 1.1], gridcolor='rgba(255,255,255,0.1)')
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    
    fig.update_layout(margin=dict(t=50)) 
    for index, row in df_events.iterrows():
        if row['start_date'] <= df_posts['Date'].max() and row['end_date'] >= df_posts['Date'].min():
            fig.add_vrect(
                x0=row['start_date'], x1=row['end_date'],
                fillcolor="red", opacity=0.1, layer="below", line_width=0,
            )

    x_pos = pd.Timestamp(selected_date).timestamp() * 1000
    fig.add_vline(x=x_pos, line_width=2, line_dash="dash", line_color="white", opacity=0.8)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Немає даних для обраних мов.")


st.divider()
st.header(f"🧐 Детальний огляд: {selected_date.strftime('%d %B %Y')}")

daily_data_all_langs = df_posts[df_posts['Date'].dt.date == selected_date]

active_events = df_events[
    (df_events['start_date'].dt.date <= selected_date) & 
    (df_events['end_date'].dt.date >= selected_date)
]

tab1, tab2, tab3 = st.tabs(["🌍 Події та Статистика", "📊 Порівняння країн за день", "🗣️ Типові пости"])

with tab1:
    col1a, col1b = st.columns([2, 1])
    with col1a:
        st.subheader("Що відбувалось у світі?")
        if not active_events.empty:
            for _, event in active_events.iterrows():
                with st.expander(f"‼️ {event['event_name']}", expanded=True):
                    st.write(event['description'])
                    st.caption(f"Період події: {event['start_date'].date()} - {event['end_date'].date()}")
        else:
            st.info("На цю дату немає записаних глобальних подій у базі.")
    
    with col1b:
        st.subheader("Загальна статистика дня")
        st.metric("Всього постів (всі мови)", len(daily_data_all_langs))
        if not daily_data_all_langs.empty:
            avg_sent = daily_data_all_langs['sentiment_score'].mean()
            
            sent_label = "Нейтральний 😐"
            sent_color = "off"
            if avg_sent > 0.1: 
                sent_label = "Позитивний 😊"
                sent_color = "normal"
            elif avg_sent < -0.1: 
                sent_label = "Негативний 😠"
                sent_color = "inverse"
                
            st.metric("Середній настрій світу", f"{avg_sent:.2f}", sent_label, delta_color=sent_color)

with tab2:
    st.subheader("Як про це писали в різних мовних групах саме сьогодні?")
    
    if not daily_data_all_langs.empty:
        daily_lang_sent = daily_data_all_langs.groupby('Full Language')['sentiment_score'].agg(['mean', 'count']).reset_index()
        daily_lang_sent.rename(columns={'mean': 'Середній сентимент', 'count': 'Кількість постів'}, inplace=True)
        daily_lang_sent = daily_lang_sent.sort_values('Середній сентимент', ascending=False)
        
        fig_day_bar = px.bar(daily_lang_sent, 
                             x='Середній сентимент', 
                             y='Full Language',
                             color='Середній сентимент',
                             orientation='h',
                             hover_data=['Кількість постів'],
                             color_continuous_scale=px.colors.diverging.RdBu,
                             range_color=[-1, 1],
                             title=f"Сентимент по мовах на {selected_date}",
                             height=400)
        fig_day_bar.update_layout(yaxis_title=None, xaxis_title="Сентимент (-1 негатив ... +1 позитив)")
        fig_day_bar.add_vline(x=0, line_width=1, line_color="grey")
        st.plotly_chart(fig_day_bar, use_container_width=True)
    else:
        st.write("Немає даних для порівняння за цей день.")

with tab3:
    st.subheader("Приклади постів за цей день")
    st.caption("Показуємо 5 випадкових постів для розуміння загального контексту.")
    
    if not daily_data_all_langs.empty:
        sample_size = min(5, len(daily_data_all_langs))
        sample_posts = daily_data_all_langs.sample(n=sample_size, random_state=42) 
        
        for _, post in sample_posts.iterrows():
            sent_emoji = "😐"
            if post['sentiment_score'] > 0: sent_emoji = "😊"
            elif post['sentiment_score'] < 0: sent_emoji = "😠"
            
            with st.expander(f"[{post['Full Language']}] {sent_emoji} {post['Sentiment'].title()}"):
                st.markdown(f"**{post['Post Description']}**")
                st.divider()
                st.caption(f"Post ID: {post['PostID']}")
    else:
        st.write("Немає постів за цю дату.")


st.divider()
with st.expander("🌍 Переглянути загальну географію настроїв за ВЕСЬ період (Натисніть, щоб розгорнути)"):
    if 'Region_Simple' in df_posts.columns:
        avg_sentiment_by_region = df_posts.groupby('Region_Simple')['sentiment_score'].mean().reset_index()
        fig_bar_all = px.bar(avg_sentiment_by_region, x='Region_Simple', y='sentiment_score',
                         color='sentiment_score',
                         color_continuous_scale=px.colors.diverging.RdBu,
                         range_color=[-1, 1],
                         title="Середній сентимент по регіонах (за весь час)")
        fig_bar_all.add_hline(y=0, line_width=1, line_color="grey")
        st.plotly_chart(fig_bar_all, use_container_width=True)
    else:
        st.error("Помилка: Колонка 'Region_Simple' не знайдена.")