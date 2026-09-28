import time

import streamlit as st

from randselect.selector import random_selection

st.session_state.setdefault("roster", [])
st.session_state.setdefault("questions", [])
st.session_state.setdefault("used_names", set())
st.session_state.setdefault("used_questions", set())
st.session_state.setdefault("last_result", None)

st.title("RandSelect")

name_col, question_col = st.columns(2)

with name_col:
    st.subheader("Roster")
    with st.form("add_name_form", clear_on_submit=True):
        name = st.text_input("Name")
        if st.form_submit_button("Add name") and name.strip():
            st.session_state.roster.append(name.strip())
    if st.session_state.roster:
        for n in st.session_state.roster:
            st.write(f"- {n}")
    else:
        st.caption("No names added yet.")

with question_col:
    st.subheader("Questions")
    with st.form("add_question_form", clear_on_submit=True):
        question = st.text_input("Question")
        if st.form_submit_button("Add question") and question.strip():
            st.session_state.questions.append(question.strip())
    if st.session_state.questions:
        for q in st.session_state.questions:
            st.write(f"- {q}")
    else:
        st.caption("No questions added yet.")

st.divider()

st.checkbox("No repeats this session", key="no_repeats")

can_draw = bool(st.session_state.roster and st.session_state.questions)

if st.button("Draw", disabled=not can_draw):
    if not can_draw:
        st.warning("Add at least one name and one question before drawing.")
    else:
        placeholder = st.empty()
        deadline = time.time() + 3.0
        while time.time() < deadline:
            flash_name, flash_question = random_selection(
                st.session_state.roster, st.session_state.questions
            )
            placeholder.markdown(f"### {flash_name} — {flash_question}")
            time.sleep(0.1)

        names_pool = st.session_state.roster
        if st.session_state.no_repeats:
            available_names = [
                n for n in names_pool if n not in st.session_state.used_names
            ]
            if available_names:
                names_pool = available_names
            else:
                st.session_state.used_names = set()

        questions_pool = st.session_state.questions
        if st.session_state.no_repeats:
            available_questions = [
                q for q in questions_pool if q not in st.session_state.used_questions
            ]
            if available_questions:
                questions_pool = available_questions
            else:
                st.session_state.used_questions = set()

        chosen_name, chosen_question = random_selection(names_pool, questions_pool)

        if st.session_state.no_repeats:
            st.session_state.used_names.add(chosen_name)
            st.session_state.used_questions.add(chosen_question)

        st.session_state.last_result = (chosen_name, chosen_question)
        placeholder.empty()

if st.session_state.last_result:
    chosen_name, chosen_question = st.session_state.last_result
    st.success(f"{chosen_name}, please answer: {chosen_question}")
