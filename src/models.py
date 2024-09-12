import time
from utils import progress_bar
import sys

class Model:
    def __init__(self, name: str, complexity:int):
        self.name = name
        self.complexity = complexity
        self.progress = 0

    def train(self, device):
        total_time = self.complexity
        interval = 0.1  # Intervalo de atualização do progresso em segundos
        steps = int(total_time / interval)

        print(f"\nStarting training for model: {self.name} on {device.name} (complexity: {self.complexity})")

        for i in range(steps + 1):
            time.sleep(interval)
            self.progress = (i / steps) * 100
            self.update_log(device)

        print(f"\nFinished training for model: {self.name} on {device.name}")

    def update_log(self, device):
        bar = progress_bar(self.progress, 100)
        sys.stdout.write(f"\r{self.name} on {device.modelName}: {bar}")
        sys.stdout.flush()