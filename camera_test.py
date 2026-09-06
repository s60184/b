import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("エラー: カメラを開けませんでした。")
    exit()

print("カメラ起動中...'q'で終了、's'で保存")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h_frame, w_frame, _ = frame.shape
    
    # 1. 本棚が映りやすいように中央付近のエリアを切り出し（ROI設定）
    # 必要に応じて比率は調整してください
    y_min, y_max = int(h_frame * 0.2), int(h_frame * 0.9)
    x_min, x_max = int(w_frame * 0.05), int(w_frame * 0.95)
    roi = frame[y_min:y_max, x_min:x_max]
    roi_h, roi_w, _ = roi.shape

    # 2. グレースケール化 ＆ エッジ検出
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # 3. 垂直投影ヒストグラムの作成（横軸Xごとの白ピクセル数を縦方向に合計）
    projection = np.sum(edges, axis=0) / 255

    # 4. ヒストグラムの「谷（隙間）」を利用して本を1冊ずつ分離する
    # エッジの量が一定値以下の場所を「本と本の境界（隙間）」とみなす
    threshold = np.max(projection) * 0.08  # 感度調整用の閾値
    
    books = []
    in_book = False
    start_x = 0

    for x in range(roi_w):
        if projection[x] > threshold and not in_book:
            in_book = True
            start_x = x
        elif projection[x] <= threshold and in_book:
            in_book = False
            end_x = x
            # 極端に狭すぎるノイズを除外し、ある程度幅があるものを「1冊」とする
            if (end_x - start_x) > 15:
                books.append((start_x, end_x))

    # 5. 検出した範囲を全体のフレーム座標に変換して緑の枠で描画
    for (start_x, end_x) in books:
        x1 = start_x + x_min
        y1 = y_min
        x2 = end_x + x_min
        y2 = y_max
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Bookshelf Monitor - Prototype', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite('bookshelf_detect.jpg', frame)
        print("画像を保存しました！")

cap.release()
cv2.destroyAllWindows()