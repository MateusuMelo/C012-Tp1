from device import Device
from job_queue import Queue
from models import Model

if __name__ == "__main__":
    gtx_1080 = Device("Geforce Gtx 1080", 100)

    modelN = Model("modelN", 10)
    modelS = Model("modelS", 20)
    modelM = Model("modelM", 40)
    modelL = Model("modelL", 80)

    # Testando com diferentes mecanismos de sincronização
    for sync_mechanism in ["binary_semaphore", "monitor", "counting_semaphore"]:
        print(f"\n=== Testing with {sync_mechanism} ===")
        fila = Queue(gtx_1080, sync_mechanism=sync_mechanism)

        # Adiciona modelos à fila
        fila.queue_add_job(modelN)
        fila.queue_add_job(modelS)
        fila.queue_add_job(modelM)
        fila.queue_add_job(modelL)

        # Inicia o processamento da fila
        fila.queue_start()
