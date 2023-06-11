class EventLoopCommand():
    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):
    def __init__(self, seconds):
        self.seconds = seconds
