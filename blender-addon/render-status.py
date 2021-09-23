bl_info = {
    "name": "Render Status",
    "author": "Josh Barlow",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "doc_url": "https://github.com/joshbarlow/render-status",
    "category": "Render",
}

import bpy
import requests
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.app.handlers import persistent

class ExampleAddonPreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    sitepath: bpy.props.StringProperty(
        name="Render-Status URL",
        subtype='NONE',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Enter the url of the render-status site eg. 127.0.0.1:5000")
        layout.prop(self, "sitepath")

class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.sitepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

# The postFrame Submit Script
@persistent
def submitFrame(scene):
    # url = 'http://127.0.0.1:5000/update'
    url = str(bpy.context.preferences.addons["render-status"].preferences.sitepath) + '/update'

    if 'http://' not in url:
        url = 'http://' + url

    print(url)
    currentFilename = bpy.path.basename(bpy.data.filepath)
    submitData = {'name': 'unsavedBlenderScene'}
    if currentFilename != '':
        submitData['name'] = currentFilename
    submitData['firstFrame'] = scene.frame_start
    submitData['lastFrame'] = scene.frame_end
    submitData['latestFrame'] = scene.frame_current

    x = requests.post(url, data = submitData)
    print(x)

bpy.app.handlers.render_post.append(submitFrame)
#bpy.app.handlers.frame_change_pre.append(submitFrame)

# Registration
def register():
    bpy.utils.register_class(OBJECT_OT_addon_prefs_example)
    bpy.utils.register_class(ExampleAddonPreferences)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_addon_prefs_example)
    bpy.utils.unregister_class(ExampleAddonPreferences)

if __name__ == "__main__":
    register()
