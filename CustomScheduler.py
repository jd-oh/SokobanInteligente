from mesa.time import BaseScheduler

class CustomScheduler(BaseScheduler):
    def step(self):
        for agent in self.agent_buffer(shuffled=False):
            agent.step()
        self.steps += 1
        self.time += 1
