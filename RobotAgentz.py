from mesa import Agent

from PackageAgent import PackageAgent
from RoadAgent import RoadAgent

class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.contador=0
    
    def step(self):
        self.move()

    def move(self):
        old_position = self.pos
        self.contador+=1
        package_agent = self.model.get_package_agent()
        if self.pos == self.get_next_position(package_agent,package_agent.pos):
            package_agent.is_robot_ready = True
        else:
            package_agent.is_robot_ready = False
        
        # Verifica si el PackageAgent ha llegado a la meta
        if not package_agent.end:
            next_position = self.get_next_position(package_agent,package_agent.pos)
            self.model.grid.move_agent(self, next_position)



             #Comprueba si la antigua posición está vacía
            #Esto se hace para que cuando el agente se mueva de la primera posición, llene ese espacio
            #con un RoadAgent
            if len(self.model.grid.get_cell_list_contents([old_position])) == 0:
                print("vacio")
                # Si está vacía, crea un nuevo RoadAgent en esa posición
                road_agent = RoadAgent(self.model.nextId(), self.model)
                self.model.grid.place_agent(road_agent, old_position)
                self.model.schedule.add(road_agent)
        else:
            print("El paquete ha llegado a la meta. El robot se detiene.")


    def get_package_position(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, PackageAgent):
                return agent.pos
            
    def get_next_position(self, package_agent, package_pos):
        # Obtiene la próxima posición del PackageAgent
        next_package_pos = package_agent.get_next_position()
        
        # Calcula la dirección en la que el PackageAgent se moverá
        dx = next_package_pos[0] - package_pos[0]
        dy = next_package_pos[1] - package_pos[1]

        # Calcula la posición necesaria para empujar el PackageAgent en esa dirección
        push_pos = (package_pos[0] - dx, package_pos[1] - dy)

        return push_pos

    