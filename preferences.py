import os
import subprocess
import sys

import bpy


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    

    check_installation: bpy.props.StringProperty(
        name="",
        default="",
    )
 
    def draw(self, context):
        layout = self.layout
        layout.label(text='This is Lite version of Sound Nodes addon.')
        layout.label(text='To access all features of Sound Nodes please consider purchasing the full version addon.')
        layout.label(text='https://blendermarket.com/products/sound-nodes')
        layout.label(text=' ')
        layout.label(text='For addon to work we need to install librosa python library:')
        row = layout.row()
        col1 = row.split()
        col2 = row.split()
        col1.operator("sound_nodes.install_dependencies")
        col2.operator("sound_nodes.uninstall_dependencies", icon="CANCEL")
        layout.label(text='Check if librosa is installed (restart might be needed):')
        row2 = layout.row()
        row2.split().operator("scene.check_installation_sound_nodes")
        row2.split().prop(self, "check_installation")


class InstallDependencies(bpy.types.Operator):
    bl_idname = "sound_nodes.install_dependencies"
    bl_label = "Install Requirements"
    bl_description = "Install Librosa library"
 
    def execute(self, context):
        python_exe = os.path.join(sys.executable)
        site_packages = os.path.join(sys.prefix, 'lib', 'site-packages')
        subprocess.call([python_exe, "-m", "ensurepip"])

        try:
            # test if we have write access to site-packages
            f = open(os.path.join(site_packages, "test-temp-soundnodes.txt"), "w")
            f.close()
            os.remove(os.path.join(site_packages, "test-temp-soundnodes.txt"))
            access = True
        except:
            access = False


        try:
            if access:
                print ("installing to site-packages")
                # install librosa to site-packages
                subprocess.call([python_exe, "-m", "pip", "install", "--target=%s"%(site_packages), "librosa==0.9.2"])
            else:
                print ("installing to user directory")
                # install librosa to user directory
                subprocess.call([python_exe, "-m", "pip", "install", "librosa==0.9.2"])

            return {'FINISHED'}
        except Exception as e:
            return {'CANCELLED'}

        


class UninstallDepencencies(bpy.types.Operator):
    bl_idname = "sound_nodes.uninstall_dependencies"
    bl_label = "Remove"
    bl_description = "Uninstall Librosa library"
    icon = 'CANCEL'
 
    def execute(self, context):
        python_exe = os.path.join(sys.executable)
        subprocess.call([python_exe, "-m", "pip", "uninstall", "-y", "librosa"])
        
        return {'FINISHED'}


class CheckInstallation(bpy.types.Operator):
    bl_idname = "scene.check_installation_sound_nodes"
    bl_label = "Check Installation"
    bl_description = "Check if Librosa library is installed"
 
    def execute(self, context):
        preferences = bpy.context.preferences.addons[__package__].preferences
        
        # Check if Librosa python library is installed
        try:
            import librosa
            del librosa
            preferences.check_installation = "Librosa is installed"
            print("Librosa is installed")
            return {'FINISHED'}
        except:
            try:
                # try adding site-packages to path
                python_exe = os.path.join(sys.executable)
                loc = subprocess.check_output([python_exe, "-m", "pip", "show", "librosa"])
                loc = loc.splitlines()[7].split()[1].decode("utf-8")
                sys.path.insert(0, loc)

                import librosa
                del librosa
                preferences.check_installation = "Librosa is installed"
                print("Librosa is installed")
                return {'FINISHED'}
            except:
                preferences.check_installation = "Missing requirements"
                print("Missing requirements")
                return {'FINISHED'}