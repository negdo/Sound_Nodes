'''
Copyright (C) 2023 Miha Marinko
miha.marinko20@gmail.com

Created by Miha Marinko

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Sound Nodes",
    "description": "Visualize sound in Blender with Geometry Nodes",
    "author": "Miha Marinko",
    "version": (1, 0, 1),
    "blender": (3, 4, 0),
    "location": "Geometry Nodes",
    "warning": "",
    "wiki_url": "",
    "category": "scene",
    "bl_options": {"REGISTER", "UNDO"}}

import importlib
import sys

import bpy

from .compute import RunAnalysis
from .load_audio import *
from .preferences import *
from .properties import *
from .ui import *


def register():
    # preferences
    bpy.utils.register_class(InstallDependencies)
    bpy.utils.register_class(UninstallDepencencies)
    bpy.utils.register_class(CheckInstallation)
    bpy.utils.register_class(Preferences)

    # properties
    bpy.utils.register_class(SoundNodesPropertyGroup)
    bpy.types.Scene.sound_nodes = bpy.props.PointerProperty(type=SoundNodesPropertyGroup)

    # operators
    bpy.utils.register_class(LoadAudio)
    bpy.utils.register_class(RunAnalysis)

    # ui
    bpy.utils.register_class(SOUNDNODES_PT_Panel)
    bpy.utils.register_class(SOUNDNODES_PT_AdvancedPanel)


def unregister():
    # preferences
    bpy.utils.unregister_class(Preferences)
    bpy.utils.unregister_class(InstallDependencies)
    bpy.utils.unregister_class(UninstallDepencencies)
    bpy.utils.unregister_class(CheckInstallation)

    # properties
    bpy.utils.unregister_class(SoundNodesPropertyGroup)

    # operators
    bpy.utils.unregister_class(LoadAudio)
    bpy.utils.unregister_class(RunAnalysis)

    # ui
    bpy.utils.unregister_class(SOUNDNODES_PT_Panel)
    bpy.utils.unregister_class(SOUNDNODES_PT_AdvancedPanel)


if __name__ == '__main__':
    register()