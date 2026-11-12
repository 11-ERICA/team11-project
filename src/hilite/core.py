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

    TODO(oblgudei-spec): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError


def enhance_document(image):
    """Adjust brightness and contrast so the text is easier to read.

    TODO(yj-min-i): write Args, Returns, Raises, Examples.
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
        list[PIL.Image.Image]: One cropped image per box, in the same
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
