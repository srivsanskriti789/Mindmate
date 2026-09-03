import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
import time


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MindMate | Student Wellness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');


/* -------------------------
   GLOBAL
------------------------- */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f6faf7;
}


/* -------------------------
   SIDEBAR
------------------------- */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #17352a 0%,
            #214c39 100%
        );

}

[data-testid="stSidebar"] * {
    color: white !important;
}


.sidebar-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 5px;
}

.sidebar-subtitle {
    color: #b9d5c5 !important;
    font-size: 14px;
}


/* -------------------------
   MAIN TITLE
------------------------- */

.main-title {

    font-family: 'Playfair Display', serif;

    font-size: 52px;

    line-height: 1.05;

    color: #17352a;

    margin-bottom: 5px;

}

.main-title span {
    color: #4f9d69;
}


.subtitle {

    font-size: 17px;

    color: #66786e;

    margin-bottom: 30px;

}


/* -------------------------
   CARDS
------------------------- */

.card {

    background: white;

    border: 1px solid #e1eee5;

    border-radius: 22px;

    padding: 25px;

    box-shadow:
        0 10px 30px rgba(35,79,54,0.07);

    margin-bottom: 20px;

}


.card h3 {

    color: #214c39;

    margin-bottom: 8px;

}


.card p {

    color: #66786e;

}


/* -------------------------
   HERO CARD
------------------------- */

.hero {

    background:
        radial-gradient(
            circle at 90% 20%,
            #d7f0df,
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #eaf7ee,
            #f8fbf8
        );

    padding: 40px;

    border-radius: 28px;

    border: 1px solid #dcece1;

    margin-bottom: 30px;

}


.hero h2 {

    font-family: 'Playfair Display', serif;

    font-size: 38px;

    color: #17352a;

}


.hero p {

    color: #5d7166;

    font-size: 16px;

}


/* -------------------------
   METRICS
------------------------- */

.metric-card {

    background: white;

    border: 1px solid #e1eee5;

    border-radius: 20px;

    padding: 22px;

    text-align: center;

    box-shadow: 0 8px 25px rgba(35,79,54,0.06);

}


.metric-number {

    font-size: 32px;

    font-weight: 700;

    color: #4f9d69;

}


.metric-label {

    color: #73847b;

    font-size: 14px;

}


/* -------------------------
   MOOD BUTTON AREA
------------------------- */

.mood-box {

    background: white;

    padding: 30px;

    border-radius: 24px;

    border: 1px solid #e1eee5;

    box-shadow: 0 10px 30px rgba(35,79,54,0.06);

}


/* -------------------------
   TIP
------------------------- */

.tip {

    padding: 20px;

    border-radius: 18px;

    background: #eef8f1;

    border-left: 5px solid #4f9d69;

}


/* -------------------------
   BREATHING
------------------------- */

.breathing-container {

    text-align: center;

    background:
        radial-gradient(
            circle,
            #d9f2df,
            #f5faf6
        );

    padding: 45px;

    border-radius: 25px;

}


.breath-circle {

    width: 160px;

    height: 160px;

    border-radius: 50%;

    background: linear-gradient(
        145deg,
        #74bd8c,
        #4f9d69
    );

    margin: 25px auto;

    display: flex;

    align-items: center;

    justify-content: center;

    color: white;

    font-weight: 700;

    box-shadow:
        0 0 0 15px rgba(79,157,105,0.08),
        0 0 0 30px rgba(79,157,105,0.04);

}


/* -------------------------
   JOURNAL
------------------------- */

.journal-card {

    background: white;

    padding: 30px;

    border-radius: 25px;

    border: 1px solid #e1eee5;

    box-shadow: 0 10px 30px rgba(35,79,54,0.06);

}


/* -------------------------
   FOOTER
------------------------- */

.footer {

    text-align: center;

    padding: 35px;

    margin-top: 50px;

    color: #73847b;

    border-top: 1px solid #e1eee5;

}


/* -------------------------
   BUTTONS
------------------------- */

.stButton > button {

    border-radius: 12px;

    border: none;

    background: #4f9d69;

    color: white;

    font-weight: 600;

    padding: 10px 20px;

}


.stButton > button:hover {

    background: #397a4f;

    color: white;

}


/* -------------------------
   MOBILE
------------------------- */

@media(max-width: 800px) {

    .main-title {

        font-size: 40px;

    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MyNewPassword@123",
        database="student_wellness"
    )


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def save_mood(name, mood, score, note):

    db = get_connection()

    cursor = db.cursor()

    query = """
    INSERT INTO mood_entries
    (name, mood, mood_score, note)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, mood, score, note)
    )

    db.commit()

    cursor.close()
    db.close()


def save_journal(name, title, content):

    db = get_connection()

    cursor = db.cursor()

    query = """
    INSERT INTO journal_entries
    (name, title, content)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (name, title, content)
    )

    db.commit()

    cursor.close()
    db.close()


def get_moods():

    db = get_connection()

    query = """
    SELECT *
    FROM mood_entries
    ORDER BY created_at DESC
    """

    df = pd.read_sql(query, db)

    db.close()

    return df


def get_journals():

    db = get_connection()

    query = """
    SELECT *
    FROM journal_entries
    ORDER BY created_at DESC
    """

    df = pd.read_sql(query, db)

    db.close()

    return df


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🧠 MindMate</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Student Wellness Companion</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "😊 Mood Check-in",
            "📊 Mood Analytics",
            "📖 My Journal",
            "🧘 Breathing Space",
            "🌱 Wellness Tips"
        ]
    )

    st.divider()

    st.markdown(
        """
        <div style="text-align:center;">
        <p style="color:#b9d5c5;">
        Take care of your mind.<br>
        One day at a time 🌿
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LOAD DATA
# =========================================================

try:

    mood_df = get_moods()

except Exception as e:

    st.error(
        "Database connection failed. Check your MySQL password and make sure MySQL is running."
    )

    st.stop()


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">

        <h2>
        Welcome to <span style="color:#4f9d69;">MindMate</span> 🌿
        </h2>

        <p>
        A calm digital space designed to help students
        understand their emotions, reflect on their day
        and build healthier wellness habits.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # Metrics

    total_checkins = len(mood_df)

    if total_checkins > 0:

        average_score = round(
            mood_df["mood_score"].mean(),
            1
        )

        latest_mood = mood_df.iloc[0]["mood"]

    else:

        average_score = 0

        latest_mood = "No check-in"


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-number">
            {total_checkins}
            </div>

            <div class="metric-label">
            Total Check-ins
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-number">
            {average_score}/5
            </div>

            <div class="metric-label">
            Average Mood
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-number">
            {latest_mood}
            </div>

            <div class="metric-label">
            Latest Mood
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # Two columns

    left, right = st.columns([1.4, 1])


    with left:

        st.markdown(
            """
            <div class="card">

            <h3>✨ Your Wellness Journey</h3>

            <p>
            Checking in with yourself regularly can help
            you notice patterns in your emotions and
            understand what affects your day.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        if len(mood_df) > 0:

            chart_data = mood_df[
                ["created_at", "mood_score"]
            ].copy()

            chart_data["created_at"] = pd.to_datetime(
                chart_data["created_at"]
            )

            chart_data = chart_data.sort_values(
                "created_at"
            )

            st.line_chart(
                chart_data.set_index("created_at")[
                    "mood_score"
                ]
            )


    with right:

        st.markdown(
            """
            <div class="tip">

            <strong>🌱 Today's Reminder</strong>

            <br><br>

            You don't need to have everything
            figured out today. Small positive
            steps still count.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# MOOD CHECK-IN
# =========================================================

elif page == "😊 Mood Check-in":

    st.markdown(
        '<div class="main-title">How are you <span>feeling?</span> 😊</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Take a moment to check in with yourself.</div>',
        unsafe_allow_html=True
    )


    with st.form("mood_form"):

        name = st.text_input(
            "Your Name"
        )


        mood_options = {

            "😊 Happy": 5,

            "🙂 Good": 4,

            "😐 Okay": 3,

            "😔 Sad": 2,

            "😣 Stressed": 1

        }


        mood = st.selectbox(
            "How are you feeling today?",
            list(mood_options.keys())
        )


        note = st.text_area(
            "What's on your mind?",
            placeholder="Write a few thoughts about your day..."
        )


        submitted = st.form_submit_button(
            "💚 Save My Mood"
        )


        if submitted:

            if name.strip() == "":

                st.warning(
                    "Please enter your name."
                )

            else:

                score = mood_options[mood]

                mood_name = mood.split(" ", 1)[1]

                save_mood(
                    name,
                    mood_name,
                    score,
                    note
                )

                st.success(
                    "Your mood has been saved successfully! 🌱"
                )

                st.balloons()


# =========================================================
# MOOD ANALYTICS
# =========================================================

elif page == "📊 Mood Analytics":

    st.markdown(
        '<div class="main-title">Your <span>Mood Analytics</span> 📊</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Understand your emotional patterns over time.</div>',
        unsafe_allow_html=True
    )


    if len(mood_df) == 0:

        st.info(
            "No mood data yet. Complete your first mood check-in."
        )

    else:

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Check-ins",
                len(mood_df)
            )


        with col2:

            st.metric(
                "Average Score",
                f"{mood_df['mood_score'].mean():.1f}/5"
            )


        with col3:

            happiest = mood_df[
                "mood"
            ].value_counts().idxmax()

            st.metric(
                "Most Common",
                happiest
            )


        with col4:

            highest = mood_df[
                "mood_score"
            ].max()

            st.metric(
                "Best Score",
                f"{highest}/5"
            )


        st.write("")


        left, right = st.columns(2)


        with left:

            st.subheader(
                "Mood Distribution"
            )

            mood_counts = mood_df[
                "mood"
            ].value_counts()

            st.bar_chart(
                mood_counts
            )


        with right:

            st.subheader(
                "Mood Score Trend"
            )

            trend = mood_df[
                ["created_at", "mood_score"]
            ].copy()

            trend["created_at"] = pd.to_datetime(
                trend["created_at"]
            )

            trend = trend.sort_values(
                "created_at"
            )

            st.line_chart(
                trend.set_index("created_at")
            )


        st.subheader(
            "Recent Check-ins"
        )

        display_df = mood_df[
            [
                "name",
                "mood",
                "mood_score",
                "note",
                "created_at"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# JOURNAL
# =========================================================

elif page == "📖 My Journal":

    st.markdown(
        '<div class="main-title">Your <span>Journal</span> 📖</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A private space for your thoughts and reflections.</div>',
        unsafe_allow_html=True
    )


    with st.form("journal_form"):

        name = st.text_input(
            "Your Name"
        )

        title = st.text_input(
            "Journal Title",
            placeholder="e.g. A productive day"
        )

        content = st.text_area(
            "Write your thoughts",
            height=250,
            placeholder="Write freely. There is no right or wrong way..."
        )

        submitted = st.form_submit_button(
            "📖 Save Journal Entry"
        )


        if submitted:

            if (
                name.strip() == ""
                or title.strip() == ""
                or content.strip() == ""
            ):

                st.warning(
                    "Please complete all fields."
                )

            else:

                save_journal(
                    name,
                    title,
                    content
                )

                st.success(
                    "Journal entry saved successfully! 📖"
                )


    st.write("")

    st.subheader(
        "Reflection Prompts 💭"
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        st.markdown(
            """
            <div class="card">

            <h3>🌟 Today's Highlight</h3>

            <p>
            What was the best moment of your day?
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p2:

        st.markdown(
            """
            <div class="card">

            <h3>💭 What's on my mind?</h3>

            <p>
            What thoughts are taking up your attention?
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p3:

        st.markdown(
            """
            <div class="card">

            <h3>🎯 Tomorrow</h3>

            <p>
            What is one small thing you want to accomplish?
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# BREATHING
# =========================================================

elif page == "🧘 Breathing Space":

    st.markdown(
        '<div class="main-title">Breathing <span>Space</span> 🧘</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Slow down. Breathe. Give your mind a moment.</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="breathing-container">

        <h2>4 - 4 - 4 Breathing</h2>

        <p>
        Breathe in for 4 seconds · Hold for 4 seconds ·
        Breathe out for 4 seconds
        </p>

        <div class="breath-circle">
        Breathe
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    if st.button(
        "🧘 Start Breathing Exercise"
    ):

        progress = st.progress(0)

        message = st.empty()


        for i in range(100):

            progress.progress(i + 1)

            if i < 40:

                message.info(
                    "🌬️ Breathe in slowly..."
                )

            elif i < 70:

                message.warning(
                    "⏸️ Hold..."
                )

            else:

                message.success(
                    "🌿 Breathe out slowly..."
                )

            time.sleep(0.1)


        message.success(
            "✨ Well done. Take another calm breath."
        )


# =========================================================
# WELLNESS TIPS
# =========================================================

elif page == "🌱 Wellness Tips":

    st.markdown(
        '<div class="main-title">Wellness <span>Tips</span> 🌱</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Small habits can make a meaningful difference.</div>',
        unsafe_allow_html=True
    )


    tips = [

        (
            "💧",
            "Stay Hydrated",
            "Keep water nearby and stay hydrated throughout the day."
        ),

        (
            "😴",
            "Prioritize Sleep",
            "Give your mind and body enough time to rest."
        ),

        (
            "🚶",
            "Move Your Body",
            "Take a short walk or stretch between study sessions."
        ),

        (
            "📵",
            "Take Digital Breaks",
            "Step away from your screen for a few minutes."
        ),

        (
            "🥗",
            "Eat Regularly",
            "Don't skip meals during busy college days."
        ),

        (
            "👥",
            "Stay Connected",
            "Talk to friends, family or someone you trust."
        ),

        (
            "🌳",
            "Spend Time Outside",
            "A little fresh air can give you a refreshing break."
        ),

        (
            "📝",
            "Write It Down",
            "Journaling can help organize your thoughts."
        )

    ]


    for i in range(0, len(tips), 2):

        col1, col2 = st.columns(2)


        with col1:

            icon, title, text = tips[i]

            st.markdown(
                f"""
                <div class="card">

                <h2>{icon}</h2>

                <h3>{title}</h3>

                <p>{text}</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        if i + 1 < len(tips):

            with col2:

                icon, title, text = tips[i + 1]

                st.markdown(
                    f"""
                    <div class="card">

                    <h2>{icon}</h2>

                    <h3>{title}</h3>

                    <p>{text}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

    🧠 <strong>MindMate</strong> — Student Mental Wellness Companion

    <br>

    <small>
    A student-focused wellness and self-reflection tool.
    </small>

    </div>
    """,
    unsafe_allow_html=True
)