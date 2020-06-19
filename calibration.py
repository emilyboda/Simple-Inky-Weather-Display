from PIL import Image, ImageDraw, ImageFont, ImageColor
from epdconfig import *
from fonts import *
from settings import *
import epd_7_in_5 as driver

display_width, display_height = driver.EPD_WIDTH, driver.EPD_HEIGHT

image = Image.new('RGB', (display_width, display_height), 'white')
draw = ImageDraw.Draw(image)

regular_font_path = '/home/pi/simple-weather/fonts/NotoSansCJK/NotoSansCJKsc-Regular.otf'
font = ImageFont.truetype(regular_font_path, 15)

inc = 5
for x in range(0,display_width//inc):
    if x%5 == 0:
        width = 3
    else:
        width = 1
    draw.line(((x*inc,0),(x*inc,display_height)),fill='black', width = width)

for y in range(0,display_height//inc):
    if y%5 == 0:
        width = 3
        draw.text((y*inc, y*inc), str(y*inc), 'black',font)
    else:
        width = 1
    draw.line(((0,y*inc),(display_width,y*inc)),fill='black', width = width)
    
## PRINT ONTO IMAGE
epaper = driver.EPD()
print('Initialising E-Paper...', end = '')
epaper.init()
print('Done')

print('Sending image data and refreshing display...', end='')
# epaper.display(epaper.getbuffer(image), epaper.getbuffer(image_col))
epaper.display(epaper.getbuffer(image))
print('Done')
epaper.sleep()
