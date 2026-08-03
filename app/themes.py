"""
Premium Theme Engine v3
"""

from copy import deepcopy
from app.presets import get_preset

THEMES = {

    "apple": {
        "overlay_opacity":0.22,
        "brightness":1.00,
        "font_size":54,
        "text_color":(255,255,255),
        "shadow_color":(0,0,0),
        "shadow_blur":2,
        "animation":"fade",
        "zoom_speed":1.05,
        "card":True,
        "card_alpha":85,
        "card_radius":55,
        "gradient":False,
    },

    "luxury":{
        "overlay_opacity":0.45,
        "brightness":0.82,
        "font_size":60,
        "text_color":(245,215,110),
        "shadow_color":(0,0,0),
        "shadow_blur":5,
        "animation":"fade",
        "zoom_speed":1.08,
        "card":True,
        "card_alpha":120,
        "card_radius":45,
        "gradient":True,
    },

    "motivation":{
        "overlay_opacity":0.18,
        "brightness":1.10,
        "font_size":58,
        "text_color":(255,255,255),
        "shadow_color":(0,0,0),
        "shadow_blur":4,
        "animation":"slide_up",
        "zoom_speed":1.06,
        "card":False,
        "gradient":False,
    },

    "stoic":{
        "overlay_opacity":0.48,
        "brightness":0.72,
        "font_size":56,
        "text_color":(235,235,235),
        "shadow_color":(0,0,0),
        "shadow_blur":6,
        "animation":"fade",
        "zoom_speed":1.03,
        "card":True,
        "card_alpha":90,
        "card_radius":40,
        "gradient":False,
    },

    "podcast":{
        "overlay_opacity":0.30,
        "brightness":0.95,
        "font_size":48,
        "text_color":(255,255,255),
        "shadow_color":(0,0,0),
        "shadow_blur":3,
        "animation":"slide_up",
        "zoom_speed":1.02,
        "card":False,
        "gradient":False,
    },

    "finance":{
        "overlay_opacity":0.30,
        "brightness":0.92,
        "font_size":52,
        "text_color":(175,255,175),
        "shadow_color":(0,0,0),
        "shadow_blur":3,
        "animation":"fade",
        "zoom_speed":1.05,
        "card":True,
        "card_alpha":90,
        "card_radius":45,
        "gradient":False,
    },

    "neon":{
        "overlay_opacity":0.38,
        "brightness":1.00,
        "font_size":56,
        "text_color":(120,240,255),
        "shadow_color":(30,120,255),
        "shadow_blur":8,
        "animation":"fade",
        "zoom_speed":1.07,
        "card":True,
        "card_alpha":70,
        "card_radius":60,
        "gradient":True,
    }

}


def get_theme(theme_name, preset_name=None):

    theme = deepcopy(
        THEMES.get(
            theme_name.lower(),
            THEMES["apple"]
        )
    )

    if preset_name:

        preset = get_preset(
            preset_name
        )

        if preset:

            for key, value in preset.items():

                if key != "theme":

                    theme[key] = value

    return theme


def list_themes():

    return list(
        THEMES.keys()
    )