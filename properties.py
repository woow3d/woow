#GNU GENERAL PUBLIC LICENSE - Version 3

#Add-on Name: Woow

#Version: 1.0.0

#Copyright (C) 2024 Abdulrahman Baggash

#Permission is hereby granted to anyone to obtain a copy of this software and associated documentation files (the "Software"), to deal in the Software under the terms of the GNU General Public License (GPL) version 3 as published by the Free Software Foundation.

#You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that you maintain the same terms and conditions under GPLv3.




import bpy

class Woow_Src_Action(bpy.types.PropertyGroup):
    file_src: bpy.props.StringProperty(
        name="",
        description="Path to the text file",
        default="",
        maxlen=1024
    )

class MyProperties(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(
        name="Text Path",
        description="Path to the text file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )
    sp_text: bpy.props.IntProperty(
        name="Speed Text",
        description="",
        default=2,
        min=0,
        max=100
    )
    sp_emoji: bpy.props.IntProperty(
        name="Speed Emoji",
        description="",
        default=5,
        min=0,
        max=100
    )
    wo_random: bpy.props.IntProperty(
        name="Random",
        default=8,
        description="Enter a Speed random value",
        min=1,
        max=100
    )
    delete_key: bpy.props.BoolProperty(
        name="Delete list Key Frame",
        description="Delete list frame in frame apply ",
        default=False
    )
    cliber_key: bpy.props.BoolProperty(
        name="Enable Copy Text",
        description="A simple checkbox example",
        default=False
    )
    end_frame: bpy.props.BoolProperty(
        name="End Frame",
        description="Set end frame with end apply text",
        default=False
    )
    random_frame: bpy.props.BoolProperty(
        name="Random Frame",
        description="Use animation Random with text",
        default=False
    )

    Text: bpy.props.EnumProperty(
        name="Text",
        description="Choose the Text",
        items=[
            ('1', "Key Shape", ""),
            ('2', "Armature", ""),
        ]
    )
    Emoji: bpy.props.EnumProperty(
        name="Emoji",
        description="Choose the Emoji",
        items=[
            ('1', "Key Shape", ""),
            ('2', "Armature", ""),
        ]
    )
    body: bpy.props.EnumProperty(
        name="Body",
        description="Choose the Body",
        items=[
            ('1', "Body", ""),
            ('2', "Body, Tongue, Teeth, Eyes", ""),
        ]
    )


class Woow_Setting(bpy.types.PropertyGroup):
    wo_type: bpy.props.EnumProperty(
        name="Type",
        description="Choose the Type Key iput for Face Char, Emoji",
        items=[
            ('char', "Char", ""),
            ('emoji', "Emoji", ""),

        ]
    )
    wo_typesd: bpy.props.EnumProperty(
        name="Gander",
        description="Choose the Gander input  Armature , Key Shape",
        items=[
            ('1', "Armature", ""),
            ('2', "Key Shape", ""),

        ]
    )
    wo_image: bpy.props.FloatProperty(
        name="Scale",
        default=10,
        description="Enter a Scale image view value",
        min=0.0,
        max=40.0
    )

