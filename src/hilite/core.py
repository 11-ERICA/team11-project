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

    TODO(songsongjiwoo): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError


def make_review_sheet(crops, out_path):
    """Stack the cropped regions into one review image and save it.

    TODO(yeojin1115-eng): write Args, Returns, Raises, Examples.
    """
    raise NotImplementedError
