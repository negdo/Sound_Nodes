import bpy


class SoundNodesPropertyGroup(bpy.types.PropertyGroup):
    audio_source: bpy.props.StringProperty(
        description="Path to audio file",
        default="",
        maxlen=1024
    )

    loudness: bpy.props.FloatProperty(
        description="Loudness of audio",
        default=0.0,
        min=0.0,
        max=1.0
    )

    spectrogram1: bpy.props.FloatVectorProperty(
        description="Spectrogram of audio",
        size=32,
        default=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    )

    spectrogram2: bpy.props.FloatVectorProperty(
        description="Spectrogram of audio",
        size=32,
        default=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    )

    spect_bins: bpy.props.IntProperty(
        description="Number of bins in spectrogram",
        default=12,
        min=1,
        max=64
    )

    estimated_tempo: bpy.props.IntProperty(
        description="Estimated tempo of audio",
        default=120,
        min=0,
        max=500
    )

    spect_smoothing: bpy.props.FloatProperty(
        description="Ratio of skipped frames",
        default=1.0,
        min=1.0
    )

    chroma_smoothing: bpy.props.FloatProperty(
        description="Ratio of skipped frames",
        default=1.0,
        min=1.0
    )

    avg_freq_smoothing: bpy.props.FloatProperty(
        description="Ratio of skipped frames",
        default=1.0,
        min=1.0
    )

    loudness_smoothing: bpy.props.FloatProperty(
        description="Ratio of skipped frames",
        default=1.0,
        min=1.0
    )

    loudness_normalization: bpy.props.BoolProperty(
        description="Normalize loudness",
        default=True
    )

    spectrogram_normalization: bpy.props.BoolProperty(
        description="Normalize spectrogram",
        default=True
    )

    detected_tempo: bpy.props.FloatProperty(
        description="Detected tempo of audio",
        default=0.0,
        min=0.0
    )

    limit_frames: bpy.props.BoolProperty(
        description="Limit frames to only scene frame range",
        default=True
    )