#GNU GENERAL PUBLIC LICENSE - Version 3

#Add-on Name: Woow

#Version: 1.0.0

#Copyright (C) 2024 Abdulrahman Baggash

#Permission is hereby granted to anyone to obtain a copy of this software and associated documentation files (the "Software"), to deal in the Software under the terms of the GNU General Public License (GPL) version 3 as published by the Free Software Foundation.

#You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that you maintain the same terms and conditions under GPLv3.



import webbrowser

import bpy
from .utils import copy_action_from_file, copy_key_frame, process_text, past_copy, Charsx, Selecte_BonesIn_Frame_On, \
    insert_key_frame


class ActionListItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Action Name")
    icon: bpy.props.StringProperty(name="Icon", default='ACTION')  # Default icon

class ImagePathItem(bpy.types.PropertyGroup):
        name: bpy.props.StringProperty(name="Image Name", default="Untitled")
        name2: bpy.props.StringProperty(name="Char", default="Untitled")


class EmojiPathItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Image Name", default="Untitled")
    name2: bpy.props.StringProperty(name="Image Name", default="Untitled")
    size: bpy.props.FloatProperty(name="Size", default=1.0, min=0.0, max=1.0)
    sized: bpy.props.FloatProperty(name="Size", default=1.0, min=0.0, max=1.0)



class ActionList_UL_Items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon=item.icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon=item.icon)



class ActionList_OT_LoadActions(bpy.types.Operator):
    bl_idname = "action_list.load_actions"
    bl_label = "Load Actions"
    bl_description = "Load actions from a source file"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        context.scene.action_list.clear()
        context.scene.woow_src_action.file_src = self.filepath
        with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
            for action_name in data_from.actions:
                item = context.scene.action_list.add()
                item.name = action_name
                item.icon = 'ACTION'
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PRINT_OT_TextFileContent(bpy.types.Operator):
        bl_idname = "wm.print_text_file_content"
        bl_label = "apply"
        Armature: bpy.props.PointerProperty(name="Armature", type=bpy.types.Object)
        Bodys: bpy.props.PointerProperty(name="Body", type=bpy.types.Object)
        Tongue: bpy.props.PointerProperty(name="Tongue", type=bpy.types.Object)
        Teeth: bpy.props.PointerProperty(name="Teeth", type=bpy.types.Object)
        Eyes: bpy.props.PointerProperty(name="Eyes", type=bpy.types.Object)
        Eyeslashes: bpy.props.PointerProperty(name="Eyeslashes", type=bpy.types.Object)

        def execute(self, context):
            scene = context.scene
            mytool = scene.my_tool
            file_path = bpy.path.abspath(mytool.file_path)
            if scene.my_tool.cliber_key == True:
                try:
                    process_text(past_copy(), context)
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to read file: {e}")
            else:
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        process_text(content, context)
                        self.report({'INFO'}, "Text file content apply to the console.")
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to read file: {e}")
            return {'FINISHED'}

    # Define the panel to use the property and button


class UILIST_UL_ImagePaths(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon='ACTION')
        layout.label(text=item.name2, icon='SMALL_CAPS')


class Lod_IL_Json_UI(bpy.types.Operator):
    bl_idname = "er.load_data"
    bl_label = "Lode Data"

    def execute(self, context):
        scene = context.scene
        scene.image_paths.clear()
        scene.emoji_paths.clear()
        for i in Charsx:
            if Charsx[i].Type == "char":
                item = scene.image_paths.add()
                item.name = i
                item.name2 = "".join(Charsx[i].char)  # Safeguard for missing key
            else:
                item = scene.emoji_paths.add()
                item.name = i
        return {'FINISHED'}


class Insert_Key_Of_Image(bpy.types.Operator):
    bl_idname = "er.insert_key_of_image"
    bl_label = "Insert Keyframe"

    def execute(self, context):
        scene = context.scene
        index = scene.image_paths_index if scene.woow_set.wo_type == "char" else scene.emoji_paths_index
        name = (scene.image_paths[index].name if scene.woow_set.wo_type == "char" else scene.emoji_paths[index].name)
        frame = Charsx[name].frame
        if frame:
            Selecte_BonesIn_Frame_On(1 if scene.woow_set.wo_type == "char" else 2)
            insert_key_frame(int(frame))
        return {'FINISHED'}


class ActionList_OT_PrintSelected(bpy.types.Operator):
    bl_idname = "action_list.print_selected"
    bl_label = "Insert"
    bl_description = "Insert Key Frame"

    def execute(self, context):
        scene = context.scene
        index = scene.action_list_index
        if index >= 0 and index < len(scene.action_list):
            action_name = scene.action_list[index].name
            self.report({'INFO'}, f"Selected Action: {action_name}")

            eppend = copy_action_from_file(scene.woow_src_action.file_src, action_name, context)
            copy_key_frame(eppend, context)
        else:
            self.report({'WARNING'}, "No action selected")

        return {'FINISHED'}

class OBJECT_OT_open_link(bpy.types.Operator):
    bl_idname = "object.open_link"
    bl_label = "Open woow3d.com"
    bl_description = "Open a web bag woow add-ons in the default browser"
    bl_options = {'REGISTER', 'UNDO'}
    url: bpy.props.StringProperty(
        name="URL",
        description="woow add-ons bag",
        default="http://www.woow3d.com"
    )
    def execute(self, context):
        webbrowser.open(self.url)
        return {'FINISHED'}

