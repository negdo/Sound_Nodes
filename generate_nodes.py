import bpy


def set_driver(node, path):
    # add new driver
    driver = node.outputs[0].driver_add("default_value")
    driver.driver.expression = "var"

    var = driver.driver.variables.new()
    var.name = "var"
    var.targets[0].id_type = 'SCENE'
    var.targets[0].id = bpy.data.scenes['Scene']
    var.targets[0].data_path = path

# We need a frame driver or else the animation doesn't work :(
def add_frame_driver(group):
    frame = group.nodes.new('ShaderNodeValue')
    frame.label = 'Frame'
    frame.location = (-200,-200)
    driver = frame.outputs[0].driver_add("default_value")
    driver.driver.expression = "frame"


def generate_loudness_group():
    group_label = "Loudness"
    node_label = "Loudness"
    value_label = "Loudness"
    value_type = "NodeSocketFloat"
    driver_name = "loudness"

    if group_label in bpy.data.node_groups:
        # refresh drivers
        loudness_group = bpy.data.node_groups[group_label]

        # delete old drivers
        loudness_group.animation_data_clear()

        # add new drivers
        for node in loudness_group.nodes:
            if node.label == node_label:
                set_driver(node, "sound_nodes[\"" + driver_name + "\"]")
            elif node.label == "Frame":
                driver = node.outputs[0].driver_add("default_value")
                driver.driver.expression = "frame"

        return

    loudness_group = bpy.data.node_groups.new(group_label, "GeometryNodeTree") 
    loudness_group.outputs.new(value_type, value_label)
    
    # create group outputs
    group_outputs = loudness_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300,0) 

    # loudness
    loudness_node = loudness_group.nodes.new('ShaderNodeValue')
    loudness_node.label = node_label
    loudness_node.location = (-200,100)
    set_driver(loudness_node, "sound_nodes[\"" + driver_name + "\"]")

    add_frame_driver(loudness_group)

    loudness_group.links.new(loudness_node.outputs[0], group_outputs.inputs[value_label])

def generate_avg_freq():
    group_label = "Average Frequency"
    node_label = "Average Frequency"
    value_label = "Average Frequency"
    value_type = "NodeSocketFloat"
    driver_name = "avg_freq"

    if group_label in bpy.data.node_groups:
        # refresh drivers
        avg_freq_group = bpy.data.node_groups[group_label]

        # delete old drivers
        avg_freq_group.animation_data_clear()

        # add new drivers
        for node in avg_freq_group.nodes:
            if node.label == node_label:
                set_driver(node, "sound_nodes[\"" + driver_name + "\"]")
            elif node.label == "Frame":
                driver = node.outputs[0].driver_add("default_value")
                driver.driver.expression = "frame"

        return
    
    avg_freq_group = bpy.data.node_groups.new(group_label, "GeometryNodeTree")
    avg_freq_group.outputs.new(value_type, value_label)

    # create group outputs
    group_outputs = avg_freq_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300,0)

    # avg_freq
    avg_freq_node = avg_freq_group.nodes.new('ShaderNodeValue')
    avg_freq_node.label = node_label
    avg_freq_node.location = (-200,100)
    set_driver(avg_freq_node, "sound_nodes[\"" + driver_name + "\"]")

    add_frame_driver(avg_freq_group)

    avg_freq_group.links.new(avg_freq_node.outputs[0], group_outputs.inputs[value_label])

def generate_beats_raw():
    group_label = "Beats Raw"
    node_label = "Beats Raw"
    value_label = "Beats Raw"
    value_type = "NodeSocketFloat"
    driver_name = "beats_raw"

    if group_label in bpy.data.node_groups:
        # refresh drivers
        beats_raw_group = bpy.data.node_groups[group_label]

        # delete old drivers
        beats_raw_group.animation_data_clear()

        # add new drivers
        for node in beats_raw_group.nodes:
            if node.label == node_label:
                set_driver(node, "sound_nodes[\"" + driver_name + "\"]")
            elif node.label == "Frame":
                driver = node.outputs[0].driver_add("default_value")
                driver.driver.expression = "frame"

        return

    beats_raw_group = bpy.data.node_groups.new(group_label, "GeometryNodeTree")
    beats_raw_group.outputs.new(value_type, value_label)

    # create group outputs
    group_outputs = beats_raw_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300,0)

    # beats_raw
    beats_raw_node = beats_raw_group.nodes.new('ShaderNodeValue')
    beats_raw_node.label = node_label
    beats_raw_node.location = (-200,100)
    set_driver(beats_raw_node, "sound_nodes[\"" + driver_name + "\"]")

    add_frame_driver(beats_raw_group)

    beats_raw_group.links.new(beats_raw_node.outputs[0], group_outputs.inputs[value_label])

# beats_triangle
def generate_beats_triangle():
    group_label = "Beats Triangle"
    node_label = "Beats Triangle"
    value_label = "Beats Triangle"
    value_type = "NodeSocketFloat"
    driver_name = "beats_triangle"

    if group_label in bpy.data.node_groups:
        # refresh drivers
        beats_triangle_group = bpy.data.node_groups[group_label]

        # delete old drivers
        beats_triangle_group.animation_data_clear()

        # add new drivers
        for node in beats_triangle_group.nodes:
            if node.label == node_label:
                set_driver(node, "sound_nodes[\"" + driver_name + "\"]")
            elif node.label == "Frame":
                driver = node.outputs[0].driver_add("default_value")
                driver.driver.expression = "frame"

        return

    beats_triangle_group = bpy.data.node_groups.new(group_label, "GeometryNodeTree")
    beats_triangle_group.outputs.new(value_type, value_label)

    # create group outputs
    group_outputs = beats_triangle_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (300,0)

    # beats_triangle
    beats_triangle_node = beats_triangle_group.nodes.new('ShaderNodeValue')
    beats_triangle_node.label = node_label
    beats_triangle_node.location = (-200,100)
    set_driver(beats_triangle_node, "sound_nodes[\"" + driver_name + "\"]")

    add_frame_driver(beats_triangle_group)

    beats_triangle_group.links.new(beats_triangle_node.outputs[0], group_outputs.inputs[value_label])


def generate_chromagram():
    tones = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']   

    # check if group does not already exists
    if "Chromagram" not in bpy.data.node_groups:
        chromagram = bpy.data.node_groups.new("Chromagram", "GeometryNodeTree")

        # create group outputs
        group_outputs = chromagram.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)

        i = 0
        for tone in tones:
            chromagram.outputs.new('NodeSocketFloat', tone)
            i += 1


def generate_spectrogram(spect_bins):
    # check if group already exists
    if "Spectrogram" not in bpy.data.node_groups:
        spectrogram = bpy.data.node_groups.new("Spectrogram", "GeometryNodeTree")

        # create group outputs
        group_outputs = spectrogram.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)

        for i in range(spect_bins):
            spectrogram.outputs.new('NodeSocketFloat', str(i))

    else:
        spectrogram = bpy.data.node_groups["Spectrogram"]
        group_outputs = spectrogram.nodes["Group Output"]

        # delete all nodes except group inputs and outputs
        for node in spectrogram.nodes:
            if node.type != "GROUP_OUTPUT":
                spectrogram.nodes.remove(node)

    
    for i in range(0, spect_bins):
        # node
        node = spectrogram.nodes.new('ShaderNodeValue')
        node.label = str(i)
        node.location = (-200,100 - (i * 100))
        if i < 32:
            set_driver(node, "sound_nodes[\"spectrogram1\"][" + str(i) + "]")
        else:
            set_driver(node, "sound_nodes[\"spectrogram2\"][" + str(i-32) + "]")

        # connect
        spectrogram.links.new(node.outputs[0], group_outputs.inputs[str(i)])

    add_frame_driver(spectrogram)


def generate_spectrogram_v2(spect_bins):
    # check if group already exists
    if "Spectrogram Separate" not in bpy.data.node_groups:
        spectrogram = bpy.data.node_groups.new(" ̶S̶p̶e̶c̶t̶r̶o̶g̶r̶a̶m̶ ̶S̶e̶p̶a̶r̶a̶t̶e̶ ̶", "GeometryNodeTree")

        # create group inputs
        group_inputs = spectrogram.nodes.new('NodeGroupInput')
        group_inputs.location = (-600,0)
        spectrogram.inputs.new('NodeSocketInt','Index')

        # create group outputs
        group_outputs = spectrogram.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)
        spectrogram.outputs.new('NodeSocketFloat','Value')