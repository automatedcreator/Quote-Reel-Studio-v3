"""
Premium Theme Presets

Each preset is a ready-made Instagram style.
It overrides selected values from the base theme.
"""

PRESETS = {

    "Apple Minimal": {
        "theme": "apple",
        "font_size": 52,
        "overlay_opacity": 0.18,
        "brightness": 1.00,
        "zoom_speed": 1.03,
        "animation": "fade",
        "card": False,
    },

    "Apple Dark": {
        "theme": "apple",
        "font_size": 54,
        "overlay_opacity": 0.35,
        "brightness": 0.82,
        "zoom_speed": 1.05,
        "animation": "fade",
        "card": True,
    },

    "Luxury Gold": {
        "theme": "luxury",
        "font_size": 58,
        "overlay_opacity": 0.45,
        "brightness": 0.80,
        "zoom_speed": 1.08,
        "animation": "fade",
        "card": True,
    },

    "Luxury Black": {
        "theme": "luxury",
        "font_size": 56,
        "overlay_opacity": 0.55,
        "brightness": 0.70,
        "zoom_speed": 1.06,
        "animation": "fade",
        "card": True,
    },

    "Podcast": {
        "theme": "podcast",
        "font_size": 48,
        "overlay_opacity": 0.28,
        "brightness": 0.95,
        "zoom_speed": 1.02,
        "animation": "slide_up",
        "card": False,
    },

    "Finance": {
        "theme": "finance",
        "font_size": 52,
        "overlay_opacity": 0.30,
        "brightness": 0.90,
        "zoom_speed": 1.04,
        "animation": "fade",
        "card": True,
    },

    "Motivation": {
        "theme": "motivation",
        "font_size": 60,
        "overlay_opacity": 0.22,
        "brightness": 1.10,
        "zoom_speed": 1.08,
        "animation": "slide_up",
        "card": False,
    },

    "Neon": {
        "theme": "neon",
        "font_size": 56,
        "overlay_opacity": 0.38,
        "brightness": 1.00,
        "zoom_speed": 1.08,
        "animation": "fade",
        "card": True,
    },

    "Minimal White": {
        "theme": "apple",
        "font_size": 50,
        "overlay_opacity": 0.10,
        "brightness": 1.08,
        "zoom_speed": 1.02,
        "animation": "fade",
        "card": False,
    },

    "OpenAI Style": {
        "theme": "apple",
        "font_size": 54,
        "overlay_opacity": 0.20,
        "brightness": 0.95,
        "zoom_speed": 1.04,
        "animation": "fade",
        "card": True,
    }

}


def list_presets():
    return list(PRESETS.keys())


def get_preset(name):
    return PRESETS.get(name)