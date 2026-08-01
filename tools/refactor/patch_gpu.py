from __future__ import annotations

from .common import replace_once

MARKER = "// EXO_HARDENING_V1"


def apply(text: str) -> str:
    text = text.replace('link "./src/stb_image_shim.o"', 'link "./build/native/stb_image_shim.o"', 1)
    text = text.replace('val DEFAULT_SCREEN_HEIGHT: i32 = 900', 'val DEFAULT_SCREEN_HEIGHT: i32 = 900\n\n' + MARKER, 1)

    text = replace_once(
        text,
        """type WaterFragmentUniforms = {
    camera_pos:  mut Vec4f
    water_color: mut Vec4f
    light_dir:   mut Vec4f
    water_params: mut Vec4f
}
""",
        """type WaterFragmentUniforms = {
    camera_pos:   mut Vec4f
    water_color:  mut Vec4f
    light_dir:    mut Vec4f
    water_params: mut Vec4f
    water_center: mut Vec4f
}
""",
        "water uniforms",
    )

    text = replace_once(
        text,
        """type VertexAttributeTriple = {
    first: mut SDLGPUVertexAttribute
    second: mut SDLGPUVertexAttribute
    third: mut SDLGPUVertexAttribute
}
""",
        """type VertexAttributeTriple = {
    first: mut SDLGPUVertexAttribute
    second: mut SDLGPUVertexAttribute
    third: mut SDLGPUVertexAttribute
}

type TextureSamplerBindingPair = {
    first:  mut SDLGPUTextureSamplerBinding
    second: mut SDLGPUTextureSamplerBinding
}
""",
        "binding pair type",
    )

    text = replace_once(
        text,
        """        val copy_pass: ref void = SDL_BeginGPUCopyPass(cmd)
        val src: mut SDLGPUTextureTransferInfo = {
            transfer_buffer: tbuf, offset: 0 as u32,
            pixels_per_row: w as u32, rows_per_layer: h as u32
        }
        val dst: mut SDLGPUTextureRegion = {
            texture: texture, mip_level: 0 as u32, layer: 0 as u32,
            x: 0 as u32, y: 0 as u32, z: 0 as u32,
            w: w as u32, h: h as u32, d: 1 as u32
        }
        SDL_UploadToGPUTexture(copy_pass, @addr(src), @addr(dst), false)
        SDL_EndGPUCopyPass(copy_pass)
        SDL_SubmitGPUCommandBuffer(cmd)
        SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
        return texture
""",
        """        val copy_pass: ref void = SDL_BeginGPUCopyPass(cmd)
        if copy_pass == none {
            SDL_CancelGPUCommandBuffer(cmd)
            SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
            SDL_ReleaseGPUTexture(runtime.device, texture)
            return none as ref void
        }
        val src: mut SDLGPUTextureTransferInfo = {
            transfer_buffer: tbuf, offset: 0 as u32,
            pixels_per_row: w as u32, rows_per_layer: h as u32
        }
        val dst: mut SDLGPUTextureRegion = {
            texture: texture, mip_level: 0 as u32, layer: 0 as u32,
            x: 0 as u32, y: 0 as u32, z: 0 as u32,
            w: w as u32, h: h as u32, d: 1 as u32
        }
        SDL_UploadToGPUTexture(copy_pass, @addr(src), @addr(dst), false)
        SDL_EndGPUCopyPass(copy_pass)
        if !SDL_SubmitGPUCommandBuffer(cmd) {
            SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
            SDL_ReleaseGPUTexture(runtime.device, texture)
            return none as ref void
        }
        SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
        return texture
""",
        "PNG upload submission",
    )

    text = replace_once(
        text,
        """    val copy_pass: ref void = SDL_BeginGPUCopyPass(cmd)
    val src: mut SDLGPUTextureTransferInfo = {
        transfer_buffer: tbuf, offset: 0 as u32,
        pixels_per_row: w as u32, rows_per_layer: h as u32
    }
    val dst: mut SDLGPUTextureRegion = {
        texture: texture, mip_level: 0 as u32, layer: 0 as u32,
        x: 0 as u32, y: 0 as u32, z: 0 as u32,
        w: w as u32, h: h as u32, d: 1 as u32
    }
    SDL_UploadToGPUTexture(copy_pass, @addr(src), @addr(dst), false)
    SDL_EndGPUCopyPass(copy_pass)
    SDL_SubmitGPUCommandBuffer(cmd)
    SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
    runtime.glb_texture = texture
""",
        """    val copy_pass: ref void = SDL_BeginGPUCopyPass(cmd)
    if copy_pass == none {
        SDL_CancelGPUCommandBuffer(cmd)
        SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
        SDL_ReleaseGPUTexture(runtime.device, texture)
        return
    }
    val src: mut SDLGPUTextureTransferInfo = {
        transfer_buffer: tbuf, offset: 0 as u32,
        pixels_per_row: w as u32, rows_per_layer: h as u32
    }
    val dst: mut SDLGPUTextureRegion = {
        texture: texture, mip_level: 0 as u32, layer: 0 as u32,
        x: 0 as u32, y: 0 as u32, z: 0 as u32,
        w: w as u32, h: h as u32, d: 1 as u32
    }
    SDL_UploadToGPUTexture(copy_pass, @addr(src), @addr(dst), false)
    SDL_EndGPUCopyPass(copy_pass)
    if !SDL_SubmitGPUCommandBuffer(cmd) {
        SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
        SDL_ReleaseGPUTexture(runtime.device, texture)
        return
    }
    SDL_ReleaseGPUTransferBuffer(runtime.device, tbuf)
    runtime.glb_texture = texture
""",
        "GLB texture upload submission",
    )

    text = replace_once(
        text,
        """    val runtime: mut ref ExoSDL3Runtime = @alloc(@sizeof(ExoSDL3Runtime)) as mut ref ExoSDL3Runtime
    if runtime == none {
        SDL_Quit()
        return set_exo_error_ptr("failed to allocate runtime")
    }
    runtime.window = SDL_CreateWindow(title, width, height, 0 as u64)
""",
        """    val runtime: mut ref ExoSDL3Runtime = @alloc(@sizeof(ExoSDL3Runtime)) as mut ref ExoSDL3Runtime
    if runtime == none {
        SDL_Quit()
        return set_exo_error_ptr("failed to allocate runtime")
    }
    @memset(runtime as ref void, 0, @sizeof(ExoSDL3Runtime) as usize)
    runtime.window = SDL_CreateWindow(title, width, height, 0 as u64)
""",
        "runtime initialization",
    )
    return text
