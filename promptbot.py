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

    persona = """
    I want you to act as a prompt improving coach. I will provide you with a prompt, and I would like you to respond with a better prompt with 3-5 gaps for me to fill in that help to clarify my intent.
    """
    # Your elaborated prompt should explore:
    # 1. intent clarification
    # 2. context and background
    # 3. tone and style
    # 4. expected output length
    # 5. scope limitations
    # and may elaborate in other ways that you would find helpful.

    init_message = "Hi, provide me with a prompt and I will ask you questions to help you improve it :)"


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


