import streamlit as st
import openai

openai.api_key = st.secrets.openai_api_key


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
