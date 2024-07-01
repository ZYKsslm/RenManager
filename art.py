import random

import colorama
from pyfiglet import Figlet


colorama.init(autoreset=True)
ENV_STYLE = colorama.Fore.CYAN + colorama.Style.BRIGHT
PMT_STYLE = colorama.Fore.MAGENTA + colorama.Style.BRIGHT

BOOT_TEXT_FONT_LIST = [
    "3-d",
    "4max",
    "5lineoblique",
    "ansi_regular",
    "ansi_shadow",
    "avatar",
    "banner3-D",
    "basic",
    "big",
    "bigchief",
    "big_money-ne",
    "block",
    "bloody",
    "braced",
    "broadway_kb",
    "cola",
    "contessa",
    "crawford",
    "doom",
    "dos_rebel",
    "double",
    "double_shorts",
    "drpepper",
    "eftitalic",
    "elite",
    "epic",
    "fender",
    "fuzzy",
    "ogre",
    "puffy",
    "rounded",
    "soft",
    "speed",
    "standard",
    "stforek",
    "varsity"
]
BOOT_TEXT_COLOR_LIST = [
    "#000000",
    "#800000",
    "#008000",
    "#808000",
    "#000080",
    "#800080",
    "#008080",
    "#c0c0c0",
    "#808080",
    "#ff0000",
    "#00ff00",
    "#ffff00",
    "#0000ff",
    "#ff00ff",
    "#00ffff",
    "#ffffff",
    "#00005f",
    "#000087",
    "#0000d7",
    "#0000ff",
    "#005f00",
    "#005faf",
    "#005fd7",
    "#005fff",
    "#008700",
    "#00875f",
    "#008787",
    "#0087d7",
    "#0087ff",
    "#00af87",
    "#00afaf",
    "#00afd7",
    "#00afff",
    "#00d700",
    "#00d75f",
    "#00d7af",
    "#00d7d7",
    "#00d7ff",
    "#00ff00",
    "#00ff5f",
    "#00ff87",
    "#00ffaf",
    "#00ffd7",
    "#00ffff",
    "#5f00af",
    "#5f00d7",
    "#5f00ff",
    "#5f5f5f",
    "#5f5f87",
    "#5f5fd7",
    "#5f5fff",
    "#5f8700",
    "#5f8787",
    "#5f87af",
    "#5f87d7",
    "#5f87ff",
    "#5faf5f",
    "#5fafaf",
    "#5fafd7",
    "#5fd700",
    "#5fd787",
    "#5fd7af",
    "#5fd7d7",
    "#5fd7ff",
    "#5fff5f",
    "#5fffaf",
    "#5fffff",
    "#870000",
    "#8700af",
    "#875f00",
    "#875f5f",
    "#875f87",
    "#875fd7",
    "#875fff",
    "#87875f",
    "#878787",
    "#8787af",
    "#8787d7",
    "#8787ff",
    "#87af00",
    "#87af87",
    "#87afd7",
    "#87afff",
    "#87d700",
    "#87d787",
    "#87d7d7",
    "#87d7ff",
    "#87ff00",
    "#87ff87",
    "#87ffd7",
    "#87ffff",
    "#af005f",
    "#af0087",
    "#af00d7",
    "#af00ff",
    "#af5faf",
    "#af5fd7",
    "#af8700",
    "#af8787",
    "#af87af",
    "#af87d7",
    "#af87ff",
    "#afaf5f",
    "#afaf87",
    "#afafaf",
    "#afafd7",
    "#afafff",
    "#afd75f",
    "#afd787",
    "#afd7d7",
    "#afd7ff",
    "#afff00",
    "#afff5f",
    "#afff87",
    "#afffaf",
    "#afffff",
    "#d70000",
    "#d70087",
    "#d700d7",
    "#d75f00",
    "#d75f5f",
    "#d75f87",
    "#d75faf",
    "#d75fd7",
    "#d78700",
    "#d7875f",
    "#d78787",
    "#d787af",
    "#d787d7",
    "#d787ff",
    "#d7af00",
    "#d7af5f",
    "#d7af87",
    "#d7afaf",
    "#d7afd7",
    "#d7afff",
    "#d7d700",
    "#d7d75f",
    "#d7d7af",
    "#d7d7d7",
    "#d7d7ff",
    "#d7ff00",
    "#d7ff87",
    "#d7ffaf",
    "#d7ffd7",
    "#d7ffff",
    "#ff0000",
    "#ff005f",
    "#ff00af",
    "#ff00d7",
    "#ff00ff",
    "#ff5f00",
    "#ff5f87",
    "#ff5fd7",
    "#ff5fff",
    "#ff8700",
    "#ff875f",
    "#ff8787",
    "#ff87af",
    "#ff87d7",
    "#ff87ff",
    "#ffaf00",
    "#ffaf5f",
    "#ffaf87",
    "#ffafaf",
    "#ffafd7",
    "#ffafff",
    "#ffd700",
    "#ffd787",
    "#ffd7af",
    "#ffd7d7",
    "#ffd7ff",
    "#ffff00",
    "#ffff5f",
    "#ffff87",
    "#ffffaf",
    "#ffffd7",
    "#ffffff",
    "#080808",
    "#121212",
    "#1c1c1c",
    "#262626",
    "#303030",
    "#3a3a3a",
    "#444444",
    "#4e4e4e",
    "#585858",
    "#626262",
    "#6c6c6c",
    "#767676",
    "#808080",
    "#8a8a8a",
    "#949494",
    "#9e9e9e",
    "#a8a8a8",
    "#b2b2b2",
    "#bcbcbc",
    "#c6c6c6",
    "#d0d0d0",
    "#dadada",
    "#e4e4e4",
    "#eeeeee"
]
BOOT_TEXT_COLOR = random.choice(BOOT_TEXT_COLOR_LIST)
BOOT_TEXT_FONT = random.choice(BOOT_TEXT_FONT_LIST)

try:
    BOOT_TEXT = Figlet(font=BOOT_TEXT_FONT).renderText("RenManager")
except ModuleNotFoundError:
    BOOT_TEXT = None