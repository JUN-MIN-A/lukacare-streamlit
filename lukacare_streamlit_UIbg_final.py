
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt

# OpenAI API 키
openai.api_key = "sk-여기에_API_키_입력"

# 페이지 설정
st.set_page_config(
    page_title="루카케어 Mini – 건강 에이전트",
    page_icon="❤️",
    layout="centered"
)

# 배경 스타일 + 앱 소개 고정 출력
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/민아GitHubID/lukacare-streamlit/main/lukacare_bg_transparent.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(255,255,255,0.5);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #F7CAC9;
        color: #4B3F33;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    h1, h4 {
        color: #B45F5F;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 앱 로고 + 소개 출력
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4>AI 기반 건강 관리 에이전트 – 챗봇 & GPT 자동 연결</h4>", unsafe_allow_html=True)
st.markdown("<div class='main-box'>", unsafe_allow_html=True)

# 프리셋 응답
preset_responses = {
    "두통": "휴식 부족이나 스트레스로 인한 일시적 두통일 수 있어요.",
    "소화불량": "기름진 음식이나 과식이 원인이 될 수 있어요.",
    "불면": "수면 위생을 지켜보세요. 취침 전 1시간은 스마트폰 사용을 줄여보세요.",
    "피로": "지속적인 피로는 수면 부족, 스트레스, 철분 부족 등이 원인일 수 있어요.",
    "생리통": "복부를 따뜻하게 하고 무리하지 마세요.",
    "어지러움": "식사 불규칙, 저혈압, 과로일 수 있어요. 앉아서 쉬어보세요.",
    "우울감": "마음이 무거울 땐 가벼운 산책, 대화가 도움이 됩니다."
}

# GPT 함수
def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 의원 추천 리스트
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

# 기능 선택
option = st.selectbox("기능을 선택하세요", [
    "사전 진료", "주변 의원 연락처"
])
user_input = st.text_input("증상/질환/문의 입력")

if st.button("실행하기"):
    if option == "사전 진료":
        if not user_input:
            st.warning("증상을 입력해주세요.")
        else:
            found = False
            for k in preset_responses:
                if k in user_input:
                    st.success(f"루카의 응답: {preset_responses[k]}")
                    found = True
                    break
            if not found:
                st.info("GPT 연결 중...")
                st.write(ask_gpt(f"사용자의 증상: {user_input}"))
    elif option == "주변 의원 연락처":
        if not user_input:
            for dept, info in clinics.items():
                st.markdown(f"- **{dept}**: {info}")
        else:
            matched = [info for key, info in clinics.items() if key in user_input]
            if matched:
                for i in matched:
                    st.success(i)
            else:
                st.info("GPT 연결 중...")
                st.write(ask_gpt(f"{user_input} 진료 가능한 병원을 추천해주세요."))

st.markdown("</div>", unsafe_allow_html=True)
