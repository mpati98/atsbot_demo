import streamlit as st
from src.utils import write_json



def get_infor(tag):
    if tag == "get_name":
        full_response = "Chào bạn, cho mình xin số điện thoại để tiện liên hệ nhé"
        st.session_state["tag"] = "get_phone"
    elif tag == "get_phone":
        full_response = "Hiện bạn đang ở khu vực nào thế? HCM, DN, HN, ..."
        st.session_state["tag"] = "get_location"
    elif tag == "get_location":
        full_response = "Năm nay bạn bao nhiêu tuổi rồi, bạn có dự kiến đi du học khi nào?"
        st.session_state["tag"] = "get_age"
    elif tag == "get_age":
        full_response = "Bạn đang nhắm đến du học nước nào? Úc, Canada hay Mỹ?"
        st.session_state["tag"] = "get_country"
    elif tag == "get_country":
        full_response = "Bạn có hứng thú hay quan tâm đến ngành nào không?"
        st.session_state["tag"] = "end_get_infor"
    elif tag == "end_get_infor":
        full_response = "Done, giờ bạn có thể hỏi chatGPT thoải mái nhé!"
        st.session_state["tag"] = ""
        st.session_state["state"] = ""
        # Write session state to dict
        widget_values = {}
        for key in st.session_state:
            widget_values[key] = st.session_state[key]
        write_json(widget_values)
    return full_response