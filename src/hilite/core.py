"""Core functions of hilite. Docstrings first; code comes in Week 11."""


def load_image(path):
    """Load a photo of notes as a color image.

    Args:
        path (str): Path to the image file.

    Returns:
        PIL.Image.Image: The image in RGB color.

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
        list[tuple[int, int, int, int]]: A list of bounding boxes in
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
        PIL.Image.Image: A new image with adjusted brightness and
            contrast. It has the same size as ``image``. The input image
            is not changed.

    Examples:
        >>> photo = load_image("examples/lecture_notes.jpg")  # 800 x 600
        >>> enhance_document(photo).size
        (800, 600)
    """
    raise NotImplementedError


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
        crops(list[PIL.Image.Image]): One cropped image per box, in the same
            order as ``boxes``.

    Raises:
        ValueError: If ``margin`` is negative or a box is outside the image.

    Examples:
        >>> crops = crop_regions(image, [(50, 100, 400, 140)])
        >>> len(crops)
        1
    """
    raise NotImplementedError



def make_review_sheet(crops, out_path):
    """Stack the cropped regions into one review image and save it.

    TODO(yeojin1115-eng): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError
