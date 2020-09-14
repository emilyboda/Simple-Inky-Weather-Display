## Note:
This repo is not maintained. Files may not work. You'll have to install the dependencies yourself.

Also, this project uses the Dark Sky weather API. You must already have a Dark Sky API key to use it and the API will stop working in 2021. I used this API because I couldn't find any other free API that gives the "high" and a "low" for the day. Suggestions of other APIs to use are welcome! 

## Update Sept 2020
I added an option to use this vertically. The vertical version does not have the current temperature, it instead shows the weather icon for the entire day and has a blurb summarizing the weather for the rest of the day, such as "Rain in the morning" or "Humid and muggy all day".

## What makes this project different from all the other Inky projects?
The biggest difference is that I have allowed the user to use a picture frame mat that is smaller than the screen itself. The 7.5 inch screen is an unusual size and I have yet to find an off-the-shelf frame that fits this display. As a result, many users cut their own mats. This looks pretty awful. I created a calibration file that allows the user to say "15 pixels are cut off on the left", and "20 pixels are cut off on the top", etc. The display program takes into account that smaller sized area and centers the display on the actual area shown.

See the image below. The outer box is the actual full display, and the inner box represents the image that you can see under the mat. The mat cuts off the outer edges. If I centered the weather display on the outer box, it would not be centered when looking at it in the picture frame.

## Display Raw Saved Image
<p align="center">
<img src="https://github.com/emilyboda/Simple-Inky-Weather-Display/blob/master/raw_image_calibration.png" width="900"><img 
</p>

## Display In Use
<p align="center">
<img src="https://github.com/emilyboda/Simple-Inky-Weather-Display/blob/master/display_in_the_wild.jpg" width="900"><img 
</p>

## Installation Instructions:
### You will need:
- [Raspberry Pi Zero](https://www.amazon.com/gp/product/B0748MPQT4/ref=as_li_ss_tl?ie=UTF8&psc=1&linkCode=ll1&tag=nova08-20&linkId=fdde8192b5aa90f4fe858929bb859e76&language=en_US)
- [7.5" ePaper Screen](https://www.amazon.com/waveshare-7-5inch-HAT-Raspberry-Consumption/dp/B075R4QY3L/ref=as_li_ss_tl?dchild=1&keywords=waveshare+7.5&qid=1600103451&sr=8-1&linkCode=ll1&tag=nova08-20&linkId=999ec0a6b15e20a99789c3f37ad49e07&language=en_US)
### Installing:
1. Clone this repo with:
**`git clone https://github.com/emilyboda/Simple-Inky-Weather-Display simple-weather`**
2. Follow the instructions in the settings.py file

## Calibration Example
Each small line represents 5 pixels. The text "50" is telling you that the point (50, 50) is where the two dark lines cross to the top left of the text.

**`top_edge = 30`**

**`left_edge = 49`**

**`right_edge = 593`**

**`bottom_edge = 375`**
<p align="center">
<img src="https://github.com/emilyboda/Simple-Inky-Weather-Display/blob/master/example_calibration.jpg" width="900"><img 
</p>

## Thanks to:
Many thanks to https://github.com/aceisace for his help with this project. Much of my code is based on his code.

Weather Font is from Eric Flowers: https://github.com/erikflowers/weather-icons
