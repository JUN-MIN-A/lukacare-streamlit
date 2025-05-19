
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

# 스타일 커스터마이징 (따뜻한 홈케어 톤)
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
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 앱 제목 및 설명
st.title("루카케어 Mini – 건강 관리 에이전트")
with st.expander("앱 소개"):
    st.markdown("- 이 앱은 감성 기반 건강 관리 에이전트입니다.")
    st.markdown("- 혈당, 혈압, 체온, 정서 상태, 사전 진료 의견 등을 제공합니다.")
    st.markdown("- 생성형 AI를 통해 상담과 해석 기능을 함께 지원합니다.")

# 기능 선택
option = st.selectbox("기능을 선택하세요", [
    "혈당 측정 관리", "혈압 측정 관리", "체온 측정 관리",
    "정서 관리", "사전 진료", "주변 의원 연락처"
])
user_input = st.text_input("증상이나 질문을 입력해주세요 (해당되는 경우에만)")

# 샘플 데이터
glucose = [95, 110, 135, 102, 99]
temperature = [36.4, 36.7, 37.1, 36.5, 36.6]
bp_data = pd.DataFrame({
    "날짜": ["6/1", "6/2", "6/3", "6/4", "6/5"],
    "수축기(mmHg)": [120, 145, 130, 128, 160],
    "이완기(mmHg)": [80, 95, 88, 82, 102]
})
emotion_log = []

# 의사 GPT 응답
def get_medical_opinion(symptom):
    prompt = f"사용자의 증상: {symptom}\n친절한 1차 진료 전문의처럼 조언해주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 실행 버튼
if st.button("실행하기"):
    st.markdown("---")

    if option == "혈당 측정 관리":
        st.subheader("혈당 측정 결과")
        st.line_chart(glucose)
        last_value = glucose[-1]
        if last_value < 70:
            st.warning("저혈당 주의! 간단한 탄수화물 섭취가 필요할 수 있어요.")
        elif last_value > 125:
            st.error("고혈당 주의! 식단/운동 조절이 필요해요.")
        else:
            st.success("정상 범위에 있습니다. 잘 유지하고 계세요!")

    elif option == "혈압 측정 관리":
        st.subheader("혈압 측정 데이터")
        st.dataframe(bp_data)
        high = bp_data[bp_data["수축기(mmHg)"] > 140]
        if not high.empty:
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
            opinion = get_medical_opinion(user_input)
            st.write(opinion)
        else:
            st.warning("증상을 입력해주세요.")

    elif option == "주변 의원 연락처":
        st.subheader("추천 의원")
        st.write("- 서울 강남구 민들레의원: 02-123-4567")
        st.write("- 서울 송파구 연세건강의원: 02-234-5678")
        st.write("- 경기도 성남시 참편한의원: 031-111-2222")
