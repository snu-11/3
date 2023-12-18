import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import koreanize_matplotlib 
from docx import Document
from io import BytesIO

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# Streamlit 페이지 설정
st.set_page_config(
    page_title="미래 직업 예측 보고서",
    page_icon="./image/job.png",
    layout="centered",
    initial_sidebar_state="auto"
)

def create_word_document(thoughts):
    doc = Document()
    doc.add_heading('Student Thoughts', 0)
    for thought in thoughts:
        doc.add_paragraph(thought)
        doc.add_paragraph()  # Add a blank paragraph for spacing
    return doc

# Streamlit 앱의 제목 설정
st.title("미래 직업 예측 보고서")

st.divider()

# 오늘 배울 내용
st.subheader("학습목표 :book:")
st.write(":blue[[사회]] 변화하는 직업세계를 이해하고, 자신의 진로를 스스로 설계해 갈 수 있다.")
st.write(":blue[[정보]] 필요한 데이터를 찾고, 데이터를 파악하고, 데이터에 기반하여 의사결정을 할 수 있다.")
st.write(":blue[[수학]] 공학적 도구를 이용하여 정보 데이터를 그래프로 나타내고, 그래프의 의미를 해석할 수 있다.")

st.divider()
st.caption(":blue_heart:복습해 보자!")
st.subheader("세상에는 어떤 직업이 있을까?")
st.video('https://www.youtube.com/watch?v=nnUIz_TbznA', format="video/mp4", start_time=0)

st.divider()

st.caption(":blue_heart:선생님 강의")
st.subheader("고용과 관련하여 필요한 데이터는 어디에서 찾을 수 있을까?")
st.write(":gray[고용노동통계: http://laborstat.moel.go.kr/]")
st.write(":gray[한국노동패널: https://www.kli.re.kr/klips/]")

st.divider()
st.subheader("시간이 지나면서 각 직업 별로 어떤 변화가 있었을까?")
st.write(":gray[자료출처: 고용노동통계]")

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=0, index_col=0)
    df.index = pd.to_numeric(df.index, errors='coerce')
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    st.success('파일 업로드 성공!')

    occupations = df.columns.tolist()
    selected_occupation = st.selectbox("직업 선택:", occupations)

    # 연도 범위 설정 시 정수 변환 적용
    start_year = st.slider("시작 연도:", min_value=int(df.index.min()), max_value=int(df.index.max()) - 1, value=int(df.index.min()))
    end_year = st.slider("끝 연도:", min_value=start_year + 1, max_value=int(df.index.max()), value=int(df.index.max()))

    filtered_df = df.loc[start_year:end_year, [selected_occupation]]

    st.subheader(f"{selected_occupation}의 {start_year}에서 {end_year}까지의 변화📈")
    fig, ax = plt.subplots()
    filtered_df.plot(ax=ax, marker='o')
    plt.xlabel("연도")
    plt.ylabel(selected_occupation)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xticks(filtered_df.index)
    ax.set_xticklabels(filtered_df.index.astype(int), fontsize=8, rotation=45)
    st.pyplot(fig)

    st.subheader("전체 연도와 선택한 직업에 대한 데이터 시각화📈")
    selected_occupations = st.multiselect("직업 선택:", occupations, default=[selected_occupation])

    if selected_occupations:
        selected_df = df.loc[start_year:end_year, selected_occupations]
        fig, ax = plt.subplots()
        selected_df.plot(ax=ax, marker='o')
        plt.xlabel("연도")
        plt.ylabel("값")
        ax.set_xticks(selected_df.index)
        ax.set_xticklabels(selected_df.index.astype(int), fontsize=8, rotation=45)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        st.pyplot(fig)

st.divider()

st.subheader("시간에 따라 직업에 어떤 변화가 있었나요?")
student_thought = st.text_area("그래프를 통해 발견한 내용을 적어주세요🖊️")

# Initialize an empty DataFrame for student thoughts outside the button click condition
if 'student_thoughts_df' not in st.session_state:
    st.session_state.student_thoughts_df = pd.DataFrame({'학생 생각': []})

# When the button is clicked
if st.button("제출", key="submit_button"):
    # Append the new thought to the DataFrame
    new_thought = {'학생 생각': student_thought}
    st.session_state.student_thoughts_df = st.session_state.student_thoughts_df.append(new_thought, ignore_index=True)
    st.session_state.student_thoughts_df.to_csv('student_thoughts.csv', index=False, encoding='utf-8')

    # Display the submitted thought
    st.subheader("나의 생각")
    st.write(student_thought)

    # Create a Word document with the student thoughts
    student_thoughts = st.session_state.student_thoughts_df['학생 생각'].tolist()
    doc = create_word_document(student_thoughts)

    # Save the document to a BytesIO object
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Create a download button for the document
    st.download_button(
        label="나의 생각 다운로드",
        data=buffer,
        file_name="student_thoughts.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


st.divider()

st.caption(":blue_heart:오늘의 과제")
st.subheader("나에게 중요한 가치는 무엇일지, 이를 찾기 위한 '질문'이 무엇일지 고민하기")
st.caption("예) 돈이 중요해. 어떤 직종이 돈을 많이 벌까? (임금 데이터 활용)")
st.caption("예) 워라벨이 중요해. 어떤 직종이 업무시간이 적고, 휴식시간이 많을까? (업무 시간, 휴식 시간 등 근무 시간 데이터 활용)")
