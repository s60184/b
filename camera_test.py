import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("エラー: カメラを開けませんでした。")
    exit()

print("カメラ起動中...'q'で終了、's'で保存")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. 画像処理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # ★ 閾値を少し広めに調整 (30, 100に変更)
    edges = cv2.Canny(blur, 30, 100)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        # ★ 面積のハードルを 500 から 100 に下げて、小さなものも検知しやすくする
        if cv2.contourArea(cnt) > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 映像を表示
    cv2.imshow('Bookshelf Monitor - Prototype', frame)
    
    # ★ エッジ（白黒の線）がどう見えているか確認用の小窓を追加
    cv2.imshow('Edges Check', edges)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite('bookshelf_detect.jpg', frame)
        print("画像を保存しました！")

cap.release()
cv2.destroyAllWindows()
