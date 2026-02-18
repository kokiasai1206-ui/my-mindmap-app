import streamlit as st
import google.generativeai as genai
import os

# ページ設定
st.set_page_config(page_title="AIマインドマップ", layout="wide")

# タイトル
st.title("🧠 AIマインドマップ・ジェネレーター")
st.write("テーマを入力すると、AIが思考を整理してマインドマップを描画します。")

# サイドバーでAPIキー設定（セキュアに入力可能）
api_key = st.sidebar.text_input("Google API Key", type="password")
if not api_key:
    # Secretsから取得を試みる（デプロイ後用）
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

# メインエリア
topic = st.text_input("マインドマップのテーマを入力（例：宇宙旅行の準備、カレーの作り方）", "")

if st.button("生成する") and topic and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash') # モデルは必要に応じて変更

        # プロンプト：Graphviz形式で出力させる
        prompt = f"""
        あなたは優秀な思考整理アシスタントです。
        ユーザーのテーマ「{topic}」について、マインドマップを作成してください。
        
        【重要】出力は必ず「GraphvizのDOT言語」のコードブロックのみにしてください。
        解説や前置きは不要です。
        
        構造のヒント:
        - 中心にテーマを置く
        - 関連するサブトピックを分岐させる
        - 色や形を使って見やすくする
        - 日本語で出力する
        """
        
        with st.spinner("AIが思考中..."):
            response = model.generate_content(prompt)
            content = response.text
            
            # コードブロック ```graphviz ... ``` を除去して中身だけ取り出す処理
            clean_dot = content.replace("```graphviz", "").replace("```dot", "").replace("```", "").strip()
            
            # 表示
            st.graphviz_chart(clean_dot)
            st.success("生成完了！")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
elif not api_key:
    st.warning("左側のサイドバーにGoogle API Keyを入力してください。")
