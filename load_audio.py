import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
import os

class LoadAudio(bpy.types.Operator, ImportHelper):
    bl_idname = "sound_nodes.load_audio"
    bl_label = "Load Audio"
    bl_description = "Choose file from disk"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default='*.wav;*.mp3;*.ogg;*.flac',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #filepath = self.filepath
        directory = str(os.path.dirname(self.filepath))
        filename = str(os.path.basename(self.filepath))

        # save to scene properties
        context.scene.sound_nodes.audio_source = self.filepath

        # add audio to scene
        if not context.scene.sequence_editor:
            context.scene.sequence_editor_create()
        
        # delete all sequences that end with "- sound nodes"
        for seq in context.scene.sequence_editor.sequences:
            if seq.name.endswith("- sound nodes"):
                context.scene.sequence_editor.sequences.remove(seq)

        # add audio to scene
        context.scene.sequence_editor.sequences.new_sound(name=filename + " - sound nodes", filepath=self.filepath, frame_start=1, channel=4)

        # set audio sync mode
        context.scene.sync_mode = 'AUDIO_SYNC'

        return {'FINISHED'}