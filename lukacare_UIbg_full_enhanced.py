
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt

openai.api_key = "sk-여기에_API_키_입력"

st.set_page_config(
    page_title="루카케어 Mini – 건강 에이전트",
    page_icon="❤️",
    layout="centered"
)

# 세션 상태 초기화
if "emotion_log" not in st.session_state:
    st.session_state["emotion_log"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/JUN-MIN-A/lukacare-streamlit/main/lukacare_bg_final_50.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(255,255,255,0.9);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        color: #333333;
    }
    .card {
        background-color: #fff;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #F7CAC9;
        color: #4B3F33;
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    h1, h3, h4 {
        color: #B45F5F;
        text-align: center;
    }
    p, label, div, input, .stTextInput {
        color: #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4>AI 기반 건강 관리 에이전트 – 챗봇 & GPT 자동 연결</h4>", unsafe_allow_html=True)

st.markdown("""
<div class='main-box'>
<h3>앱 소개 및 개요</h3>
<p style='font-size:16px;'>
<strong>루카케어 Mini</strong>는 프리셋 응답 + GPT를 결합하여<br>
정서/건강/병원 추천을 제공하는 홈케어형 AI 건강상담 에이전트입니다.<br>
Streamlit 기반으로 웹에서 언제든지 상담 가능하며, 정서기록 저장, 대화 이어하기, 지도 안내 기능까지 제공합니다.
</p>
</div>
""", unsafe_allow_html=True)

# 카드 안내
features = [
    ("🩸 혈당 분석", "혈당 수치 그래프 및 건강 메시지 제공"),
    ("💓 혈압 분석", "수축기/이완기 수치 분석 및 경고"),
    ("🌡️ 체온 분석", "체온 그래프 및 발열 판단"),
    ("😊 정서 관리", "기분 입력 및 정서 기록"),
    ("🩺 사전 진료", "GPT 기반 상담 또는 프리셋 응답"),
    ("🏥 주변 의원 연락처", "진료과별 추천 병원 or GPT 병원 안내"),
    ("🧠 상담 이어하기", "이전 GPT 대화 기반 후속 질문"),
    ("🗺️ 지도 기능 안내", "지도 연동 병원위치 API 안내")
]
st.markdown("<h3>기능 안내</h3>", unsafe_allow_html=True)
for icon, desc in features:
    st.markdown(f"<div class='card'><h4>{icon}</h4><p>{desc}</p></div>", unsafe_allow_html=True)

# 라디오로 기능 선택
option = st.radio("기능을 선택하세요", [f[0][2:] for f in features])
user_input = st.text_input("증상/질환/문의 입력")

# 프리셋 + GPT
preset_responses = {
    "두통": "휴식 부족이나 스트레스로 인한 일시적 두통일 수 있어요.",
    "소화불량": "기름진 음식이나 과식이 원인이 될 수 있어요.",
    "불면": "수면 위생을 지켜보세요. 취침 전 1시간은 스마트폰 사용을 줄여보세요.",
    "피로": "지속적인 피로는 수면 부족, 스트레스, 철분 부족 등이 원인일 수 있어요.",
    "생리통": "복부를 따뜻하게 하고 무리하지 마세요.",
    "어지러움": "식사 불규칙, 저혈압, 과로일 수 있어요. 앉아서 쉬어보세요.",
    "우울감": "마음이 무거울 땐 가벼운 산책, 대화가 도움이 됩니다."
}
def ask_gpt(prompt):
    st.session_state.chat_history.append(prompt)
    history_prompt = "\n".join(st.session_state.chat_history)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": history_prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

clinics = {
    "내과": "서울 내과의원 02-1111-1111",
    "이비인후과": "숨편한 이비인후과 02-2222-2222",
    "외과": "튼튼 외과의원 02-3333-3333",
    "안과": "밝은눈 안과 02-4444-4444",
    "피부과": "더마인 피부과 02-5555-5555",
    "성형외과": "아름 성형외과 02-6666-6666",
    "정신과": "마음편한 정신과 02-7777-7777",
    "대학병원": "서울대병원 02-880-5114",
    "2차병원": "강동경희대병원 02-440-7000"
}
glucose = [95, 110, 135, 102, 99]
temperature = [36.4, 36.7, 37.1, 36.5, 36.6]
bp_data = pd.DataFrame({
    "날짜": ["6/1", "6/2", "6/3", "6/4", "6/5"],
    "수축기(mmHg)": [120, 145, 130, 128, 160],
    "이완기(mmHg)": [80, 95, 88, 82, 102]
})

if st.button("실행하기"):
    if option == "혈당 분석":
        st.subheader("혈당 분석 결과")
        st.line_chart(glucose)

    elif option == "혈압 분석":
        st.subheader("혈압 측정 결과")
        st.dataframe(bp_data)

    elif option == "체온 분석":
        st.subheader("체온 변화")
        st.line_chart(temperature)

    elif option == "정서 관리":
        st.subheader("오늘의 감정 기록")
        mood = st.radio("오늘 기분은 어떤가요?", ["좋음", "보통", "우울", "지침", "불안"])
        reason = st.text_input("그 기분의 이유는 무엇인가요?")
        if reason:
            st.session_state["emotion_log"].append({"기분": mood, "이유": reason})
            df = pd.DataFrame(st.session_state["emotion_log"])
            st.dataframe(df)

    elif option == "사전 진료":
        st.subheader("전문의 의견")
        if not user_input:
            st.warning("증상을 입력해주세요.")
        else:
            for k in preset_responses:
                if k in user_input:
                    st.success(f"루카의 응답: {preset_responses[k]}")
                    break
            else:
                st.write(ask_gpt(user_input))

    elif option == "주변 의원 연락처":
        st.subheader("추천 병원 안내")
        if not user_input:
            for dept, info in clinics.items():
                st.markdown(f"- **{dept}**: {info}")
        else:
            matched = [info for key, info in clinics.items() if key in user_input]
            if matched:
                for i in matched:
                    st.success(i)
            else:
                st.write(ask_gpt(f"{user_input} 진료 가능한 병원을 추천해주세요."))

    elif option == "상담 이어하기":
        st.subheader("이전 대화 이어서 GPT 상담")
        if user_input:
            st.write(ask_gpt(user_input))
        else:
            st.warning("상담할 내용을 입력해주세요.")

    elif option == "지도 기능 안내":
        st.subheader("지도 기반 병원 안내")
        st.info("Google Maps API와 연동하면 위치 기반 병원 안내 기능을 구현할 수 있어요.")
        st.markdown("예시: [Google Maps Platform](https://developers.google.com/maps/documentation)")

