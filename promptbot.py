import streamlit as st
import openai

openai.api_key = st.secrets.OPENAI_API_KEY

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    system_msg = ""

# persona taken from: https://www.reddit.com/r/ChatGPTPromptGenius/comments/11tzh3p/prompt_engineer/
    persona = """
    I want you to act as a prompt engineer. Your goal is to provide iteratively better prompts based on a starting prompt given by me, the user, and also provide relevant questions about the prompt and its subject. Your questions should be based on current best practices in the field of prompt engineering and their goal should be always to clarify and improve the prompt. Each of your anwers should provide clear and concise a) the revised prompt and b) short questions to keep improving it. I'll tell you we're Done when I'm satisfied with the final result.
    """
    init_message = "Hi, provide me with a prompt and I will help you improve it :)"


    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", 
            "content": persona
            },
            {"role": "assistant",
            "content": init_message
            }]

    # add if clause to choose avatar for diff roles


    prompt = st.chat_input("Say something")
    if prompt:
        # add to session state
        st.session_state.messages.append(
            {"role": "user",
            "content": prompt
            })
        # send to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = st.session_state.messages)
        assistant_msg = response.choices[0].message
        # st.write(response)
        st.session_state.messages.append(assistant_msg)

    # st.write(st.session_state["messages"])    

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


