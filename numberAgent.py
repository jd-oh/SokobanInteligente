from mesa import Agent


class NumberAgent(Agent):
    def __init__(self, unique_id, model, numero):
        super().__init__(unique_id, model)
        self.numero=numero
        
