import streamlit as st
import pandas as pd
import random

# --- データ読み込み ---
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFIKs64-EmxSEdNTWwqiOdmH3A7S-xF2YyJsim1_TOabIHjYQ0poefEImHnM9nNclklfQVVBTMQgp0/pub?output=csv"
df = pd.read_csv(URL)

families = sorted(df["family"].unique())
TOTAL = 20

# --- セッション状態 初期化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "quiz" not in st.session_state:
    st.session_state.quiz = df.sample(TOTAL).reset_index(drop=True)
if "choices" not in st.session_state:
    st.session_state.choices = []

# --- 全問終了 ---
if st.session_state.current_q >= TOTAL:
    st.title("結果")
    st.write(f"{TOTAL}問中 {st.session_state.score}問正解！")

    if st.button("もう一度やる"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.quiz = df.sample(TOTAL).reset_index(drop=True)
        st.session_state.choices = []
        st.rerun()

    st.stop()


# --- 現在の問題 ---
plant = st.session_state.quiz.iloc[st.session_state.current_q]
name = plant["name"]
answer = plant["family"]

st.title(f"第 {st.session_state.current_q + 1} 問")
st.write(f"🌿 植物名：**{name}**")


# --- 選択肢生成（初回だけ）
if len(st.session_state.choices) == 0:
    wrong = random.sample([f for f in families if f != answer], 3)
    st.session_state.choices = wrong + [answer]
    random.shuffle(st.session_state.choices)

choices = st.session_state.choices

# --- 回答フォーム ---
user_answer = st.radio("何科でしょう？", choices, key=f"q_{st.session_state.current_q}")

# --- 回答ボタン ---
if not st.session_state.answered:
    if st.button("回答する"):
        if user_answer == answer:
            st.success("正解！🟢")
            st.session_state.score += 1
        else:
            st.error(f"❌ 不正解！ 正解は **{answer}**")

        st.session_state.answered = True

# --- 次へ ---
if st.session_state.answered:
    if st.button("次へ →"):
        st.session_state.current_q += 1
        st.session_state.answered = False
        st.session_state.choices = []  # 次の問題で新しい選択肢生成
        st.rerun()
