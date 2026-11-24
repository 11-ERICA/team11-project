"""Core functions of hilite."""

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
    try:
        with Image.open(path) as img:
            return ImageOps.exif_transpose(img).convert("RGB")

    except FileNotFoundError:
        raise

    except (OSError, ValueError) as e:
        raise ValueError(f"Cannot open image: {path}") from e
    

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

    if image.mode not in ("RGB", "RGBA", "P", "CMYK"):
        raise ValueError("Input image must be a color image.")

    image = image.convert("RGB")
    width, height = image.size
    pixels = image.load()

    # Create a mask for yellow highlight pixels.
    mask = bytearray(width * height)

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if (
                r >= 160
                and g >= 140
                and b <= 150
                and r > b * 1.25
                and g > b * 1.15
            ):
                mask[y * width + x] = 1

    # Find connected yellow regions.
    visited = bytearray(width * height)
    boxes = []
    min_area = max(8, int(width * height * 0.000005))

    for start in range(width * height):
        if not mask[start] or visited[start]:
            continue

        queue = [start]
        visited[start] = 1
        min_x = max_x = start % width
        min_y = max_y = start // width
        area = 0

        while queue:
            current = queue.pop()
            x = current % width
            y = current // width
            area += 1

            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < width and 0 <= ny < height:
                        neighbor = ny * width + nx

                        if mask[neighbor] and not visited[neighbor]:
                            visited[neighbor] = 1
                            queue.append(neighbor)

        if area >= min_area:
            boxes.append((min_x, min_y, max_x + 1, max_y + 1))

    # Group regions by vertical center, then sort each row left to right.
    rows = []

    for box in sorted(boxes, key=lambda box: (box[1] + box[3]) / 2):
        center_y = (box[1] + box[3]) / 2

        if rows and rows[-1][0] <= center_y <= rows[-1][1]:
            rows[-1][2].append(box)
            rows[-1][1] = max(rows[-1][1], box[3])
        else:
            rows.append([box[1], box[3], [box]])

    boxes = []
    for row in rows:
        boxes.extend(sorted(row[2], key=lambda box: box[0]))

    return boxes



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
