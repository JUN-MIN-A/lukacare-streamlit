
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt

# OpenAI API 키 입력
openai.api_key = "sk-여기에_API_키_입력"

# 샘플 데이터
glucose = [95, 110, 108, 102, 99]
temperature = [36.4, 36.7, 37.1, 36.5, 36.6]
bp_data = pd.DataFrame({
    "날짜": ["6/1", "6/2", "6/3", "6/4", "6/5"],
    "수축기(mmHg)": [120, 125, 130, 128, 126],
    "이완기(mmHg)": [80, 85, 88, 82, 81]
})
emotion_data = [
    {"날짜": "2024-06-01", "기분": "우울", "원인": "업무 스트레스"},
    {"날짜": "2024-06-02", "기분": "보통", "원인": "충분한 수면"},
    {"날짜": "2024-06-03", "기분": "좋음", "원인": "운동"},
]

# 사전진료 응답 함수
def get_medical_opinion(symptom):
    prompt = f"사용자의 증상: {symptom}\n친절한 1차 진료 전문의처럼 조언해주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# UI 시작
st.set_page_config(page_title="루카케어 Mini", layout="centered")
st.title("루카케어 Mini – 건강 관리 에이전트")

option = st.selectbox("기능을 선택하세요", [
    "혈당 측정 관리", "혈압 측정 관리", "체온 측정 관리",
    "정서 관리", "사전 진료", "주변 의원 연락처"
])

user_input = st.text_input("증상이나 질문을 입력해주세요 (해당되는 경우에만)")

if st.button("실행하기"):
    if option == "혈당 측정 관리":
        st.subheader("혈당 측정 그래프")
        st.line_chart(glucose)

    elif option == "혈압 측정 관리":
        st.subheader("혈압 측정 데이터")
        st.dataframe(bp_data)

    elif option == "체온 측정 관리":
        st.subheader("체온 그래프")
        st.line_chart(temperature)

    elif option == "정서 관리":
        st.subheader("정서 상태 기록")
        df = pd.DataFrame(emotion_data)
        st.dataframe(df)

    elif option == "사전 진료":
        if not user_input:
            st.warning("증상을 입력해주세요.")
        else:
            st.subheader("전문의 의견")
            opinion = get_medical_opinion(user_input)
            st.write(opinion)

    elif option == "주변 의원 연락처":
        st.subheader("추천 의원")
        st.write("서울 강남구 민들레의원: 02-123-4567")
        st.write("서울 송파구 연세건강의원: 02-234-5678")
        st.write("경기도 성남시 참편한의원: 031-111-2222")
