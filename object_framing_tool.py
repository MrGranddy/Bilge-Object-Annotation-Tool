import pygame
import sys, os
from os import listdir
from os.path import isfile, join
import json

IMAGES_PATH = "img/"    # Images to annotate
DATA_PATH = "data/data.json"    # Frame information
LABELS = [label for label in sys.argv[1:]]  # Possible classes for objects ( Given as console argument )

class Frame:
    """
    The class to store every box and its information:

    Attributes
    ----------
    self.x : int
        x coordinate of the top-left corner of the frame. Origin is taken as
        the top-left corner of the window and down-right directions are
        positive.
    self.y : int
        y coordinate of the top-left corner of the frame. Origin is taken as
        the top-left corner of the window and down-right directions are
        positive.
    self.width : int
        Width of the frame.
    self.height : int
        Height of the frame.
    self.label : string
        Class of the object in the box.

    """
    def __init__(self, x, y, height, width, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label


pygame.init()   # Initialize PyGame
pygame.display.set_caption("Object Framing Tool")   # Window title

screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h  # Resolution of screen in pixel length

window_to_screen_ratio = 0.8    # Ratio of the window's lengths and the screen's
size = width, height = int(screen_width * window_to_screen_ratio), int(screen_height * window_to_screen_ratio) # Window size
window = pygame.display.set_mode(size)  # Create window
screen = pygame.display.get_surface()   # Get window surface ( will be used to draw things on the window )
bg_color = (255,255,255)    # Background color in RGB
info_ratio = 0.2    # Info windows ratio to the total length of the window
len_info = int(width * info_ratio)  # Width of the info window
width = width - len_info    # width is then updated to make calculations easier,
# the window is created with the previous width but now will be refering to the
# width without info window.

frames = [] # The array to store drawn frames in runtime

images = [f for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f))]
# Names of the image files in the set path as IMAGES_PATH
curr_img = 0
# Index of the image that is currently displayed, this is the index for images
# array.
selected_frame = None
# The currently focused frame, also held as an index integer.

data = {} # Information of frames, it gives a list of frames for the given
# image name as a key.

def delete_frame(x, y):
    """
    Deletes the frame with the given coordinates. Will not handle
    if the given coordinate is in multiple boxes.

    Parameters
    ----------
    x : int
        x of the point of interest.
    y : int
        y of the point of interest.

    Returns
    -------
    None

    """
    global selected_frame # use global variable selected frame
    to_delete = None      # if a frame can be found containing the given point
                          # this will be the index of it
    for index, frame in enumerate(frames):
        if 0 <= x - frame.x <= frame.width and 0 <= y - frame.y <= frame.height:
            to_delete = index
            break
    if to_delete is not None: del frames[to_delete] # If found delete it
    selected_frame = None # Selected frame is reset because indices may shift

def load_image(img_path):
    """
    Loads the image with the given path and resizes it into a size which
    it will fit into the window. The w/h ratio of the image is fixed.

    Parameters
    ----------
    img_path : string
        The path of the image to load.

    Returns
    -------
    PyGame Surface
        The loaded and resized image file.
    int
        The width of the image.
    int
        The height of the image.
    int, int
        The margins to center the image in window.

    """
    image = pygame.image.load(img_path).convert()
    h = image.get_height() 
    w = image.get_width()


    if h / height > 1 or w / width > 1:
    # If image is not fitting in the window as it is
        if h / height > w / width:
        # If height exceeds more
            image = pygame.transform.smoothscale(image, (w * height // h, height)) 
            # resize
        else:
        # If width exceeds more or they exceed equally
            image = pygame.transform.smoothscale(image, (width, h * width // w))
            # resize
        h = image.get_height()
        w = image.get_width()
    


    img_height_margin = (height - h) // 2 # To center
    img_width_margin = (width - w) // 2 # To center
    return image, w, h, img_width_margin, img_height_margin
        
def find_frame(x, y):
    """
    Returns the index of the frame with the given coordinates. Will not handle
    if the given coordinate is in multiple boxes.

    Parameters
    ----------
    x : int
        x of the point of interest.
    y : int
        y of the point of interest.

    Returns
    -------
    int
        Index of the found frame.

    """
    for index, frame in enumerate(frames):
        if 0 <= x - frame.x <= frame.width and 0 <= y - frame.y <= frame.height:
            return index

def jsonify(frame,  img_width_margin, img_height_margin, img_width, img_height):
    """
    Converts the pixel coordinates into new coordinates where the x and y coordinates
    recalculated relative to images top-left taken as 0,0 and images bottom-right
    taken as 1,1, also height and width are now the ratio of the image's height/width
    and frame's height/width

    Parameters
    ----------
    frame : Frame
        Frame object to jsonify
    img_width_margin : int
        Margin of image to center in window.
    img_height_margin : int
        Margin of image to center in window.
    img_width : int
        Width of the current image.
    img_height : int
        Height of the current image.

    Returns
    -------
    List of floats
        A list where the attributes of the frame converted into a list of floats according to the given description.

    """
    return [(frame.x - img_width_margin)/img_width, (frame.y - img_height_margin)/img_height, frame.width/img_width, frame.height/img_height, frame.label]

def save_curr_frames():
    """
    Saves the data dict as a JSON file to the DATA_PATH given.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    with open(DATA_PATH, "w") as f:
        json.dump(data, f)

def draw_image(image, img_width_margin, img_height_margin):
    """
    This function draws the given image on screen.

    Parameters
    ----------
    image : PyGame Surface
        Image to draw.
    img_width_margin : int
        Margin to center the image.
    img_height_margin : int
        Margin to center the image.

    Returns
    -------
    None

    """
    screen.fill(bg_color) # Erase everything ( fill with background color)
    screen.blit(image, (img_width_margin, img_height_margin)) # Draw image

def draw_frames():
    """
    This function draws the frames in the global list frames with their labels.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    font = pygame.font.SysFont("comicsansms", 16, True)
    for frame in frames:
        f = pygame.Rect(frame.x, frame.y, frame.width, frame.height)
        pygame.draw.rect(screen, (255, 0, 0), f, 2)
        # Draw box in red
        text = font.render(frame.label, True, (255, 255, 255))
        text_height_margin = (frame.height - text.get_height()) // 2
        text_width_margin = (frame.width - text.get_width()) // 2
        # Margins to center the text in box
        screen.blit(text, (frame.x + text_width_margin, frame.y + text_height_margin))
        # Draw text

def draw_info(img_width_margin, img_height_margin):
    """
    This function draws the information of the selected rectangle on the information window.

    Parameters
    ----------
    img_width_margin : int
        Margin between the image and the window to center the image.
    img_height_margin :
        Margin between the image and the window to center the image.

    Returns
    -------
    None

    """
    font = pygame.font.SysFont('Comic Sans MS', 12)
    pygame.draw.line(screen, (0,0,0), (width, 0), (width, height), 2) # To seperate info window and image
    if selected_frame != None:
        f = pygame.Rect(frames[selected_frame].x, frames[selected_frame].y, frames[selected_frame].width, frames[selected_frame].height)
        pygame.draw.rect(screen, (0, 255, 0), f, 2) # Draw the selected rectangle green

        x = frames[selected_frame].x
        y = frames[selected_frame].y
        w = frames[selected_frame].width
        h = frames[selected_frame].height

        text = font.render('Top-left: (%d, %d)' % (x - img_width_margin, y - img_height_margin), False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 2))
        
        text = font.render('Top-right: (%d, %d)' % (x - img_width_margin + w, y - img_height_margin), False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 4))

        text = font.render('Bottom-left: (%d, %d)' % (x - img_width_margin, y - img_height_margin + h), False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 6))
    
        text = font.render('Bottom-right: (%d, %d)' % (x - img_width_margin + w, y - img_height_margin + h), False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 8))

        text = font.render('Width: %d' % frames[selected_frame].width, False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 10))

        text = font.render('Height: %d' % frames[selected_frame].height, False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 12))

        text = font.render('Label: ' + frames[selected_frame].label, False, (0, 0, 0))
        centered_w = (len_info - text.get_width()) // 2
        screen.blit(text,(width + centered_w, text.get_height() * 14))
        # Write the information

def select_frame(img, img_width_margin, img_height_margin):
    """
    This function handles the drag and drop frame selection event.
    
    This is the first part of a three stage labeling process. After selecting
    the frame's coordinates it gives those to a function which creates a Frame
    object that function calls the class selection function which is called
    select_label that function makes user select a label then the label
    is returned to create_frame function then with this label create_frame
    creates the Frame object and returns it to this function. The Frame
    object is added to global frames list.

    Parameters
    ----------
    img : PyGame Surface
        Currently selected image to annotate
    img_width_margin : int
        Margin between the image and the window to center the image.
    img_height_margin :
        Margin between the image and the window to center the image.

    Returns
    -------
    None

    """
    global frames   # Using global frames list
    start_pos = pygame.mouse.get_pos()  # The position when you click to select the box
    if start_pos[0] > width: start_pos = width, start_pos[1]
    # This is to prevent people from drawing frames on info window
    while True:
        """
        This loop is like a sub loop of the main drawing loop. It does
        everything the main loop does but in addition to that it draws the
        frame with updated coordinates as you drag your mouse on the window.
        """

        draw_image(img, img_width_margin, img_height_margin)    # Draws the image on screen ( centered )
        draw_frames()   # Draw the boxes created 
        draw_info(img_width_margin, img_height_margin) # Draw the info window

        ### These 3 are the default drawing funtions ###

        curr_pos = pygame.mouse.get_pos()   # Current position of the mouse
        # The frame will be drawn between the curr_pos and the start_pos
        if curr_pos[0] > width: curr_pos = width, curr_pos[1]
        # Handling the situation where the mouse is on info window
        x = min(start_pos[0], curr_pos[0])
        y = min(start_pos[1], curr_pos[1])
        w = abs(start_pos[0] - curr_pos[0])
        h = abs(start_pos[1] - curr_pos[1])
        f = pygame.Rect(x, y, w, h)
        # Deciding coordinates and creating a PyGame Rect object to draw.
        pygame.draw.rect(screen, (255, 0, 0), f, 2)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # User stopped dragging so create the frame
                frame = create_frame(x, y, w, h)
                # Currently calculated coordinates
                if frame is None: return    # If there is an error cancel
                frames += [ frame ] # Else add frame to the frames
                return  # End the function
            if event.type == pygame.QUIT:
                sys.exit()

def create_frame(x, y, w, h):
    """
    Calls a function to let user select the frames label. Then it creates
    a frame object with it and returns.

    Parameters
    ----------
    x : int
        Top-left x coordinate of the frame.
    y : int
        Top-left y coordinate of the frame.
    w : int
        Width of the frame.
    h : int
        Height of the frame.

    Returns
    -------
    Frame
        The created Frame object after drag and drop and label selection.

    """
    label = select_label(x + w, y + h, 100, 100, LABELS)
    # Function to select the label of the frame
    if label is None: return None   # Error handling
    return Frame(x, y, h, w, label)

def select_label(x, y, w, h, LABELS):
    """
    Opens a small box which consists of possible labels to select.
    It waits for the user to select a label and after the label
    is selected, returns the selected label.

    Parameters
    ----------
    x : int
        Top-left x coordinate of the label selection box.
        ( Default is the bottom right corner of the according frame. )
    y : int
        Top-left y coordinate of the label selection box.
        ( Default is the bottom right corner of the according frame. )
    w : int
        Width of the selecting box.
    h : int
        Height of the selecting box.
    LABELS : List of strings
        Possible labels to select.

    Returns
    -------
    String
        The selected label by the user.

    """
    if x + w >= width: x = width - w
    if y + h >= height: y = height - h
    # If box exceeds window limits then move it to the min distant valid point.
    per_label_h = h // len(LABELS)  # Divide to get each label box's height.
    font = pygame.font.SysFont("comicsansms", 16, True) # Set text font
    for index, label in enumerate(LABELS):
        lb = pygame.Rect(x, y + index * per_label_h, w, per_label_h)    # Label box
        pygame.draw.rect(screen, (255, 255, 255), lb, 0)
        # Draw the label box
        pygame.draw.line(screen, (0, 0, 0), (x, y + index * per_label_h), (x + w, y + index * per_label_h), 2)
        # This line is to seperate each label box
        text = font.render(label, True, (0, 0, 0))
        # Create label as a text object
        text_height_margin = (per_label_h - text.get_height()) // 2
        text_width_margin = (w - text.get_width()) // 2
        # Calculate the margins to center the text in the box
        screen.blit(text, (x + text_width_margin, y + index * per_label_h + text_height_margin))
        # Draw the text
    pygame.draw.line(screen, (0, 0, 0), (x, y + h), (x + w, y + h), 2)
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + h), 2)
    pygame.draw.line(screen, (0, 0, 0), (x + w, y), (x + w, y + h), 2)
    # Borders of label box
    pygame.display.flip() # Update screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # Return the selected label, if mouse is out of borders
                # do nothing and wait for valid selection
                curr_pos = pygame.mouse.get_pos()
                if x < curr_pos[0] < x + w and y < curr_pos[1] < y + h:
                    return LABELS[ (curr_pos[1] - y) // per_label_h ]
            if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                # Cancel the selection by pressing backspace
                return None
            if event.type == pygame.QUIT:
                sys.exit()

def check_and_do_frame_adjustment():
    """
    Checks if there is a selected frame and the valid keys are pressed,
    if so adjusts the frame accordingly.

    W - Make shorter
    S - Make Taller
    A - Make thinner
    D - Make wider
    arrows - To move the frame

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    keys = pygame.key.get_pressed() # Get pressed keys map

    if keys[pygame.K_a] and selected_frame is not None: # A to make thinner
        frames[selected_frame].width -= 1
        if frames[selected_frame].width <= 0: frames[selected_frame].width = 1
        pygame.time.delay(10)
    if keys[pygame.K_w] and selected_frame is not None: # W to make shorter
        frames[selected_frame].height -= 1
        if frames[selected_frame].height <= 0: frames[selected_frame].height = 1
        pygame.time.delay(10)
    if keys[pygame.K_d] and selected_frame is not None: # D to make wider
        frames[selected_frame].width += 1
        if frames[selected_frame].x + frames[selected_frame].width > width: frames[selected_frame].width = width - frames[selected_frame].x
        pygame.time.delay(10)
    if keys[pygame.K_s] and selected_frame is not None: # S to make taller
        frames[selected_frame].height += 1
        if frames[selected_frame].y + frames[selected_frame].height > height: frames[selected_frame].height = height - frames[selected_frame].y
        pygame.time.delay(10)
    # with size adjustements the top-left corner is always fixed

    if keys[pygame.K_LEFT] and selected_frame is not None:
        frames[selected_frame].x -= 1
        if frames[selected_frame].x <= 0: frames[selected_frame].x = 0
        pygame.time.delay(10)
    if keys[pygame.K_UP] and selected_frame is not None:
        frames[selected_frame].y -= 1
        if frames[selected_frame].y <= 0: frames[selected_frame].y = 0
        pygame.time.delay(10)
    if keys[pygame.K_RIGHT] and selected_frame is not None:
        frames[selected_frame].x += 1
        if frames[selected_frame].x + frames[selected_frame].width > width: frames[selected_frame].x = width - frames[selected_frame].width
        pygame.time.delay(10)
    if keys[pygame.K_DOWN] and selected_frame is not None:
        frames[selected_frame].y += 1
        if frames[selected_frame].y + frames[selected_frame].height > height: frames[selected_frame].y = height - frames[selected_frame].height
        pygame.time.delay(10)
    # Move the rectangle with the arrow keys


load_flag = True    # To prevent loading the image every frame
img_width = None    # Current image's width
img_height = None   # Current image's height
img = None  # Current image object
img_height_margin = None    # Margin to center the image
img_width_margin = None # Margin to center the image

while True :

    if load_flag:   # If the current image to display is not loaded to the RAM yet
        img, img_width, img_height, img_width_margin, img_height_margin = load_image(IMAGES_PATH + images[curr_img])
        # Load the image
        load_flag = False
        # Since image is loaded make the flag false so it will not be loaded
        # over and over.
    draw_image(img, img_width_margin, img_height_margin)
    draw_frames()
    draw_info(img_width_margin, img_height_margin)
    pygame.display.flip()
    # Default drawing phase

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] < width:
            # if left clicked start frame selecting process
            select_frame(img, img_width_margin, img_height_margin)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            # if right clicked on a frame, delete it
            curr_pos = pygame.mouse.get_pos()
            delete_frame(curr_pos[0], curr_pos[1])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                # if RETURN key is pressed add the frames to data dict and move to the next img
                data[images[curr_img]] = [jsonify(frame, img_width_margin, img_height_margin, img_width, img_height) for frame in frames]
                frames = [] # Empty the old images frame list
                selected_frame = None   # If there were any selected frames unselect it
                curr_img += 1 # Iterate to the next image
                load_flag = True # Since new image will be loaded make the flag True
                if curr_img == len(images):
                    # If there are no image left save and exit
                    save_curr_frames()
                    sys.exit()
            if event.key == pygame.K_t:
                # To select hover on a box and press T
                curr_pos = pygame.mouse.get_pos()
                selected_frame = find_frame(curr_pos[0], curr_pos[1])

        if event.type == pygame.QUIT:
            save_curr_frames()
            sys.exit()

    check_and_do_frame_adjustment() # Edit the selected frame with WASD and arrows
