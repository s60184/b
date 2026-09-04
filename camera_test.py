import cv2

# Webカメラのキャプチャを開始 (0は標準のカメラ)
cap = cv2.VideoCapture(0)

# カメラが正常に開けたか確認
if not cap.isOpened():
    print("エラー: カメラを開けませんでした。")
    exit()

print("カメラを起動しました。終了するには 'q' キーを、画像を保存するには 's' キーを押してください。")

while True:
    # カメラから1フレーム読み込み
    ret, frame = cap.read()

    if not ret:
        print("エラー: フレームを読み込めませんでした。")
        break

    # 読み込んだ映像をウィンドウに表示
    cv2.imshow('Bookshelf Monitor - Prototype', frame)

    # キーボード入力を待機
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        # 'q'キーで終了
        print("終了します。")
        break
    elif key == ord('s'):
        # 's'キーで現在の映像を画像として保存
        cv2.imwrite('bookshelf_sample.jpg', frame)
        print("画像を 'bookshelf_sample.jpg' として保存しました！")

# 終了処理
cap.release()
cv2.destroyAllWindows()
