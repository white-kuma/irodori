# coding:utf-8
import irodori

_CODE = "#ABCDEF"
_RGB = [171, 205, 239]
_HSV = [210, 72, 239]

# カラーコードをRGBに
rgb = irodori.code_to_rgb(_CODE)
print("code -> rgb", rgb, rgb == _RGB)

# カラーコードをHSVに
hsv = irodori.code_to_hsv(_CODE)
print("code -> hsv", hsv, hsv == _HSV)

# RGBをカラーコードに
code = irodori.rgb_to_code(_RGB)
print("rgb -> code", code, code == _CODE)

# RGBをhsvに
hsv = irodori.rgb_to_hsv(_RGB)
print("rgb -> hsv", hsv, hsv == _HSV)

# HSVをカラーコードに
code = irodori.hsv_to_code(_HSV)
print("hsv -> code", code, code == _CODE)

# HSVをRGBに
rgb = irodori.hsv_to_rgb(_HSV)
print("hsv -> rgb", rgb, rgb == _RGB)
