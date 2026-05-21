"""
main engine class

for the game loop scene management and asset handling.
"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import ClockObject

from asp.gameobject import GameObject

# create clock
globalClock = ClockObject.get_global_clock()

class Engine(ShowBase):
    def __init__(self):
        super().__init__()
        
        # setup engine state
        self.running = True
        self.all_entities: list[GameObject] = []
        
        # link the engine loop func to run every frame
        self.taskMgr.add(self._engine_loop, "MainEngineLoop")

    def _engine_loop(self, task):
        # time since last frame (delta time)
        dt = globalClock.getDt()
        
        # update all the entities
        for entity in self.all_entities:
            entity._update_components(dt)
            
        return task.cont # run again next frame

    def run(self):
        super().run()