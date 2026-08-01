from __future__ import annotations

from .common import replace_once


def apply(text: str) -> str:
    text = replace_once(
        text,
        """fn set_active_scene(app: mut ExoApp, index: usize) void = {
    if @get(app.scenes, index) is some scene {
        app.active_scene_index = index
        app.scene = scene
    }
}
""",
        """fn persist_active_scene(app: mut ExoApp) void = {
    if app.active_scene_index < @len(app.scenes) {
        @set(app.scenes, app.active_scene_index, app.scene)
    }
}

fn set_active_scene(app: mut ExoApp, index: usize) void = {
    if @get(app.scenes, index) is some scene {
        persist_active_scene(app)
        app.active_scene_index = index
        app.scene = scene
    }
}
""",
        "scene state persistence",
    )

    text = replace_once(
        text,
        """fn scene_reflection_plane(scene: ecs.Scene3D) f32 = {
    if scene.water is some water { return water.y }
    if scene.floor is some floor { return floor.y }
    return -0.18 as f32
}
""",
        """fn scene_reflection_plane(scene: ecs.Scene3D) f32 = {
    if scene.water is some water {
        if water.size_x == (0.0 as f32) && water.size_z == (0.0 as f32) && scene.model.valid {
            return scene.model_position.y + scene.model.bounds_max_y * scene.model_scale + water.y
        }
        return water.y
    }
    if scene.floor is some floor { return floor.y }
    return -0.18 as f32
}
""",
        "fitted-water reflection plane",
    )

    text = replace_once(
        text,
        """    if play_loops < (0 as i32) {
        play_loops = 0 as i32
    }
""",
        """    if play_loops < (0 as i32) { play_loops = 0 as i32 }
    if play_loops > (64 as i32) { play_loops = 64 as i32 }
""",
        "audio loop bound",
    )
    return text
