import streamlit as st
import pandas as pd
import random

# --- データ読み込み ---
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFIKs64-EmxSEdNTWwqiOdmH3A7S-xF2YyJsim1_TOabIHjYQ0poefEImHnM9nNclklfQVVBTMQgp0/pub?output=csv"
df = pd.read_csv(URL)

# ユニークな科名リスト
families = sorted(df["family"].unique())

# --- セッション状態(問題番号・点数)を初期化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0

TOTAL = 20  # 出題数

# --- 全問終了 ---
if st.session_state.current_q >= TOTAL:
    st.title("📊 結果")
    st.write(f"{TOTAL}問中 {st.session_state.score}問正解！")
    
    if st.button("もう一度やる"):
        st.session_state.current_q = 0
        st.session_state.score = 0
    
    st.stop()

# --- 1問取得 ---
plant = df.sample(1).iloc[0]
name = plant["name"]
answer = plant["family"]

st.title(f"第 {st.session_state.current_q + 1} 問")
st.write(f"🌿 植物名：**{name}**")

# --- 誤答選択肢を作る ---
choices = random.sample(families, 3)  # 適当に3つ
if answer not in choices:
    # 正解を含める
    choices.append(answer)

random.shuffle(choices)

# --- 回答フォーム ---
user_answer = st.radio("何科でしょう？", choices)

if st.button("回答する"):
    if user_answer == answer:
        st.success("正解！🌈")
        st.session_state.score += 1
    else:
        st.error(f"残念… 正解は **{answer}**")

    st.session_state.current_q += 1
    st.experimental_rerun()
