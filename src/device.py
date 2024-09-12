class Device:
    def __init__(self, name, resources):
        self.name = name
        self.total_resources = resources
        self.current_resources = resources

    def aloc_resources(self, model):
        self.current_resources -= model.complexity
        return self.current_resources

    def desaloc_resources(self, model):
        self.current_resources += model.complexity
        return self.current_resources

    def execute(self, model):
        return model.train(self)

    def reset(self):
        self.current_resources = self.total_resources
        return self.current_resources
