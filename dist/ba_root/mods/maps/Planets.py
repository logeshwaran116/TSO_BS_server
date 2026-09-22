# ba_meta require api 9

#==============================================================================#
#
#     Version 1.1
#     Create by Unknown_#7004 - ( @uwu.user )
#         - Github https://github.com/uwu-user
#         - https://gamebanana.com/members/2496091
#
#==============================================================================#

from __future__ import annotations
from typing import TYPE_CHECKING, cast

import bascenev1 as ba
from bascenev1 import _map
import random, math, babase
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable, List, Dict, Tuple, Optional, Union

#==============================================================================#

class Mapdefs:
    boxes = {
        "area_of_interest_bounds": (0.0, 5.0, 1.0) + (0.0, 0.0, 0.0) + (50, 30, 50),
        "map_bounds": (0.0, 0.795, -0.468) + (0, -30, 0) + (17.5, 30, 17.5),
        "level_bounds": (-50, -50, -50) + (0.0, 0, 0) + (50, 50, 50),
        "edge_box": (0.0, 0.0, 0.0) + (0.0, 0.0, 0.0) + (0.0, 0.0, 0.0)}

    points = {
        "spawn1": (-6, 5.1, 0),
        "spawn2": (6, 5.1, 0),
        "ffa_spawn1": (4, 5.1, -3),
        "ffa_spawn2": (-4, 5.1, -3),
        "ffa_spawn3": (4, 5.1, 4),
        "ffa_spawn4": (-4, 5.1, 4),
        "powerup_spawn1": (5, 6, 4),
        "powerup_spawn2": (-5, 6, -4),
        "powerup_spawn3": (5, 6, -4),
        "powerup_spawn4": (-5, 6, 4),}

#==============================================================================#
  
class PlanetsMap(ba.Map):
    defs = Mapdefs()
    name = "Planets World"

    @classmethod
    def get_play_types(cls) -> List[str]:
        return ["melee"]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return "achievementFlawlessVictory"

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {
            "bgtex": ba.gettexture('bg'),
            "bgmesh": ba.getmesh('thePadBG')}
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self._player_floor = ba.Material()
        self._player_floor.add_actions(conditions=("we_are_older_than", 1), actions=("modify_part_collision", "collide", True))
        self.background = ba.newnode("terrain", attrs={"mesh": self.preloaddata["bgmesh"], "lighting": False, "background": True, "color": (0, 0, 0), "color_texture": self.preloaddata["bgtex"]})
        self.floor = ba.newnode("region", attrs={"position": (0, 5, 0), "scale": (40, 0.1, 40), "type": "box", "materials": [self._player_floor, shared.footing_material]})
        self.locator = ba.newnode("locator", attrs={"shape": "circleOutline", "position": (0, 5, 0), "opacity": 0.7, "draw_beauty":True, "additive":False, "size": [17.5]})

        settings = {
            "tint": (1, 1, 1),
            "ambient_color": (0.2, 0.2, 0.2),
            "vignette_outer": (0.60, 0.62, 0.66),
            "vignette_inner": (0.97, 0.95, 0.93),
            "vr_camera_offset": (0, 5, 0),
            "vr_near_clip": 1.0}

        gnode = ba.getactivity().globalsnode
        for key, value in settings.items(): setattr(gnode, key, value)
        self.effects = MapEffects()
        self.effects.load("void")
        self.effects.load("planets")

#==============================================================================#

class MapEffects:
    def __init__(self):
        self.effects = {
            "void": VoidSystem(),
            "planets": PlanetarySystem(),
        }

    def load(self, effect):
        if effect in self.effects:
            self.effects[effect].load()

    def delete(self, active_effect):
        for key, effect in self.effects.items():
            if key != active_effect:
                effect.delete()

#==============================================================================#

class VoidSystem:
    def __init__(self):
        self.flash_nodes = []
        self.timer = None
        self.activated = False
        self.num_objects = 50
        self.map_bounds = {'x': (-25, 25), 'y': (-20, 30), 'z': (-25, 25)}
        self.speed_range = (0.15, 1.0)
        self.size_range = (0.05, 0.2)

    def create_void_system(self):
        for i in range(self.num_objects):
            x = random.uniform(self.map_bounds['x'][0], self.map_bounds['x'][1])
            y = random.uniform(self.map_bounds['y'][0], self.map_bounds['y'][1])
            z = random.uniform(self.map_bounds['z'][0], self.map_bounds['z'][1])
            flash = ba.newnode("flash", attrs={'position': (x, y, z), 'size': random.uniform(self.size_range[0], self.size_range[1]), 'color': (2, 2, 2)})
            self.flash_nodes.append({
                'node': flash,
                'velocity': (
                    random.uniform(-self.speed_range[1], self.speed_range[1]),
                    random.uniform(-self.speed_range[0], self.speed_range[0]),
                    random.uniform(-self.speed_range[1], self.speed_range[1])
                ), 'direction': random.choice([-1, 1])
            })

    def update_flashes(self):
        if not self.activated: self.stop_timer(); return
        for flash_data in self.flash_nodes:
            flash = flash_data['node']
            vel = flash_data['velocity']
            pos = flash.position
            new_pos = (pos[0] + vel[0] * 0.01, pos[1] + vel[1] * 0.01, pos[2] + vel[2] * 0.01)
            reset_needed = False
            for axis, (min_val, max_val) in enumerate([self.map_bounds['x'], self.map_bounds['y'], self.map_bounds['z']]):
                if new_pos[axis] < min_val or new_pos[axis] > max_val:
                    reset_needed = True
                    break
            
            if reset_needed:
                new_pos = (
                    random.uniform(self.map_bounds['x'][0] * -0.5, self.map_bounds['x'][1] * -0.5),
                    random.uniform(self.map_bounds['y'][0], self.map_bounds['y'][1]),
                    random.uniform(self.map_bounds['z'][0] * -0.5, self.map_bounds['z'][1] * -0.5))
                flash_data['velocity'] = (
                    random.uniform(-self.speed_range[1], self.speed_range[1]),
                    random.uniform(-self.speed_range[0], self.speed_range[0]),
                    random.uniform(-self.speed_range[1], self.speed_range[1]))
            flash.position = new_pos
        if self.activated: self.timer = ba.timer(0.01, ba.Call(self.update_flashes))

    def delete(self):
        for flash_data in self.flash_nodes:
            if flash_data['node'] and flash_data['node'].exists(): flash_data['node'].delete()
        self.flash_nodes.clear()
        self.stop_timer()

    def load(self):
        self.delete()
        self.start()

    def start(self):
        self.activated = True
        self.create_void_system()
        self.start_timer()

    def start_timer(self):
        if not self.timer:
            self.timer = ba.timer(0.01, ba.Call(self.update_flashes))

    def stop_timer(self):
        if self.timer:
            self.timer = None

    def deactivate(self):
        self.activated = False
        self.stop_timer()

#==============================================================================#

class PlanetarySystem:
    Planet_data = [
        ("Mercury", (0.5, 0.5, 0.5), 0.2, 2.5, 0.24),
        ("Venus", (1, 0.8, 0), 0.25, 3.5, 0.615),
        ("Earth", (0, 0, 1), 0.3, 4.5, 1.0, (9.7, 9.7, 9.7), 0.3),
        ("Mars", (1, 0, 0), 0.2, 5.5, 1.88),
        ("Jupiter", (0.7, 0.5, 0.3), 0.4, 6.5, 11.86),
        ("Saturn", (1, 0.85, 0.25), 0.35, 7.5, 29.46),
        ("Uranus", (0.5, 0.7, 1), 0.3, 8.5, 84.01),
        ("Neptune", (0.1, 0.1, 0.8), 0.3, 9.5, 164.79)
    ]

    def __init__(self):
        self.fix_position = (0, -2, -9.5)
        self.sun = None
        self.timer = None
        self.activated = False
        self.planets = []
        self.moons = []

    def create_planetary_system(self):
        fix_x, fix_y, fix_z = self.fix_position
        self.sun = ba.newnode("shield", attrs={"position": (fix_x, fix_y, fix_z), "color": (39, 39, 0), "radius": 2})
        for data in self.Planet_data:
            if len(data) == 7: name, color, size, distance, speed, moon_color, moon_distance = data
            else:
                name, color, size, distance, speed = data
                moon_color = None
                moon_distance = None
            
            planet = Planet(name, self.x9_color(color), size, distance, speed, self.fix_position)
            self.planets.append(planet)
            if moon_color is not None and moon_distance is not None:
                moon = Moon(self.x9_color(moon_color), moon_distance, 0, self.fix_position)
                self.moons.append((planet, moon))

    def x9_color(self, color: tuple):
        return (color[0] * 9, color[1] * 9, color[2] * 9)

    def update_positions(self):
        if not self.activated: self.stop_timer(); return
        for planet in self.planets: planet.update_position(self.angle_increment)
        for planet, moon in self.moons: moon.update_position(planet.node.position, self.angle_increment)
        if bool(self.activated): self.timer = ba.timer(0.01, ba.Call(self.update_positions))

    def delete(self):
        self.deactivate()
        for objects, is_moon in [(self.planets, False), (self.moons, True)]:
            for body_info in objects:
                body = body_info[1] if is_moon else body_info
                for attr in ["node", "text_node"]:
                    if hasattr(body, attr) and getattr(body, attr):
                        getattr(body, attr).delete(); setattr(body, attr, None)
            objects.clear()
        if self.sun: self.sun.delete(); self.sun = None
        
    def load(self):
        self.deactivate()
        self.delete()
        self.start()
        
    def start(self):
        self.activated = True
        self.angle_increment = 0.1
        self.create_planetary_system()
        self.start_timer()

    def start_timer(self):
        if not self.timer:
            self.timer = ba.timer(0.01, ba.Call(self.update_positions))

    def stop_timer(self):
        if self.timer:
            self.timer = None

    def deactivate(self):
        self.activated = False
        self.stop_timer()

class Planet:
    def create_text_node(self, text: str, color: tuple, scale: float):
        return ba.newnode("text", attrs={"in_world": True, "h_align": "center", "scale": scale, "color": color, "text": text})

    def __init__(self, name: str, color: tuple, size: float, distance: float, speed: float, fix_position: tuple = (0, 8, 0)):
        self.name = name
        self.color = color
        self.size = size
        self.distance = distance
        self.speed = speed
        self.fix_position = fix_position
        self.node = ba.newnode("shield", attrs={"color": color, "radius": size + 0.5})
        self.text_node = self.create_text_node(text=f"» {name} «", color=color, scale=0.01)

    def update_position(self, angle_increment: float):
        fix_x, fix_y, fix_z = self.fix_position
        angle = self.speed * angle_increment
        x = fix_x + (self.distance * math.cos(angle))
        z = fix_z + (self.distance * math.sin(angle))
        self.node.position = (x, fix_y, z)
        self.text_node.position = (x, fix_y + 0.75, z)
        self.speed += angle_increment

class Moon:
    def create_text_node(self, text: str, color: tuple, scale: float):
        return ba.newnode("text", attrs={"in_world": True, "h_align": "center", "scale": scale, "color": color, "text": text})

    def __init__(self, color: tuple, distance: float, angle: float, fix_position: tuple = (0, 8, 0)):
        self.color = color
        self.distance = distance
        self.angle = angle
        self.fix_position = fix_position
        self.node = ba.newnode("shield", attrs={"color": color, "radius": 0.15})
        self.text_node = self.create_text_node(text=f"» Moon «", color=color, scale=0.01)

    def update_position(self, planet_position: tuple, angle_increment: float):
        self.angle += angle_increment
        if self.angle >= 2 * math.pi: self.angle -= 2 * math.pi
        moon_x = planet_position[0] + (self.distance * math.cos(self.angle))
        moon_y = planet_position[1] + (self.distance * math.sin(math.radians(37)))
        moon_z = planet_position[2] + (self.distance * math.sin(self.angle))
        self.node.position = (moon_x, moon_y, moon_z)
        self.text_node.position = (moon_x, moon_y + 0.25, moon_z)

#==============================================================================#

# ← change babase.Plugin → ba.Plugin
class system(ba.Plugin):           
    _map.register_map(PlanetsMap)