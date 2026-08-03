"""
Progress Manager
"""

import time


class ProgressTracker:

    def __init__(self, total):

        self.total = max(1, total)

        self.current = 0

        self.start_time = time.time()

    def update(self):

        self.current += 1

    @property
    def percent(self):

        return round(
            (self.current / self.total) * 100,
            1
        )

    @property
    def elapsed(self):

        return time.time() - self.start_time

    @property
    def average_time(self):

        if self.current == 0:
            return 0

        return self.elapsed / self.current

    @property
    def eta(self):

        remaining = self.total - self.current

        return remaining * self.average_time

    @property
    def eta_string(self):

        seconds = int(self.eta)

        minutes = seconds // 60

        seconds = seconds % 60

        return f"{minutes}m {seconds}s"

    @property
    def progress_string(self):

        filled = int(self.percent // 10)

        empty = 10 - filled

        return "█" * filled + "□" * empty

    def status(self):

        return (
            f"\n"
            f"Generating Reel "
            f"{self.current}/{self.total}\n\n"
            f"{self.progress_string}\n\n"
            f"{self.percent}% Complete\n\n"
            f"ETA : {self.eta_string}\n"
        )