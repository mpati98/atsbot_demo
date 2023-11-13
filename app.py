import openai
import streamlit as st
import time
import json

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

def write_json(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
    # Writing to sample.json
    with open(time.strftime("%Y%m%d-%H%M%S") + ".json", "w+") as outfile:
        outfile.write(json_object)

if prompt := st.chat_input("Bạn cần gì?"):
    with st.chat_message("user"):

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if st.session_state["state"] == "get_infor":
            if st.session_state["tag"] == "get_name":
                full_response = "Chào bạn, cho mình xin số điện thoại để tiện liên hệ nhé"
                st.session_state["tag"] = "get_phone"
            elif st.session_state["tag"] == "get_phone":
                full_response = "Hiện bạn đang ở khu vực nào thế? HCM, DN, HN, ..."
                st.session_state["tag"] = "get_location"
            elif st.session_state["tag"] == "get_location":
                full_response = "Năm nay bạn bao nhiêu tuổi rồi, bạn có dự kiến đi du học khi nào?"
                st.session_state["tag"] = "get_age"
            elif st.session_state["tag"] == "get_age":
                full_response = "Bạn đang nhắm đến du học nước nào? Úc, Canada hay Mỹ?"
                st.session_state["tag"] = "get_country"
            elif st.session_state["tag"] == "get_country":
                full_response = "Bạn có hứng thú hay quan tâm đến ngành nào không?"
                st.session_state["tag"] = "end_get_infor"
            elif st.session_state["tag"] == "end_get_infor":
                full_response = "Done, giờ bạn có thể hỏi chatGPT thoải mái nhé!"
                st.session_state["tag"] = ""
                st.session_state["state"] = ""
                # Write session state to dict
                widget_values = {}
                for key in st.session_state:
                    widget_values[key] = st.session_state[key]
                write_json(widget_values)

        else:
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})