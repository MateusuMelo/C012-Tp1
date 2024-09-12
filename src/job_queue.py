from device import Device
from models import Model
from multiprocessing.pool import ThreadPool

class Queue:
    def __init__(self, device: Device):
        self.worker = device
        self.queue = []

    def queue_add_job(self, model: Model):
        print("Add queue.")
        self.queue.append(model)

    def queue_start(self):
        if not self.queue:
            print("Queue is empty")
            return

        total_complexity = sum(model.complexity for model in self.queue)
        if total_complexity == 0:
            print("Total complexity is zero, cannot determine the number of threads.")
            return

        n_threads = max(1, int(self.worker.total_resources / total_complexity))  # Garantir pelo menos 1 thread

        pool = ThreadPool(processes=n_threads)

        for model in self.queue:
            pool.apply_async(self.worker.execute, (model,))  # Corrigido para passar a função e os argumentos

        pool.close()
        pool.join()

        return None