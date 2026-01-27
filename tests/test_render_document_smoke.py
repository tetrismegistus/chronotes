from __future__ import annotations

from chronotes.render.latex_render import render_document


def test_render_document_wraps_pages() -> None:
    pages = [r"\section*{Page 1}", r"\section*{Page 2}"]
    tex = render_document(pages)

    assert r"\begin{document}" in tex
    assert r"\end{document}" in tex
    assert r"\section*{Page 1}" in tex
    assert r"\section*{Page 2}" in tex
