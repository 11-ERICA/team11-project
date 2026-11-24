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
