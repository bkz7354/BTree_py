
class BaseAnimation:
    def __init__(self, duration):
        self.progress = 0
        self.duration = duration

    def update(self, time_delta):
        if self.is_done():
            return

        self.progress += time_delta/self.duration

    def is_done(self):
        return self.progress >= 1

class AnimationManager:
    def __init__(self):
        self.running = []

    def is_running(self):
        return len(self.running) > 0

    def start_animation(self, animation, callback=None):
        self.running.append((animation, callback))

    def chain_animations(self, animation_list, callback=None):
        if len(animation_list) == 0:
            return

        if len(animation_list) == 1:
            self.start_animation(animation_list[0], callback)
        else:
            self.start_animation(animation_list[0], lambda: self.chain_animations(animation_list[1:], callback))

    def update(self, time_delta):
        for animation, cb in self.running:
            animation.update(time_delta)
            if animation.is_done() and cb is not None:
                cb()

        self.running = [(a, cb) for (a, cb) in self.running if not a.is_done()]

