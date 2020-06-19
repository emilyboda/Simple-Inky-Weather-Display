## Note:
This repo is not maintained. Files may not work. You'll have to install the dependencies yourself.

## What makes this project different from all the other Inky projects?
The biggest difference is that I have allowed the user to use a picture frame mat that is smaller than the screen itself. The 7.5 inch screen is an unusual size and I have yet to find an off-the-shelf frame that fits this display. As a result, many users cut their own mats. This looks pretty awful. I created a calibration file that allows the user to say "15 pixels are cut off on the left", and "20 pixels are cut off on the top", etc. The display program takes into account that smaller sized area and centers the display on the actual area shown.

My code isn't perfect, but please incorporate it into your own projects and build on it.

## Installation Instructions:
1. Clone this repo with:
git clone https://github.com/emilyboda/simple-inky-weather-display simple-weather
2. Follow the instructions in the settings.py file

## Display In Use
<p align="center">
<img src="https://github.com/emilyboda/simple-inky-weather-display/blob/master/display_in_the_wild.jpg" width="900"><img 
</p>

## Calibration Example
Each small line represents 5 pixels. The text "50" is telling you that the point (50, 50) is where the two dark lines cross to the top left of the text.
top_edge = 30
left_edge = 49
right_edge = 593
bottom_edge = 375
<p align="center">
<img src="https://github.com/emilyboda/simple-inky-weather-display/blob/master/example_calibration.jpg" width="900"><img 
</p>

## Thanks to:
Many thanks to https://github.com/aceisace for his help with this project. Much of my code is based on his code.
