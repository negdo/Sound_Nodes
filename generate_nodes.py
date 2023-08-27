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



def generate_sound_basic():
    # check if group already exists
    if "Sound Info" not in bpy.data.node_groups:
        sound_basic = bpy.data.node_groups.new("Sound Info", "GeometryNodeTree")

        # create group outputs
        group_outputs = sound_basic.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)
        sound_basic.outputs.new('NodeSocketFloat','Loudness')
        sound_basic.outputs.new('NodeSocketFloat',' ̶A̶v̶e̶r̶a̶g̶e̶ ̶F̶r̶e̶q̶u̶e̶n̶c̶y̶ ̶')
        sound_basic.outputs.new('NodeSocketFloat',' ̶B̶e̶a̶t̶s̶ ̶R̶a̶w̶ ̶')
        sound_basic.outputs.new('NodeSocketFloat',' ̶B̶e̶a̶t̶s̶ ̶T̶r̶i̶a̶n̶g̶l̶e̶ ̶')

        #loudness
        loudness = sound_basic.nodes.new('ShaderNodeValue')
        loudness.label = 'Loudness'
        loudness.location = (-200,100)
        set_driver(loudness, "sound_nodes[\"loudness\"]")

        # frame
        frame = sound_basic.nodes.new('ShaderNodeValue')
        frame.label = 'Frame'
        frame.location = (-200,-200)
        driver = frame.outputs[0].driver_add("default_value")
        driver.driver.expression = "frame"

        # connect
        sound_basic.links.new(loudness.outputs[0], group_outputs.inputs['Loudness'])

    else: 
        # refresh drivers
        sound_basic = bpy.data.node_groups["Sound Info"]

        # delete old drivers
        sound_basic.animation_data_clear()

        # add new drivers
        for node in sound_basic.nodes:
            if node.label == "Loudness":
                set_driver(node, "sound_nodes[\"loudness\"]")
            elif node.label == "Frame":
                driver = node.outputs[0].driver_add("default_value")
                driver.driver.expression = "frame"



def generate_chromagram():
    tones = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']   

    # check if group does not already exists
    if "Chromagram" not in bpy.data.node_groups:
        chromagram = bpy.data.node_groups.new(" ̶C̶h̶r̶o̶m̶a̶g̶r̶a̶m̶ ̶", "GeometryNodeTree")

        # create group outputs
        group_outputs = chromagram.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)

        i = 0
        for tone in tones:
            chromagram.outputs.new('NodeSocketFloat',tone)
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

    # frame
    frame = spectrogram.nodes.new('ShaderNodeValue')
    frame.label = 'Frame'
    frame.location = (-400,-200)
    driver = frame.outputs[0].driver_add("default_value")
    driver.driver.expression = "frame"


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