#GNU GENERAL PUBLIC LICENSE - Version 3

#Add-on Name: Woow

#Version: 1.0.0

#Copyright (C) 2024 Abdulrahman Baggash

#Permission is hereby granted to anyone to obtain a copy of this software and associated documentation files (the "Software"), to deal in the Software under the terms of the GNU General Public License (GPL) version 3 as published by the Free Software Foundation.

#You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that you maintain the same terms and conditions under GPLv3.



import os

import bpy


from .operators import *
from .properties import *
from .utils import image_folder_path, preview_collections
class VIEW3D_PT_MyPanel(bpy.types.Panel):
    bl_label = "Load and Animation Text File"
    bl_idname = "PT_MyPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'woow'
    bl_context = "objectmode"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "file_path")
        layout.prop(mytool, "cliber_key")
        layout.prop(mytool, "delete_key")
        layout.prop(mytool, "end_frame")
        layout.prop(mytool, "random_frame")
        layout.prop(mytool, "Text")
        layout.prop(mytool, "Emoji")
        layout.prop(mytool, "body")
        row = layout.row()
        row.prop(mytool, "sp_text")
        row.prop(mytool, "sp_emoji")
        row = layout.row()
        row.prop(mytool,"wo_random")
        row = layout.row()
        row.prop(context.scene, "Armature", text="Armature")
        row.prop(context.scene, "Bodys", text="Body")
        if float(scene.my_tool.body) != 1:
            row = layout.row()
            row.prop(context.scene, "Tongue", text="Tongue")
            row.prop(context.scene, "Teeth", text="Teeth")
            row = layout.row()
            row.prop(context.scene, "Eyes", text="Eyes")
            row.prop(context.scene, "Eyeslashes", text="Eyeslashes")
        layout.operator("wm.print_text_file_content")


class ActionList_PT_Panel(bpy.types.Panel):
    bl_idname = "ACTION_LIST_PT_panel"
    bl_label = "Action List"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'woow'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        velsrc = scene.woow_src_action
        row = layout.row()
        row.operator("action_list.load_actions", text="", icon="BLENDER")
        row.prop(velsrc, "file_src")
        layout.template_list(
            "ActionList_UL_Items",
            "",
            scene,
            "action_list",
            scene,
            "action_list_index"
        )
        layout.operator("action_list.print_selected", text="Insert")


class VIEW3D_PT_custom_image_panel(bpy.types.Panel):
    bl_label = "Image Action Panel"
    bl_idname = "VIEW3D_PT_custom_image_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'woow'
    bl_context = "posemode"
    @classmethod
    def poll(cls, context):
        return True
    def draw(self, context):
        layout = self.layout
        # Check if the folder exists
        scene = context.scene
        global Charsx
        if len(Charsx) < 1:
            loadjson()
        index = scene.image_paths_index if scene.woow_set.wo_type == "char" else scene.emoji_paths_index
        if index >0:
            name = (
                scene.image_paths[index].name if scene.woow_set.wo_type == "char" else scene.emoji_paths[index].name)
            if context.object.animation_data.action.name == "Face":
                frame = Charsx[name].frame
                if frame:
                    bpy.context.scene.frame_set(frame)
            frame = Charsx[name].frame
            if os.path.exists(image_folder_path):
                pcoll = preview_collections["custom_previews"]
                image_file = name + ".jpg"
                image_path = os.path.join(image_folder_path, image_file)
                if image_file not in pcoll:
                    thumb = pcoll.load(image_file, image_path, 'IMAGE')
                    pcoll[image_file] = thumb
                layout.template_icon(pcoll[image_file].icon_id, scale=bpy.context.scene.woow_set.wo_image)
            else:
                layout.label(text="Folder does not exist", icon='ERROR')
        return


class VIEW3D_PT_ImageFolderSelector(bpy.types.Panel):
    bl_label = "Action Input List"
    bl_idname = "VIEW3D_PT_image_folder_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'woow'
    bl_context = "posemode"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE' and context.mode == 'POSE'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.woow_set
        global indexn
        layout.operator("er.load_data")
        row = layout.row()
        row.prop(props, "wo_type")
        row.prop(props, "wo_typesd")
        row.prop(props, "wo_image")
        row = layout.row()
        row.template_list("UILIST_UL_ImagePaths", "", scene, "image_paths" if scene.woow_set.wo_type == "char"
        else "emoji_paths", scene, "image_paths_index" if scene.woow_set.wo_type == "char"
                          else "emoji_paths_index")
        layout.operator("er.insert_key_of_image")



class OBJECT_PT_open_link_panel(bpy.types.Panel):
    bl_label = "About"
    bl_idname = "OBJECT_PT_open_link_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'woow'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.open_link")




def menu_func(self, context):
    self.layout.operator(OBJECT_OT_open_link.bl_idname)