import pygame
from ..scenes import AbstractHorizontalScene
from game.entities import Platform, Player, Enemy
from ..scenes.backgrounds import MainBackground
from ..scenes import Scene
from ..util import Clog
from ..entities import Object
from ..entities import Trigger
from game import Configuration
from pygame.locals import *
import os
import json

class Level():
    def __init__(self, filename, director):
        self._clog = Clog(__name__)
        self.id = None
        self.name = None
        self.scenes = []
        self.director = director

        self._clog.info("Loading level")
        self.construct_file_path(filename)
        self.load_json_file()
        self.parse_json(self._json_data)
        self._clog.info("Level loading finished")

    def get_scenes(self):
        return self.scenes

    def construct_file_path(self, filename):
        path = os.path.dirname(os.path.realpath(__file__))
        self._level_file = os.path.join(path, filename, "level.json")

    def load_json_file(self):
        with open(self._level_file) as f:
            self._json_data = json.loads(f.read())

    def parse_coords(self, json):
        return (json['pos_x'], json['pos_y'])

    def parse_player(self, json):
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        speedx = 25 #REPLACE ME
        speedy = 40 #REPLACE ME
        datafn = json['data']
        return Player(self.name, datafn, coords, speedx, speedy, invert)

    def parse_platform(self, json):
        sprite = json['sprite']
        collid = json['collides']
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        return Platform(self.name, sprite, collid, coords, invert)

    def parse_object(self, json):
        kind   = json['kind']
        sprite = json['sprite']
        collid = json['collides']
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        return Object(self.name, kind, sprite, collid, coords, invert)

    def parse_size(self, json):
        return (json['width'], json['height'])

    def parse_enemy(self, j):
        collid = j['collides']
        datafn = j['data']
        speedx = 10 #REPLACE ME
        speedy = 20 #REPLACE ME
        coords = self.parse_coords(j['coords'])
        invert = j['coords']['inverted']

        return Enemy(self.name, datafn, coords, speedx, speedy, invert)

    def parse_trigger(self, json):
        id     = json['event']
        indica = json['indicator']
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        size   = self.parse_size(json['size'])
        return Trigger(self.name, id, indica, coords, size, invert)

    def parse_json(self, json):
        self.id = json['id']
        self.name =  json['name']

        self._clog.info("populating level")
        for scene in json['scenes']:
            s = Scene(self.name, self.director, scene['id'], scene['background'], scene['scroll'])
            s.set_player(self.parse_player(scene['player']))
        for object in scene['objects']:
            s.add_object(self.parse_object(object))
        for enemy in scene['enemies']:
            s.add_enemy(self.parse_enemy(enemy))
        for trigger in scene['triggers']:
            s.add_trigger(self.parse_trigger(trigger))
        for platform in scene['platforms']:   ###### CAREFUL ###### THIS ###### MUST ####### BE ###### THE #######
            s.add_platform(self.parse_platform(platform)) ###### LAST ###### ADDED ###### ELEMENT
                                                        ###### scene needs to know the enemies/players before this
        self.scenes.append(s)
        self._clog.info("scene added")
