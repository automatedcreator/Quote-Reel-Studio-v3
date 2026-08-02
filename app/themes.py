"""
Premium Theme Engine
"""

THEMES = {

    "apple": {

        "overlay_opacity": 0.28,
        "brightness": 0.95,
        "text_color": (255, 255, 255),
        "shadow_color": (0, 0, 0),
        "shadow_blur": 3,
        "font_size": 66,
        "text_position": "center",
        "animation": "fade",
        "zoom_speed": 1.03,
        "blur": 0,
    },

    "luxury": {

        "overlay_opacity": 0.45,
        "brightness": 0.82,
        "text_color": (245, 215, 110),
        "shadow_color": (0, 0, 0),
        "shadow_blur": 6,
        "font_size": 70,
        "text_position": "center",
        "animation": "slide_up",
        "zoom_speed": 1.06,
        "blur": 0,
    },

    "motivation": {

        "overlay_opacity": 0.20,
        "brightness": 1.08,
        "text_color": (255, 255, 255),
        "shadow_color": (20, 20, 20),
        "shadow_blur": 4,
        "font_size": 72,
        "text_position": "lower",
        "animation": "slide_up",
        "zoom_speed": 1.10,
        "blur": 0,
    },

    "stoic": {

        "overlay_opacity": 0.50,
        "brightness": 0.75,
        "text_color": (235, 235, 235),
        "shadow_color": (0, 0, 0),
        "shadow_blur": 5,
        "font_size": 66,
        "text_position": "center",
        "animation": "fade",
        "zoom_speed": 1.02,
        "blur": 1,
    },

    "podcast": {

        "overlay_opacity": 0.35,
        "brightness": 0.92,
        "text_color": (255, 255, 255),
        "shadow_color": (0, 0, 0),
        "shadow_blur": 4,
        "font_size": 58,
        "text_position": "bottom",
        "animation": "slide_up",
        "zoom_speed": 1.02,
        "blur": 0,
    },

    "finance": {

        "overlay_opacity": 0.32,
        "brightness": 0.90,
        "text_color": (180, 255, 180),
        "shadow_color": (0, 0, 0),
        "shadow_blur": 4,
        "font_size": 64,
        "text_position": "center",
        "animation": "fade",
        "zoom_speed": 1.04,
        "blur": 0,
    },

    "neon": {

        "overlay_opacity": 0.40,
        "brightness": 1.00,
        "text_color": (120, 240, 255),
        "shadow_color": (20, 120, 255),
        "shadow_blur": 8,
        "font_size": 68,
        "text_position": "center",
        "animation": "slide_down",
        "zoom_speed": 1.08,
        "blur": 0,
    }

}


def get_theme(name):

    return THEMES.get(
        name.lower(),
        THEMES["apple"]
    )


def list_themes():

    return list(THEMES.keys())