import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import random
import time
from datetime import datetime
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="wide"
)

st.markdown("""
<style>

.main{
background:#0E1117;
}

.stButton>button{
width:100%;
border-radius:10px;
height:45px;
font-weight:bold;
font-size:16px;
}

.stTextInput input{
border-radius:10px;
}

.chat-user{
padding:15px;
background:#1f77b4;
border-radius:10px;
margin-bottom:10px;
color:white;
}

.chat-ai{
padding:15px;
background:#262730;
border-radius:10px;
margin-bottom:20px;
color:white;
}

.footer{
text-align:center;
padding-top:20px;
color:gray;
}

</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history=[]

personalities={
"🦾 Iron Man":"You are Tony Stark (Iron Man). Speak confidently with humor and intelligence.",

"🦇 Batman":"You are Batman. Be dark, serious and mysterious.",

"🕵 Sherlock Holmes":"You are Sherlock Holmes. Answer with logical deductions.",

"⚽ Ronaldo Fan":"You are Cristiano Ronaldo's biggest fan.",

"💻 Hacker":"You are an ethical hacker who explains cybersecurity.",

"🧙 Harry Potter":"You are Harry Potter from Hogwarts.",

"🤣 Stand-up Comedian":"Always answer with jokes.",

"🇺🇸 Donald Trump":"Talk like Donald Trump.",

"🤖 Robot":"You are a futuristic AI robot.",

"🧠 Albert Einstein":"Explain everything scientifically.",

"⚡ Thor":"You are Thor, God of Thunder.",

"😈 Loki":"You are Loki, clever and mischievous.",

"🏏 Virat Kohli":"Speak like Virat Kohli.",

"🚀 Elon Musk":"Talk like Elon Musk.",

"📱 Steve Jobs":"Talk like Steve Jobs.",

"🎬 Deadpool":"Talk like Deadpool with funny sarcasm."
}

styles={
"Friendly":"Be friendly.",
"Funny":"Be humorous.",
"Professional":"Be professional.",
"Motivational":"Motivate the user.",
"Short":"Keep replies concise."
}

lengths={
"Short":"Maximum 60 words.",
"Medium":"Around 120 words.",
"Long":"Around 250 words."
}

st.sidebar.title("⚙️ Settings")

personality=st.sidebar.selectbox(
"Choose Personality",
list(personalities.keys())
)

reply_style=st.sidebar.selectbox(
"Response Style",
list(styles.keys())
)

reply_length=st.sidebar.selectbox(
"Response Length",
list(lengths.keys())
)

surprise=[
"Tell me a joke.",
"Motivate me.",
"Teach me AI.",
"Explain quantum physics simply.",
"How can I become successful?",
"What is happiness?",
"Give me study tips.",
"Write a poem."
]

if st.sidebar.button("🎲 Surprise Me"):
    st.session_state["message"]=random.choice(surprise)

st.title("🌌 THE MULTIVERSE OF CHATBOTS")

st.write("Talk to famous personalities from across the multiverse!")

st.info(f"Currently talking to **{personality}**")

message=st.text_area(
"💬 Type your message",
value=st.session_state.get("message",""),
height=120
)

st.caption(f"Characters: {len(message)}")

col1,col2=st.columns(2)

with col1:
    send=st.button("🚀 SEND")

with col2:
    clear = st.button("🗑 CLEAR CHAT")

    if clear:
        st.session_state.history = []
        st.rerun()

if send:

    if message.strip() == "":
        st.warning("⚠ Please type a message first.")
        st.stop()

    if len(message) > 500:
        st.error("Message should be less than 500 characters.")
        st.stop()

    prompt = f"""
{personalities[personality]}

{styles[reply_style]}

{lengths[reply_length]}

Stay completely in character.

User:
{message}
"""

    start = time.time()

    with st.spinner("🧠 AI is thinking..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            reply = response.text

            current_time = datetime.now().strftime("%I:%M %p")

            st.session_state.history.append(
                {
                    "user": message,
                    "ai": reply,
                    "time": current_time,
                    "personality": personality
                }
            )

        except Exception as e:
            st.error(e)

    end = time.time()

st.divider()

for chat in st.session_state.history:

    st.markdown(f"""
<div class="chat-user">

👤 <b>You</b><br><br>

{chat["user"]}

</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="chat-ai">

{chat["personality"]} <br>
🕒 {chat["time"]}<br><br>

{chat["ai"]}

</div>
""", unsafe_allow_html=True)

if len(st.session_state.history) > 0:

    full_chat = ""

    for chat in st.session_state.history:

        full_chat += f"""
You:
{chat['user']}

AI:
{chat['ai']}

------------------------------------

"""

    st.download_button(
        "📥 Download Conversation",
        full_chat,
        file_name="conversation.txt"
    )

st.divider()

st.subheader("📊 Chat Statistics")

total_characters = sum(len(chat["user"]) for chat in st.session_state.history)

total_messages = len(st.session_state.history)

total_words = sum(len(chat["user"].split()) for chat in st.session_state.history)

c1, c2, c3 = st.columns(3)

c1.metric("Messages", total_messages)

c2.metric("Characters", total_characters)

c3.metric("Words", total_words)

if send:
    st.success(f"⏱ Response generated in {round(end-start,2)} seconds")

st.markdown("""
<div class="footer">

<hr>

🚀 <b>AI Multiverse v2.0</b><br>

Developed using ❤️ Streamlit + Google Gemini

</div>
""", unsafe_allow_html=True)