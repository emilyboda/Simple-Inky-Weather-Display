from PIL import Image, ImageDraw, ImageFont, ImageColor
from epdconfig import *
from fonts import *
from settings import *
import epd_7_in_5 as driver

background_colour = 'white'
text_colour = 'black'

display_width, display_height = driver.EPD_HEIGHT, driver.EPD_WIDTH

image = Image.new('RGB', (display_width, display_height), background_colour)

## DEFINE THE BOUNDS OF THE CURRENT CONFIG, imported from settings.py
b_left = left_edge
b_right = right_edge
b_top = top_edge
b_bottom = bottom_edge

width = int(b_right - b_left) # this width and height is the width and height of inside the picture frame mat
height = int(b_bottom - b_top)

print('inside of picture frame mat is', width, 'wide by', height, 'high')
d_image = Image.new('RGB', (width, height), background_colour) # creating a smaller image, based on the inside of the mat
draw = ImageDraw.Draw(d_image)

## DEFINE FONTS
regular_font_path = '/home/pi/simple-weather/fonts/NotoSans-hinted/NotoSans-Condensed.ttf'
summary_font_path = '/home/pi/simple-weather/fonts/NotoSans-hinted/NotoSans-CondensedItalic.ttf'
weather_font_path = '/home/pi/simple-weather/fonts/WeatherFont/weathericons-regular-webfont.ttf'
font = ImageFont.truetype(regular_font_path, 20)

## GET WEATHER INFO ##
import requests
import json
import math

if debugging_choice_weather == True:
    icon = 'rain'
    # icon = 'clear-day'
    hi = 77.3
    lo = 68
    hi_time = 1599935700
    lo_time = 1599935700
    today_summary = "Rain and humid throughout the day."
    week_summary = "Light rain on Thursday through next Monday."
else:
    r = requests.get('https://api.darksky.net/forecast/'+dark_sky_api_key+'/'+dark_sky_coords)
    weather = r.json()
    # print(json.dumps(weather, indent=4))
    weather_file_path = "/home/pi/simple-weather/forecast.json"
    with open(weather_file_path, 'w') as outfile:
        json.dump(weather, outfile)

    icon = weather['daily']['data'][0]['icon']
    hi = weather['daily']['data'][0]['temperatureHigh']
    lo = weather['daily']['data'][0]['temperatureLow']
    hi_time = weather['daily']['data'][0]['temperatureHighTime']
    lo_time = weather['daily']['data'][0]['temperatureLowTime']
    today_summary = weather['daily']['data'][0]['summary']
    week_summary = weather['daily']['summary']


## GET DATE INFO ##
import datetime

dayy = datetime.datetime.now().strftime('%d')

if dayy[-1] == "1" and dayy[0] != "1":
    end = "st"
elif dayy[-1] == "2" and dayy[0] != "1":
    end = "nd"
elif dayy[-1] == "3" and dayy[0] != "1":
    end = "rd"
else:
    end = "th"

todayis_string = "Today is "+datetime.datetime.now().strftime('%A')
date_string = datetime.datetime.now().strftime('%B %-d')+end
hilo_string = 'High of '+str(round(hi))+'°, low of '+str(round(lo))+'°'

summary_string = today_summary.replace(".", "")

allowed_width = int(width*0.75)

## GET FONT SIZE ##
### gets the font size from the strings that are consistently sized
font_size = 20
consistent_strings = [todayis_string, date_string, hilo_string]
max_size = 0
while max_size <= allowed_width:
    max_size = 0
    for line in consistent_strings:
        cs = ImageFont.truetype(regular_font_path, font_size).getsize(line)
        if cs[0] > max_size:
            max_size = cs[0]
    font_size = font_size + 2
font = ImageFont.truetype(regular_font_path, font_size)
print(font_size)


## SPLIT FONT INTO TWO LINES IF NECESSARY ##
# the summary message is frequently too long to fit on one line.

summary_font_size = 20
summary_font = ImageFont.truetype(summary_font_path, font_size)
summary_first_size = summary_font.getsize(summary_string)

# test to see if the width of the summary line is larger than the allowed width.
if summary_first_size[0] > allowed_width:
    # if it is, split it into two lines by finding the first space before the middle and the first space after the middle of the string
    summary_find = [
                        summary_string[0:summary_string.find(" ",int(len(summary_string)/2))],
                        summary_string[summary_string.find(" ",int(len(summary_string)/2))+1:len(summary_string)]
                    ]
    summary_rfind = [
                        summary_string[0:summary_string.rfind(" ",0,int(len(summary_string)/2))],
                        summary_string[summary_string.rfind(" ",0,int(len(summary_string)/2))+1:len(summary_string)]
                    ]
    summary_find_diff = abs(summary_font.getsize(summary_find[0])[0] - summary_font.getsize(summary_find[1])[0])
    summary_rfind_diff = abs(summary_font.getsize(summary_rfind[0])[0] - summary_font.getsize(summary_rfind[1])[0])
    
    print(summary_find_diff, summary_rfind_diff)
    # we're going to find the one where the two lines are closest in length and pick that one
    if summary_find_diff <= summary_rfind_diff:
        summary_array = summary_find
    else:
        summary_array = summary_rfind
else:
    # if it's not longer than the allowed width, we'll keep it on one line
    summary_array = [summary_string]


### GET WEATHER ICON ###
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

## DEFINE WHERE TEXT IS TO BE DRAWN
text_to_display = []

line_height = 2

# Today is Thursday
text_to_display = [
    {
        "text": todayis_string,
        "font": font,
        "top": 0,
        "bottom": 0+font.getsize(todayis_string)[1],
        "left": int(width/2 - font.getsize(todayis_string)[0]/2)
    }
]

# September 10th
text_to_display.append(
    {
        "text": date_string,
        "font": font,
        "top": text_to_display[0]["bottom"] + line_height,
        "bottom": text_to_display[0]["bottom"] + line_height + font.getsize(date_string)[1],
        "left": int(width/2 - font.getsize(date_string)[0]/2)
    }
)

# weather icon
icon_size = 60
weather_font = ImageFont.truetype(weather_font_path, icon_size)
y_correction = 5
text_to_display.append(
    {
        "text": icon_text,
        "font": weather_font,
        "top": text_to_display[1]["bottom"] + line_height - y_correction,
        "bottom": text_to_display[1]["bottom"] + line_height - y_correction + weather_font.getsize(icon_text)[1],
        "left": int(width/2 - weather_font.getsize(icon_text)[0]/2)
    }
)

# Hi of 77, low of 68
text_to_display.append(
    {
        "text": hilo_string,
        "font": font,
        "top": text_to_display[2]["bottom"] + line_height,
        "bottom": text_to_display[2]["bottom"] + line_height + font.getsize(hilo_string)[1],
        "left": int(width/2 - font.getsize(hilo_string)[0]/2)
    }
)

# Rain and humid
# throughout the day
counter = 3
for sum in summary_array:
    text_to_display.append(
        {
            "text": sum,
            "font": summary_font,
            "top": text_to_display[counter]["bottom"] + line_height,
            "bottom": text_to_display[counter]["bottom"] + line_height + summary_font.getsize(sum)[1],
            "left": int(width/2 - summary_font.getsize(sum)[0]/2)
        }
    )
    counter = counter + 1

## draw all the text onto the display
y_start = int(height/2 - text_to_display[-1]['bottom']/2)
for item in text_to_display:
    draw.text((item['left'], item['top']+y_start), item['text'], text_colour, font = item['font'])
    
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
    box_draw.line(((b_left + width/2, b_top), (b_left+width/2, b_bottom)), 'black', width=3)
    for item in text_to_display:
        box_draw.line(((b_left, b_top+y_start+item['top']), (b_right, b_top+y_start+item['top'])), 'black', width=1)
        box_draw.line(((b_left, b_top+y_start+item['bottom']), (b_right, b_top+y_start+item['bottom'])), 'black', width=1)
    # weather_point = (weather_point[0]+b_left, weather_point[1]+b_top)
    # box_draw.line((weather_point, (weather_point[0], weather_point[1]+weather_size[1])), 'black', width=3)
    # box_draw.line((weather_point, (weather_point[0]+weather_size[0], weather_point[1])), 'black', width=3)
    # box_draw.line(((weather_point[0]+weather_size[0], weather_point[1]), (weather_point[0]+weather_size[0], weather_point[1]+weather_size[1])), 'black', width=3)
    # box_draw.line(((weather_point[0], weather_point[1]+weather_size[1]), (weather_point[0]+weather_size[0], weather_point[1]+weather_size[1])), 'black', width=3)

    box_draw.line(((b_left,b_top),(b_left,b_bottom)),'black', width = 3)
    box_draw.line(((b_right,b_top),(b_right,b_bottom)),'black', width = 3)
    box_draw.line(((b_left,b_top),(b_right,b_top)),'black', width = 3)
    box_draw.line(((b_left,b_bottom),(b_right,b_bottom)),'black', width = 3)
    
    # box_draw.line(((0,0),(0,display_height)),'black', width = 3)
    # box_draw.line(((display_width,0),(display_width,display_height)),'black', width = 3)
    # box_draw.line(((0,0),(display_width,0)),'black', width = 3)
    # box_draw.line(((0,display_height),(display_width,display_height)),'black', width = 3)

## SAVE TO FILE
image.save('/home/pi/test.png')
print('image saved')

if debugging_choice_screen == False:
    # PRINT ONTO SCREEN
    epaper = driver.EPD()
    print('Initialising E-Paper...', end = '')
    epaper.init()
    print('Done')

    print('Sending image data and refreshing display...', end='')
    # epaper.display(epaper.getbuffer(image), epaper.getbuffer(image_col))
    epaper.display(epaper.getbuffer(image))
    print('Done')
    epaper.sleep()
