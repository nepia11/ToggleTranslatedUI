import bpy
import rna_keymap_ui
from bl_i18n_utils.settings import LANGUAGES

bl_info = {
    "name": "Toggle Translated UI",
    "author": "Original:Satoshi Yamasaki(yamyam), Converted to 2.83: Toudou++, nepia11",
    "version": (6, 1),
    "blender": (2, 83, 0),
    "description": "Toggle Language",
    "location": "shortcut: End key",
    "wiki_url": "https://www.cgradproject.com/archives/5503/",
    "tracker_url": "",
    "category": "System",
}


def update_language(self, context):
    """ prefの言語設定を反映する """
    pref = bpy.context.preferences
    addon_prefs = pref.addons[__name__].preferences
    if addon_prefs.is_main_language:
        pref.view.language = addon_prefs.main_language
        pref.view.use_translate_interface = addon_prefs.main_interface
        pref.view.use_translate_tooltips = addon_prefs.main_tooltips
        pref.view.use_translate_new_dataname = addon_prefs.main_new_data
    else:
        pref.view.language = addon_prefs.sub_language
        pref.view.use_translate_interface = addon_prefs.sub_interface
        pref.view.use_translate_tooltips = addon_prefs.sub_tooltips
        pref.view.use_translate_new_dataname = addon_prefs.sub_new_data
    return None


class TTUI_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    # LANGUAGESがenumに適していない形式っぽいのでよしなにする
    LANGUAGE_ENUM_ITEMS = [(code, name, "", number) for number, name, code in LANGUAGES]

    # props
    def prop_template(items: list, lang: str):
        Language = bpy.props.EnumProperty(
            name="Language",
            items=items,
            default=lang,
            update=update_language,
        )
        Tooltips = bpy.props.BoolProperty(
            name="Tooltips",
            default=True,
            update=update_language,
        )

        Interface = bpy.props.BoolProperty(
            name="Interface",
            default=True,
            update=update_language,
        )
        New_Data = bpy.props.BoolProperty(
            name="New Data",
            default=False,
            update=update_language,
        )
        return Language, Tooltips, Interface, New_Data

    main_language, main_tooltips, main_interface, main_new_data = prop_template(
        items=LANGUAGE_ENUM_ITEMS, lang="en_US"
    )
    sub_language, sub_tooltips, sub_interface, sub_new_data = prop_template(
        items=LANGUAGE_ENUM_ITEMS, lang=bpy.context.preferences.view.language
    )

    is_main_language = bpy.props.BoolProperty(
        name="is main language",
        subtype="POWER",
        default=False,
        update=update_language,
    )

    # keymaps
    keymaps = []

    @classmethod
    def register(cls):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        if kc:
            km = kc.keymaps.new(name="Window", space_type="EMPTY")
            kmi = km.keymap_items.new(
                idname="preferences.language_toggle", type="END", value="PRESS"
            )
            # ショートカットキー一覧に登録
            cls.keymaps.append((km, kmi))

    @classmethod
    def unregister(cls):
        for km, kmi in cls.keymaps:
            # ショートカットキーの登録解除
            km.keymap_items.remove(kmi)
        # ショートカットキー一覧をクリア
        cls.keymaps.clear()

    def draw(self, context):
        layout = self.layout

        # keymaps
        layout.label(text="keymap")
        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in self.keymaps:
            rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)

        layout.prop(self, "is_main_language")
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
    """ 英語とその他で言語設定を切り替える """

    bl_idname = "preferences.language_toggle"
    bl_label = "Toggle UI Language"

    def execute(self, context):
        # 言語切り替えをする
        pref = bpy.context.preferences
        addon_prefs = pref.addons[__name__].preferences
        addon_prefs.is_main_language = not addon_prefs.is_main_language
        return {"FINISHED"}


# Registration
classes = [
    TTUI_Preferences,
    TTUI_Language_Toggle,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
