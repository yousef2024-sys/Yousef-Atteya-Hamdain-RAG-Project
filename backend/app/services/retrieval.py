from __future__ import annotations

import re
import time
from dataclasses import dataclass
import json
from pathlib import Path


STOP_WORDS = {
    "a", "an", "and", "are", "be", "by", "for", "from", "how", "in",
    "is", "it", "of", "on", "or", "the", "to", "what", "when", "why", "with",
}


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    title: str
    section: str
    text: str


def _terms(value: str) -> list[str]:
    return [
        term
        for term in re.findall(r"[a-z0-9]+", value.lower())
        if len(term) > 2 and term not in STOP_WORDS
    ]


class Retriever:
    def __init__(self, documents_dir: Path, index_path: Path | None = None):
        if index_path and index_path.exists():
            self.chunks = self._load_index(index_path)
        else:
            self.chunks = self._load_chunks(documents_dir)

    @staticmethod
    def _load_index(index_path: Path) -> list[Chunk]:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        return [
            Chunk(
                id=item["id"],
                document_id=item["document_id"],
                title=item["title"],
                section=item["section"],
                text=item["text"],
            )
            for item in payload.get("chunks", [])
        ]

    @staticmethod
    def _load_chunks(documents_dir: Path) -> list[Chunk]:
        chunks: list[Chunk] = []
        for path in sorted(documents_dir.glob("*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            title = lines[0].removeprefix("# ").strip()
            section: str | None = None
            body: list[str] = []
            section_number = 0
            for line in lines[1:]:
                if line.startswith("## "):
                    if section and body:
                        chunks.append(
                            Chunk(
                                id=f"{path.stem}-{section_number}",
                                document_id=path.stem,
                                title=title,
                                section=section,
                                text=" ".join(body).strip(),
                            )
                        )
                    section = line.removeprefix("## ").strip()
                    body = []
                    section_number += 1
                elif section:
                    body.append(line)
            if section and body:
                chunks.append(
                    Chunk(
                        id=f"{path.stem}-{section_number}",
                        document_id=path.stem,
                        title=title,
                        section=section,
                        text=" ".join(body).strip(),
                    )
                )
        return chunks

    def search(self, question: str, top_k: int) -> list[tuple[float, Chunk]]:
        query_terms = set(_terms(question))
        ranked: list[tuple[float, Chunk]] = []
        for chunk in self.chunks:
            chunk_terms = set(_terms(f"{chunk.title} {chunk.section} {chunk.text}"))
            overlap = len(query_terms & chunk_terms)
            score = overlap / max(4, len(query_terms)) if overlap else 0.0
            if query_terms & set(_terms(chunk.section)):
                score += 0.12
            ranked.append((min(score, 0.99), chunk))
        return sorted(ranked, key=lambda item: item[0], reverse=True)[:top_k]

    def answer(self, question: str, top_k: int = 3) -> dict:
        started = time.perf_counter()
        ranked = self.search(question, top_k)
        grounded = any(score >= 0.08 for score, _ in ranked)
        sources = [
            {
                "id": chunk.id,
                "title": chunk.title,
                "section": chunk.section,
                "excerpt": chunk.text[:300].rstrip() + ("…" if len(chunk.text) > 300 else ""),
                "score": round(score, 2),
                "document_type": "Study guide",
            }
            for score, chunk in ranked
            if score > 0
        ]
        if not grounded:
            answer = (
                f'I could not find enough evidence in the StudyMate library to answer '
                f'"{question}" reliably.'
            )
        else:
            best = next(chunk for score, chunk in ranked if score >= 0.08)
            answer = f"Based on the StudyMate library, {best.text} [{best.section}]."
        return {
            "answer": answer,
            "sources": sources,
            "related_questions": [
                "How does chunking affect grounded answers?",
                "How do I evaluate retrieval separately from generation?",
            ],
            "retrieval": {
                "query": question,
                "chunks_considered": len(self.chunks),
                "latency_ms": max(1, round((time.perf_counter() - started) * 1000)),
                "model": "tfidf-local-v1",
                "grounded": grounded,
            },
        }