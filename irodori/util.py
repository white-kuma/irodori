# coding:utf-8

SV_MAX_100 = 0  # 彩度と明度を0～100で表す（相互変換時に誤差が出る）
SV_MAX_255 = 1  # 彩度と明度を0～255で表す


def _is_rgb_array(rgb):
	"""
	RGB値かチェック
	"""
	if len(rgb) != 3:
		return False
	if len([x for x in rgb if x > 255 or x < 0]) > 0:
		return False
	return True


def _is_hsv_array(hsv, sv_max = SV_MAX_255):
	"""
	HSV値かチェック
	"""
	limit = 0
	if sv_max == SV_MAX_100:
		limit = 100
	elif sv_max == SV_MAX_255:
		limit = 255
	else:
		raise ValueError

	if len(hsv) != 3:
		return False
	if not (0 <= hsv[0] <= 360):
		return False
	if not (0 <= hsv[1] <= limit):
		return False
	if not (0 <= hsv[2] <= limit):
		return False
	return True


def code_to_rgb(code):
	"""
	カラーコードをRGB値に変換
	"""
	if code[0] == "#":
		code = code[1:]

	if len(code) == 3:
		rgb = [int("%s%s" % (x, x), 16) for x in code]
	elif len(code) == 6:
		rgb = [int("%s" % code[i:i+2], 16) for i in range(0, 6, 2)]
	else:
		raise ValueError
	return rgb


def rgb_to_code(rgb):
	"""
	RGB値をカラーコードに変換
	"""
	if _is_rgb_array(rgb) == False:
		raise ValueError
	return "#" + "".join(["%02X" % x for x in rgb])


def rgb_to_hsv(rgb, sv_max = SV_MAX_255):
	"""
	RGB値をHSVに変換
	"""
	if _is_rgb_array(rgb) == False:
		raise ValueError

	max_i = rgb.index(max(rgb))
	max_rgb = max(rgb)
	min_rgb = min(rgb)
	r, g, b = rgb

	# Black
	if r == g == b == 0:
		return [0, 0, 0]

	# Hue (0 ~ 360)
	H = 0
	if rgb[0] == rgb[1] == rgb[2]:
		H = 0
	elif max_i == 0:
		H = 60 * ((g - b) / (max_rgb - min_rgb))
	elif max_i == 1:
		H = 60 * ((b - r) / (max_rgb - min_rgb)) + 120
	elif max_i == 2:
		H = 60 * ((r - g) / (max_rgb - min_rgb)) + 240
	else:
		# Unreachable
		raise RuntimeError
	if H < 0:
		H += 360

	# Saturation (0 ~ 255)
	S = (max_rgb - min_rgb) / max_rgb

	# Value (0 ~ 255)
	V = max_rgb

	if sv_max == SV_MAX_100:
		S *= 100
		V = (V / 255) * 100
	elif sv_max == SV_MAX_255:
		S *= 255
	else:
		raise ValueError

	return [int(H), int(S), int(V)]


def hsv_to_rgb(hsv, sv_max = SV_MAX_255):
	"""
	HSV値をRGB値に変換
	"""
	if _is_hsv_array(hsv, sv_max) == False:
		raise ValueError
	
	h, s, v = hsv
	if sv_max == SV_MAX_100:
		s = s / 100 * 255
		v = v / 100 * 255
	elif sv_max == SV_MAX_255:
		pass
	else:
		raise ValueError

	max_rgb = v
	min_rgb = max_rgb - ((s / 255) * max_rgb)
	c = (max_rgb - min_rgb)
	if h <= 60:
		return [int(max_rgb), int((h / 60) * c + min_rgb), int(min_rgb)]
	elif h <= 120:
		return [int(((120 - h) / 60) * c + min_rgb), int(max_rgb), int(min_rgb)]
	elif h <= 180:
		return [int(min_rgb), int(max_rgb), int(((h - 120) / 60) * c + min_rgb)]
	elif h <= 240:
		return [int(min_rgb), int(((240 - h) / 60) * c + min_rgb), int(max_rgb)]
	elif h <= 300:
		return [int(((h - 240) / 60) * c + min_rgb), int(min_rgb), int(max_rgb)]
	elif h <= 360:
		return [int(max_rgb), int(min_rgb), int(((360 - h) / 60) * c + min_rgb)]
	else:
		raise ValueError


def code_to_hsv(code, sv_max = SV_MAX_255):
	rgb = code_to_rgb(code)
	return rgb_to_hsv(rgb, sv_max)


def hsv_to_code(hsv, sv_max = SV_MAX_255):
	rgb = hsv_to_rgb(hsv, sv_max)
	return rgb_to_code(rgb)
