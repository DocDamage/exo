from __future__ import annotations


def apply(text: str) -> str:
    text = text.replace(
        'vertex_path: "./assets/shaders/fxaa.vert.spv"',
        'vertex_path: "./assets/shaders/postprocess.vert.spv"',
        1,
    )
    text = text.replace(
        'fragment_path: "./assets/shaders/fxaa.frag.spv"',
        'fragment_path: "./assets/shaders/postprocess.frag.spv"',
        1,
    )
    return text
