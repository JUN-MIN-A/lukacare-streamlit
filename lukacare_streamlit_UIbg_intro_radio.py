
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

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/minahjeon/lukacare-streamlit/main/lukacare_bg_transparent.jpg");
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

st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4>AI 기반 건강 관리 에이전트 – 챗봇 & GPT 자동 연결</h4>", unsafe_allow_html=True)

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

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
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

# 측정값 샘플
glucose = [95, 110, 135, 102, 99]
temperature = [36.4, 36.7, 37.1, 36.5, 36.6]
bp_data = pd.DataFrame({
    "날짜": ["6/1", "6/2", "6/3", "6/4", "6/5"],
    "수축기(mmHg)": [120, 145, 130, 128, 160],
    "이완기(mmHg)": [80, 95, 88, 82, 102]
})
emotion_log = []

# 기능 선택을 목록형으로
option = st.radio("기능을 선택하세요", [
    "혈당 분석", "혈압 분석", "체온 분석",
    "정서 관리", "사전 진료", "주변 의원 연락처"
])
user_input = st.text_input("증상/질환/문의 입력")

# 실행
if st.button("실행하기"):
    if option == "혈당 분석":
        st.subheader("혈당 분석 결과")
        st.line_chart(glucose)
        last = glucose[-1]
        if last < 70:
            st.warning("저혈당 주의! 탄수화물 섭취가 필요할 수 있어요.")
        elif last > 125:
            st.error("고혈당 주의! 식단/운동 조절이 필요해요.")
        else:
            st.success("정상 범위입니다. 잘 유지하고 계세요!")

    elif option == "혈압 분석":
        st.subheader("혈압 측정 결과")
        st.dataframe(bp_data)
        if (bp_data["수축기(mmHg)"] > 140).any():
            st.warning("수축기 혈압이 높은 기록이 있어요. 정기적 관리가 필요합니다.")

    elif option == "체온 분석":
        st.subheader("체온 변화")
        st.line_chart(temperature)
        if max(temperature) >= 37.5:
            st.error("발열 의심 증상이 있습니다. 휴식과 수분 보충이 필요해요.")
        else:
            st.success("체온이 안정적으로 유지되고 있어요.")

    elif option == "정서 관리":
        st.subheader("오늘의 감정 기록")
        mood = st.radio("오늘 기분은 어떤가요?", ["좋음", "보통", "우울", "지침", "불안"])
        reason = st.text_input("그 기분의 이유는 무엇인가요?")
        if reason:
            emotion_log.append({"기분": mood, "이유": reason})
            df = pd.DataFrame(emotion_log)
            st.dataframe(df)

    elif option == "사전 진료":
        st.subheader("전문의 의견")
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
                st.info("GPT 연결 중...")
                st.write(ask_gpt(f"{user_input} 진료 가능한 병원을 추천해주세요."))

