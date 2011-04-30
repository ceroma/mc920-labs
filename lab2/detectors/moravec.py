import sys
from PIL import Image

def draw_point(image, x, y, radius = 1):
    """Draw a point centered at (x, y) with specified radius."""
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            image.putpixel((x+dx, y+dy), 255)

def draw_corners(image, corners_map):
    """Draw a point for each possible corner."""
    for corner in corners_map:
        draw_point(image, corner[0], corner[1])

def moravec(image, threshold = 100):
    """Moravec's corner detection for each pixel of the image."""

    corners = []
    xy_shifts = [(1, 0), (1, 1), (0, 1), (-1, 1)]

    for y in range(1, image.size[1]-1):
        for x in range(1, image.size[0]-1):
            # Look for local maxima in min(E) above threshold:
            E = 100000
            for shift in xy_shifts:
                diff = image.getpixel((x + shift[0], y + shift[1]))
                diff = diff - image.getpixel((x, y))
                diff = diff * diff
                if diff < E:
                    E = diff
            if E > threshold:
                corners.append((x, y))

    return corners

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python moravec.py [-t threshold] image[s]..."
    else:
        # Threshold:
        if "-t" in sys.argv:
            threshold = int(sys.argv[sys.argv.index("-t") + 1])
        else:
            threshold = 100

        # Find corners:
        for arg in sys.argv:
            if arg[-4:].lower() in (".jpg", ".png"):
                image = Image.open(arg).convert("L")
                corners = moravec(image, threshold)
                draw_corners(image, corners)
                image.save(arg[:-4] + "_t" + str(threshold) + arg[-4:])
