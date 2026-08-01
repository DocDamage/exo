from __future__ import annotations

from .common import replace_once


def apply(text: str) -> str:
    text = replace_once(
        text,
        """val SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM: i32 = 4
""",
        """val SDL_GPU_TEXTUREFORMAT_R8G8B8A8_UNORM: i32 = 4
val SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT: i32 = 29
""",
        "HDR texture format",
    )
    text = replace_once(
        text,
        """    swapchain_format: mut i32
    render_width: mut u32
""",
        """    swapchain_format: mut i32
    scene_format: mut i32
    render_width: mut u32
""",
        "runtime scene format",
    )

    target_creation = """runtime.reflection_color = exo_create_texture(
        runtime,
        runtime.swapchain_format,
"""
    text = replace_once(
        text,
        target_creation,
        """runtime.reflection_color = exo_create_texture(
        runtime,
        runtime.scene_format,
""",
        "HDR reflection target",
    )
    text = replace_once(
        text,
        """runtime.scene_color = exo_create_texture(
        runtime,
        runtime.swapchain_format,
""",
        """runtime.scene_color = exo_create_texture(
        runtime,
        runtime.scene_format,
""",
        "HDR scene target",
    )

    text = text.replace(
        """        runtime.swapchain_format
    )
    if runtime.scene_pipeline == none {
""",
        """        runtime.scene_format
    )
    if runtime.scene_pipeline == none {
""",
        1,
    )
    for label in ("floor_pipeline", "glow_pipeline"):
        marker = f"""        runtime.swapchain_format,
        true,
"""
        if marker not in text:
            raise RuntimeError(f"{label}: scene pipeline format marker missing")
        text = text.replace(marker, """        runtime.scene_format,
        true,
""", 1)
    water_marker = """        runtime.swapchain_format,
        true,
        SDL_GPU_BLENDFACTOR_SRC_ALPHA,
        SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,
        SDL_GPU_BLENDFACTOR_ONE,
"""
    text = replace_once(
        text,
        water_marker,
        """        runtime.scene_format,
        true,
        SDL_GPU_BLENDFACTOR_SRC_ALPHA,
        SDL_GPU_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,
        SDL_GPU_BLENDFACTOR_ONE,
""",
        "water HDR pipeline",
    )

    text = replace_once(
        text,
        """    runtime.swapchain_format = SDL_GetGPUSwapchainTextureFormat(runtime.device, runtime.window)
    if !exo_create_pipelines(runtime, shaders) {
""",
        """    runtime.swapchain_format = SDL_GetGPUSwapchainTextureFormat(runtime.device, runtime.window)
    runtime.scene_format = SDL_GPU_TEXTUREFORMAT_R16G16B16A16_FLOAT
    if !exo_create_pipelines(runtime, shaders) {
""",
        "runtime HDR setup",
    )
    return text
