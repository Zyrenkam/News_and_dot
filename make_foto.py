from PIL import Image, ImageFont, ImageDraw
import course_weather
import random


def make_foto():
    patterns = ['foto_post/foto_pattern1.jpg', 'foto_post/foto_pattern1.jpg']

    img = Image.open(patterns[random.randint(0, len(patterns)-1)])

    text = course_weather.do()

    draw = ImageDraw.Draw(img)
    draw.text((1800, 150), text[0], font=ImageFont.truetype("fonts/garamond.ttf", 90), fill="#000000")
    draw.text((200, 150), text[1], font=ImageFont.truetype("fonts/garamond_bold.ttf", 120), fill="#000000")

    img.save("foto_post/output.png", "PNG")

    print("FOTO CREATED")
