import mysql.connector
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys

conn = mysql.connector.connect( #thiết lập connect với database
    host='localhost',
    user="root",
    password='0329217749',
    database='multimedia'
)
cursor = conn.cursor() # tạo đối tượng con trỏ để thực thi câu lệnh querry

def encrypt_and_save_audio(input_audio, filename):

    with open(input_audio, 'rb') as f: # mở tệp âm thanh đầu vào và ở chế độ đọc nhị phân và lưu vào biến 'data'
        data = f.read()

        key = get_random_bytes(32)
        iv = get_random_bytes(12)

        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)# mã hóa mode GCM

        encrypted_data, auth_tag = cipher.encrypt_and_digest(data)
        #auth_tag: Thẻ xác thực, một phần của quá trình xác thực GCM,
        #được sử dụng để đảm bảo rằng dữ liệu không bị thay đổi sau khi được mã hóa.

        cursor.execute('''INSERT INTO audio (filename, encrypted_data, `key`, iv, auth_tag) VALUES (%s, %s, %s, %s, %s)''', # thực thi truy vấn sql 
                       (filename, encrypted_data, key, iv, auth_tag))
        conn.commit()

        print("Encryption and storage successful!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <audio_input> <filename>")
        sys.exit(1)
    encrypt_and_save_audio(sys.argv[1], sys.argv[2])
