# Bilge Object Annotation Tool

This is an easy to use program to annotate images probably for the use of machine learning purposes.
It lets you select a frame with drag and drop mechanism, lets you select frames and make small
adjustments on them like changing size and moving the frame. After the images are annotated
it saves them in an easy to use JSON format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Here is a quick list of the things you'll have to run this program.

```
Python 3.6 or higher
```
```
PyGame Module
```
## Running the test

You can run test.py to see if the frames are at the right place.

## How to run the program?

First you have to create two directories in the directory which the main program sits.
One is "img" the other is "data". You do not need to put anything in the data folder but
you should put the images you want to annotate into the img folder.
After the setup is done you can run the program with
```
>>> python3 object_framing_tool.py [LABEL1] [LABEL2] [LABEL3] ...
```
So you give the labels as console arguments with spaces.

## How to use the program?

* Creating a Frame
```
First you have to left click on the point where you want one corner of the frame, then holding the mouse
drag the cursor and when the wanted frame is selected release the left click. Then a window will pop where you
select the label of the frame you are creating. After you select your label then the frame is created.
```

* Selecting and Adjusting a Frame
```
To select a frame hover on the wanted frame then press 'T' on your keyboard. After the frame is
selected it will turn into green. Then you can use WASD keys to change the size of the frame:

W - Make it shorter
S - Make it taller
A - Make it thinner
D - Make it wider

also you can use the arrow keys to move the frame on image.
```

* Deleting a Frame
```
Hover on the frame you want to delete then right click on it.
```

* Working on the Next Picture
```
Press ENTER or RETURN key to move to the next image.
```

* Canceling the Frame Selection Without Choosing a Label
```
If you press BACKSPACE when a label for the frame is asked the frame selection is canceled.
```
