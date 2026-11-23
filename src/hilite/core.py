"""Core functions of hilite. Docstrings first; code comes in Week 11."""

from PIL import Image, ImageEnhance, ImageOps


def load_image(path):
    """Load a photo of notes as a color image.

    Args:
        path (str): Path to the image file.

    Returns:
        image (PIL.Image.Image): The image in RGB color.

    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the image cannot be opened.

    Examples:
        >>> load_image("examples/lecture_notes.jpg").mode
        'RGB'
    """
    raise NotImplementedError



def find_highlights(image):
    """Find yellow highlighted regions in the original photo.

    Args:
        image (PIL.Image.Image): The original color image to analyze.

    Returns:
        boxes (list[tuple[int, int, int, int]]): A list of bounding boxes in
            (left, top, right, bottom) pixel coordinates. The boxes
            are sorted from top to bottom and then from left to right.
            Returns an empty list if no highlighted regions are found.

    Raises:
        ValueError: If the input image is not a color image.

    Examples:
        >>> boxes = find_highlights(image)
        >>> len(boxes)
        2
    """
    raise NotImplementedError



def enhance_document(image):
    """Adjust brightness and contrast so the text is easier to read.

    Args:
        image (PIL.Image.Image): The original color photo from
            ``load_image``.

    Returns:
        enhanced (PIL.Image.Image): A new image with adjusted brightness and
            contrast. It has the same size as ``image``. The input image
            is not changed.

    Examples:
        >>> photo = load_image("examples/lecture_notes.jpg")  # 800 x 600
        >>> enhance_document(photo).size
        (800, 600)
    """
    # Work on an RGB copy so the input image is not changed.
    rgb = image.convert("RGB")
    # Stretch the darkest and brightest 1% to the full range.
    # preserve_tone keeps the colors, so yellow highlights stay yellow.
    stretched = ImageOps.autocontrast(rgb, cutoff=1, preserve_tone=True)
    # Add a little more contrast so the text stands out.
    enhanced = ImageEnhance.Contrast(stretched).enhance(1.2)
    return enhanced


def crop_regions(image, boxes, margin=10):
    """Cut the highlighted regions out of the enhanced image.

    Args:
        image (PIL.Image.Image): The enhanced document image.
        boxes (list[tuple[int, int, int, int]]): Highlighted regions as
            (left, top, right, bottom) pixel coordinates, in the order
            they appear in the original photo.
        margin (int): Extra pixels kept around each region so the text
            is not cut off. Must be 0 or more. Defaults to 10.

    Returns:
        crops (list[PIL.Image.Image]): One cropped image per box, in the same
            order as ``boxes``.

    Raises:
        ValueError: If ``margin`` is negative, a box is outside the image,
            or a box has no area.

    Examples:
        >>> crops = crop_regions(image, [(50, 100, 400, 140)])
        >>> len(crops)
        1
    """
    if margin < 0:
        raise ValueError(f"margin must be 0 or more, got {margin}")

    width, height = image.size
    crops = []
    for box in boxes:
        left, top, right, bottom = box
        if left < 0 or top < 0 or right > width or bottom > height:
            raise ValueError(f"box {box} is outside the image size {image.size}")
        if left >= right or top >= bottom:
            raise ValueError(f"box {box} has no area")

        # Add the margin, but never go past the image edges.
        crop_box = (
            max(0, left - margin),
            max(0, top - margin),
            min(width, right + margin),
            min(height, bottom + margin),
        )
        crops.append(image.crop(crop_box))
    return crops



def make_review_sheet(crops, out_path):
    """Stack the cropped regions into one review image and save it.

    Args:
        crops (list[PIL.Image.Image]): Images returned by ``crop_regions``.
            They are stacked from top to bottom in the order provided.
        out_path (str): Path to the output image file.

    Returns:
        path (str): The path to the saved review image.

    Raises:
        ValueError: If ``crops`` is empty.
        OSError: If the review image cannot be saved.

    Examples:
        >>> crops = crop_regions(enhanced_image, [(50, 100, 400, 140)])
        >>> make_review_sheet(crops, "review_sheet.png")
        'review_sheet.png'
    """
    if not crops:
        raise ValueError("crops must not be empty")

    width = max(crop.width for crop in crops)
    height = sum(crop.height for crop in crops)
    sheet = Image.new("RGB", (width, height), "white")

    y = 0
    for crop in crops:
        sheet.paste(crop, (0, y))
        y += crop.height

    sheet.save(out_path)
    return str(out_path)
