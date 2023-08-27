import bpy


class SOUNDNODES_PT_Panel(bpy.types.Panel):
    bl_idname = "SOUNDNODES_PT_Panel"
    bl_label = "Sound Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Sound Nodes"
    bl_context = "object"

    def draw(self, context):
        propeties = context.scene.sound_nodes

        layout = self.layout
        layout.label(text="Audio source:")
        layout.prop(propeties, "audio_source", text="")
        layout.operator("sound_nodes.load_audio")
        layout.operator("sound_nodes.run_analysis")


class SOUNDNODES_PT_AdvancedPanel(bpy.types.Panel):
    bl_idname = "SOUNDNODES_PT_AdvancedPanel"
    bl_label = "Advanced"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Sound Nodes"
    bl_context = "object"
    bl_parent_id = "SOUNDNODES_PT_Panel"

    def draw(self, context):
        propeties = context.scene.sound_nodes

        layout = self.layout

        layout.label(text="A fork of Sound Nodes addon.")
        layout.label(text="Consider buying the original version here:")
        layout.label(text="https://blendermarket.com/products/sound-nodes")

        box0 = layout.box()
        box0.label(text="General:")
        box0.prop(propeties, "limit_frames", text="Limit to scene frames")

        box1 = layout.box()
        box1.label(text="Loudness:")
        box1.prop(propeties, "loudness_smoothing", text="Smoothing factor")
        box1.prop(propeties, "loudness_normalization", text="Normalize")
        box1.enabled = False

        box2 = layout.box()
        box2.label(text="Average Frequency:")
        box2.prop(propeties, "avg_freq_smoothing", text="Smoothing factor")
        box2.enabled = False

        box3 = layout.box()
        box3.label(text="Beats:")
        box3.prop(propeties, "estimated_tempo", text="Estimated tempo")
        box3.enabled = False

        box4 = layout.box()
        box4.label(text="Spectrogram:")
        box4.prop(propeties, "spect_bins", text="Number of bins")
        box4.prop(propeties, "spect_smoothing", text="Smoothing factor")
        box4.prop(propeties, "spectrogram_normalization", text="Normalize")
        box4.enabled = False

        box5 = layout.box()
        box5.label(text="Chromagram:")
        box5.prop(propeties, "chroma_smoothing", text="Smoothing factor")
        box5.enabled = False