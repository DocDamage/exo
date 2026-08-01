from __future__ import annotations

from .common import replace_once


def apply(text: str) -> str:
    text = replace_once(
        text,
        """fn exo_sdl3_get_keyboard_state() ref u8 = trust {
    return SDL_GetKeyboardState(none as ref i32) as ref u8
}
""",
        """fn exo_sdl3_get_keyboard_state(num_keys: mut ref i32) ref u8 = trust {
    return SDL_GetKeyboardState(num_keys) as ref u8
}
""",
        "keyboard state count",
    )

    text = replace_once(
        text,
        """    val mesh: mut ref ExoSDL3Mesh = @alloc(@sizeof(ExoSDL3Mesh)) as mut ref ExoSDL3Mesh
    if mesh == none {
        return set_exo_error_ptr("failed to allocate mesh")
    }
    val vertex_info: mut SDLGPUBufferCreateInfo = {
""",
        """    val mesh: mut ref ExoSDL3Mesh = @alloc(@sizeof(ExoSDL3Mesh)) as mut ref ExoSDL3Mesh
    if mesh == none {
        return set_exo_error_ptr("failed to allocate mesh")
    }
    @memset(mesh as ref void, 0, @sizeof(ExoSDL3Mesh) as usize)
    val vertex_info: mut SDLGPUBufferCreateInfo = {
""",
        "mesh initialization",
    )

    text = replace_once(
        text,
        """    val audio: mut ref ExoSDL3Audio = @alloc(@sizeof(ExoSDL3Audio)) as mut ref ExoSDL3Audio
    if audio == none {
        return set_exo_error_ptr("failed to allocate audio")
    }
    if !SDL_LoadWAV(wav_path, @addr(audio.speci), @addr(audio.buffer), @addr(audio.length)) {
""",
        """    val audio: mut ref ExoSDL3Audio = @alloc(@sizeof(ExoSDL3Audio)) as mut ref ExoSDL3Audio
    if audio == none {
        return set_exo_error_ptr("failed to allocate audio")
    }
    @memset(audio as ref void, 0, @sizeof(ExoSDL3Audio) as usize)
    if !SDL_LoadWAV(wav_path, @addr(audio.speci), @addr(audio.buffer), @addr(audio.length)) {
""",
        "audio initialization",
    )

    text = text.replace(
        "SDL_SetAudioStreamGain(audio.stream, (volume as f32) / (128.0 as f32))",
        "SDL_SetAudioStreamGain(audio.stream, clamp_audio_gain(volume))",
    )
    text = replace_once(
        text,
        """fn exo_sdl3_create_audio(wav_path: ref u8, volume: i32) ref void = trust {
""",
        """fn clamp_audio_gain(volume: i32) f32 = {
    val safe_volume: mut i32 = volume
    if safe_volume < (0 as i32) { safe_volume = 0 as i32 }
    if safe_volume > (128 as i32) { safe_volume = 128 as i32 }
    return (safe_volume as f32) / (128.0 as f32)
}

fn exo_sdl3_create_audio(wav_path: ref u8, volume: i32) ref void = trust {
""",
        "audio gain helper",
    )

    text = replace_once(
        text,
        """fn exo_sdl3_end_pass(runtime_raw: ref void) void = trust {
    if runtime_raw == none {
        return
    }
    val runtime: mut ref ExoSDL3Runtime = runtime_raw as mut ref ExoSDL3Runtime
    if runtime.current_pass != none {
        SDL_EndGPURenderPass(runtime.current_pass)
        runtime.current_pass = none
    }
}
""",
        """fn exo_sdl3_end_pass(runtime_raw: ref void) void = trust {
    if runtime_raw == none {
        return
    }
    val runtime: mut ref ExoSDL3Runtime = runtime_raw as mut ref ExoSDL3Runtime
    if runtime.current_pass != none {
        SDL_EndGPURenderPass(runtime.current_pass)
        runtime.current_pass = none
    }
}

fn exo_sdl3_abort_frame(runtime_raw: ref void) void = trust {
    if runtime_raw == none { return }
    val runtime: mut ref ExoSDL3Runtime = runtime_raw as mut ref ExoSDL3Runtime
    exo_sdl3_end_pass(runtime_raw)
    if runtime.command_buffer != none {
        SDL_CancelGPUCommandBuffer(runtime.command_buffer)
    }
    runtime.command_buffer = none
    runtime.swapchain_texture = none
    runtime.frame_active = false
}
""",
        "abort frame",
    )

    text = replace_once(
        text,
        """    alpha: f32,
    light_pos: ref f32,
""",
        """    alpha: f32,
    use_albedo_texture: bool,
    light_pos: ref f32,
""",
        "draw texture parameter",
    )
    text = replace_once(
        text,
        """    if runtime.glb_texture != none {
        tex_to_bind = runtime.glb_texture
        has_tex = 1.0 as f32
        fu.alpha_pad.y = has_tex
    }
""",
        """    if use_albedo_texture && runtime.glb_texture != none {
        tex_to_bind = runtime.glb_texture
        has_tex = 1.0 as f32
        fu.alpha_pad.y = has_tex
    }
""",
        "texture isolation",
    )
    return text
