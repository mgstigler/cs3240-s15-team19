from Crypto.Cipher import DES3

def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_file.write(des3.decrypt(chunk))

file_name = input("Please enter the file you want to decrypt: ")
dec_file = file_name[:-4]
key = input("Please enter the key to decrypt this file: ")
iv = input("Please enter the IV to decrypt this file: ")
decrypt_file(file_name, dec_file, 8192, key, iv)