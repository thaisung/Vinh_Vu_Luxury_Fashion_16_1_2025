import os
import requests
import re

# Đường dẫn URL cần gửi yêu cầu
url = "https://cuongpopauth.com/"

# Gửi yêu cầu HTTP để lấy mã HTML từ trang web
try:
    response = requests.get(url)
    response.raise_for_status()  # Kiểm tra lỗi HTTP
    html_code = response.text  # Lấy mã HTML trả về
    print("Lấy mã HTML thành công!")
except requests.exceptions.RequestException as e:
    print(f"Đã xảy ra lỗi khi gửi yêu cầu đến {url}: {e}")
    html_code = ""

# Regex patterns để tìm URL của các tệp CSS và JS
css_pattern = r'href="(https?://.*?\.css)(?:\?[^"]*)?"'
js_pattern = r'src="(https?://.*?\.js)(?:\?[^"]*)?"'

# Tìm các URL CSS và JS trong mã HTML
css_files = re.findall(css_pattern, html_code)
js_files = re.findall(js_pattern, html_code)

# Kết hợp các URL CSS và JS thành một danh sách
urls = css_files + js_files

# Hiển thị danh sách URL
print("Danh sách URL:", urls)

# Thư mục lưu trữ tệp CSS và JS
save_dir = "downloaded_files_home"
os.makedirs(save_dir, exist_ok=True)

# Hàm tải tệp
def download_file(url, save_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi khi tải tệp
        
        # Lấy tên tệp từ URL (loại bỏ các tham số query string)
        file_name = os.path.join(save_dir, url.split("/")[-1].split("?")[0])
        
        # Lưu tệp vào thư mục
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"Tệp {file_name} đã được tải về.")
    except requests.exceptions.RequestException as e:
        print(f"Không thể tải tệp từ {url}. Lỗi: {e}")

# Tải từng tệp trong danh sách URL
for url in urls:
    download_file(url, save_dir)
