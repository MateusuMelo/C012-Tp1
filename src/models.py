import time
from utils import progress_bar
import sys
import threading

# Lock para sincronizar a saída do console
print_lock = threading.Lock()

class Model:
    def __init__(self, name: str, complexity: int):
        self.name = name
        self.complexity = complexity
        self.progress = 0

    def train(self, device, model_num):
        total_time = self.complexity
        interval = 0.1  # Intervalo de atualização do progresso em segundos
        steps = int(total_time / interval)

        # Imprime o início do treinamento
        with print_lock:
            print(f"Starting training for model: {self.name} on {device.name} (complexity: {self.complexity})")

        # Loop para simular o progresso do treinamento
        for i in range(steps + 1):
            time.sleep(interval)
            self.progress = (i / steps) * 100
            self.update_log(device, model_num)

        # Imprime a finalização do treinamento
        with print_lock:
            print(f"Finished training for model: {self.name} on {device.name}")

    def update_log(self, device, model_num):
        bar = progress_bar(self.progress, 100)
        with print_lock:
            sys.stdout.write(f"\033[{model_num + 1}B")  # Move o cursor uma linha abaixo
            sys.stdout.write(f"\r{self.name} on {device.name}: {bar}")
            sys.stdout.flush()
