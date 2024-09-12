from models import Model
from device import Device
from job_queue import Queue
if __name__ == "__main__":
    gtx_1080 = Device("Geforce Gtx 1080",100)

    modelN = Model("modelN", 10)
    modelS = Model("modelS", 20)
    modelM = Model("modelM", 40)
    modelL= Model("modelL", 80)


    fila = Queue(gtx_1080)

    fila.queue_add_job(modelN)
    fila.queue_add_job(modelS)
    fila.queue_add_job(modelM)
    fila.queue_add_job(modelL)

    fila.queue_start()

    #modelN.train(gtx_1080)