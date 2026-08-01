from __future__ import annotations

from .common import replace_once


def apply(text: str) -> str:
    text = replace_once(
        text,
        """fn safe_key(keys: ref u8, scancode: i32) u8 = trust {
    if scancode <= (0 as i32) || scancode >= (512 as i32) {
        return 0 as u8
    }
    return @load8(@ptradd(keys, scancode as usize))
}

fn update_camera(camera: mut Camera, input: InputConfig, dt: f32, keys: ref u8, mouse_dx: f32, mouse_dy: f32) void = trust {
    val yaw_step:   f32 = camera.turn_speed * dt
    val move_step:  f32 = camera.move_speed * dt
    val key_fwd:    u8 = safe_key(keys, input.keys.move_forward)
    val key_back:   u8 = safe_key(keys, input.keys.move_back)
    val key_left:   u8 = safe_key(keys, input.keys.move_left)
    val key_right:  u8 = safe_key(keys, input.keys.move_right)
    val key_tleft:  u8 = safe_key(keys, input.keys.turn_left)
    val key_tright: u8 = safe_key(keys, input.keys.turn_right)
    val key_up:     u8 = safe_key(keys, input.keys.look_up)
    val key_down:   u8 = safe_key(keys, input.keys.look_down)
""",
        """fn safe_key(keys: ref u8, key_count: i32, scancode: i32) u8 = trust {
    if keys == none || scancode <= (0 as i32) || scancode >= key_count {
        return 0 as u8
    }
    return @load8(@ptradd(keys, scancode as usize))
}

fn update_camera(camera: mut Camera, input: InputConfig, dt: f32, keys: ref u8, key_count: i32, mouse_dx: f32, mouse_dy: f32) void = trust {
    val yaw_step:   f32 = camera.turn_speed * dt
    val move_step:  f32 = camera.move_speed * dt
    val key_fwd:    u8 = safe_key(keys, key_count, input.keys.move_forward)
    val key_back:   u8 = safe_key(keys, key_count, input.keys.move_back)
    val key_left:   u8 = safe_key(keys, key_count, input.keys.move_left)
    val key_right:  u8 = safe_key(keys, key_count, input.keys.move_right)
    val key_tleft:  u8 = safe_key(keys, key_count, input.keys.turn_left)
    val key_tright: u8 = safe_key(keys, key_count, input.keys.turn_right)
    val key_up:     u8 = safe_key(keys, key_count, input.keys.look_up)
    val key_down:   u8 = safe_key(keys, key_count, input.keys.look_down)
""",
        "safe keyboard access",
    )

    text = replace_once(
        text,
        """fn draw_mesh(runtime: ref void, mesh: MeshGPU, model: Mat4, view_proj: Mat4, color: ecs.Vec3, camera_pos: ecs.Vec3, reflective: f32, glow: f32, alpha: f32, light: ecs.PointLight) void = trust {
""",
        """fn draw_mesh(runtime: ref void, mesh: MeshGPU, model: Mat4, view_proj: Mat4, color: ecs.Vec3, camera_pos: ecs.Vec3, reflective: f32, glow: f32, alpha: f32, light: ecs.PointLight, use_albedo_texture: bool) void = trust {
""",
        "draw mesh signature",
    )
    text = replace_once(
        text,
        """        reflective,
        glow,
        alpha,
        @addr(light.position.x),
""",
        """        reflective,
        glow,
        alpha,
        use_albedo_texture,
        @addr(light.position.x),
""",
        "draw mesh texture forwarding",
    )
    text = text.replace(
        "draw_mesh(runtime, mesh, mm, view_proj, E.se_color(entity), camera.position, E.se_reflective(entity), glow_scale * (0.025 as f32), 1.0 as f32, light)",
        "draw_mesh(runtime, mesh, mm, view_proj, E.se_color(entity), camera.position, E.se_reflective(entity), E.se_emissive(entity) + glow_scale * (0.025 as f32), 1.0 as f32, light, false)",
        1,
    )

    text = replace_once(
        text,
        """fn draw_water(runtime: ref void, mesh: MeshGPU, model: Mat4, view_proj: Mat4, reflect_view_proj: Mat4, camera: Camera, color: ecs.Vec3, wave_offset: f32, wave_amplitude: f32, wave_frequency: f32, light: ecs.PointLight, corner_radius: f32, size_x: f32, size_z: f32) void = trust {
""",
        """fn draw_water(runtime: ref void, mesh: MeshGPU, model: Mat4, view_proj: Mat4, reflect_view_proj: Mat4, camera: Camera, color: ecs.Vec3, wave_offset: f32, wave_amplitude: f32, wave_frequency: f32, light: ecs.PointLight, corner_radius: f32, size_x: f32, size_z: f32, center_x: f32, center_z: f32) void = trust {
""",
        "water draw signature",
    )
    text = replace_once(
        text,
        """        light_dir:    { x: light_dir.x, y: light_dir.y, z: light_dir.z, w: light.intensity },
        water_params: { x: corner_radius, y: size_x, z: size_z, w: 0.0 as f32 }
    }
""",
        """        light_dir:    { x: light_dir.x, y: light_dir.y, z: light_dir.z, w: light.intensity },
        water_params: { x: corner_radius, y: size_x, z: size_z, w: 0.0 as f32 },
        water_center: { x: center_x, y: 0.0 as f32, z: center_z, w: 0.0 as f32 }
    }
""",
        "water center uniform",
    )
    text = replace_once(
        text,
        """    val bindings_raw: ref void = @alloc(2 as usize * @sizeof(SDLGPUTextureSamplerBinding) as usize)
    val b0: mut ref SDLGPUTextureSamplerBinding = bindings_raw as mut ref SDLGPUTextureSamplerBinding
    val b1: mut ref SDLGPUTextureSamplerBinding = @ptradd(bindings_raw, @sizeof(SDLGPUTextureSamplerBinding) as usize) as mut ref SDLGPUTextureSamplerBinding
    b0.texture = rt.reflection_color
    b0.sampler = rt.linear_sampler
    b1.texture = normal_tex
    b1.sampler = rt.repeat_sampler
    SDL_BindGPUFragmentSamplers(rt.current_pass, 0 as u32, bindings_raw as ref SDLGPUTextureSamplerBinding, 2 as u32)
    @free(bindings_raw)
""",
        """    val bindings: mut TextureSamplerBindingPair = {
        first:  { texture: rt.reflection_color, sampler: rt.linear_sampler },
        second: { texture: normal_tex, sampler: rt.repeat_sampler }
    }
    SDL_BindGPUFragmentSamplers(rt.current_pass, 0 as u32, @addr(bindings.first), 2 as u32)
""",
        "water stack bindings",
    )

    text = replace_once(
        text,
        """fn render_reflection_scene(runtime: ref void, cube_mesh: MeshGPU, sphere_mesh: MeshGPU, scene: ecs.Scene3D, camera: Camera, width: i32, height: i32, time: f32, plane_y: f32) void = trust {
    val mirror_y: mut f32 = plane_y
    if scene.water is some water { mirror_y = water.y }
    val mirrored: Camera = mirrored_camera(camera, mirror_y)
    val reflect_vp: Mat4 = view_projection(mirrored, width, height)
    draw_scene_entities(runtime, cube_mesh, sphere_mesh, scene, mirrored, reflect_vp, time, 0.60 as f32)
}
""",
        """fn scene_reflection_plane(scene: ecs.Scene3D) f32 = {
    if scene.water is some water { return water.y }
    if scene.floor is some floor { return floor.y }
    return -0.18 as f32
}

fn render_reflection_scene(runtime: ref void, cube_mesh: MeshGPU, sphere_mesh: MeshGPU, glb_mesh: MeshGPU, scene: ecs.Scene3D, camera: Camera, width: i32, height: i32, time: f32, plane_y: f32) void = trust {
    val mirrored: Camera = mirrored_camera(camera, plane_y)
    val reflect_vp: Mat4 = view_projection(mirrored, width, height)
    draw_scene_entities(runtime, cube_mesh, sphere_mesh, scene, mirrored, reflect_vp, time, 0.60 as f32)
    if mesh_valid(glb_mesh) {
        val glb_mm: Mat4 = model_matrix(scene.model_position, scene.model_scale, scene.model_rotation_y)
        draw_mesh(runtime, glb_mesh, glb_mm, reflect_vp, scene.light.color, mirrored.position, 0.05 as f32, 0.0 as f32, 1.0 as f32, scene.light, true)
    }
}
""",
        "reflection model support",
    )

    text = replace_once(
        text,
        """    val vp: Mat4 = view_projection(camera, width, height)
    val floor_y: f32 = -0.18 as f32
    val floor_position: ecs.Vec3 = vec3(0.0 as f32, floor_y - (0.08 as f32), -1.45 as f32)
    val floor_scale: ecs.Vec3 = vec3(7.8 as f32, 0.16 as f32, 7.8 as f32)
    val reflect_vp: Mat4 = view_projection(mirrored_camera(camera, floor_y), width, height)
""",
        """    val vp: Mat4 = view_projection(camera, width, height)
    val floor_y: mut f32 = -0.18 as f32
    val floor_position: mut ecs.Vec3 = vec3(0.0 as f32, floor_y - (0.08 as f32), -1.45 as f32)
    val floor_scale: mut ecs.Vec3 = vec3(7.8 as f32, 0.16 as f32, 7.8 as f32)
    if scene.floor is some floor {
        floor_y = floor.y
        floor_position = vec3(floor.offset_x, floor.y - floor.thickness * (0.5 as f32), floor.offset_z)
        floor_scale = vec3(floor.size_x, floor.thickness, floor.size_z)
    }
    val reflect_vp: Mat4 = view_projection(mirrored_camera(camera, floor_y), width, height)
""",
        "floor visual source of truth",
    )
    text = text.replace(
        "val glb_mm: Mat4 = model_matrix(vec3(0.0 as f32, 0.0 as f32, 0.0 as f32), scene.model_scale, 0.0 as f32)",
        "val glb_mm: Mat4 = model_matrix(scene.model_position, scene.model_scale, scene.model_rotation_y)",
    )
    text = text.replace(
        "draw_mesh(runtime, glb_mesh, glb_mm, vp, scene.light.color, camera.position, 0.05 as f32, 0.0 as f32, 1.0 as f32, scene.light)",
        "draw_mesh(runtime, glb_mesh, glb_mm, vp, scene.light.color, camera.position, 0.05 as f32, 0.0 as f32, 1.0 as f32, scene.light, true)",
        1,
    )
    text = replace_once(
        text,
        """            fit_ox = ((scene.model.bounds_min_x + scene.model.bounds_max_x) * 0.5 as f32) * s
            fit_oz = ((scene.model.bounds_min_z + scene.model.bounds_max_z) * 0.5 as f32) * s
            fit_y  = scene.model.bounds_max_y * s + water.y
""",
        """            fit_ox = scene.model_position.x + ((scene.model.bounds_min_x + scene.model.bounds_max_x) * 0.5 as f32) * s
            fit_oz = scene.model_position.z + ((scene.model.bounds_min_z + scene.model.bounds_max_z) * 0.5 as f32) * s
            fit_y  = scene.model_position.y + scene.model.bounds_max_y * s + water.y
""",
        "water fit model transform",
    )
    text = replace_once(
        text,
        """        draw_water(runtime, cube_mesh, water_model, vp, reflect_water_vp, camera, water.color, wave_offset, water.wave_amplitude, water.wave_frequency, scene.light, water.corner_radius, fit_x, fit_z)
""",
        """        draw_water(runtime, cube_mesh, water_model, vp, reflect_water_vp, camera, water.color, wave_offset, water.wave_amplitude, water.wave_frequency, scene.light, water.corner_radius, fit_x, fit_z, fit_ox, fit_oz)
""",
        "water center forwarding",
    )

    text = replace_once(
        text,
        """        val keys: ref u8 = exo_sdl3_get_keyboard_state()
        val quit_pressed: u8 = @load8(@ptradd(keys, app.input.quit_key as usize))
        val scene_pressed: u8 = @load8(@ptradd(keys, app.next_scene_key as usize))
        val audio_pressed: u8 = @load8(@ptradd(keys, app.audio.trigger_key as usize))
""",
        """        val key_count: mut i32 = 0 as i32
        val keys: ref u8 = exo_sdl3_get_keyboard_state(@addr(key_count))
        val quit_pressed: u8 = safe_key(keys, key_count, app.input.quit_key)
        val scene_pressed: u8 = safe_key(keys, key_count, app.next_scene_key)
        val audio_pressed: u8 = safe_key(keys, key_count, app.audio.trigger_key)
""",
        "main-loop key safety",
    )
    text = replace_once(
        text,
        """        update_camera(app.camera, app.input, dt, keys, mx, my)
""",
        """        update_camera(app.camera, app.input, dt, keys, key_count, mx, my)
""",
        "camera key count",
    )
    text = replace_once(
        text,
        """        render_reflection_scene(runtime, cube_mesh, sphere_mesh, app.scene, app.camera, frame_w as i32, frame_h as i32, time_value, -0.18 as f32)
""",
        """        render_reflection_scene(runtime, cube_mesh, sphere_mesh, glb_mesh, app.scene, app.camera, frame_w as i32, frame_h as i32, time_value, scene_reflection_plane(app.scene))
""",
        "reflection call",
    )

    for message in (
        "SDL3 reflection pass failed",
        "SDL3 scene pass failed",
        "SDL3 FXAA pass failed",
    ):
        old = f'''            print_sdl_error("{message}")\n            exit_code = 1 as i32\n            break\n'''
        new = f'''            print_sdl_error("{message}")\n            exo_sdl3_abort_frame(runtime)\n            exit_code = 1 as i32\n            break\n'''
        text = replace_once(text, old, new, f"abort on {message}")

    text = replace_once(
        text,
        """    shutdown_runtime_audio(audio_runtime)
    destroy_mesh(runtime, glb_mesh)
""",
        """    exo_sdl3_abort_frame(runtime)
    shutdown_runtime_audio(audio_runtime)
    destroy_mesh(runtime, glb_mesh)
""",
        "teardown abort",
    )
    return text
