#!/usr/bin/env python3
"""
A simple text analyzer that counts word frequency.

This script accepts either a path to a text file as a command‑line argument
or prompts the user to enter a path or paste text directly. It removes
punctuation, converts all words to lower case and uses a Counter to tally
word occurrences. After analysing, it prints the ten most common words
along with their counts.

Usage:
    python text_analyzer.py path/to/file.txt

If no file is supplied, the program will ask the user whether to supply a
file path or paste text manually.
"""

import string
import sys
from collections import Counter
from typing import Iterable, Tuple


def read_text_from_file(path: str) -> str:
    """Read the contents of a file.

    Args:
        path: The path to a UTF‑​8 encoded text file.

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnicodeDecodeError: If the file contains invalid encoding.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def tokenize(text: str) -> Iterable[str]:
    """Split text into lowercase words, stripping punctuation."""
    translator = str.maketrans('', '', string.punctuation)
    # Remove punctuation and convert to lowercase
    normalized = text.translate(translator).lower()
    # Split on whitespace
    for word in normalized.split():
        if word:
            yield word


def analyze_words(words: Iterable[str]) -> Counter:
    """Count the occurrences of words using a Counter."""
    return Counter(words)


def display_top_words(counter: Counter, top_n: int = 10) -> None:
    """Print the most common words and their counts."""
    print(f"Top {top_n} words:\n")
    for i, (word, count) in enumerate(counter.most_common(top_n), start=1):
        print(f"{i:2}. {word:<15} — {count}")


def prompt_for_text() -> str:
    """Prompt the user to enter a block of text via the console."""
    print(
        "Enter/paste your text. When you're done, press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows)."
    )
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        # User signalled end of input
        pass
    print()  # extra line break
    return "\n".join(lines)


def main(argv: Iterable[str]) -> None:
    """Parse arguments, read text and display analysis."""
    if len(argv) >= 2:
        # If a file path is provided as the first argument
        path = argv[1]
        try:
            text = read_text_from_file(path)
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            return
        except UnicodeDecodeError:
            print(f"Error: could not decode file '{path}'. Ensure it is UTF‑​8 encoded.")
            return
    else:
        # Interactive prompt
        choice = input(
            "Do you want to analyze a file or paste text? (f/p): "
        ).strip().lower()
        if choice == 'f':
            path = input("Enter the path to the text file: ").strip()
            try:
                text = read_text_from_file(path)
            except FileNotFoundError:
                print(f"Error: file '{path}' not found.")
                return
            except UnicodeDecodeError:
                print(f"Error: could not decode file '{path}'. Ensure it is UTF‑​8 encoded.")
                return
        else:
            text = prompt_for_text()
    words = list(tokenize(text))
    if not words:
        print("No words found to analyze.")
        return
    counter = analyze_words(words)
    display_top_words(counter)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)
