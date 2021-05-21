import bpy

bl_info = {
    "name": "Toggle Translated UI",
    "author": "Original:Satoshi Yamasaki(yamyam), Converted to 2.83: Toudou++, nepia11",
    "version": (5, 0),
    "blender": (2, 83, 0),
    "description": "Toggle Language",
    "location": "shortcut: End key",
    "wiki_url": "https://www.cgradproject.com/archives/5503/",
    "tracker_url": "",
    "category": "System",
}


class TTUI_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def prop_template(name: str, lang):
        locales = bpy.app.translations.locales
        items = list(zip(locales, locales, [""] * len(locales)))
        items.append(("DEFAULT", "DEFAULT", ""))
        Language = bpy.props.EnumProperty(
            name="Language",
            items=items,
            default=lang,
        )
        Tooltips = bpy.props.BoolProperty(
            name="Tooltips",
            default=True,
        )

        Interface = bpy.props.BoolProperty(
            name="Interface",
            default=True,
        )
        New_Data = bpy.props.BoolProperty(
            name="New Data",
            default=False,
        )
        return Language, Tooltips, Interface, New_Data

    main_language, main_tooltips, main_interface, main_new_data = prop_template(
        "main", "en_US"
    )
    sub_language, sub_tooltips, sub_interface, sub_new_data = prop_template(
        "sub", bpy.context.preferences.view.language
    )

    is_main_language = bpy.props.BoolProperty(
        name="is main language",
        default=False,
    )

    def draw(self, context):
        layout = self.layout

        # layout.prop(self, "is_main_language")
        row = layout.row(align=True)
        # main_lang = row.column(align=True)
        main_lang = row.box()
        main_lang.label(text="main language")
        # localeを流用すると、locale文字列で言語選択することになるので視認性が悪い　どうやったらいい感じに言語名とlocaleのenumを取得できるかな
        main_lang.prop(self, "main_language")
        main_lang.prop(self, "main_tooltips")
        main_lang.prop(self, "main_interface")
        main_lang.prop(self, "main_new_data")

        # sub_lang = row.column(align=True)
        sub_lang = row.box()
        sub_lang.label(text="sub language")
        sub_lang.prop(self, "sub_language")
        sub_lang.prop(self, "sub_tooltips")
        sub_lang.prop(self, "sub_interface")
        sub_lang.prop(self, "sub_new_data")


class TTUI_Language_Toggle(bpy.types.Operator):
    """ 英語とその他で言語設定を切り替える　新規データのオプション強制False """

    bl_idname = "preferences.language_toggle"
    bl_label = "Toggle UI Language"

    # アドオン有効時に切り替える前の状態を保存しておく
    pref = bpy.context.preferences
    lang = "DEFAULT"

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        # 言語切り替えをする
        pref = bpy.context.preferences
        if not addon_prefs.is_main_language:
            pref.view.language = addon_prefs.main_language
            pref.view.use_translate_interface = addon_prefs.main_interface
            pref.view.use_translate_tooltips = addon_prefs.main_tooltips
            pref.view.use_translate_new_dataname = addon_prefs.main_new_data
        else:
            pref.view.language = addon_prefs.sub_language
            pref.view.use_translate_interface = addon_prefs.sub_interface
            pref.view.use_translate_tooltips = addon_prefs.sub_tooltips
            pref.view.use_translate_new_dataname = addon_prefs.sub_new_data
        addon_prefs.is_main_language = not addon_prefs.is_main_language
        return {"FINISHED"}


# Registration
classes = [
    TTUI_Preferences,
    TTUI_Language_Toggle,
]

keymaps = []


def register():
    for c in classes:
        bpy.utils.register_class(c)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
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
