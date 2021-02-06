import cv2 as cv


# Class used to display the map and trackers.
class Map:
    marker_positions = {
        "cafeteria": (730, 191),
        "medbay": (435, 280),
        "upper_engine": (185, 210),
        "reactor": (68, 388),
        "security": (329, 379),
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

    colors = ["red", "blue", "green", "pink", "orange", "yellow", "black", "white", "purple", "brown", "cyan",
              "lime"]
    # Attributes
    positions = {}
    last_seen = {}
    markers = {}
    display = None
    map = None

    # Constructor
    def __init__(self, player_positions, player_last_seen):
        self.positions = player_positions
        self.last_seen = player_last_seen
        self.map = cv.imread(r"../gui/img/theskeld.png")

    # Set markers at corresponding positions
    def set_markers(self):
        for color in self.colors:
            if self.positions[color]:
                # get position of room
                room = self.positions[color]
                # get marker at this position
                self.markers.update({color: self.marker_positions[room]})
            else:
                self.markers.update({color: None})

    # Display the map
    def display_map(self):
        cv.imshow('Map', self.map)
        cv.waitKey(0)  # waits until a key is pressed
        cv.destroyAllWindows()  # destroys the window showing image

    # Display markers
    def display_markers(self, time=True):
        y_shift = 13
        tmp = {}  # Temporary dict used to shift text down when multiple colors are in the same room
        for color in self.colors:
            # Display icon
            if self.markers[color]:
                transparent = cv.imread(r"../gui/img/transparent.png")
                marker = cv.imread(r"../gui/img/marker_test.png")

                # TODO fix this
                # Resize the size of the marker to allow addWeighted
                '''
                marker = marker.transpose().copy()
                marker.resize((3, 1366, 768), refcheck=False)
                marker = marker.transpose()

                marker = cv.addWeighted(transparent, 0.1, marker, 1, 0.0)
                self.map = cv.addWeighted(self.map, 1, marker, 1, 0.0)
                '''

                # Display timings
                if time:

                    # If it's the first time looping on this room then create a key for it
                    if self.markers[color] not in tmp:
                        tmp.update({self.markers[color]: 1})

                    # Otherwise increment the count for this room
                    else:
                        tmp[self.markers[color]] = tmp[self.markers[color]] + 1

                    # Display text
                    cv.putText(self.map, color + ' : ' + str(int(self.last_seen[color])) + 's',
                               (self.markers[color][0], self.markers[color][1] + y_shift*tmp[self.markers[color]]),
                               cv.FONT_HERSHEY_PLAIN, 1.1, (0, 255, 0), 1, cv.LINE_AA)
