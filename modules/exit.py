class Exit:

    def __init__(self):
        self.status = False

    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status