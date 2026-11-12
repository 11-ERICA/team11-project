"""Core functions of hilite. Docstrings first; code comes in Week 11."""


def load_image(path):
    """Load a photo of notes as a color image.

    TODO(Usukhjargal111): write Args, Returns, Raises, Examples.
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

    TODO(yj-min-i): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError


def crop_regions(image, boxes, margin=10):
    """Cut the highlighted regions out of the enhanced image.

    TODO(songsongjiwoo): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError


def make_review_sheet(crops, out_path):
    """Stack the cropped regions into one review image and save it.

    TODO(yeojin1115-eng): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError
