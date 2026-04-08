import ctypes
import sys

fontconfig = ctypes.CDLL("libfontconfig.so.1")
fontconfig.FcLangNormalize.argtypes = [ctypes.c_char_p]
fontconfig.FcLangNormalize.restype = ctypes.c_char_p
print(fontconfig.FcLangNormalize(sys.argv[1].encode('utf-8')).decode('utf-8'))
