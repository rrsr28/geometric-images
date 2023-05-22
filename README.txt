# Geometric Image Canvas

The "Geometric Image Canvas" is a PyQt-based application that allows users to render and manipulate geometric images on a canvas. It provides two main features:

1. Render Image: Clicking the "Render Image" button downloads a random geometric image from an open-source repository and renders it at a random location on the canvas. The images are selectable and movable within the canvas.
2. Group Images: The "Group Images" button enables users to select multiple images on the canvas and group them together as a single object. Once grouped, the images move as a cohesive unit.

## Requirements

- Python 3.x
- PyQt6 library
- requests library
- BeautifulSoup library

## How to Use

1. Clone the repository or download the source code files.
2. Install the required libraries mentioned above.
3. Run the main script `main.py` using Python.
4. The application window will open with a canvas and two buttons: "Render Image" and "Group Images".
5. Click the "Render Image" button to download and render a random geometric image on the canvas. The image will appear at a random location and can be moved by clicking and dragging it.
6. Repeat step 5 to render more images on the canvas. Each new image will be placed at a random location, and all images can be individually moved.
7. To group multiple images as a single object, click the "Group Images" button. The all images will then move together as a group.
8. The image information, including size and dominant color, will be displayed below the canvas.

## Additional Notes

- The code fetches geometric images from the open-source repository mentioned in the code. Ensure you have an internet connection to download the images.
- The application supports resizing of the window, and the canvas will adjust accordingly.
- Further improvements can be made to the user interface (UI) and functionality, as mentioned in the code's TODO section.

## Author

This code was authored by Sanjay Ram RR.

