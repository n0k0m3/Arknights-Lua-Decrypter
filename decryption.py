from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pathlib import Path
import glob, os

AES_KEY = b'8OjXUSNSi8yXC0u9'
AES_MASK = b'8mNWvh7MRLGhyEuQ'
AES_KEY_LENGTH = 16  # from il2cpp, implies AES 128 bit
AES_IV_LENGTH = 16  # CBC Mode


# aes-128-cbc encrypt
# CBC mode requires padding to have data length of multiple of 16 bytes (AES 128 block size)
def rijndaelmanaged_encrypt(data, key, iv):
    encrypt_data = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(data, AES_KEY_LENGTH))
    return encrypt_data


# aes-128-cbc decrypt
# Since encryption data is padded, naturally we want the unpad the decrypted data
def rijndaelmanaged_decrypt(data, key, iv):
    decrypt_data = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(data), AES_KEY_LENGTH)
    return decrypt_data


# TextAsset decryption, referenced from InfiniteTsukuyomi/PyAutoGame
def text_asset_decrypt(filename):
    # TextAsset uses aes-128-cbc encryption algorithm, encryption key (AES_KEY) is the first 16 bytes of CHAT_MASK
    # Note: CHAT_MASK (chatMask) is just how the concat'ed key is called in il2cpp
    with open(filename, 'rb') as file:
        # Read file data
        data = file.read()
        # XOR first 16 bytes of the encrypted file and AES_MASK
        masked_iv = data[:AES_IV_LENGTH]
        print(masked_iv)
        aes_iv = bytearray(b ^ m for (b, m) in zip(masked_iv, AES_MASK))
        print(aes_iv)
        # Decrypt the data with generated aes_iv key
        game_data = rijndaelmanaged_decrypt(data[AES_IV_LENGTH:], AES_KEY, aes_iv)
        # Save the decrypted data
        with open(filename.replace('.txt', '') + '.decrypted.json', 'wb') as fw:
            fw.write(game_data)


def text_asset_encrypt(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        # aes_iv is the first 16 bytes (characters, UTF-8 encoded) of the plaintext asset
        aes_iv = bytearray(data[:AES_IV_LENGTH])
        # Of course, aes_iv cannot be stored as plaintext, also should not be encrypted either (waste of resource),
        # so it will be XOR'ed with AES_MASK key
        masked_iv = bytearray(i ^ m for (i, m) in zip(aes_iv, AES_MASK))
        # Encrypt the data AES, we need to encrypt the whole file
        game_data_encrypted = rijndaelmanaged_encrypt(data, AES_KEY, aes_iv)
        with open(filename.replace('decrypted', 'encrypted'), 'wb') as fw:
            # Structure of the encrypted assets: Masked IV key + Encrypted text (of the whole file)
            fw.write(masked_iv + game_data_encrypted)

text_asset_decrypt('TextAsset\\HotfixBase.lua.txt')

# text_asset_decrypt('skill_table.txt')
# text_asset_encrypt('skill_table.decrypted.json')

# if __name__ == "__main__":
#     os.chdir('TextAsset')
#     for file in glob.glob("**/*.txt",recursive=True):
#         text_asset_decrypt(file)
