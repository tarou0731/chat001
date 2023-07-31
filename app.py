
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# 設定
system_prompt = st.secrets.AppSettings.chatbot_setting

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("対話型ゲーム")
st.image("11_rpg.png")
st.write("対話型営業ゲームです。行動回数は10回。0になる前に生命保険契約を結んでください。")
st.write("相手の名前は鈴木太郎。４０歳メーカー勤務、既婚男性、子供２人（６歳男の子と４歳男の子）")
st.write("あなたは生命保険の営業担当者です。")
st.write("第一声は、必ず「あなたは生命保険の営業担当であること」や「生命保険の話をしたいこと」など、生命保険に触れる話をしてください")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
