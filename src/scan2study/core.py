"""Core functions for Scan2Study."""


def extract_text(file_path: str) -> str:
    """Extract text from an image or PDF.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Extracted text.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is unsupported.
    """
    raise NotImplementedError


def clean_text(text: str) -> str:
    """Clean and organize extracted text.

    Args:
        text (str): Raw extracted text.

    Returns:
        str: Cleaned text.

    Raises:
        ValueError: If the input is empty.
    """
    raise NotImplementedError


def generate_summary(text: str, max_sentences: int = 5) -> str:
    """Generate a concise study summary.

    Args:
        text (str): Learning material.
        max_sentences (int): Maximum number of sentences.

    Returns:
        str: Generated summary.

    Raises:
        ValueError: If the input or sentence limit is invalid.
    """
    raise NotImplementedError


def generate_flashcards(
    text: str, count: int = 10
) -> list[dict[str, str]]:
    """Generate question-and-answer flashcards.

    Args:
        text (str): Learning material.
        count (int): Number of flashcards.

    Returns:
        list[dict[str, str]]: Generated flashcards.

    Raises:
        ValueError: If the input or count is invalid.
    """
    raise NotImplementedError
