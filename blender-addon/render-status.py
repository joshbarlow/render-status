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

class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    sitepath: StringProperty(
        name="Example Site URL",
        subtype='NONE',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "sitepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")

class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

# The postFrame Submit Script
@persistent
def submitFrame(scene):
    url = 'http://127.0.0.1:5000/update'
    currentFilename = bpy.path.basename(bpy.data.filepath)
    submitData = {'name': 'unsavedBlenderScene'}
    if currentFilename != '':
        submitData['name'] = currentFilename
    submitData['firstFrame'] = scene.frame_start
    submitData['lastFrame'] = scene.frame_end
    submitData['latestFrame'] = scene.frame_current

    x = requests.post(url, data = submitData)
    print(x)

bpy.app.handlers.frame_change_pre.append(submitFrame)

# Registration
def register():
    bpy.utils.register_class(OBJECT_OT_addon_prefs_example)
    bpy.utils.register_class(ExampleAddonPreferences)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_addon_prefs_example)
    bpy.utils.unregister_class(ExampleAddonPreferences)

if __name__ == "__main__":
    register()
