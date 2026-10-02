import random
import time

import streamlit as st

from randselect.selector import random_selection, remaining

FLASH_SECONDS = 3.0
FLASH_INTERVAL = 0.12

st.set_page_config(page_title="Random Question Picker", page_icon="🎲")
st.title("🎲 Random Question Picker")

# --- State (survives reruns) ---
if "rng" not in st.session_state:
    st.session_state.rng = random.Random()
for key in ("names", "questions", "history"):
    if key not in st.session_state:
        st.session_state[key] = []
if "pick" not in st.session_state:
    st.session_state.pick = None
if "animate" not in st.session_state:
    st.session_state.animate = False


def add_form(label, key):
    # Text input + Add button; the submit block only mutates state.
    with st.form(f"add_{key}", clear_on_submit=True):
        entry = st.text_input(label)
        if st.form_submit_button("Add"):
            entry = entry.strip()
            if not entry:
                st.toast("Nothing to add — the box was empty.")
            elif entry in st.session_state[key]:
                st.toast(f"'{entry}' is already on the list.")
            else:
                st.session_state[key].append(entry)


def show_list(items, empty_msg):
    if items:
        st.markdown("\n".join(f"{i}. {item}" for i, item in enumerate(items, 1)))
    else:
        st.caption(empty_msg)


# --- Build roster and questions ---
col_names, col_questions = st.columns(2)
with col_names:
    st.subheader("Roster")
    add_form("Name", "names")
    show_list(st.session_state.names, "No names yet.")
with col_questions:
    st.subheader("Questions")
    add_form("Question", "questions")
    show_list(st.session_state.questions, "No questions yet.")

st.divider()

# --- Draw ---
names = st.session_state.names
questions = st.session_state.questions
history = st.session_state.history
rng = st.session_state.rng


def used_so_far():
    # Names and questions to exclude from the next draw.
    if not st.session_state.no_repeats:
        return [], []
    history = st.session_state.history
    return [n for n, _ in history], [q for _, q in history]


st.checkbox("No repeats this session", value=False, key="no_repeats")
used_names, used_questions = used_so_far()
can_draw = bool(remaining(names, used_names) and remaining(questions, used_questions))

if not names or not questions:
    st.info("Add at least one name and one question to draw.")
elif not can_draw:
    st.warning("Every name or every question has already been drawn. "
               "Add more, untick 'No repeats', or reset the history.")


# Callbacks run before the rerun, so the buttons below render with up-to-date state.
def draw():
    used_n, used_q = used_so_far()
    pick = random_selection(st.session_state.names, st.session_state.questions,
                            rng=st.session_state.rng, used_names=used_n, used_questions=used_q)
    st.session_state.pick = pick
    st.session_state.history.append(pick)
    st.session_state.animate = True


def reset_history():
    st.session_state.history = []
    st.session_state.pick = None


col_draw, col_reset = st.columns([1, 1])
with col_draw:
    st.button("Draw", type="primary", disabled=not can_draw, on_click=draw)
with col_reset:
    st.button("Reset drawn history", disabled=not history, on_click=reset_history)

# --- Render result (outside the button blocks) ---
result = st.empty()
if st.session_state.animate:
    # Clear the flag first so an interrupted animation still shows the pick.
    st.session_state.animate = False
    end = time.monotonic() + FLASH_SECONDS
    while time.monotonic() < end:
        name, question = random_selection(names, questions, rng=rng)
        result.info(f"### {name}\n{question}")
        time.sleep(FLASH_INTERVAL)

if st.session_state.pick:
    name, question = st.session_state.pick
    result.success(f"### {name}, please answer:\n{question}")

if st.session_state.history:
    with st.expander(f"Drawn so far ({len(st.session_state.history)})"):
        show_list([f"{n} — {q}" for n, q in st.session_state.history], "")
