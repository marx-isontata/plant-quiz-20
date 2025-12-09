import streamlit as st
import pandas as pd
import random

# --- データ読み込み ---
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFIKs64-EmxSEdNTWwqiOdmH3A7S-xF2YyJsim1_TOabIHjYQ0poefEImHnM9nNclklfQVVBTMQgp0/pub?output=csv"
df = pd.read_csv(URL)

# ユニークな科名リスト
families = sorted(df["family"].unique())
TOTAL = 20  # 出題数

# --- セッション状態 初期化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "quiz" not in st.session_state:
    # 最初に20問ぶんを抽選して、固定しておく
    st.session_state.quiz = df.sample(TOTAL).reset_index(drop=True)

# --- 全問終了 ---
if st.session_state.current_q >= TOTAL:
    st.title("結果")
    st.write(f"{TOTAL}問中 {st.session_state.score}問正解！")

    if st.button("もう一度やる"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.quiz = df.sample(TOTAL).reset_index(drop=True)
        st.rerun()  # 最初の問題からやり直し

    st.stop()

# --- 現在の問題を取得 ---
plant = st.session_state.quiz.iloc[st.session_state.current_q]
name = plant["name"]
answer = plant["family"]

st.title(f"第 {st.session_state.current_q + 1} 問")
st.write(f"🌿 植物名：**{name}**")

# --- 選択肢作成（正解除外して3つランダム＋正解で4択） ---
wrong = random.sample([f for f in families if f != answer], 3)
choices = wrong + [answer]
random.shuffle(choices)

# --- 回答フォーム ---
user_answer = st.radio("何科でしょう？", choices, index=None)

# 回答ボタンが押されたとき
if not st.session_state.answered:
    if st.button("回答する"):
        if user_answer is None:
            st.warning("選択肢を選んでから『回答する』を押してください。")
        else:
            st.session_state.answered = True
            if user_answer == answer:
                st.success("正解〇！")
                st.session_state.score += 1
            else:
                st.error(f"不正解× 正解は **{answer}**")

# 『次へ』ボタンでのみ次の問題へ進む
if st.session_state.answered:
    if st.button("次へ"):
        st.session_state.current_q += 1
        st.session_state.answered = False
        st.rerun()
