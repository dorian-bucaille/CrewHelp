from detection.visionhsv import HsvFilter

bgr_colors = {
    "red": (0, 0, 255),
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "pink": (255, 0, 255),
    "orange": (0, 127, 255),
    "yellow": (0, 255, 255),
    "black": (255, 255, 255),
    "white": (0, 0, 0),
    "purple": (191, 0, 191),
    "brown": (20, 70, 120),
    "cyan": (255, 255, 0),
    "lime": (0, 255, 0)
}

filters = {
    "red": HsvFilter(0, 229, 0, 179, 237, 255, 0, 0, 255, 0),
    "blue": HsvFilter(114, 221, 0, 119, 255, 255, 0, 0, 0, 0),
    "green": HsvFilter(67, 218, 0, 76, 222, 255, 0, 0, 0, 0),
    "pink": HsvFilter(146, 160, 0, 161, 255, 255, 0, 0, 0, 0),
    "orange": HsvFilter(6, 219, 0, 20, 255, 255, 0, 0, 0, 0),
    "yellow": HsvFilter(19, 164, 184, 30, 213, 255, 0, 0, 0, 0),
    "black": HsvFilter(104, 49, 36, 116, 55, 255, 0, 0, 255, 0),
    "white": HsvFilter(108, 22, 176, 113, 95, 255, 0, 0, 0, 0),
    "purple": HsvFilter(129, 190, 0, 134, 255, 255, 0, 0, 0, 0),
    "brown": HsvFilter(6, 186, 0, 17, 198, 255, 0, 0, 255, 0),
    "cyan": HsvFilter(83, 198, 0, 95, 255, 255, 0, 0, 0, 0),
    "lime": HsvFilter(55, 193, 0, 56, 194, 255, 0, 0, 255, 0),
    "room": HsvFilter(0, 0, 0, 0, 0, 255, 0, 0, 0, 0),
    "meeting": HsvFilter(0, 0, 209, 179, 255, 255, 0, 0, 0, 0)
}

colors = ["red", "blue", "green", "pink", "orange", "yellow", "black", "white", "purple", "brown", "cyan", "lime"]

rooms = ["cafeteria", "medbay", "upper_engine", "reactor", "security", "lower_engine", "electrical", "storage", "admin",
         "communications", "shields", "navigation", "o2", "weapons"]

thresholds = {
    "red": 0.5,  # Seems OK
    "blue": 0.5,
    "green": 0.5,  # OK
    "pink": 0.4,
    "orange": 0.4,  # OK
    "yellow": 0.53,  # OK but not 100% accurate. Had to lower threshold because of empty bin storage task.
    "black": 0.5,  # Not OK (reactor)
    "white": 0.4,
    "purple": 0.4,
    "brown": 0.45,  # OK
    "cyan": 0.45,
    "lime": 0.3,  # OK
    "room": 0.72  # OK
}

# TODO test if those are good
marker_positions = {
    "cafeteria": (716, 150),  # OK
    "medbay": (455, 356),
    "upper_engine": (200, 204),
    "reactor": (77, 390),
    "security": (342, 375),
    "lower_engine": (185, 576),
    "electrical": (455, 500),
    "storage": (616, 576),
    "admin": (818, 440),
    "communications": (806, 651),
    "shields": (965, 593),
    "navigation": (1210, 374),
    "o2": (900, 308),
    "weapons": (965, 156),
}
