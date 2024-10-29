
from PIL import Image
 
def convertImage(filename: str):
    img = Image.open(filename)
    img = img.convert("RGBA")
 
    datas = img.getdata()
 
    newData = []
 
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
 
    img.putdata(newData)
    img.save(filename, "PNG")
    print("Successful")

if __name__ == '__main__':
    # img_l = ["./bg/buildings.png", "./bg/bush.png"]
    img_l = ["./pipe.png", "./pipe_flip.png"]
    for i in img_l:
        convertImage(i)