class Camera:
    """Defines the camera class. Essentially just a fancy way to store variables (But isn't that kinda the heart of OOP?)."""
    def __init__(self,mode,focuspoint, bounds):
        """Initializer for the camera.
        :param mode: does nothing. Had a function planned, but never realized.
        :param focuspoint: the point the camera is following
        :bounds: the extents where the camera will stop following the specified point
        :return: a camera object"""
        self.pos = [0,0]
        #bounds are arranged thusly:[xmin, ymin, xmax, ymax]
        self.bounds = bounds
        self.zoom = 0
        self.screensize = (1280, 720)
        self.focuspoint = focuspoint
    def update(self)->None:
        """Update the camera."""
        self.pos = [self.focuspoint[0]-self.screensize[0]/2, self.focuspoint[1]-self.screensize[1]/2]
        if self.pos[0] < self.bounds[0]:
            self.pos[0] = self.bounds[0]
        if self.pos[1] < self.bounds[1]:
            self.pos[1] = self.bounds[1]
        if self.pos[0] > self.bounds[2]:
            self.pos[0] = self.bounds[2]
        if self.pos[1] > self.bounds[3]:
            self.pos[1] = self.bounds[3]
