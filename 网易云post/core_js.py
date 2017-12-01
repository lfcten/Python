"""
生成随机16位字符串
function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }

作者：ioiogoo
链接：http://www.jianshu.com/p/edbca827317a
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
import random


def a(length):
    x =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = ""
    for _ in range(length):
        index = random.randint(0, len(x) - 1)
        result += x[index]
    return result
print(a(16))


"""
AES加密函数
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")   偏移量已知
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }

作者：ioiogoo
链接：http://www.jianshu.com/p/edbca827317a
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
import base64
from Crypto.Cipher import AES
def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text += pad * chr(pad)                             # 16 (*AES-128*)
    encrypt = AES.new(secKey, 2, '0102030405060708')   # 2: mode_CBC
    cipher = encrypt.encrypt(text)
    cipher = base64.b64encode(cipher)
    return cipher
format()
