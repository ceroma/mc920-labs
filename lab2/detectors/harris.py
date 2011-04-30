from PIL import Image
import math, numpy, sys

def draw_point(image, x, y, radius = 1):
    """Draw a point centered at (x, y) with specified radius."""
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            image.putpixel((x+dx, y+dy), 255)

def draw_corners(image, corners_map):
    """Draw a point for each possible corner."""
    for corner in corners_map:
        draw_point(image, corner[0], corner[1])

def harris(image, threshold = 100000000, sigma = 1.5, k = 0.04):
    """Harris' corner detection for each pixel of the image."""

    corners = []

    # Calculate gradients:
    X2 = [[0] * image.size[0] for y in xrange(image.size[1])]
    Y2 = [[0] * image.size[0] for y in xrange(image.size[1])]
    XY = [[0] * image.size[0] for y in xrange(image.size[1])]
    for y in xrange(1, image.size[1]-1):
        for x in xrange(1, image.size[0]-1):
            X = image.getpixel((x + 1, y)) - image.getpixel((x - 1, y))
            Y = image.getpixel((x, y + 1)) - image.getpixel((x, y - 1))

            X2[y][x] = X * X
            Y2[y][x] = Y * Y
            XY[y][x] = X * Y

    # Gaussian 3x3:
    G = [[0,0,0], [0,0,0], [0,0,0]]
    for y in xrange(3):
        for x in xrange(3):
            u, v = x-1, y-1
            G[y][x] = (math.exp(-(u*u + v*v)/(2*sigma*sigma)))

    # Convolve with Gaussian 3x3:
    A = [[0] * image.size[0] for y in xrange(image.size[1])]
    B = [[0] * image.size[0] for y in xrange(image.size[1])]
    C = [[0] * image.size[0] for y in xrange(image.size[1])]
    for y in xrange(1, image.size[1]-1):
        for x in xrange(1, image.size[0]-1):
            for i in xrange(3):
                for j in xrange(3):
                    u, v = j-1, i-1
                    A[y][x] = A[y][x] + X2[y + v][x + u] * G[i][j]
                    B[y][x] = B[y][x] + Y2[y + v][x + u] * G[i][j]
                    C[y][x] = C[y][x] + XY[y + v][x + u] * G[i][j]
    del X2, Y2, XY

    # Harris Response Function:
    R = [[0] * image.size[0] for y in xrange(image.size[1])]
    for y in xrange(image.size[1]):
        for x in xrange(image.size[0]):
            a, b, c = A[y][x], B[y][x], C[y][x]
            Tr = a + b
            Det = a * b - c * c
            R[y][x] = Det - k * Tr * Tr
    del A, B, C

    # Suppress Non-Maximum Points:
    for y in xrange(1, image.size[1]-1):
        for x in xrange(1, image.size[0]-1):
            maximum = True
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if R[y][x] < R[y + dy][x + dx]:
                        maximum = False 
            if maximum and R[y][x] > threshold:
                corners.append((x, y))
            
    return corners

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python harris.py [-t threshold] image[s]..."
    else:
        # Threshold:
        if "-t" in sys.argv:
            threshold = int(sys.argv[sys.argv.index("-t") + 1])
        else:
            threshold = 100000000

        # Find corners:
        for arg in sys.argv:
            if arg[-4:].lower() in (".jpg", ".png"):
                image = Image.open(arg).convert("L")
                corners = harris(image, threshold)
                draw_corners(image, corners)
                image.save(arg[:-4] + "_t" + str(threshold) + arg[-4:])

