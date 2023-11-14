import openai
import streamlit as st
from src.get_infor import get_infor
st.title("ChatGPT-like clone")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state["state"] = "get_infor"
    st.session_state.messages.append({"role": "assistant", "content": "Trước khi vào nội dung chính, ta làm quen với nhau trước được không, bạn tên gì?"})
    st.session_state["tag"] = "get_name"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bạn cần gì?"):
    with st.chat_message("user"):

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if st.session_state["state"] == "get_infor":
            full_response = get_infor(st.session_state["tag"])

        else:
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": "Đóng vai trò như 1 nhân viên tư vấn du học của ATS, công ty chuyên tư ván du học Úc, Canada và Mỹ. Với hơn 20 năm kinh nghiệm hiện có văn phòng tại 55 Trương Quốc Dung, Phú Nhuận",
                    "role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
