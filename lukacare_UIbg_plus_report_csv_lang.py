
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

openai.api_key = "sk-여기에_API_키_입력"

st.set_page_config(page_title="루카케어 Mini", page_icon="❤️", layout="centered")

# UI 스타일
st.markdown("""
<style>
.stApp {
    background-image: url("https://raw.githubusercontent.com/JUN-MIN-A/lukacare-streamlit/main/lukacare_bg_final_50.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.main-box {
    background-color: rgba(255,255,255,0.9);
    padding: 1.5rem;
    border-radius: 12px;
    margin-top: 1rem;
    box-shadow: 0 0 10px rgba(0,0,0,0.08);
    color: #333333;
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

# 앱 헤더
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712103.png", width=80)
st.markdown("<h1>루카케어 Mini</h1>", unsafe_allow_html=True)
st.markdown("<h4>AI 기반 건강 관리 에이전트 – GPT 연동 & CSV 기록</h4>", unsafe_allow_html=True)

# 소개 박스
with st.container():
    st.markdown("""
    <div class='main-box'>
    <h3>앱 소개 및 기능 안내</h3>
    <p style='font-size:15px;'>
    루카케어 Mini는 감성 기반 AI 건강 에이전트입니다.<br>
    - 건강 분석 + 정서관리 + GPT 상담 지원<br>
    - 감정 기록 저장, 다국어 전환, 데일리 리포트 포함
    </p>
    </div>
    """, unsafe_allow_html=True)

# 다국어 안내
if st.checkbox("영문 모드 (English Mode)", False):
    st.info("영문 UI는 준비 중입니다. 질문을 영어로 입력하면 GPT가 응답할 수 있습니다.")

# 데이터
glucose = [95, 110, 135, 102, 99]
temperature = [36.4, 36.7, 37.1, 36.5, 36.6]
bp_data = pd.DataFrame({
    "날짜": ["6/1", "6/2", "6/3", "6/4", "6/5"],
    "수축기(mmHg)": [120, 145, 130, 128, 160],
    "이완기(mmHg)": [80, 95, 88, 82, 102]
})
emotion_log = []

preset_responses = {
    "두통": "휴식 부족이나 스트레스로 인한 일시적 두통일 수 있어요.",
    "불면": "수면 위생을 지켜보세요.",
    "우울감": "산책, 햇빛 쬐기, 대화가 도움이 됩니다."
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
    "산부인과": "미래 산부인과 02-8888-8888",
    "소아과": "행복한 소아과 02-9999-9999",
    "치과": "스마일 치과 02-1010-1010",
    "가정의학과": "가정메디 의원 02-1212-1212",
    "재활의학과": "재활케어 의원 02-1313-1313",
    "정형외과": "튼튼정형외과 02-1414-1414",
    "한의원": "편안한 한의원 02-1515-1515",
    "대학병원": "서울대학교병원 02-880-5114",
    "종합병원": "삼성서울병원 02-3410-0200",
    "지역병원": "강동경희대병원 02-440-7000",
    "보건소": "강남구보건소 02-3423-7200"
}

# 선택
option = st.radio("기능을 선택하세요", [
    "혈당 분석", "혈압 분석", "체온 분석", "정서 관리", "사전 진료", "주변 의원 연락처", "감정 기록 저장", "데일리 리포트"
])
user_input = st.text_input("질문/증상/의원 검색어")

# 실행
if st.button("실행하기"):
 if option == "혈당 분석":
        st.subheader("혈당 수치 직접 입력")
        val = st.number_input("혈당 (mg/dL)", min_value=0, step=1)
        if val > 0:
            if val < 70:
                st.error(f"{val} mg/dL – 저혈당 위험")
            elif val > 125:
                st.warning(f"{val} mg/dL – 고혈당 경고")
            else:
                st.success(f"{val} mg/dL – 정상 범위입니다.")

    elif option == "혈압 분석":
        st.subheader("혈압 수치 직접 입력")
        sys = st.number_input("수축기(mmHg)", min_value=0, step=1)
        dia = st.number_input("이완기(mmHg)", min_value=0, step=1)
        if sys > 0 and dia > 0:
            if sys >= 140 or dia >= 90:
                st.error(f"{sys}/{dia} mmHg – 고혈압 주의")
            elif sys < 90 or dia < 60:
                st.warning(f"{sys}/{dia} mmHg – 저혈압 경고")
            else:
                st.success(f"{sys}/{dia} mmHg – 정상 혈압")

    elif option == "체온 분석":
        st.subheader("체온 수치 직접 입력")
        temp = st.number_input("체온 (℃)", min_value=30.0, max_value=42.0, step=0.1)
        if temp > 0:
            if temp >= 37.5:
                st.error(f"{temp}℃ – 발열 상태입니다.")
            elif temp < 35.5:
                st.warning(f"{temp}℃ – 저체온 주의")
            else:
                st.success(f"{temp}℃ – 정상 체온")


    elif option == "정서 관리":
        st.subheader("감정 기록")
        mood = st.radio("오늘 기분?", ["좋음", "보통", "우울", "불안"])
        reason = st.text_input("이유는?")
        if reason:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            emotion_log.append({"시간": timestamp, "기분": mood, "이유": reason})
            st.dataframe(pd.DataFrame(emotion_log))

    elif option == "사전 진료":
        st.subheader("GPT 진료")
        if not user_input:
            st.warning("질문을 입력하세요")
        else:
            for k in preset_responses:
                if k in user_input:
                    st.success(preset_responses[k])
                    break
            else:
                st.write(ask_gpt(user_input))

    elif option == "주변 의원 연락처":
        st.subheader("의원 안내")
        if not user_input:
            for dept, info in clinics.items():
                st.markdown(f"- **{dept}**: {info}")
        else:
            found = [v for k, v in clinics.items() if k in user_input]
            if found:
                for f in found:
                    st.success(f)
            else:
                st.write(ask_gpt(f"{user_input} 관련 병원"))

    elif option == "감정 기록 저장":
        if emotion_log:
            df = pd.DataFrame(emotion_log)
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("감정기록 CSV 다운로드", csv, file_name="emotion_log.csv", mime="text/csv")
        else:
            st.warning("저장할 감정기록이 없습니다.")

    elif option == "데일리 리포트":
        st.subheader("AI 건강 리포트")
        summary = (
            f"- 혈당: {glucose[-1]} mg/dL\n"
            f"- 혈압: {bp_data.iloc[-1]['수축기(mmHg)']}/{bp_data.iloc[-1]['이완기(mmHg)']} mmHg\n"
            f"- 체온: {temperature[-1]} ℃\n"
            f"- 감정: {emotion_log[-1]['기분'] if emotion_log else '기록 없음'}"
        )
        st.code(summary)
