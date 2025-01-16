import pyautogui
import easyocr
import time
from PIL import Image

# Khởi tạo EasyOCR Reader
reader = easyocr.Reader(['en', 'vi'])  # Bạn có thể thêm ngôn ngữ khác nếu cần

def capture_and_recognize_text():
    # Chụp ảnh màn hình
    screenshot = pyautogui.screenshot()

    # Lưu ảnh chụp màn hình (tùy chọn)
    screenshot.save('screenshot.png')

    # Xử lý ảnh
    img = Image.open('screenshot.png')

    # Sử dụng EasyOCR để nhận diện văn bản từ ảnh
    result = reader.readtext(img)

    # In văn bản nhận diện được
    print("Văn bản nhận diện được từ ảnh chụp màn hình:")
    for detection in result:
        print(detection[1])  # In ra văn bản nhận diện

# Quét hình ảnh và nhận diện văn bản mỗi 5 giây
while True:
    capture_and_recognize_text()
    time.sleep(5)  # Chờ 5 giây trước khi quét lại
