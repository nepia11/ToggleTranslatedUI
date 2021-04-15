import bpy

bl_info = {
    "name": "Toggle Translated UI",
    "author": "Original:Satoshi Yamasaki(yamyam), Converted to 2.83: Toudou++",
    "version": (3, 0),
    "blender": (2, 83, 0),
    "description": "Toggle International Fonts option to switch translated / non transleted UI.",
    "location": "shortcut: End key",
    "wiki_url": "https://www.cgradproject.com/archives/5503/",
    "tracker_url": "",
    "category": "System",
}


class OBJECT_OT_translatedUI_toggle(bpy.types.Operator):
    """Toggle International Fonts"""

    bl_idname = "object.translatedui_toggle"
    bl_label = "Toggle Translated UI"

    def execute(self, context):
        b = bpy.context.preferences.view.use_translate_interface
        bpy.context.preferences.view.use_translate_interface = not b
        b = bpy.context.preferences.view.use_translate_tooltips
        bpy.context.preferences.view.use_translate_tooltips = not b
        return {"FINISHED"}


# Registration


def register():
    bpy.utils.register_class(OBJECT_OT_translatedUI_toggle)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
        #        kmi = km.keymap_items.new('object.translatedui_toggle', 'SPACE', 'PRESS', shift=True)
        kmi = km.keymap_items.new("object.translatedui_toggle", "END", "PRESS")


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_translatedUI_toggle)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["Window"]
        for kmi in km.keymap_items:
            if kmi.idname == "object.translatedui_toggle":
                km.keymap_items.remove(kmi)
                break


if __name__ == "__main__":
    register()
