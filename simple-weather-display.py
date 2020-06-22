from PIL import Image, ImageDraw, ImageFont, ImageColor
from epdconfig import *
from fonts import *
from settings import *
import epd_7_in_5 as driver

background_colour = 'white'
text_colour = 'black'

display_width, display_height = driver.EPD_WIDTH, driver.EPD_HEIGHT

image = Image.new('RGB', (display_width, display_height), background_colour)

## DEFINE THE BOUNDS OF THE CURRENT CONFIG, imported from settings.py
b_left = left_edge
b_right = right_edge
b_top = top_edge
b_bottom = bottom_edge

width = int(b_right - b_left) # this width and height is the width and height of inside the picture frame mat
height = int(b_bottom - b_top)

d_image = Image.new('RGB', (width, height), background_colour) # creating a smaller image, based on the inside of the mat
draw = ImageDraw.Draw(d_image)

## DEFINE FONTS
regular_font_path = '/home/pi/simple-weather/fonts/NotoSansCJK/NotoSansCJKsc-Regular.otf'
weather_font_path = '/home/pi/simple-weather/fonts/WeatherFont/weathericons-regular-webfont.ttf'
font = ImageFont.truetype(regular_font_path, 20)

## GET WEATHER INFO ##
import requests
import json
import math

r = requests.get('https://api.darksky.net/forecast/'+dark_sky_api_key+'/'+dark_sky_coords)
weather = r.json()

curr_temp = weather['currently']['temperature']
icon = weather['currently']['icon']
hi = weather['daily']['data'][0]['temperatureHigh']
lo = weather['daily']['data'][0]['temperatureLow']

## GET DATE INFO ##
import datetime
dayy = datetime.datetime.now().strftime('%d')[-1]
if dayy == "1":
    end = "st"
elif dayy == "2":
    end = "nd"
elif dayy == "3":
    end = "rd"
else:
    end = "th"
now_string = datetime.datetime.now().strftime('%A, %B %d')+end

display_text = ["", 
                'Today is '+now_string, 
                "", 
                'High of '+str(round(hi))+'°F, low of '+str(round(lo))+'°F',
                ""]

allowed_width = int(width*0.8)

## GET FONT SIZE ##
font_size = 20
max_size = 0
while max_size <= allowed_width:
    max_size = 0
    for line in display_text:
        cs = ImageFont.truetype(regular_font_path, font_size).getsize(line)
        if cs[0] > max_size:
            max_size = cs[0]
    font_size = font_size + 2
font = ImageFont.truetype(regular_font_path, font_size)


line_height = int(height/len(display_text))

## DRAW THE TEXT TO DISPLAY ##
for line in range(0,len(display_text)):
    x = int((width - font.getsize(display_text[line])[0])/2)
    font_height = font.getsize(display_text[line])[1]
    y = int(height//len(display_text)*line) + int((line_height - font_height)/2)
    draw.text((x, y),display_text[line], text_colour, font = font)

### DRAW WEATHER ###
iconmap =   {
            'clear-day':'\uf00d',               'clear-night':'\uf02e',
            'rain':'\uf019',                    'snow':'\uf01b',
            'sleet':'\uf0b5',                   'wind':'\uf050',
            'cloudy':'\uf013',                  'partly-cloudy-day': '\uf002',
            'partly-cloudy-night': '\uf031',    'hail':'\uf015',
            'thunderstorm':'\uf01e',            'tornado':'\uf056',
            'other':'\uf053'
            }
try:
    icon_text = iconmap[icon]
except:
    icon_text = iconmap['other']
temp_text = str(round(curr_temp))+"°F" 

### FIND ICON FONT SIZE ###
icon_font = 40
size = ImageFont.truetype(weather_font_path, icon_font).getsize(icon_text)[1]
while size < line_height*0.8:
    size = ImageFont.truetype(weather_font_path, icon_font).getsize(icon_text)[1]
    icon_font = icon_font + 2

### FIND TEMP FONT SIZE ###
temp_font = 40
size = ImageFont.truetype(regular_font_path, temp_font).getsize(temp_text)[1]
while size < line_height*0.8:
    size = ImageFont.truetype(regular_font_path, temp_font).getsize(temp_text)[1]
    temp_font = temp_font + 2
weather_font = ImageFont.truetype(weather_font_path, icon_font)
weather_size = weather_font.getsize(icon_text)

temp_font_font = ImageFont.truetype(regular_font_path, temp_font)
temp_size = temp_font_font.getsize(temp_text)


## DOING A BUNCH OF CALCULATIONS FOR THE CENTER ICON AND TEMP TEXT
"""
The center line was stupid complicated. I had to combine the icon (which is in the
weather font) with the temperature (which is in the regular font).

I took the sizes of the icon and the temp text and added a gap between them and then
centered them as best I could.
"""
gap_width = 10 
weather_start = int((width - (weather_size[0]+gap_width+temp_size[0]))/2)
temp_start = weather_start + weather_size[0] + gap_width

line3start = int(height//len(display_text)*2)
weather_correction = 3
size_correction = 5

draw.text((weather_start, line3start + int((line_height - weather_size[1])/2)+weather_correction-size_correction),icon_text, text_colour, font = weather_font)
draw.text((temp_start, line3start + int((line_height - temp_size[1])/2)-size_correction),temp_text, text_colour, font = temp_font_font)

## Add a last updated line, if requested
if last_updated_choice == True:
    last_updated_font_size = 14
    nowtext = datetime.datetime.now().strftime("%Y-%m%-d %H:%M")
    last_updated_text = "Last updated at "+nowtext
    last_updated_font = ImageFont.truetype(regular_font_path, last_updated_font_size)
    last_updated_size = last_updated_font.getsize(last_updated_text)
    draw.text((width - last_updated_size[0], height - last_updated_size[1]),last_updated_text, text_colour,last_updated_font)

## PASTE THE SMALLER INSIDE IMAGE ONTO THE FULL SCREEN
image.paste(d_image, (b_left, b_top))

## Draw the calibration boxes (to check numbers) onto full screen, if requested
if check_calibration_choice == True:
    box_draw = ImageDraw.Draw(image)
    box_draw.line(((b_left,b_top),(b_left,b_bottom)),'black', width = 3)
    box_draw.line(((b_right,b_top),(b_right,b_bottom)),'black', width = 3)
    box_draw.line(((b_left,b_top),(b_right,b_top)),'black', width = 3)
    box_draw.line(((b_left,b_bottom),(b_right,b_bottom)),'black', width = 3)
    
    box_draw.line(((0,0),(0,display_height)),'black', width = 3)
    box_draw.line(((display_width,0),(display_width,display_height)),'black', width = 3)
    box_draw.line(((0,0),(display_width,0)),'black', width = 3)
    box_draw.line(((0,display_height),(display_width,display_height)),'black', width = 3)

## SAVE TO FILE
image.save('/home/pi/test.png')

## PRINT ONTO SCREEN
epaper = driver.EPD()
print('Initialising E-Paper...', end = '')
epaper.init()
print('Done')

print('Sending image data and refreshing display...', end='')
# epaper.display(epaper.getbuffer(image), epaper.getbuffer(image_col))
epaper.display(epaper.getbuffer(image))
print('Done')
epaper.sleep()
