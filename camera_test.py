import cv2

# Webカメラのキャプチャを開始
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("エラー: カメラを開けませんでした。")
    exit()

print("カメラ起動中...'q'で終了、's'で保存")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ==========================================
    # ▼▼▼ ここから画像処理のロジックを追加 ▼▼▼
    # ==========================================
    
    # 1. 映像をグレースケール（白黒）に変換（処理を軽くするため）
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. ノイズを消すために少しぼかす
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. エッジ（線の境界）を抽出
    edges = cv2.Canny(blur, 50, 150)
    
    # 4. エッジから「輪郭」のまとまりを探し出す
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 5. 見つかった輪郭を元の映像に緑色の線で描画する
    for cnt in contours:
        # 小さすぎるゴミ（ノイズ）は無視する（面積500以上を対象）
        if cv2.contourArea(cnt) > 500:
            # 輪郭をぴったり囲む長方形（X座標, Y座標, 幅, 高さ）を計算
            x, y, w, h = cv2.boundingRect(cnt)
            # 映像に緑色の四角形を描画 (色指定は B, G, R の順なので (0, 255, 0) が緑)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # ==========================================
    # ▲▲▲ 画像処理のロジックここまで ▲▲▲
    # ==========================================

    # 処理結果の映像を表示
    cv2.imshow('Bookshelf Monitor - Prototype', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite('bookshelf_detect.jpg', frame)
        print("画像を保存しました！")

cap.release()
cv2.destroyAllWindows()
