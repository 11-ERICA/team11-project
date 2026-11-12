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

    Args:
        crops (list[PIL.Image.Image]): Images returned by ``crop_regions``.
            They are stacked from top to bottom in the order provided.
        out_path (str): Path to the output image file.

    Returns:
        str: The path to the saved review image.

    Raises:
        ValueError: If ``crops`` is empty.
        OSError: If the review image cannot be saved.

    Examples:
        >>> crops = crop_regions(enhanced_image, [(50, 100, 400, 140)])
        >>> make_review_sheet(crops, "review_sheet.png")
        'review_sheet.png'
    """
    raise NotImplementedError
