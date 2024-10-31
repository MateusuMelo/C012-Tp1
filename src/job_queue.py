import time
from device import Device
from models import Model
from multiprocessing.pool import ThreadPool
import threading

# Define semáforos e bloqueios
binary_semaphore = threading.Semaphore(1)
monitor_lock = threading.Lock()
counting_semaphore = threading.Semaphore(2)  # Permite até 2 treinamentos simultâneos

class Queue:
    def __init__(self, device: Device, sync_mechanism="binary_semaphore"):
        self.worker = device
        self.queue = []
        self.sync_mechanism = sync_mechanism  # Mecanismo de sincronização a ser usado
        self.wait_times = []  # Lista para armazenar tempos de espera

    def queue_add_job(self, model: Model):
        print(f"Adding {model.name} to queue.")
        self.queue.append(model)

    def queue_start(self):
        if not self.queue:
            print("Queue is empty")
            return

        print(f"Starting queue with {self.sync_mechanism} synchronization...")
        start_time = time.time()  # Início do processamento total
        # Enquanto houver modelos na fila
        while self.queue:
            ready = []

            # Verificar quais modelos podem ser alocados ao mesmo tempo
            for model in self.queue:
                if model.complexity <= self.worker.current_resources:
                    self.worker.aloc_resources(model)
                    ready.append(model)

            if not ready:
                print("No available resources for any model, waiting...")
                break  # Isso previne loops infinitos se não houver capacidade suficiente

            # Remover modelos prontos da fila original
            for model in ready:
                self.queue.remove(model)

            # Número de threads é o número de modelos prontos para treinar simultaneamente
            n_threads = len(ready)
            pool = ThreadPool(processes=n_threads)

            # Iniciar o treinamento de cada modelo em uma thread separada com o mecanismo de sincronização adequado
            for i, model in enumerate(ready):
                model_start_time = time.time()  # Tempo de início do modelo
                wait_time = model_start_time - model.arrival_time  # Calcula o tempo de espera
                self.wait_times.append(wait_time)  # Armazena o tempo de espera

                # Escolha do mecanismo de sincronização
                if self.sync_mechanism == "binary_semaphore":
                    pool.apply_async(self.train_with_binary_semaphore, (model, i))
                elif self.sync_mechanism == "monitor":
                    pool.apply_async(self.train_with_monitor, (model, i))
                elif self.sync_mechanism == "counting_semaphore":
                    pool.apply_async(self.train_with_counting_semaphore, (model, i))
                else:
                    raise ValueError("Unsupported synchronization mechanism")

            pool.close()
            pool.join()

            # Depois que os modelos são treinados, liberar os recursos ocupados
            for model in ready:
                self.worker.desaloc_resources(model)

            end_time = time.time()
            total_time = end_time - start_time
            average_wait_time = sum(self.wait_times) / len(self.wait_times)
            print(f"\nTotal processing time: {total_time:.2f}s")
            print(f"Average wait time: {average_wait_time:.2f}s\n")
            ready = []

        print("Queue finished processing.")

    # Métodos para cada mecanismo de sincronização
    def train_with_binary_semaphore(self, model, model_num):
        with binary_semaphore:
            model.train(self.worker, model_num)

    def train_with_monitor(self, model, model_num):
        with monitor_lock:
            model.train(self.worker, model_num)

    def train_with_counting_semaphore(self, model, model_num):
        with counting_semaphore:
            model.train(self.worker, model_num)
