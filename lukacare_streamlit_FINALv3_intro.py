
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt

openai.api_key = "sk-여기에_API_키_입력"

st.set_page_config(
    page_title="루카케어 Mini – 건강 관리 에이전트",
    page_icon="❤️",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/민아GitHubID/lukacare-streamlit/main/lukacare_bg_transparent.jpg');
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
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    h1, h3, h4 {
        color: #B45F5F;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 앱 이름 + 소개 문단 출력
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4>AI 기반 건강상담 에이전트</h4>", unsafe_allow_html=True)
st.markdown("""
<div class='main-box'>
<h3>앱 소개 및 개요</h3>
<p style='font-size:16px'>
<strong>루카케어 Mini</strong>는 일상적인 건강 질문에는 사전 정의된 프리셋 응답을 제공하고,<br>
복잡하거나 드물게 입력되는 증상에는 생성형 AI(GPT)를 연동하여 전문가 수준의 안내를 제공하는<br>
홈케어형 <strong>감성 기반 AI 건강상담 에이전트</strong>입니다.<br><br>
사용자는 두통, 소화불량, 불면과 같은 흔한 증상에 대해 빠르고 직관적인 조언을 받을 수 있고,<br>
보다 세밀한 증상이나 병원 정보에 대해서는 GPT 기반의 안내를 통해 맞춤형 상담을 받을 수 있습니다.<br>
앱 전체는 병원 앱처럼 따뜻하고 안정적인 UI로 구성되어 있으며,<br>
Streamlit을 통해 구현되어 웹브라우저만 있으면 언제든지 접속하여 상담이 가능합니다.
</p>
</div>
""", unsafe_allow_html=True)

# 아래 기능 구현은 이전 코드에서 그대로 이어지도록 처리
# ... (중략) 이후 동일한 기능 처리 코드 삽입 ...
