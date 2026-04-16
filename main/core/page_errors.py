from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Optional


def take_visible_text(page, selector: str) -> str:
    loc = page.locator(selector)
    if loc.count() == 0:
        return ""
    if not loc.first.is_visible():
        return ""
    text = loc.first.text_content() or ""
    return text.strip()


def collect_visible_texts(
    page,
    mapping: Sequence[tuple[str, str]],
    global_selector_optional: Optional[str] = None,
    global_label: str = "Global",
) -> str:
    parts: list[str] = []
    for label, selector in mapping:
        text = take_visible_text(page, selector)
        if text:
            parts.append(f"{label}: {text}")

    if global_selector_optional:
        global_text = take_visible_text(page, global_selector_optional)
        if global_text:
            parts.append(f"{global_label}: {global_text}")

    return " | ".join(parts)

