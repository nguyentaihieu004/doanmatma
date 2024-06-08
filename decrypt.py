from Crypto.Cipher import AES

def decrypt_audio(encrypted_data, key, iv, auth_tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    cipher.update(auth_tag)  # Cập nhật auth_tag để xác thực

    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data
