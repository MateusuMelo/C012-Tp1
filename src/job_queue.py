from device import Device
from models import Model
import time

class Queue:
    def __init__(self, device: Device):
        self.worker = device
        self.queue = []
        self.wait_times = []  # Armazenar os tempos de espera

    def queue_add_job(self, model: Model):
        model.arrival_time = time.time()  # Registra o tempo de chegada do modelo
        print(f"Adding {model.name} to queue.")
        self.queue.append(model)

    def queue_start(self, scheduling="FCFS"):
        if not self.queue:
            print("Queue is empty")
            return

        # Escolhe o algoritmo de escalonamento
        if scheduling == "SJF":
            self.queue.sort(key=lambda model: model.complexity)  # Shortest Job First
        elif scheduling == "FCFS":
            pass  # First-Come, First-Served (não precisa de ordenação)
        else:
            print(f"Scheduling '{scheduling}' not supported")
            return None

        print(f"Starting queue with {scheduling} scheduling...\n")
        start_time = time.time()  # Marca o início do processamento total

        # Processa cada modelo
        for model in self.queue:
            model_start_time = time.time()  # Tempo de início do modelo
            wait_time = model_start_time - model.arrival_time  # Calcula o tempo de espera
            self.wait_times.append(wait_time)  # Armazena o tempo de espera

            self.worker.execute(model)  # Executa o modelo
            model_end_time = time.time()  # Tempo de fim do modelo
            execution_time = model_end_time - model_start_time  # Tempo de execução
            print(f"Model {model.name} executed in {execution_time:.2f}s after waiting {wait_time:.2f}s")

        # Marca o tempo total de execução de todos os modelos
        end_time = time.time()
        total_time = end_time - start_time

        # Calcula o tempo médio de espera
        average_wait_time = sum(self.wait_times) / len(self.wait_times)
        print(f"\nTotal processing time: {total_time:.2f}s")
        print(f"Average wait time: {average_wait_time:.2f}s")

        return None
