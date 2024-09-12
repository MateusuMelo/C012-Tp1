class Device:
    def __init__(self,name, resources):
        self.name = name
        self.total_resources = resources
        self.current_resources = resources

    def execute(self, model):
        self.current_resources -= model.complexity

        if self.current_resources < 0:
            raise Exception("Erro, device is out of resources")

        model.train(self)

        self.current_resources += model.complexity

        return None