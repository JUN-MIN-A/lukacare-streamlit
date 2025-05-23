
import streamlit as st
import openai
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="루카케어 Mini – 건강상담 에이전트",
    page_icon="❤️",
    layout="centered"
)

# 스타일 적용 (병원 앱 + 따뜻한 톤)
st.markdown("""
    <style>
    body {
        background-color: #FFF8F0;
        color: #4B3F33;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2 {
        color: #B45F5F;
    }
    .stButton>button {
        background-color: #F7CAC9;
        color: #4B3F33;
        border-radius: 8px;
        height: 2.5em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# API 키 입력 (배포 시 GitHub secret 연동 가능)
openai.api_key = "sk-여기에_API_키_입력"

# 프리셋 응답 딕셔너리
preset_responses = {
    "두통": "휴식 부족이나 스트레스로 인한 일시적 두통일 수 있어요. 물을 충분히 마셔보세요.",
    "소화불량": "기름진 음식이나 과식이 원인이 될 수 있어요. 따뜻한 물과 가벼운 산책을 권장해요.",
    "불면": "수면 위생을 지켜보세요. 취침 전 1시간은 스마트폰 사용을 줄이는 것이 좋아요.",
    "피로": "지속되는 피로는 철분 부족, 수면 부족, 스트레스가 원인일 수 있어요.",
    "생리통": "복부를 따뜻하게 하고, 무리하지 않는 휴식이 필요해요.",
    "어지러움": "식사 불규칙, 저혈압, 과로 등이 원인일 수 있어요. 앉아서 휴식해보세요.",
    "우울감": "마음이 무거울 땐 누군가와의 대화나 가벼운 산책이 도움이 될 수 있어요."
}

# GPT 응답 함수
def ask_gpt(symptom):
    prompt = f"사용자가 '{symptom}'이라고 했을 때, 친절한 1차 진료 전문의처럼 안내해주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 상단 UI
st.title("루카케어 Mini")
st.markdown("**홈케어에 어울리는 AI 건강상담 에이전트입니다.**")
st.markdown("가벼운 증상은 직접 안내해드리고, 복잡하거나 전문적인 내용은 GPT 의사에게 연결됩니다.")

# 탭 구성
tab1, tab2 = st.tabs(["건강 상담하기", "기록 보기"])

with tab1:
    user_input = st.text_input("증상이나 고민을 입력해보세요 (예: 두통, 불면 등)")
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

with tab2:
    st.markdown("곧 사용자 기록 기능이 추가될 예정입니다. 감사합니다!")
