from __future__ import annotations

from .common import replace_once


def apply(text: str) -> str:
    text = replace_once(
        text,
        """pub fn build_app(builder: ExoAppBuilder) ExoApp = {
    val config: ExoConfig = {
        title: builder.title,
        width: builder.width,
        height: builder.height,
        shaders: builder.shaders
    }
    return create_scene_app(
        config,
        builder.scenes,
        builder.camera,
        builder.input,
        builder.next_scene_key,
        builder.audio
    )
}
""",
        """fn valid_scancode(scancode: i32) bool = {
    return scancode >= (0 as i32) && scancode < (512 as i32)
}

fn normalized_scancode(scancode: i32, fallback: i32) i32 = {
    if valid_scancode(scancode) { return scancode }
    return fallback
}

pub fn app_builder_valid(builder: ExoAppBuilder) bool = {
    if builder.width <= (0 as i32) || builder.height <= (0 as i32) { return false }
    if @len(builder.scenes) == (0 as usize) { return false }
    if !valid_scancode(builder.input.quit_key) { return false }
    if !valid_scancode(builder.next_scene_key) { return false }
    if !valid_scancode(builder.audio.trigger_key) { return false }
    return true
}

pub fn build_app(builder: ExoAppBuilder) ExoApp = {
    val width: mut i32 = builder.width
    val height: mut i32 = builder.height
    if width <= (0 as i32) { width = DEFAULT_SCREEN_WIDTH }
    if height <= (0 as i32) { height = DEFAULT_SCREEN_HEIGHT }

    val input: mut InputConfig = builder.input
    val defaults: KeyBindings = default_key_bindings()
    input.keys.move_forward = normalized_scancode(input.keys.move_forward, defaults.move_forward)
    input.keys.move_back = normalized_scancode(input.keys.move_back, defaults.move_back)
    input.keys.move_left = normalized_scancode(input.keys.move_left, defaults.move_left)
    input.keys.move_right = normalized_scancode(input.keys.move_right, defaults.move_right)
    input.keys.turn_left = normalized_scancode(input.keys.turn_left, defaults.turn_left)
    input.keys.turn_right = normalized_scancode(input.keys.turn_right, defaults.turn_right)
    input.keys.look_up = normalized_scancode(input.keys.look_up, defaults.look_up)
    input.keys.look_down = normalized_scancode(input.keys.look_down, defaults.look_down)
    input.quit_key = normalized_scancode(input.quit_key, SDL_SCANCODE_ESCAPE)

    val next_scene_key: i32 = normalized_scancode(builder.next_scene_key, SDL_SCANCODE_X)
    val audio: mut AudioMixerConfig = builder.audio
    audio.trigger_key = normalized_scancode(audio.trigger_key, SDL_SCANCODE_Y)
    if audio.music_volume < (0 as i32) { audio.music_volume = 0 as i32 }
    if audio.music_volume > (128 as i32) { audio.music_volume = 128 as i32 }

    val scenes: mut list[ecs.Scene3D] = builder.scenes
    if @len(scenes) == (0 as usize) { @append(scenes, fallback_scene()) }

    val config: ExoConfig = {
        title: builder.title,
        width: width,
        height: height,
        shaders: builder.shaders
    }
    return create_scene_app(config, scenes, builder.camera, input, next_scene_key, audio)
}
""",
        "builder validation",
    )

    text = replace_once(
        text,
        """fn parse_accessor_count(accessors: ref void, idx: i64) i32 = trust {
    if json.arr_get(accessors, idx as usize) is some accessor {
        if json.obj_get_int(accessor, "count") is some count {
            return count as i32
        }
    }
    return 0 as i32
}

fn parse_accessor_offset(accessors: ref void, buffer_views: ref void, idx: i64) usize = trust {
    val offset: mut usize = 0 as usize
    if json.arr_get(accessors, idx as usize) is some accessor {
        if json.obj_get_int(accessor, "byteOffset") is some acc_off {
            offset = offset + (acc_off as usize)
        }
        if json.obj_get_int(accessor, "bufferView") is some bv_idx {
            if json.arr_get(buffer_views, bv_idx as usize) is some bv {
                if json.obj_get_int(bv, "byteOffset") is some bv_off {
                    offset = offset + (bv_off as usize)
                }
            }
        }
    }
    return offset
}
""",
        """fn parse_accessor_count(accessors: ref void, idx: i64) i32 = trust {
    if idx < (0 as i64) { return 0 as i32 }
    if json.arr_get(accessors, idx as usize) is some accessor {
        if json.obj_get_int(accessor, "count") is some count {
            if count > (0 as i64) && count <= (2147483647 as i64) { return count as i32 }
        }
    }
    return 0 as i32
}

fn parse_accessor_offset(accessors: ref void, buffer_views: ref void, idx: i64) usize = trust {
    val offset: mut usize = 0 as usize
    if idx < (0 as i64) { return offset }
    if json.arr_get(accessors, idx as usize) is some accessor {
        if json.obj_get_int(accessor, "byteOffset") is some acc_off {
            if acc_off < (0 as i64) { return 0 as usize }
            offset = offset + (acc_off as usize)
        }
        if json.obj_get_int(accessor, "bufferView") is some bv_idx {
            if bv_idx < (0 as i64) { return 0 as usize }
            if json.arr_get(buffer_views, bv_idx as usize) is some bv {
                if json.obj_get_int(bv, "byteOffset") is some bv_off {
                    if bv_off < (0 as i64) { return 0 as usize }
                    offset = offset + (bv_off as usize)
                }
            }
        }
    }
    return offset
}

fn range_fits(offset: usize, count: usize, stride: usize, total: usize) bool = {
    if stride == (0 as usize) || offset > total { return false }
    if count == (0 as usize) { return true }
    return count <= ((total - offset) / stride)
}

pub fn destroy_glb_model(model: mut ref ecs.GlbModel) void = trust {
    if model == none { return }
    if model.raw_bytes != none { @free(model.raw_bytes as ref void) }
    if model.valid && model.mesh_name != none { @free(model.mesh_name as ref void) }
    @deref(model) = ecs.empty_model()
}
""",
        "checked GLB helpers",
    )

    text = replace_once(
        text,
        """        val bin_base: ref void = @ptradd(data, (json_offset + (json_len as usize) + (8 as usize)) as usize)
        val vi: mut usize = 0 as usize
""",
        """        if !range_fits(pos_offset, vc, 12 as usize, model.bin_length) {
            json.doc_free(doc)
            @free(json_buf as ref void)
            return
        }
        val bin_base: ref void = @ptradd(data, (json_offset + (json_len as usize) + (8 as usize)) as usize)
        val vi: mut usize = 0 as usize
""",
        "bounds range validation",
    )

    text = replace_once(
        text,
        """            val vi: mut usize = 0 as usize
            for vi < vc {
""",
        """            if !range_fits(pos_offset, vc, 12 as usize, model.bin_length) ||
               (has_nrm && !range_fits(nrm_offset, vc, 12 as usize, model.bin_length)) ||
               (has_uv && !range_fits(uv_offset, vc, 8 as usize, model.bin_length)) {
                if vertices != none { @free(vertices) }
                if indices != none { @free(indices) }
                json.doc_free(doc)
                @free(json_buf as ref void)
                return result
            }
            val vi: mut usize = 0 as usize
            for vi < vc {
""",
        "vertex range validation",
    )

    text = replace_once(
        text,
        """            val ii: mut usize = 0 as usize
            if ic > (0 as usize) {
""",
        """            if ic > (0 as usize) {
                val index_stride: mut usize = 4 as usize
                if use_u16 { index_stride = 2 as usize }
                if !range_fits(idx_offset, ic, index_stride, model.bin_length) {
                    if vertices != none { @free(vertices) }
                    if indices != none { @free(indices) }
                    json.doc_free(doc)
                    @free(json_buf as ref void)
                    return result
                }
            }
            val ii: mut usize = 0 as usize
            if ic > (0 as usize) {
""",
        "index range validation",
    )

    text = replace_once(
        text,
        """    val bin_len: u32 = bin.read_u32_le(data, bin_header_offset)
    val bin_type: u32 = bin.read_u32_le(data, bin_header_offset + (4 as usize))
    if bin_type != GLB_BIN_CHUNK {
        @free(json_buf as ref void)
        return none
    }
""",
        """    val bin_len: u32 = bin.read_u32_le(data, bin_header_offset)
    val bin_type: u32 = bin.read_u32_le(data, bin_header_offset + (4 as usize))
    if bin_type != GLB_BIN_CHUNK {
        @free(json_buf as ref void)
        return none
    }
    val bin_data_offset: usize = bin_header_offset + (8 as usize)
    if bin_data_offset > total_len_usize || (bin_len as usize) > (total_len_usize - bin_data_offset) {
        @free(json_buf as ref void)
        return none
    }
""",
        "BIN chunk validation",
    )

    text = replace_once(
        text,
        """                if json.obj_get_str(mesh, "name") is some mesh_name {
                    model.mesh_name = dup_cstr(mesh_name)
                }
""",
        """                if json.obj_get_str(mesh, "name") is some mesh_name {
                    val parsed_name: ref u8 = dup_cstr(mesh_name)
                    if parsed_name != none {
                        if model.mesh_name != none { @free(model.mesh_name as ref void) }
                        model.mesh_name = parsed_name
                    }
                }
""",
        "mesh-name ownership",
    )

    text = replace_once(
        text,
        """        val raw_copy: ref u8 = @alloc(len) as ref u8
        if raw_copy != none {
            @memcpy(raw_copy as ref void, data as ref void, len)
            model.raw_bytes = raw_copy
            model.raw_bytes_len = len
        }
""",
        """        val raw_copy: ref u8 = @alloc(total_len_usize) as ref u8
        if raw_copy != none {
            @memcpy(raw_copy as ref void, data as ref void, total_len_usize)
            model.raw_bytes = raw_copy
            model.raw_bytes_len = total_len_usize
        }
""",
        "GLB owned-byte length",
    )

    text = replace_once(
        text,
        """                                    if img_len > (0 as i64) {
                                        model.texture_offset = bin_data_offset + (img_off as usize)
                                        model.texture_length = img_len as usize
                                    }
""",
        """                                    if img_off >= (0 as i64) && img_len > (0 as i64) &&
                                       range_fits(img_off as usize, img_len as usize, 1 as usize, bin_len as usize) {
                                        model.texture_offset = bin_data_offset + (img_off as usize)
                                        model.texture_length = img_len as usize
                                    }
""",
        "texture range validation",
    )

    text = replace_once(
        text,
        """    fread(buf as ref void, 1 as usize, size as usize, file)
    @store8(@ptradd(buf, size as usize), 0)
    fclose(file)
""",
        """    val bytes_read: usize = fread(buf as ref void, 1 as usize, size as usize, file)
    if bytes_read != (size as usize) {
        fclose(file)
        @free(buf as ref void)
        return none
    }
    @store8(@ptradd(buf, size as usize), 0)
    fclose(file)
""",
        "GLB file read",
    )
    return text
