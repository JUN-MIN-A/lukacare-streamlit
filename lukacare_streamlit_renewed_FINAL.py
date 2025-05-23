
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt

# OpenAI API 키 설정
openai.api_key = "sk-여기에_API_키_입력"

# 페이지 설정
st.set_page_config(
    page_title="루카케어 Mini – 건강 관리 에이전트",
    page_icon="❤️",
    layout="centered"
)

# 스타일 및 배경 이미지 적용
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1605902711622-cfb43c4437e0');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    .main-box {
        background-color: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    h1, h2, h4 {
        color: #B45F5F;
    }
    .stButton>button {
        background-color: #F7CAC9;
        color: #4B3F33;
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 상단 제목
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1 style='text-align: center;'>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>AI 기반 건강 관리 에이전트</h4>", unsafe_allow_html=True)
st.markdown("<div class='main-box'>", unsafe_allow_html=True)

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

# GPT 응답
def get_medical_opinion(symptom):
    prompt = f"사용자의 증상: {symptom}\n친절한 1차 진료 전문의처럼 조언해주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 기본 데이터
glucose = [95, 110, 135, 102, 99]
temperature = [36.4, 36.7, 37.1, 36.5, 36.6]
bp_data = pd.DataFrame({
    "날짜": ["6/1", "6/2", "6/3", "6/4", "6/5"],
    "수축기(mmHg)": [120, 145, 130, 128, 160],
    "이완기(mmHg)": [80, 95, 88, 82, 102]
})
emotion_log = []

# 기능 선택
option = st.selectbox("기능을 선택하세요", [
    "혈당 측정 관리", "혈압 측정 관리", "체온 측정 관리",
    "정서 관리", "사전 진료", "주변 의원 연락처"
])
user_input = st.text_input("증상이나 질문을 입력해주세요 (해당되는 경우에만)")

# 실행
if st.button("실행하기"):
    st.markdown("---")

    if option == "혈당 측정 관리":
        st.subheader("혈당 측정 결과")
        st.line_chart(glucose)
        last = glucose[-1]
        if last < 70:
            st.warning("저혈당 주의! 간단한 탄수화물 섭취가 필요할 수 있어요.")
        elif last > 125:
            st.error("고혈당 주의! 식단/운동 조절이 필요해요.")
        else:
            st.success("정상 범위에 있습니다. 잘 유지하고 계세요!")

    elif option == "혈압 측정 관리":
        st.subheader("혈압 측정 데이터")
        st.dataframe(bp_data)
        if (bp_data["수축기(mmHg)"] > 140).any():
            st.warning("수축기 혈압이 높은 기록이 있어요. 정기적 관리가 필요합니다.")

    elif option == "체온 측정 관리":
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
        if user_input:
            for key in preset_responses:
                if key in user_input:
                    st.success(f"루카의 응답: {preset_responses[key]}")
                    break
            else:
                st.info("GPT 의사와 연결 중...")
                st.write(get_medical_opinion(user_input))
        else:
            st.warning("증상을 입력해주세요.")

    elif option == "주변 의원 연락처":
        st.subheader("진료과별 추천 의원")
        clinic_info = {
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
        for dept, info in clinic_info.items():
            st.markdown(f"- **{dept}**: {info}")

# 닫는 div
st.markdown("</div>", unsafe_allow_html=True)
