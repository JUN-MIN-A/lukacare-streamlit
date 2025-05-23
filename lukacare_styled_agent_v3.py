
import streamlit as st
import openai
import pandas as pd

# OpenAI API 키 입력
openai.api_key = "sk-여기에_API_키_입력"

# 앱 설정
st.set_page_config(
    page_title="루카케어 Mini – AI 건강상담",
    page_icon="❤️",
    layout="centered"
)

# 배경 이미지와 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1605902711622-cfb43c4437e0');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    .main-area {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .section {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 1rem;
        background-color: #ffffffdd;
        margin-bottom: 1.5rem;
    }
    h1, h2, h4 {
        color: #B45F5F;
    }
    </style>
""", unsafe_allow_html=True)

# 상단 로고 및 제목
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1 style='text-align: center;'>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>당신의 감성 기반 AI 건강상담 에이전트</h4>", unsafe_allow_html=True)

# 카드형 박스 시작
st.markdown("<div class='main-area'>", unsafe_allow_html=True)

# 증상 입력
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("사전 진료 상담")
user_input = st.text_input("증상이나 고민을 입력해주세요 (예: 두통, 불면, 소화불량 등)")
st.markdown("</div>", unsafe_allow_html=True)

# 프리셋 응답
preset_responses = {
    "두통": "휴식 부족이나 스트레스로 인한 일시적 두통일 수 있어요. 물을 충분히 마셔보세요.",
    "소화불량": "기름진 음식이나 과식이 원인이 될 수 있어요. 따뜻한 물과 가벼운 산책을 권장해요.",
    "불면": "수면 위생을 지켜보세요. 취침 전 1시간은 스마트폰 사용을 줄이는 것이 좋아요.",
    "피로": "지속되는 피로는 철분 부족, 수면 부족, 스트레스가 원인일 수 있어요.",
    "생리통": "복부를 따뜻하게 하고, 무리하지 않는 휴식이 필요해요.",
    "어지러움": "식사 불규칙, 저혈압, 과로 등이 원인일 수 있어요. 앉아서 휴식해보세요.",
    "우울감": "마음이 무거울 땐 누군가와의 대화나 가벼운 산책이 도움이 될 수 있어요."
}

def ask_gpt(symptom):
    prompt = f"사용자가 '{symptom}'이라고 했을 때, 친절한 1차 진료 전문의처럼 안내해주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 응답 출력 영역
st.markdown("<div class='section'>", unsafe_allow_html=True)
if st.button("상담받기"):
    if not user_input:
        st.warning("입력된 내용이 없어요. 예: 두통, 불면, 소화불량")
    else:
        found = False
        for keyword, reply in preset_responses.items():
            if keyword in user_input:
                st.success(f"루카의 응답: {reply}")
                found = True
                break
        if not found:
            st.info("GPT 의사와 연결 중...")
            gpt_reply = ask_gpt(user_input)
            st.write(gpt_reply)
st.markdown("</div>", unsafe_allow_html=True)

# 카드형 박스 종료
st.markdown("</div>", unsafe_allow_html=True)
