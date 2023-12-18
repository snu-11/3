import streamlit as st
import pandas as pd
import os
import koreanize_matplotlib 

# Streamlit 페이지 설정
st.set_page_config(
    page_title="직업 도감",
    page_icon="📕",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("직업 도감📕")
# 능력 및 설명이 포함된 사전 정의
skill_emoji_dict = {
    "창의": ("💡", "새롭고 독창적인 생각을 할 수 있는 능력"),
    "수리논리": ("➕", "수학적 및 논리적 문제를 해결하는 능력"),
    "사회정서": ("💗", "타인과의 관계에서 감정을 이해하고 관리하는 능력"),
    "의사소통": ("🗣️", "효과적으로 의견을 전달하고 타인의 의견을 이해하는 능력"),
    "문제해결": ("🧩", "복잡한 문제를 분석하고 해결책을 찾는 능력"),
    "리더십": ("👑", "타인을 영향력 있게 이끌고 조직의 목표를 달성하는 능력"),
    "자기관리": ("🕒", "자신의 시간과 자원을 효율적으로 관리하는 능력"),
    "팀워크": ("🤝", "다른 사람들과 협력하여 공동의 목표를 달성하는 능력"),
    "디지털 리터러시": ("💻", "디지털 언어가 구성하는 메시지를 분석할 수 있는 능력"),
    "비판적 사고": ("🔍", "정보를 분석하고 판단하는 능력"),
    "기업가정신": ("🚀", "새로운 아이디어를 사업으로 전환하고 혁신을 추구하는 능력"),
    "문화적 이해": ("🌍", "다양한 문화와 관점을 이해하고 존중하는 능력")
}

st.subheader("미래에 인기있을 직업, 새로 나타날 직업")
st.write("미래직업 참고자료(커리어넷): https://career.go.kr/cnet/front/base/guidebook/guideBookList.do")


initial_jobs = [
    {
        "name": "사물 인터넷 전문가",
        "skill": ["창의", "수리논리"],
        "image_url": "https://cdn-icons-png.flaticon.com/128/6537/6537379.png"
    },
    {
        "name":"프롬프트 개발자",
        "skill":["창의", "수리논리"],
        "image_url":"https://cdn-icons-png.flaticon.com/128/6009/6009939.png"
    },
    {
        "name": "감정인식기술전문가",
        "skill": ["의사소통", "사회정서"],
        "image_url": "https://cdn-icons-png.flaticon.com/128/5230/5230777.png",
    },
]

if "직업" not in st.session_state:
    st.session_state.jobs = initial_jobs

with st.form(key="form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(label="직업 이름")
    with col2:
        skill = st.multiselect(
            label="직업에 필요한 능력",
            options=list(skill_emoji_dict.keys()),
            format_func=lambda x: f"{skill_emoji_dict[x][0]} {x} - {skill_emoji_dict[x][1]}",
            max_selections=2
        )
    image_url = st.text_input(label="직업 이미지 URL")
    submit = st.form_submit_button(label="제출")
    if submit:
        if not name:
            st.error("직업의 이름을 입력해주세요.")
        elif len(skill) == 0:
            st.error("직업에 필요한 능력을 적어도 한개 선택해주세요.")
        else:
            st.success("직업을 추가할 수 있습니다.")
            st.session_state.jobs.append({
                "name": name,
                "skill": skill,
                "image_url": image_url if image_url else "https://cdn-icons-png.flaticon.com/128/3899/3899616.png"
            })

for i in range(0, len(st.session_state.jobs), 3):
    row_jobs = st.session_state.jobs[i:i+3]
    cols = st.columns(3)
    for j in range(len(row_jobs)):
        with cols[j]:
            job = row_jobs[j]
            with st.expander(label=f"**{i+j+1}. {job['name']}**", expanded=True):
                st.markdown(f"<div style='text-align: center;'><img src='{job['image_url']}' style='max-width: 100%; height: auto;'></div>", unsafe_allow_html=True)
                emoji_skill = [f"{skill_emoji_dict[x][0]} {x}" for x in job["skill"]]
                st.text(" / ".join(emoji_skill))
                delete_button = st.button(label="삭제", key=i+j, use_container_width=True)
                if delete_button:
                    del st.session_state.jobs[i+j]
                    st.rerun()



st.write("최종 직업 도감을 스크린샷해서 보고서에 넣어주세요:smile:")