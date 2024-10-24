from device import Device
from models import Model
import time

class Queue:
    def __init__(self, device: Device):
        self.worker = device
        self.queue = []

    def queue_add_job(self, model: Model):
        print("Add queue.")
        self.queue.append(model)

    def queue_start(self, scheduling="FCFS"):
        if not self.queue:
            print("Queue is empty")
            return

        if scheduling == "SJF":
            self.queue.sort(key=lambda model: model.complexity)
        elif scheduling == "FCFS":
            pass
        else:
            print("Scheduling not supported")
            return None

        for model in self.queue:
            self.worker.execute(model)

        return None
