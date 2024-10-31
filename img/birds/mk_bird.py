import os
from PIL import Image, ImageColor


BASE_BIRD = "./bird_D5BE24.png"

BASE_HIGH_R, BASE_HIGH_G, BASE_HIGH_B = (220, 226, 179)
BASE_MID_R, BASE_MID_G, BASE_MID_B = (213, 190, 36)
BASE_LOW_R, BASE_LOW_G, BASE_LOW_B = (226, 127, 19)

BASE_HIGH = (220, 226, 179)
BASE_MID = (213, 190, 36)
BASE_LOW = (226, 127, 19)

def bird_color_exists(color: str) -> bool:
	'''
	looks through directory to find of there exists
	a ".png" file that contains, in its name, the base
	color.

	input: base color of to-be new bird (HEX)

	return: True if bird already exists
			False if bird doesn't exist
	'''
	for i in os.listdir("./"):
		if i.startswith("bird_") and i.endswith(".png") and i[5:11] == color.upper():
			return True

	return False

def mk_new_hight(color: tuple) -> tuple:
	r = int((color[0] + 255) / 2)
	g = int((color[1] + 255) / 2)
	b = int((color[2] + 255) / 2)
	return (r,g,b)

def mk_new_low(color: tuple) -> tuple:
	r = int(color[0] * 5 / 7)
	g = int(color[1] * 5 / 7)
	b = int(color[2] * 5 / 7)
	return (r,g,b)

def mk_birds(colors: list) -> bool:
	'''
	Make bird by copying original bird and replacing its original colors
	with input base color and generated highlight and shadow color

	input: list of base colors of to-be new birds (HEX)

	return: True if images has been created
			False if images not created
	'''

	for color in colors:
		if bird_color_exists(color):
			continue

		new_mid = ImageColor.getcolor("#" + color, "RGB")
		new_high = mk_new_hight(new_mid)
		new_low = mk_new_low(new_mid)

		im = Image.open("./bird_D5BE24.png")
		pixels = im.load()

		width, height = im.size
		for y in range(height):
			for x in range(width):
				r, g, b, a = pixels[x, y]
				if (r, g, b) == BASE_HIGH:
					pixels[x,y] = new_high

				elif (r, g, b) == BASE_MID:
					pixels[x,y] = new_mid

				elif (r, g, b) == BASE_LOW:
					pixels[x,y] = new_low

		im.save("bird_" + color.upper() + ".png")
	
	return True




def main():
	l = [
"f0285c",
"f0285c",
"b05d94",
"b05d94",
"618d1b",
"618d1b",
"ee9c2f",
"ee9c2f",
"9df3ce",
"9df3ce",
"2095b2",
"2095b2",
"e37fc7",
"e37fc7",
"568a63",
"568a63",
"734d22",
"734d22",
"cd8821",
"cd8821",
"e557b4",
"e557b4",
"ab653c",
"ab653c",
"d1245a",
"d1245a",
"9c084f",
"9c084f",
"3e59cf",
"3e59cf",
"8d6ca2",
"8d6ca2",
"6f5676",
"6f5676",
"762367",
"762367",
"1187ee",
"1187ee",
"80fa84",
"80fa84",
"208fde",
"208fde",
"4fabaf",
"4fabaf",
"f51322",
"f51322",
"805162",
"805162",
"6cdada",
"6cdada",
"06aedc",
"06aedc",
"be9050",
"be9050",
"74896e",
"74896e",
"795a07",
"795a07",
"ce4bb5",
"ce4bb5",
"9bcabf",
"9bcabf",
"497b29",
"497b29",
"51dce3",
"51dce3",
"b88b9f",
"b88b9f",
"18df1c",
"18df1c",
"8cd301",
"8cd301",
"43ba21",
"43ba21",
"fd8643",
"fd8643",
"21d2c7",
"21d2c7",
"d9b124",
"d9b124",
"e361ec",
"e361ec",
"0c0316",
"0c0316",
"5bd112",
"5bd112",
"70b400",
"70b400",
"a04f26",
"a04f26",
"c0a6fc",
"c0a6fc",
"b988d6",
"b988d6",
"14fb30",
"14fb30",
"f30f00",
"f30f00",
"032ad2",
"032ad2",
"e6ca9a",
"e6ca9a",
"deb531",
"deb531",
"5c00bb",
"5c00bb",
"992d17",
"992d17",
"4f1946",
"4f1946"
	]
	mk_birds(l)

if __name__ == '__main__':
	main()