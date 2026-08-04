"""
Premium Theme Engine v2
"""

from app.presets import get_preset

THEMES = {

    "apple": {

        "font_size": 56,
        "text_color": (255,255,255),

        "accent_color": (255, 107, 90),

        "overlay_opacity":0.28,
        "brightness":0.95,

        "shadow_color":(0,0,0),
        "shadow_blur":3,

        "text_position":"center",

        "animation":"fade",

        "card":False,
        "card_alpha":0,
        "card_radius":0,

        "zoom_speed":1.02,

    },

    "luxury":{

        "font_size":60,
        "text_color":(245,215,120),

        "accent_color": (255, 255, 255),

        "overlay_opacity":0.45,
        "brightness":0.82,

        "shadow_color":(0,0,0),
        "shadow_blur":6,

        "text_position":"center",

        "animation":"fade",

        "card":True,
        "card_alpha":70,
        "card_radius":60,

        "zoom_speed":1.01,

    },

    "motivation":{

        "font_size":64,
        "text_color":(255,255,255),

        "accent_color": (255, 99, 71),

        "overlay_opacity":0.22,
        "brightness":1.08,

        "shadow_color":(15,15,15),
        "shadow_blur":5,

        "text_position":"center",

        "animation":"zoom",

        "card":False,

        "zoom_speed":1.05,

    },

    "stoic":{

        "font_size":58,
        "text_color":(235,235,235),

        "accent_color": (255, 170, 110),

        "overlay_opacity":0.50,
        "brightness":0.75,

        "shadow_color":(0,0,0),
        "shadow_blur":5,

        "text_position":"center",

        "animation":"fade",

        "card":False,

        "zoom_speed":1.01,

    },

    "podcast":{

        "font_size":54,
        "text_color":(255,255,255),

        "accent_color": (255, 181, 71),

        "overlay_opacity":0.34,
        "brightness":0.92,

        "shadow_color":(0,0,0),
        "shadow_blur":4,

        "text_position":"upper",

        "animation":"slide_down",

        "card":True,
        "card_alpha":60,
        "card_radius":45,

        "zoom_speed":1.02,

    },

    "finance":{

        "font_size":56,
        "text_color":(185,255,185),

        "accent_color": (160, 255, 170),

        "overlay_opacity":0.30,
        "brightness":0.90,

        "shadow_color":(0,0,0),
        "shadow_blur":4,

        "text_position":"center",

        "animation":"zoom",

        "card":True,
        "card_alpha":55,
        "card_radius":45,

        "zoom_speed":1.03,

    },

    "neon":{

        "font_size":58,
        "text_color":(110,240,255),

        "accent_color": (255, 90, 170),

        "overlay_opacity":0.42,
        "brightness":1.00,

        "shadow_color":(20,120,255),
        "shadow_blur":8,

        "text_position":"center",

        "animation":"zoom",

        "card":False,

        "zoom_speed":1.04,

    },

    "book":{

        "font_size":52,
        "text_color":(252,245,225),

        "accent_color": (214, 178, 90),

        "overlay_opacity":0.34,
        "brightness":0.92,

        "shadow_color":(0,0,0),
        "shadow_blur":3,

        "text_position":"lower",

        "animation":"fade",

        "card":False,

        "zoom_speed":1.01,

    },

    "travel":{

        "font_size":48,
        "text_color":(255,255,255),

        "accent_color": (255, 200, 90),

        "overlay_opacity":0.18,
        "brightness":1.05,

        "shadow_color":(0,0,0),
        "shadow_blur":3,

        "text_position":"bottom",

        "animation":"fade",

        "card":False,

        "zoom_speed":1.04,

    },

    "emotional":{

        "font_size":60,
        "text_color":(255,255,255),

        "accent_color": (255, 120, 140),

        "overlay_opacity":0.38,
        "brightness":0.88,

        "shadow_color":(0,0,0),
        "shadow_blur":6,

        "text_position":"center",

        "animation":"zoom",

        "card":False,

        "zoom_speed":1.02,

    }

}


def get_theme(

    theme_name,

    preset_name=None,

):

    theme = dict(
        THEMES.get(
            theme_name.lower(),
            THEMES["apple"],
        )
    )

    if preset_name:

        preset = get_preset(preset_name)

        if preset:

            overrides = {
                k: v
                for k, v in preset.items()
                if k != "theme"
            }

            theme.update(overrides)

    return theme


def list_themes():

    return sorted(

        THEMES.keys()

    )