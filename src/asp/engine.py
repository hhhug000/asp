"""
main engine class

for the game loop scene management and asset handling.
"""
from typing import Optional

from direct.showbase.ShowBase import ShowBase
from panda3d.core import ClockObject

from asp.components import Camera, Transform
from asp.input import InputHandler
from asp.gameobject import GameObject

# create clock
globalClock = ClockObject.get_global_clock()

class Engine(ShowBase):
    def __init__(self):
        super().__init__()
        
        # setup engine state
        self.running = True
        self.all_entities: list[GameObject] = []
        self.active_camera: Optional[Camera] = None
        self.input = InputHandler(self)

        # link the engine loop func to run every frame
        self.taskMgr.add(self._engine_loop, "MainEngineLoop")

    def _engine_loop(self, task):
        # time since last frame (delta time)
        dt = globalClock.getDt()
        
        # update all the entities
        for entity in self.all_entities:
            entity._update_components(dt)

        self._sync_active_camera()
        self.input.update()
            
        return task.cont # run again next frame

    def _set_active_camera(self, camera: Optional[Camera]):
        if camera is not None and camera.game_object is not None and camera.game_object.engine not in (None, self):
            raise ValueError("camera belongs to a different engine")

        self.active_camera = camera
        self._sync_active_camera()

    def _sync_active_camera(self):
        camera = self.active_camera
        if camera is None or camera.game_object is None:
            return

        transform = camera.game_object.get_component(Transform)
        if transform is None:
            return

        self.camera.setPos(transform.position.x, transform.position.y, transform.position.z)
        self.camera.setHpr(transform.rotation.x, transform.rotation.y, transform.rotation.z)

    def run(self):
        super().run()