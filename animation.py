
class EmptyAnimation:
    def __init__(self, callback=None):
        self.callback = callback
        self.done = False
    
    def update(self, time_delta):
        if self.is_done():
            return
        
        self.done = True
        if self.callback is not None:
            return self.callback(self)
        return self

    def is_done(self):
        return self.done
    


class SingularAnimation:
    def __init__(self, duration, callback=None):
        self.progress = 0
        self.duration = duration
        self.callback = callback

    def update(self, time_delta):
        if self.is_done():
            return

        self.progress += time_delta/self.duration
        if self.progress > 1:
            self.progress = 1
        self.update_objects()

        if self.is_done() and self.callback is not None:
            return self.callback(self)
        return self

    def update_objects(self):
        pass

    def is_done(self):
        return self.progress >= 1

class SequentialAnimation:
    def __init__(self, animation_list, callback=None):
        self.animations = animation_list
        self.callback = callback

    def update(self, time_delta):
        if self.is_done():
            return

        self.animations[0] = self.animations[0].update(time_delta)
        if self.animations[0].is_done():
            del self.animations[0]

        if self.is_done() and self.callback is not None:
            self.callback(self)
        return self

    def is_done(self):
        return len(self.animations) == 0

class ParallelAnimation:
    def __init__(self, animation_list, callback=None):
        self.animations = animation_list
        self.callback = callback

    def update(self, time_delta):
        if self.is_done():
            return

        for a in self.animations:
            a.update(time_delta)

        if self.is_done() and self.callback is not None:
            return self.callback(self)
        return self

    def is_done(self):
        return all([x.is_done() for x in self.animations])

class AnimationManager:
    def __init__(self):
        self.running = []

    def is_running(self):
        return len(self.running) > 0

    def queue_animation(self, animation):
        self.running.append(animation)

    def update(self, time_delta):
        if not self.is_running():
            return

        self.running[0] = self.running[0].update(time_delta)
        if self.running[0].is_done():
            del self.running[0]

