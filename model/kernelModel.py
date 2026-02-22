class PhoneDriverController:
    def __init__(self):
        self._camera = None
        self._file_storage = None

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    @property
    def file_storage(self):
        return self._file_storage

    @file_storage.setter
    def file_storage(self, value):
        self._file_storage = value

    def take_picture(self):
        if self._camera is None:
            raise ValueError("Camera not set")
        return self._camera.take_picture()

    def save_picture(self, picture):
        if self._file_storage is None:
            raise ValueError("File storage not set")
        return self._file_storage.save_picture(picture)

    def capture_and_save(self):
        picture = self.take_picture()
        return self.save_picture(picture)

