# from dotenv import load_dotenv
# load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ==================================================
# 1. アプリ基本設定（必ず最上部）
# ==================================================
st.set_page_config(
    page_title="専門家AIアシスタント",
    page_icon="🤖",
)

# ==================================================
# 2. APIキー確認
# ==================================================
if "OPENAI_API_KEY" not in os.environ:
    st.error("OPENAI_API_KEY が設定されていません。Streamlit CloudのSecretsに登録してください。")
    st.stop()

# ==================================================
# 3. セッション初期化（Cloud対策）
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 専門家AIアシスタント")

st.markdown("""
## 📌 アプリ概要
このWebアプリでは、入力した質問をAIに渡し、
選択した専門家として回答を生成します。

## 🛠 操作方法
1. ラジオボタンで専門家を選択  
2. 質問を入力  
3. 「送信」ボタンをクリック  
4. AIの回答が表示されます  
""")

# ==================================================
# 4. LLM呼び出し関数
# ==================================================
def generate_response(user_input: str, expert_type: str) -> str:

    if expert_type == "A：マーケティング専門家":
        system_message = """
あなたは一流のマーケティング専門家です。
市場分析、顧客心理、ブランディング戦略の観点から
実践的で具体的なアドバイスを提供してください。
"""
    elif expert_type == "B：エンジニア専門家":
        system_message = """
あなたは優秀なソフトウェアエンジニアです。
技術的観点から論理的かつ具体的に説明してください。
必要に応じてコード例も提示してください。
"""
    else:
        system_message = "あなたは優秀なアシスタントです。"

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input)
    ]

    response = llm.invoke(messages)
    return response.content


# ==================================================
# 5. UI
# ==================================================
expert_choice = st.radio(
    "専門家を選択してください：",
    ["A：マーケティング専門家", "B：エンジニア専門家"]
)

user_text = st.text_area("✏️ 質問を入力してください")

if st.button("送信"):
    if user_text.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが回答中です..."):
            try:
                result = generate_response(user_text, expert_choice)
                st.success("✅ 回答")
                st.write(result)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")