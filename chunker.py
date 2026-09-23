"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?
    """
    target_words = 180
    max_words = 200
    overlap_words = 25

    chunks: list[Chunk] = []
    for doc in documents:
        sections = _semantic_sections(doc.text)
        current: list[str] = []
        current_words = 0
        index = 0

        for section in sections:
            section_words = len(section.split())

            if section_words > max_words:
                if current:
                    chunks.append(_make_chunk(doc, current, index))
                    index += 1
                    current = []
                    current_words = 0

                for piece in _split_long_section(section, max_words, overlap_words):
                    chunks.append(
                        Chunk(
                            text=piece,
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                continue

            would_exceed = current and current_words + section_words > max_words
            good_place_to_stop = current_words >= target_words
            if would_exceed or good_place_to_stop:
                chunks.append(_make_chunk(doc, current, index))
                index += 1
                current = []
                current_words = 0

            current.append(section)
            current_words += section_words

        if current:
            chunks.append(_make_chunk(doc, current, index))

    return chunks


def _semantic_sections(text: str) -> list[str]:
    """Prefer paragraph breaks, then sentence breaks, over raw character cuts."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    sections: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph.split()) <= 200:
            sections.append(paragraph)
        else:
            sections.extend(_sentences(paragraph))
    return sections


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _split_long_section(text: str, max_words: int, overlap_words: int) -> list[str]:
    words = text.split()
    pieces: list[str] = []
    start = 0
    step = max_words - overlap_words

    while start < len(words):
        piece = " ".join(words[start : start + max_words]).strip()
        if piece:
            pieces.append(piece)
        if start + max_words >= len(words):
            break
        start += step

    return pieces


def _make_chunk(doc: Document, parts: list[str], index: int) -> Chunk:
    return Chunk(
        text="\n\n".join(parts).strip(),
        source=doc.source,
        index=index,
        produced_by="chunker.py::split_documents",
    )


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
