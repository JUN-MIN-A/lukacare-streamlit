
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from openai import OpenAI
client = OpenAI(api_key="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")

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

# 상태 저장 초기화
for key in ["glucose_log", "bp_log", "temp_log", "emotion_log"]:
    if key not in st.session_state:
        st.session_state[key] = []

option = st.radio("기능 선택", [
    "혈당 분석", "혈압 분석", "체온 분석", "정서 관리",
    "사전 진료", "주변 의원 연락처", "감정 기록 저장", "데일리 리포트"
])
user_input = st.text_input("질문/증상/검색어")

clinics = {
    "내과": "서울 내과의원 02-1111-1111", "외과": "튼튼 외과의원",
    "안과": "밝은눈 안과", "피부과": "더마인 피부과", "정신과": "마음편한 정신과",
    "소아과": "행복한 소아과", "산부인과": "미래 산부인과", "정형외과": "튼튼정형외과",
    "치과": "스마일 치과", "이비인후과": "숨편한 이비인후과", "대학병원": "서울대병원",
    "종합병원": "삼성서울병원", "보건소": "강남구보건소"
}

preset_responses = {
# CSV 파일 로드
df = pd.read_csv("루카케어_증상목록_진료과태그-1.csv", encoding="utf-8-sig")

# 증상 ➝ 즉각 반응 딕셔너리
preset_responses = dict(zip(df["증상"], df["응답"]))

# 증상 ➝ 진료과 추천 딕셔너리
clinic_recommend = dict(zip(df["증상"], df["진료과"]))
}
def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 혈당 분석
if option == "혈당 분석":
    val = st.number_input("혈당 (mg/dL)", min_value=0, step=1, key="glucose_input")
    if val > 0:
        if len(st.session_state["glucose_log"]) == 0 or st.session_state["glucose_log"][-1] != val:
            st.session_state["glucose_log"].append(val)

        if val < 70:
            st.error(f"{val} mg/dL – 저혈당 위험")
        elif val > 125:
            st.warning(f"{val} mg/dL – 고혈당 경고")
        else:
            st.success(f"{val} mg/dL – 정상 범위입니다.")

        st.line_chart(st.session_state["glucose_log"])

# 혈압 분석
elif option == "혈압 분석":
    sys = st.number_input("수축기(mmHg)", min_value=0, step=1, key="sys_input")
    dia = st.number_input("이완기(mmHg)", min_value=0, step=1, key="dia_input")
    if sys > 0 and dia > 0:
        last = st.session_state["bp_log"][-1] if st.session_state["bp_log"] else (0, 0)
        if (sys, dia) != last:
            st.session_state["bp_log"].append((sys, dia))

        if sys >= 140 or dia >= 90:
            st.error(f"{sys}/{dia} mmHg – 고혈압 주의")
        elif sys < 90 or dia < 60:
            st.warning(f"{sys}/{dia} mmHg – 저혈압 주의")
        else:
            st.success(f"{sys}/{dia} mmHg – 정상 혈압입니다.")

        df = pd.DataFrame(st.session_state["bp_log"], columns=["수축기", "이완기"])
        st.line_chart(df)

# 체온 분석
elif option == "체온 분석":
    temp = st.number_input("체온 (℃)", min_value=30.0, max_value=42.0, step=0.1, key="temp_input")
    if temp > 0:
        if len(st.session_state["temp_log"]) == 0 or st.session_state["temp_log"][-1] != temp:
            st.session_state["temp_log"].append(temp)

        if temp >= 37.5:
            st.error(f"{temp}℃ – 발열 상태")
        elif temp < 35.5:
            st.warning(f"{temp}℃ – 저체온 주의")
        else:
            st.success(f"{temp}℃ – 정상 체온입니다.")

        st.line_chart(st.session_state["temp_log"])

# 정서 관리
elif option == "정서 관리":
    mood = st.radio("오늘 기분은?", ["좋음", "보통", "우울", "불안"])
    reason = st.text_input("이유는?")
    if reason:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state["emotion_log"].append({"시간": ts, "기분": mood, "이유": reason})
        st.dataframe(pd.DataFrame(st.session_state["emotion_log"]))

# 사전 진료
elif option == "사전 진료":
    if not user_input:
        st.warning("질문을 입력해주세요.")
    else:
        for k in preset_responses:
            if k in user_input:
                st.success(preset_responses[k])
                break
        else:
            st.write(ask_gpt(user_input))

# 주변 의원
elif option == "주변 의원 연락처":
    if not user_input:
        for dept, tel in clinics.items():
            st.markdown(f"- **{dept}**: {tel}")
    else:
        match = [tel for k, tel in clinics.items() if k in user_input]
        if match:
            for tel in match:
                st.success(tel)
        else:
            st.write(ask_gpt(f"{user_input} 관련 병원 알려줘"))

# 감정 저장
elif option == "감정 기록 저장":
    if st.session_state["emotion_log"]:
        df = pd.DataFrame(st.session_state["emotion_log"])
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("감정기록 CSV 다운로드", csv, file_name="emotion_log.csv", mime="text/csv")
    else:
        st.warning("감정 기록이 없습니다.")

# 데일리 리포트
elif option == "데일리 리포트":
    report = ""
    if st.session_state["glucose_log"]:
        report += f"- 혈당: {st.session_state['glucose_log'][-1]} mg/dL\n"
    else:
        report += "- 혈당: 없음\n"
    if st.session_state["bp_log"]:
        sys, dia = st.session_state["bp_log"][-1]
        report += f"- 혈압: {sys}/{dia} mmHg\n"
    else:
        report += "- 혈압: 없음\n"
    if st.session_state["temp_log"]:
        report += f"- 체온: {st.session_state['temp_log'][-1]} ℃\n"
    else:
        report += "- 체온: 없음\n"
    if st.session_state["emotion_log"]:
        report += f"- 감정: {st.session_state['emotion_log'][-1]['기분']}"
    else:
        report += "- 감정: 기록 없음"
    st.code(report)
