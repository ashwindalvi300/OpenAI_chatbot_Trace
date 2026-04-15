# import streamlit as st
# import requests

# # =========================
# # CONFIG
# # =========================
# N8N_WEBHOOK_URL = "http://localhost:5678/webhook/query"

# # =========================
# # PAGE SETUP
# # =========================
# st.set_page_config(page_title="Traceability AI Chat", layout="wide")
# st.title("📊 Traceability AI Assistant")

# # =========================
# # INIT SESSION STATE
# # =========================
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "context_saved" not in st.session_state:
#     st.session_state.context_saved = False

# if "user_id" not in st.session_state:
#     st.session_state.user_id = ""

# if "station_id" not in st.session_state:
#     st.session_state.station_id = ""

# if "imei" not in st.session_state:
#     st.session_state.imei = ""

# # =========================
# # TOP CONTEXT BAR
# # =========================
# with st.container():
#     st.subheader("🔐 User Context")

#     col1, col2, col3, col4 = st.columns([2, 3, 2, 2])

#     with col1:
#         st.session_state.user_id = st.text_input(
#             "User ID",
#             value=st.session_state.user_id,
#             disabled=st.session_state.context_saved
#         )

#     with col2:
#         st.session_state.imei = st.text_input(
#             "IMEI",
#             value=st.session_state.imei,
#             disabled=st.session_state.context_saved
#         )

#     with col3:
#         st.session_state.station_id = st.text_input(
#             "Station ID",
#             value=st.session_state.station_id,
#             disabled=st.session_state.context_saved
#         )

#     with col4:
#         if not st.session_state.context_saved:
#             if st.button("💾 Save Context"):
#                 if not st.session_state.user_id or not st.session_state.imei or not st.session_state.station_id:
#                     st.error("All fields are required")
#                 else:
#                     st.session_state.context_saved = True
#         else:
#             if st.button("🔄 Change Context"):
#                 st.session_state.context_saved = False
#                 st.session_state.messages = []

# st.divider()

# # =========================
# # CHAT WINDOW
# # =========================
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # =========================
# # CHAT INPUT (BOTTOM)
# # =========================
# query = st.chat_input(
#     "Ask about device activities...",
#     disabled=not st.session_state.context_saved
# )

# if query:
#     # Show user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": query
#     })

#     with st.chat_message("user"):
#         st.markdown(query)

#     payload = {
#         "userId": st.session_state.user_id,
#         "stationId": st.session_state.station_id,
#         "imei": st.session_state.imei,
#         "query": query
#     }

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             try:
#                 response = requests.post(
#                     N8N_WEBHOOK_URL,
#                     json=payload,
#                     timeout=120
#                 )
#                 response.raise_for_status()
#                 answer = response.text
#             except Exception as e:
#                 answer = f"❌ Error: {str(e)}"

#         st.markdown(answer)

#     # Save assistant response
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer
#     })


import streamlit as st
import requests
import json

# =========================
# CONFIG
# =========================
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/query"

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Traceability AI Chat", layout="wide")
st.title("📊 Traceability AI Assistant")

# =========================
# INIT SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context_saved" not in st.session_state:
    st.session_state.context_saved = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "station_id" not in st.session_state:
    st.session_state.station_id = ""

if "imei" not in st.session_state:
    st.session_state.imei = ""

# =========================
# TOP CONTEXT BAR
# =========================
with st.container():
    st.subheader("🔐 User Context")

    col1, col2, col3, col4 = st.columns([2, 3, 2, 2])

    with col1:
        st.session_state.user_id = st.text_input(
            "User ID",
            value=st.session_state.user_id,
            disabled=st.session_state.context_saved
        )

    with col2:
        st.session_state.imei = st.text_input(
            "IMEI",
            value=st.session_state.imei,
            disabled=st.session_state.context_saved
        )

    with col3:
        st.session_state.station_id = st.text_input(
            "Station ID",
            value=st.session_state.station_id,
            disabled=st.session_state.context_saved
        )

    with col4:
        if not st.session_state.context_saved:
            if st.button("💾 Save Context"):
                if not st.session_state.user_id or not st.session_state.imei or not st.session_state.station_id:
                    st.error("❌ All fields are required")
                else:
                    st.session_state.context_saved = True
        else:
            if st.button("🔄 Change Context"):
                st.session_state.context_saved = False
                st.session_state.messages = []

st.divider()

# =========================
# CHAT WINDOW
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        msg_type = msg.get("type", "text")

        # Plain text (user)
        if msg_type == "text":
            st.markdown(msg["content"])

        # Structured JSON (assistant)
        elif msg_type == "json":
            data = msg["content"]

            st.markdown(f"### {data.get('summary', 'Response')}")

            activities = data.get("activities", [])
            if activities:
                for act in activities:
                    st.markdown(f"""
                    <div style="
                        padding:10px;
                        border-radius:8px;
                        border:1px solid #ddd;
                        margin-bottom:10px;
                        background-color:#0e1117;
                    ">
                        <b>Activity:</b> {act.get('activityName')}<br>
                        <b>Txn ID:</b> {act.get('txnId')}<br>
                        <b>Detail ID:</b> {act.get('activityDetailId')}<br>
                        <b>Details:</b> {act.get('details', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No activities found.")

# =========================
# CHAT INPUT (BOTTOM)
# =========================
query = st.chat_input(
    "Ask about device activities...",
    disabled=not st.session_state.context_saved
)

if query:
    # ---- USER MESSAGE ----
    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    payload = {
        "userId": st.session_state.user_id,
        "stationId": st.session_state.station_id,
        "imei": st.session_state.imei,
        "query": query
    }

    # ---- ASSISTANT RESPONSE ----
    with st.chat_message("assistant"):
        with st.spinner("Fetching data..."):
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    timeout=120
                )
                response.raise_for_status()

                try:
                    data = response.json()
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "json",
                        "content": data
                    })

                    st.markdown(f"### {data.get('summary', 'Response')}")

                    activities = data.get("activities", [])
                    if activities:
                        for act in activities:
                            st.markdown(f"""
                            <div style="
                                padding:10px;
                                border-radius:8px;
                                border:1px solid #ddd;
                                margin-bottom:10px;
                                background-color:#0e1117;
                            ">
                                <b>Activity:</b> {act.get('activityName')}<br>
                                <b>Txn ID:</b> {act.get('txnId')}<br>
                                <b>Detail ID:</b> {act.get('activityDetailId')}<br>
                                <b>Details:</b> {act.get('details', 'N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No activities found.")

                except json.JSONDecodeError:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "text",
                        "content": response.text
                    })
                    st.markdown(response.text)

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "text",
                    "content": error_msg
                })
