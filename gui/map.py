import cv2 as cv

# Used to display the map
class Map:
    marker_positions = {
        "cafeteria": (730, 191)
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
        self.map = cv.imread("img/theskeld.png")

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



    # Display markers
    def display_markers(self, time=True):
        for color in self.colors:
            if self.markers[color]:
                cv.imread("img/marker_test.png")


            if time:
                self.map = cv.addWeighted(self.map, 1)
