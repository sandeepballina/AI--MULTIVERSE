import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import random
import time
from datetime import datetime
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []


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
    surprise_msg = random.choice(surprise)
    st.session_state.messages.append({"role": "user", "content": surprise_msg})
    
    # Prepare prompt with history
    history_context = ""
    for msg in st.session_state.messages:
        role_name = "User" if msg["role"] == "user" else personality
        history_context += f"{role_name}: {msg['content']}\n"
        
    prompt = f"""
{personalities[personality]}

{styles[reply_style]}

{lengths[reply_length]}

Stay completely in character.

Here is the conversation history so far:
{history_context}
"""
    start = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        end = time.time()
        st.session_state["response_time"] = round(end - start, 2)
    except Exception as e:
        st.error(e)
    st.rerun()

if st.sidebar.button("🗑 CLEAR CHAT"):
    st.session_state.messages = []
    if "response_time" in st.session_state:
        del st.session_state["response_time"]
    st.rerun()

st.title("🌌 THE MULTIVERSE OF CHATBOTS")

st.write("Talk to famous personalities from across the multiverse!")

st.info(f"Currently talking to **{personality}**")

# Task 2: Render the Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Task 3: Upgrade the Input UI & Task 4: Save New Messages to Memory
if user_message := st.chat_input("Say something...", max_chars=500):
    # Display the user message in the chat container
    with st.chat_message("user"):
        st.markdown(user_message)
    
    # Save user message to memory
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Prepare prompt with history
    history_context = ""
    for msg in st.session_state.messages:
        role_name = "User" if msg["role"] == "user" else personality
        history_context += f"{role_name}: {msg['content']}\n"

    prompt = f"""
{personalities[personality]}

{styles[reply_style]}

{lengths[reply_length]}

Stay completely in character.

Here is the conversation history so far:
{history_context}
"""
    
    start = time.time()
    with st.spinner("🧠 AI is thinking..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            reply = response.text
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(reply)
            
            # Save assistant response to memory
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            end = time.time()
            st.session_state["response_time"] = round(end - start, 2)
            
        except Exception as e:
            st.error(e)
            
    st.rerun()

if len(st.session_state.messages) > 0:
    full_chat = ""
    for msg in st.session_state.messages:
        role_label = "You" if msg["role"] == "user" else "AI"
        full_chat += f"""
{role_label}:
{msg['content']}

------------------------------------

"""

    st.download_button(
        "📥 Download Conversation",
        full_chat,
        file_name="conversation.txt"
    )

st.divider()

st.subheader("📊 Chat Statistics")

total_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
total_characters = sum(len(msg["content"]) for msg in st.session_state.messages if msg["role"] == "user")
total_words = sum(len(msg["content"].split()) for msg in st.session_state.messages if msg["role"] == "user")

c1, c2, c3 = st.columns(3)
c1.metric("Messages", total_messages)
c2.metric("Characters", total_characters)
c3.metric("Words", total_words)

if "response_time" in st.session_state:
    st.success(f"⏱ Response generated in {st.session_state.response_time} seconds")

st.markdown("""
<div class="footer">

<hr>

🚀 <b>AI Multiverse v2.0</b><br>

Developed using ❤️ Streamlit + Google Gemini

</div>
""", unsafe_allow_html=True)