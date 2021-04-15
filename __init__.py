import bpy

bl_info = {
    "name": "Toggle Translated UI",
    "author": "Original:Satoshi Yamasaki(yamyam), Converted to 2.83: Toudou++, nepia11",
    "version": (4, 1),
    "blender": (2, 83, 0),
    "description": "Toggle Language",
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
        # インターフェースの翻訳をするか否かを切り替えている
        b = bpy.context.preferences.view.use_translate_interface
        bpy.context.preferences.view.use_translate_interface = not b
        b = bpy.context.preferences.view.use_translate_tooltips
        bpy.context.preferences.view.use_translate_tooltips = not b
        return {"FINISHED"}


class TTUI_Language_Toggle(bpy.types.Operator):
    """ 英語とその他で言語設定を切り替える　新規データのオプション強制False """

    bl_idname = "preferences.language_toggle"
    bl_label = "Toggle UI Language"

    # アドオン有効時に切り替える前の状態を保存しておく
    pref = bpy.context.preferences
    lang = "DEFAULT"
    # interface_flag = pref.view.use_translate_interface
    # tooltips_flag = pref.view.use_translate_tooltips
    # new_dataname_flag = pref.view.use_translate_new_dataname

    def execute(self, context):
        # 言語切り替えをする
        pref = bpy.context.preferences
        if pref.view.language == self.lang:
            pref.view.language = "en_US"
        else:
            pref.view.language = self.lang
            pref.view.use_translate_interface = True
            pref.view.use_translate_tooltips = True
            pref.view.use_translate_new_dataname = False
        return {"FINISHED"}


# Registration
classes = [
    OBJECT_OT_translatedUI_toggle,
    TTUI_Language_Toggle,
]

keymaps = []


def register():
    for c in classes:
        bpy.utils.register_class(c)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
        # kmi = km.keymap_items.new('object.translatedui_toggle', 'SPACE', 'PRESS', shift=True)
        # kmi = km.keymap_items.new("object.translatedui_toggle", "END", "PRESS")
        kmi = km.keymap_items.new("preferences.language_toggle", "END", "PRESS")
        keymaps.append((km, kmi))


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        for km, kmi in keymaps:
            # ショートカットキーの登録解除
            km.keymap_items.remove(kmi)
        keymaps.clear()


if __name__ == "__main__":
    register()
