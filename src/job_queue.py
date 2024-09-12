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
        return None

    def queue_start(self):
        if not self.queue:
            print("Queue is empty")
            return
        # Enquanto houver modelos na fila
        while len(self.queue) > 0:
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

            # O número de threads é o número de modelos prontos para treinar simultaneamente
            n_threads = len(ready)
            pool = ThreadPool(processes=n_threads)

            # Iniciar o treinamento de cada modelo em uma thread separada
            for i, model in enumerate(ready):
                pool.apply_async(model.train, (self.worker, i))  # i como índice para organizar linhas

            pool.close()
            pool.join()

            # Depois que os modelos são treinados, liberar os recursos ocupados
            for model in ready:
                self.worker.desaloc_resources(model)

            ready = []

        print("Queue finished processing.")
