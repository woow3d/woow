#GNU GENERAL PUBLIC LICENSE - Version 3

#Add-on Name: Woow

#Version: 1.0.0

#Copyright (C) 2024 Abdulrahman Baggash

#Permission is hereby granted to anyone to obtain a copy of this software and associated documentation files (the "Software"), to deal in the Software under the terms of the GNU General Public License (GPL) version 3 as published by the Free Software Foundation.

#You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that you maintain the same terms and conditions under GPLv3.






bl_info = {
    "name": "woow",
    "blender": (4, 1, 0),
    "autho"	: "Abdulrhman baggash",
    "description ":"This addon for animtion text",
    "versio" : ( 1, 0,0),
    "locatio" : "Right 3d View Panel ->woow",
    "categor" : "Animation",
    "description" : "Fast create animation",
    "tracker_url": "https://woow3d.com/add-ons-portfolio.php?id=156",
    "doc_url": "https://woow3d.com/add-ons-portfolio.php?id=156",

}


import bpy
from bpy.utils import previews
from .panels import VIEW3D_PT_MyPanel, ActionList_PT_Panel, VIEW3D_PT_custom_image_panel, VIEW3D_PT_ImageFolderSelector, \
    OBJECT_PT_open_link_panel, menu_func
from .operators import ActionListItem, ActionList_OT_PrintSelected, ActionList_OT_LoadActions, \
    PRINT_OT_TextFileContent, Insert_Key_Of_Image, Lod_IL_Json_UI, UILIST_UL_ImagePaths, EmojiPathItem, ImagePathItem, \
    OBJECT_OT_open_link, ActionList_UL_Items
from .properties import Woow_Src_Action, MyProperties, Woow_Setting
from .utils import loadjson, preview_collections







classe = (
    ActionList_OT_LoadActions,
    ActionListItem,
    ActionList_OT_PrintSelected,
    ActionList_UL_Items,
    Woow_Src_Action,
    ActionList_PT_Panel,
    MyProperties,
    PRINT_OT_TextFileContent,
    VIEW3D_PT_MyPanel
)


def register():
    loadjson()
    for cls in classe:
        bpy.utils.register_class(cls)
    bpy.types.Scene.woow_src_action = bpy.props.PointerProperty(type=Woow_Src_Action)
    bpy.types.Scene.action_list = bpy.props.CollectionProperty(type=ActionListItem)
    bpy.types.Scene.action_list_index = bpy.props.IntProperty(name="Index", default=0)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)
    bpy.types.Scene.Armature = bpy.props.PointerProperty(name="Armature", type=bpy.types.Object)
    bpy.types.Scene.Bodys = bpy.props.PointerProperty(name="Body", type=bpy.types.Object)
    bpy.types.Scene.Tongue = bpy.props.PointerProperty(name="Tongue", type=bpy.types.Object)
    bpy.types.Scene.Teeth = bpy.props.PointerProperty(name="Teeth", type=bpy.types.Object)
    bpy.types.Scene.Eyes = bpy.props.PointerProperty(name="Eyes", type=bpy.types.Object)
    bpy.types.Scene.Eyeslashes = bpy.props.PointerProperty(name="Eyeslashes", type=bpy.types.Object)

    pcoll = previews.new()
    preview_collections["custom_previews"] = pcoll
    bpy.utils.register_class(VIEW3D_PT_custom_image_panel)
    bpy.utils.register_class(VIEW3D_PT_ImageFolderSelector)
    bpy.utils.register_class(Insert_Key_Of_Image)
    bpy.utils.register_class(Lod_IL_Json_UI)
    bpy.utils.register_class(UILIST_UL_ImagePaths)
    bpy.utils.register_class(EmojiPathItem)
    bpy.utils.register_class(ImagePathItem)
    bpy.utils.register_class(Woow_Setting)
    bpy.types.Scene.image_paths = bpy.props.CollectionProperty(type=ImagePathItem)
    bpy.types.Scene.image_paths_index = bpy.props.IntProperty(default=0)
    bpy.types.Scene.emoji_paths = bpy.props.CollectionProperty(type=EmojiPathItem)
    bpy.types.Scene.emoji_paths_index = bpy.props.IntProperty(default=0)
    bpy.types.Scene.woow_set = bpy.props.PointerProperty(type=Woow_Setting)

    bpy.utils.register_class(OBJECT_OT_open_link)
    bpy.utils.register_class(OBJECT_PT_open_link_panel)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    for cls in classe:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.action_list
    del bpy.types.Scene.action_list_index
    del bpy.types.Scene.woow_src_action
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.Armature
    del bpy.types.Scene.Bodys
    del bpy.types.Scene.Tongue
    del bpy.types.Scene.Teeth
    del bpy.types.Scene.Eyes
    del bpy.types.Scene.Eyeslashes

    bpy.utils.unregister_class(VIEW3D_PT_custom_image_panel)
    # Remove preview collection
    for pcoll in preview_collections.values():
        previews.remove(pcoll)
    preview_collections.clear()
    del bpy.types.Scene.image_paths
    del bpy.types.Scene.image_paths_index
    del bpy.types.Scene.emoji_paths
    del bpy.types.Scene.emoji_paths_index
    del bpy.types.Scene.woow_set
    bpy.utils.unregister_class(VIEW3D_PT_ImageFolderSelector)
    bpy.utils.unregister_class(Insert_Key_Of_Image)
    bpy.utils.unregister_class(Lod_IL_Json_UI)
    bpy.utils.unregister_class(UILIST_UL_ImagePaths)
    bpy.utils.unregister_class(EmojiPathItem)
    bpy.utils.unregister_class(ImagePathItem)
    bpy.utils.unregister_class(Woow_Setting)

    bpy.utils.unregister_class(OBJECT_OT_open_link)
    bpy.utils.unregister_class(OBJECT_PT_open_link_panel)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":

    register()
