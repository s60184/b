import streamlit as st
import cv2
import sqlite3
import pandas as pd
from datetime import datetime

# ==========================================
# 1. バックエンド担当領域 (データベース設定)
# ==========================================
def init_db():
    conn = sqlite3.connect('bookshelf.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, book_count INTEGER)''')
    conn.commit()
    return conn

# ==========================================
# 2. 画像処理担当領域 (本棚の検知)
# ==========================================
def detect_books(frame):
    # ※ここは一旦シンプルな輪郭抽出にしています。後でヒストグラム法などに差し替えます。
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    book_count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 2000:  # ノイズ除外
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            book_count += 1
            
    return frame, book_count

# ==========================================
# 3. UI・データ分析担当領域 (画面表示とグラフ化)
# ==========================================
st.title("📚 本棚在庫管理システム (Prototype)")

conn = init_db()

# サイドバーに操作ボタンを配置
st.sidebar.header("コントロールパネル")
if st.sidebar.button("📷 カメラで在庫を確認"):
    # Webカメラを起動して1枚撮影
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # 画像処理ロジックを呼び出し
        processed_frame, count = detect_books(frame)
        
        # データベースに記録
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = conn.cursor()
        c.execute("INSERT INTO inventory (timestamp, book_count) VALUES (?, ?)", (now, count))
        conn.commit()
        
        # 画面に画像と成功メッセージを表示 (OpenCVはBGR、StreamlitはRGBなので変換)
        st.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), caption=f"検知結果: {count}冊")
        st.success(f"{now} に {count}冊のデータを保存しました！")
    else:
        st.error("カメラからの映像取得に失敗しました。")

st.write("---")
st.subheader("📊 在庫データの推移")

# データベースからデータを取得してグラフ化
df = pd.read_sql_query("SELECT * FROM inventory", conn)

if not df.empty:
    # データフレーム（表）の表示
    st.dataframe(df.tail(5)) 
    
    # 折れ線グラフの表示
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    st.line_chart(df['book_count'])
else:
    st.info("まだデータがありません。左側のボタンからカメラを起動してください。")