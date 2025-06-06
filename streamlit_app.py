import streamlit as st
import google.generativeai as genai

# APIキーの設定（st.secretsから読み込む）
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("APIキーが設定されていません。")
    st.stop()

st.title("ビジネスメール作成アシスタント")

# 1. ユーザーからの入力を受け取る
st.subheader("1. メールの情報を入力してください")
to_person = st.text_input("宛名を入力", "株式会社〇〇 部長 鈴木様")
tone = st.selectbox("メールのトーンを選択", ("丁寧", "普通", "緊急度高め"))
requirements = st.text_area("伝えたいことを入力", "・明日の定例会議について\n・開始時間を1時間遅らせて、14時からに変更可能かご相談したく存じます。\n・こちらの都合で大変申し訳ございません。")

# 2. 作成ボタン
if st.button("メールを作成する"):
    if not requirements:
        st.warning("伝えたいことを入力してください。")
    else:
        # 3. AIへのプロンプトを作成
        prompt = f"""
        以下の条件に基づいて、日本のビジネス文化に合った自然なビジネスメールの本文を作成してください。

        # 条件
        - 宛名: {to_person}
        - メールのトーン: {tone}
        - 伝えたいこと: {requirements}

        # 出力形式
        件名: [ここに件名]

        [ここに本文]
        """
        
        # 4. AIを実行して結果を表示
        with st.spinner("AIがメールを作成中です..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.subheader("作成されたメールはこちらです")
            st.write(response.text)
