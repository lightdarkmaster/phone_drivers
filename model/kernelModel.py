class PhoneDriverController:
    def __init__(self):
        self.camera = None
        self.file_storage = None

    def set_camera(self, camera):
        self.camera = camera

    def set_file_storage(self, file_storage):
        self.file_storage = file_storage

    def take_picture(self):
        if self.camera is None:
            raise Exception("Camera not set")
        return self.camera.take_picture()

    def save_picture(self, picture):
        if self.file_storage is None:
            raise Exception("File storage not set")
        return self.file_storage.save_picture(picture)
