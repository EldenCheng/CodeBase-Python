import colorsys

from PIL import Image, ImageDraw


def get_rgb(snapshot_path):
    """
    Check the color of the element from the element snapshot
    :param snapshot_path:
    :return: int tuple, the r, g, b value
    """
    try:
        image = Image.open(snapshot_path)
        image = image.convert('RGB')
        max_score = 0.0001
        dominant_color = None
        for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)

            if y > 0.9:
                continue
            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)
        return dominant_color

    except Exception as msg:
        raise Exception(msg)


def get_colors(infile, outfile, numcolors=10, swatchsize=20, resize=150):

    image = Image.open(infile)
    # image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE)
    result.putalpha(0)
    colors = result.getcolors()

    #print(colors)

    # Save colors to file

    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
    draw = ImageDraw.Draw(pal)

    posx = 0
    for count, col in colors:
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
        posx = posx + swatchsize
        if count > 100:
            print(str(col), ": " + str(count))

    del draw
    pal.save(outfile, "PNG")

if __name__ == '__main__':
    get_colors('2.png', 'outfile1.png', numcolors=6)
