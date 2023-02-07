import base64
from Crypto.Cipher import AES


class aes:
    '''
    -----------------------------------------------------------------------------------
    - 处理使用PKCS7填充过的数据
    - :param text: 解密后的字符串
    - :retu
    - aes 解密方法
    -----------------------------------------------------------------------------------
    '''

    def decrypt(key: str, content: str, iv: str):
        '''
        ### AES 解密 
        - 处理使用PKCS7填充过的数据 
        - :param text: 解密后的字符串 
        - :retu 
        '''

        key_bytes = bytes(key, encoding='utf-8')
        iv_bytes = bytes(iv, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        # base64解码
        encrypt_bytes = base64.b64decode(content)
        # 解密
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        # 重新编码
        result = str(decrypt_bytes, encoding='utf-8')

        length = len(result)
        unpadding = ord(result[length - 1])
        result = result[0:length - unpadding]
        return result