
import streamlit as st
import pandas as pd
from datetime import datetime
import openai

openai.api_key = "sk-여기에_API_키_입력"

st.set_page_config(page_title="루카케어 Mini", page_icon="❤️", layout="centered")

st.title("루카케어 Mini – 수치 입력 기반 건강 분석")

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
    "두통": "휴식 부족이나 스트레스 원인일 수 있어요.",
    "불면": "수면위생을 점검하세요.",
    "우울감": "햇볕, 산책, 대화가 도움이 됩니다."
}

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
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
