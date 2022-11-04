#!/usr/bin/env python

# -*- coding: utf-8 -*-
from PIL import Image
from pathlib import Path
from glob import glob
import os
import shutil
import sys

Pixel = tuple[int, int, int]
Alpha_Pixel = tuple[int, int, int, int]


def remove_background(
    image_file: Path,
    background_color: Pixel = (0, 0, 0),
    foreground_color: Pixel = (255, 255, 255),
    sharpen: bool = True,
) -> None:
    """
    Doc String for remove_background
    """
    new_stem = image_file.stem + "-no_background" + image_file.suffix
    newfile = image_file.parent / new_stem
    img = Image.open(image_file)
    image = img.convert("RGBA")
    newImage = []
    for pixel in image.getdata():
        if sharpen:
            sharpen_pixel(pixel, foreground_color)
        if pixel == background_color + (255,):
            newImage.append(foreground_color + (255,))
        else:
            newImage.append(pixel)
    image.putdata(newImage)
    image.save(newfile)


def sharpen_pixel(alpha_pixel: Alpha_Pixel, foreground_color: Pixel) -> Alpha_Pixel:
    """
    Doc String for sharpen_pixel
    """
    if alpha_pixel[3] > 0:
        return foreground_color + (255,)
    else:
        return alpha_pixel


def change_pixel(
    alpha_pixel: Alpha_Pixel, foreground_color: Pixel, background_color: Pixel
) -> Alpha_Pixel:
    """
    Doc String for change_pixel
    """
    import logging  # Only here as reminder for future. Because it should check

    # Need to check color and set alpha to either 0 or 255 depending. See below
    logging.info(foreground_color)
    if alpha_pixel == background_color + (255,):
        return background_color + (0,)
    else:
        return alpha_pixel


def rename():
    files = glob("*")
    for file in files:
        tmp = file.replace("icons8-", "")
        tmp = tmp.replace("_nobackground", "")
        tmp = tmp.replace("_static", "")
        os.rename(file, tmp)
    return


def png():
    name = "icons8-play-96.png"
    threshold = 100
    img = Image.open(name)
    newImage = []
    for pix in img.getdata():
        if pix[3] > 0:
            newImage.append((255, 255, 255, pix[3]))
        else:
            newImage.append(pix)
    img.putdata(newImage)
    img.save("test.png")


def main(dirname="", threshold=100, main_color=(0, 0, 0)):
    """
    main Converts all Gifs in a folder to be transparent.

    Args:
        dirname (list): Path containing files where the gifs are located. Defaults to all in current path.
        threshold (int): An integer used to separate the blacks from the whites of the gifs.
    """

    gifs = glob(os.path.join(dirname, "*gif"))
    for gif_name in gifs:
        gif = Image.open(gif_name)
        name = os.path.basename(gif_name).split(".")[0]
        tmp_dir = "tmp_gifs_dir"

        if not os.path.exists(os.path.join(dirname, tmp_dir)):
            os.makedirs(os.path.join(dirname, tmp_dir))

        # Extract and Save Frames
        for frame in range(gif.n_frames):
            gif.seek(frame)
            # Transparency
            gframe = gif.convert("RGBA")
            datas = gframe.getdata()
            newImage = []
            for item in datas:
                # if item[0] < threshold or item[1] < threshold or item[2] < threshold:
                if item[3] > 0:
                    # newImage.append((item[0], item[1], item[2], 0)) # Dont sharpen
                    if main_color == (0, 0, 0):
                        newImage.append((0, 0, 0, 255))  # Sharpen
                    elif main_color == (255, 255, 255):
                        newImage.append((255, 255, 255, 0))  # Sharpen
                        # newImage.append((0, 0, 0, 0)) # Color Flipping
                    else:
                        newImage.append(
                            (main_color[0], main_color[1], main_color[2], item[3])
                        )
                else:
                    # newImage.append(item) # What was before or sharpen the image with:
                    if main_color == (0, 0, 0):
                        newImage.append((255, 255, 255, 0))  # Sharpen
                    elif main_color == (255, 255, 255):
                        newImage.append((0, 0, 0, 255))  # Sharpen
                        # newImage.append((255, 255, 255, 255)) # Color Flipping
                    else:
                        newImage.append((255, 255, 255, 0))

            gframe.putdata(newImage)
            gframe.save(
                os.path.join(dirname, tmp_dir, f"frame{str(frame).zfill(2)}.png")
            )

        images = glob(os.path.join(dirname, tmp_dir, f"frame*.png"))
        first_frame = Image.open(images[0])
        first_frame.save(os.path.join(dirname, f"{name}_nobackground.png"))
        gif_frames = []
        for image in images[1:]:
            gif_frames.append(Image.open(image))

        # Transparency color: 1 for white, and 0 for black  or red apparently
        transparency = 0
        if main_color == (255, 255, 255):
            transparency = 1
        first_frame.save(
            os.path.join(dirname, f"{name}_nobackground.gif"),
            format="GIF",
            save_all=True,
            append_images=gif_frames,
            duration=gif.info["duration"],
            loop=0,
            transparency=transparency,
            disposal=2,
        )
        print(f"Completed: {name}")
        shutil.rmtree(os.path.join(dirname, tmp_dir))


if __name__ == "__main__":
    main(sys.argv[1])
