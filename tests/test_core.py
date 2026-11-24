"""Unit tests for hilite.core.

Each test checks one promise from a docstring: Returns, Raises, or Examples.
Images are made in memory with Pillow, and any file is written to tmp_path,
so the tests never read from or write into the repository.
"""

import pytest
from PIL import Image

from hilite import (
    crop_regions,
    enhance_document,
    find_highlights,
    load_image,
    make_review_sheet,
)


# ---------- enhance_document ----------

def make_gray_photo():
    """A dull photo: light gray paper with a dark gray line of "text"."""
    image = Image.new("RGB", (800, 600), (170, 170, 170))
    for x in range(100, 700):
        for y in range(290, 310):
            image.putpixel((x, y), (90, 90, 90))
    return image


def test_enhance_document_keeps_size():
    # normal: the docstring example, 800 x 600 in, 800 x 600 out
    photo = make_gray_photo()
    assert enhance_document(photo).size == (800, 600)


def test_enhance_document_returns_rgb_image():
    photo = make_gray_photo()
    enhanced = enhance_document(photo)
    assert isinstance(enhanced, Image.Image)
    assert enhanced.mode == "RGB"


def test_enhance_document_does_not_change_input():
    # Returns: "The input image is not changed."
    photo = make_gray_photo()
    before = photo.tobytes()
    enhance_document(photo)
    assert photo.tobytes() == before


def test_enhance_document_increases_contrast():
    # the paper gets brighter and the text gets darker
    photo = make_gray_photo()
    enhanced = enhance_document(photo)
    paper = enhanced.getpixel((10, 10))
    text = enhanced.getpixel((400, 300))
    assert paper[0] > 170
    assert text[0] < 90


def test_enhance_document_keeps_yellow_yellow():
    # the comment in the code: preserve_tone keeps yellow highlights yellow
    photo = make_gray_photo()
    for x in range(100, 300):
        for y in range(100, 120):
            photo.putpixel((x, y), (230, 220, 80))
    red, green, blue = enhance_document(photo).getpixel((200, 110))
    assert red > blue and green > blue


def test_enhance_document_accepts_one_color_image():
    # boundary: a blank page, the smallest contrast possible
    blank = Image.new("RGB", (1, 1), (200, 200, 200))
    assert enhance_document(blank).size == (1, 1)


# ---------- crop_regions ----------

def test_crop_regions_docstring_example():
    # normal: the docstring example, one box gives one crop
    image = Image.new("RGB", (800, 600), "white")
    crops = crop_regions(image, [(50, 100, 400, 140)])
    assert len(crops) == 1


def test_crop_regions_adds_margin():
    # box 350 x 40, plus 10 pixels on every side
    image = Image.new("RGB", (800, 600), "white")
    crops = crop_regions(image, [(50, 100, 400, 140)], margin=10)
    assert crops[0].size == (370, 60)


def test_crop_regions_keeps_order():
    image = Image.new("RGB", (800, 600), "white")
    boxes = [(0, 0, 100, 10), (0, 200, 50, 220)]
    crops = crop_regions(image, boxes, margin=0)
    assert [crop.size for crop in crops] == [(100, 10), (50, 20)]


def test_crop_regions_margin_stops_at_image_edge():
    # boundary: a box at the corner, the margin must not go past the edge
    image = Image.new("RGB", (100, 100), "white")
    crops = crop_regions(image, [(0, 0, 10, 10)], margin=10)
    assert crops[0].size == (20, 20)


def test_crop_regions_with_no_boxes():
    # boundary: an empty list gives an empty list
    image = Image.new("RGB", (100, 100), "white")
    assert crop_regions(image, []) == []


def test_crop_regions_refuses_negative_margin():
    image = Image.new("RGB", (100, 100), "white")
    with pytest.raises(ValueError):
        crop_regions(image, [(0, 0, 10, 10)], margin=-1)


def test_crop_regions_refuses_box_outside_image():
    image = Image.new("RGB", (100, 100), "white")
    with pytest.raises(ValueError):
        crop_regions(image, [(50, 50, 150, 80)])


def test_crop_regions_refuses_box_with_no_area():
    image = Image.new("RGB", (100, 100), "white")
    with pytest.raises(ValueError):
        crop_regions(image, [(10, 10, 10, 20)])


# ---------- make_review_sheet ----------

def test_make_review_sheet_returns_path(tmp_path):
    # normal: the docstring example, it returns the path it saved to
    out = tmp_path / "review_sheet.png"
    crops = [Image.new("RGB", (350, 40), "yellow")]
    assert make_review_sheet(crops, out) == str(out)
    assert out.exists()


def test_make_review_sheet_stacks_top_to_bottom(tmp_path):
    out = tmp_path / "review.png"
    crops = [
        Image.new("RGB", (100, 10), "red"),
        Image.new("RGB", (50, 20), "blue"),
    ]
    make_review_sheet(crops, out)
    sheet = Image.open(out)
    # width of the widest crop, height of all crops together
    assert sheet.size == (100, 30)
    # the first crop is on top, the second one below it
    assert sheet.getpixel((0, 0)) == (255, 0, 0)
    assert sheet.getpixel((0, 15)) == (0, 0, 255)


def test_make_review_sheet_refuses_empty_list(tmp_path):
    with pytest.raises(ValueError):
        make_review_sheet([], tmp_path / "review.png")


def test_make_review_sheet_raises_oserror_when_it_cannot_save(tmp_path):
    crops = [Image.new("RGB", (10, 10), "yellow")]
    with pytest.raises(OSError):
        make_review_sheet(crops, tmp_path / "no_such_folder" / "review.png")
# ---------- load_image ----------

def test_load_image_returns_rgb(tmp_path):
    # normal: a grayscale PNG is loaded as RGB, like the docstring example
    path = tmp_path / "notes.png"
    Image.new("L", (20, 10), 128).save(path)
    image = load_image(path)
    assert image.mode == "RGB"
    assert image.size == (20, 10)


def test_load_image_reads_jpg(tmp_path):
    path = tmp_path / "notes.jpg"
    Image.new("RGB", (20, 10), "white").save(path)
    assert load_image(path).mode == "RGB"


def test_load_image_refuses_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_image(tmp_path / "no_such_file.jpg")


def test_load_image_refuses_file_that_is_not_an_image(tmp_path):
    path = tmp_path / "notes.jpg"
    path.write_text("this is not an image")
    with pytest.raises(ValueError):
        load_image(path)


def test_load_image_applies_phone_rotation(tmp_path):
    # a phone photo saved 40 x 20 with EXIF "rotate 90", shown as 20 x 40
    path = tmp_path / "phone.jpg"
    photo = Image.new("RGB", (40, 20), "white")
    exif = photo.getexif()
    exif[0x0112] = 6  # Orientation: rotate 90 degrees clockwise
    photo.save(path, exif=exif)
    assert load_image(path).size == (20, 40)


# ---------- find_highlights ----------

YELLOW = (255, 240, 60)


def page_with_highlights(boxes):
    """A white page with a yellow rectangle at each (left, top, right, bottom)."""
    page = Image.new("RGB", (400, 300), "white")
    for left, top, right, bottom in boxes:
        page.paste(YELLOW, (left, top, right, bottom))
    return page


def test_find_highlights_finds_one_region():
    page = page_with_highlights([(50, 100, 200, 120)])
    boxes = find_highlights(page)
    assert len(boxes) == 1
    left, top, right, bottom = boxes[0]
    # the box covers the yellow area (a few pixels of slack are fine)
    assert left <= 52 and top <= 102 and right >= 198 and bottom >= 118


def test_find_highlights_sorts_top_to_bottom():
    # the lower highlight is drawn first, but must come second
    page = page_with_highlights([(50, 200, 200, 220), (50, 50, 200, 70)])
    boxes = find_highlights(page)
    assert len(boxes) == 2
    assert boxes[0][1] < boxes[1][1]


def test_find_highlights_returns_empty_list_without_highlights():
    # boundary: a page with no yellow at all
    assert find_highlights(Image.new("RGB", (400, 300), "white")) == []


def test_find_highlights_refuses_gray_image():
    with pytest.raises(ValueError):
        find_highlights(Image.new("L", (400, 300), 255))


def test_find_highlights_reads_one_line_left_to_right():
    # the right highlight is 3 pixels higher, but both are on the same line
    page = page_with_highlights([(250, 100, 350, 120), (20, 103, 120, 123)])
    boxes = find_highlights(page)
    assert [box[0] < 200 for box in boxes] == [True, False]
