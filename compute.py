# Get usefull data from the sound file

import bpy
import librosa
import numpy as np

from .generate_nodes import *

# y - amplitude
# sr - sample rate
# d - number of keys per second

def get_music_spectrogram(y, sr, d, n_bins):
    # spectrogram - n_bins*X 2D array
    return librosa.feature.melspectrogram(y=y, sr=sr, hop_length=int(sr/d), n_mels=n_bins)


def clean_animation(context):
    scene = context.scene
    try:
        fcurves = scene.animation_data.action.fcurves

        i = 0
        while i < len(fcurves):
            if fcurves[i].data_path.startswith("sound_nodes"):
                fcurves.remove(fcurves[i])
                i -= 1
            i += 1
    except:
        pass


class RunAnalysis(bpy.types.Operator):
    bl_idname = "sound_nodes.run_analysis"
    bl_label = "Analyze Audio"
    bl_description = "Run analysis of audio file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #progress bar
        wm = context.window_manager
        wm.progress_begin(0, 100)
        wm.progress_update(0)

        # get fps from scene and properties
        fps = context.scene.render.fps
        properties = context.scene.sound_nodes

        # get data from audio file
        if properties.audio_source == "":
            self.report({'ERROR'}, "No audio file selected")
            return {'CANCELLED'}

        y, sr = librosa.load(properties.audio_source)

        offset = 0
        if properties.limit_frames:
            start_frame = context.scene.frame_start
            end_frame = context.scene.frame_end
            y = y[int(start_frame*sr/fps):int((end_frame+0.5)*sr/fps)]
            offset = start_frame
        
        wm.progress_update(10)
        spectrogram = get_music_spectrogram(y, sr, fps/properties.spect_smoothing, properties.spect_bins)
        wm.progress_update(20)
        loudness = get_music_spectrogram(y, sr, fps/properties.loudness_smoothing, 1)
        wm.progress_update(40)       

        clean_animation(context)

        # loudness
        loudness = loudness[0]
        if properties.loudness_normalization:
            loudness /= np.amax(loudness)

        for i in range(len(loudness)):
            properties.loudness = loudness[i]
            properties.keyframe_insert(data_path="loudness", frame=i*properties.loudness_smoothing+offset, group="Sound Nodes")
        wm.progress_update(80)

        # spectrogram
        if properties.spectrogram_normalization:
            spectrogram /= np.amax(spectrogram)

        num_frequency_bins = spectrogram.shape[0]

        for i in range(spectrogram.shape[1]):
            array = spectrogram[:, i]
            array = np.pad(array, (0, 32-num_frequency_bins), mode='constant', constant_values=(0, 0))

            properties.spectrogram1 = array
            properties.keyframe_insert(data_path="spectrogram1", frame=i*properties.spect_smoothing+offset, group="Sound Nodes")

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr) 
        beat_frame_numbers = [round(time * fps) for time in beat_times]
        beat_pulse_width = properties.beat_pulse_width 

        for beat_frame in beat_frame_numbers:
            start_pulse = beat_frame - beat_pulse_width // 2
            end_pulse = beat_frame + beat_pulse_width // 2

            # Set 0 just before the onset
            properties.beats_raw = 0
            properties.keyframe_insert(data_path="beats_raw", frame=start_pulse-1, group="Sound Nodes")
            
            properties.beats_triangle = 0
            properties.keyframe_insert(data_path="beats_triangle", frame=start_pulse-1, group="Sound Nodes")

            # Set 1 at the onset and offset
            properties.beats_raw = 1
            properties.keyframe_insert(data_path="beats_raw", frame=start_pulse, group="Sound Nodes")
            properties.keyframe_insert(data_path="beats_raw", frame=end_pulse, group="Sound Nodes")

            # For triangle waves set at center
            properties.beats_triangle = 1
            properties.keyframe_insert(data_path="beats_triangle", frame=beat_frame, group="Sound Nodes")

            # Set 0 just after the offset
            properties.beats_raw = 0
            properties.keyframe_insert(data_path="beats_raw", frame=end_pulse+1, group="Sound Nodes")
            
            properties.beats_triangle = 0
            properties.keyframe_insert(data_path="beats_triangle", frame=end_pulse+1, group="Sound Nodes")


        # TODO
        # average_frequency = np.mean(librosa.core.fft_frequencies(sr=sr))
        # beats_triangle = librosa.util.frame(beats_raw, frame_length=sr//fps, hop_length=sr//fps).T

        wm.progress_update(90)

        # generate / refresh nodes
        generate_loudness_group()
        generate_avg_freq()
        generate_beats_raw()
        generate_beats_triangle()
        generate_chromagram()
        generate_spectrogram(num_frequency_bins)
        generate_spectrogram_v2(num_frequency_bins)

        wm.progress_end()

        return {'FINISHED'}