# 🌌 The Multiverse of Chatbots: Memory Vault Edition

An interactive, stateful Streamlit chatbot application powered by Google Gemini, completed as part of the **MirAI School of Technology Virtual Summer Internship 2026 ("AI Builder" Track)**.

This version features the implementation of the **Memory Vault (Stateful Chatbot)** assignment, transforming a previously stateless chatbot into a fully stateful conversational experience.

## 🚀 Key Features

- **Stateful Memory Vault**: Utilizes Streamlit's `st.session_state` to store and maintain conversation history across page interactions and configuration changes.
- **Modern Chat Interface**: Employs Streamlit's native `st.chat_input` and `st.chat_message` widgets for a seamless, messaging-app feel.
- **Multiverse Personalities**: Toggle between 15+ famous personalities (e.g., Iron Man, Batman, Sherlock Holmes, Cristiano Ronaldo Fan, Ethical Hacker, Albert Einstein, and more) on-the-fly without losing chat history.
- **Customizable Responses**: Adjust response style (Friendly, Funny, Professional, etc.) and lengths (Short, Medium, Long).
- **Interactive Side Utilities**:
  - 🎲 **Surprise Me**: Generates a random topic prompt in-character.
  - 🗑 **Clear Chat**: Instantly wipes the conversation history.
  - 📥 **Download Conversation**: Exports the full transcript.
  - 📊 **Chat Statistics**: Live tracking of messages, total characters, and word counts.

## 🛠 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd AI-MULTIVERSE
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📝 Assignment Requirements Implemented

- **Task 1: Initialize the Memory Vault** - Checked and initialized `st.session_state.messages` list on application startup.
- **Task 2: Render the Chat History** - Replaced custom HTML/CSS with standard loop utilizing `st.chat_message` container.
- **Task 3: Upgrade the Input UI** - Replaced `st.text_area` and `st.button` with `st.chat_input` using the Python walrus operator (`:=`).
- **Task 4: Save New Messages to Memory** - Programmatically appended user inputs and Gemini API assistant outputs to `st.session_state.messages`.