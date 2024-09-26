#GNU GENERAL PUBLIC LICENSE - Version 3

#Add-on Name: Woow

#Version: 1.0.0

#Copyright (C) 2024 Abdulrahman Baggash

#Permission is hereby granted to anyone to obtain a copy of this software and associated documentation files (the "Software"), to deal in the Software under the terms of the GNU General Public License (GPL) version 3 as published by the Free Software Foundation.

#You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that you maintain the same terms and conditions under GPLv3.



import os.path
import subprocess
import platform
import threading
import json
import sys
import time
import random
import bpy


# ANSI escape codes for colors
RESET = "\033[0m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"


Charsx = {}
emoji = {}
pathJSON = f"{os.path.dirname(__file__)}/data.json"
image_folder_path = f"{os.path.dirname(__file__)}/Face"
preview_collections = {}
indexn = -1


class ItmeChar:
    def __init__(self, frame, keyShap, value, char, Type):
        self.frame = frame
        self.keyShap = keyShap
        self.value = value
        self.char = char
        self.Type = Type

    def __repr__(self):
        return f"Person(frame={self.frame},keyShap={self.keyShap}, value={self.value}, char={self.char} ,Type={self.Type})"

def message(texts):
    print(texts)
    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=texts), title="Info",
                                          icon='INFO')

def loadjson():
    try:
        with open(pathJSON, 'r') as file:
            data = json.load(file)
            for i in data:
                global Charsx
                Charsx[i['name']] = ItmeChar(i['frame'], i["keyShap"], i["value"], i["char"], i["Type"])


    except FileNotFoundError:
        message(f"JSON file not found: {pathJSON}")
    except json.JSONDecodeError:
        message(f"Error decoding JSON from {pathJSON}")

def get_action_name(obj_name, action_name="woow animation"):
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        message(f"Object '{obj_name}' does not exist. Creating a new action '{action_name}'.")
        new_action = bpy.data.actions.new(name=action_name)
        return new_action.name
    if obj.animation_data is None:
        obj.animation_data_create()
    if obj.animation_data.action is None:
        message(f"Object '{obj_name}' has no action. Creating and assigning a new action '{action_name}'.")
        new_action = bpy.data.actions.new(name=action_name)
        obj.animation_data.action = new_action
        return new_action.name
    current_action = obj.animation_data.action
    action_name_result = current_action.name
    if action_name_result == "Face":
        new_action = bpy.data.actions.new(name=action_name)
        obj.animation_data.action = new_action
        message(f"Assigned new action '{new_action.name}' to '{obj_name}'.")
        return new_action.name
    return action_name_result



def remove_dollar_and_quotes(text):
    text = text.replace("$", "")
    text = text.replace('"', "")
    text = text.replace("'", "")
    return text


def delete_action(action_name):
    action = bpy.data.actions.get(action_name)
    if action :
        action.user_clear()
        bpy.data.actions.remove(action)
        message(f"Action '{action_name}' deleted.")
    else:
        message(f"Action '{action_name}' not found.")


def copy_key_frame(action_name, context):
    message(f"append name is {action_name}")
    src_action = bpy.data.actions.get(action_name)
    target_action = context.object.animation_data.action
    current_frame = context.scene.frame_current
    # Copy keyframes starting at the current frame
    for fcurve in src_action.fcurves:
        new_fcurve = target_action.fcurves.find(fcurve.data_path, index=fcurve.array_index)
        if not new_fcurve:
            new_fcurve = target_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
        for keyframe in fcurve.keyframe_points:
            new_frame = keyframe.co[0] - fcurve.range()[0] + current_frame
            new_keyframe = new_fcurve.keyframe_points.insert(new_frame, keyframe.co[1])
            new_keyframe.interpolation = keyframe.interpolation
    delete_action(action_name)


def copy_action_from_file(filepath, action_name, context):  # import action name 
    # Ensure the file path is correct and formatted properly
    filepath = bpy.path.abspath(filepath)
    directory = filepath + "/Action/"
    filename = action_name
    # Append the action
    bpy.ops.wm.append(
        filepath=directory + filename,
        directory=directory,
        filename=filename
    )
    # Get the new action name
    # Blender will add ".001", ".002", etc. if an action with the same name already exists
    new_action_name = None  # rename name if get
    for action in bpy.data.actions:
        if action.name.startswith(action_name):
            new_action_name = action.name
    return new_action_name




def check_action_exists(action_name="Face"):
    Face = False
    for action in bpy.data.actions:
        if action.name == action_name:
            Face = True
    if Face:
        Face = True
    else:
        for action in bpy.context.scene.action_list:  # if action in file src import action
            if action.name == action_name:
                copy_action_from_file(bpy.context.scene.woow_src_action.file_src, action_name, bpy.context)
                Face = True
    return Face



def print_progress_bar(iteration, total, length=40, frameand=0, current=0, Char="Woow"):
    percent = (100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    if percent < 20:
        color = WHITE
    elif percent < 50:
        color = YELLOW
    elif percent < 80:
        color = GREEN
    else:
        color = BLUE
    bar = color + '█' * filled_length + RESET + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.1f}% [step:{current},end:{frameand}] Woow {Char}')
    sys.stdout.flush()
    bpy.context.window_manager.progress_begin(0, total)
    bpy.context.window_manager.progress_update(current + 1)


def copy_ring_frame(src_action, trg_action, frame_start, frame_end,target_start_frame):  # النسخ من الفريم الى الفريم ثم لصقهم في الاكشن يبدا عند الفريم
    source_action = bpy.data.actions.get(src_action)
    target_action = bpy.data.actions.get(trg_action)
    if source_action and target_action:
        for fcurve in source_action.fcurves:
            target_fcurve = target_action.fcurves.find(data_path=fcurve.data_path, index=fcurve.array_index)
            if not target_fcurve:
                target_fcurve = target_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
            for keyframe in fcurve.keyframe_points:
                if frame_start <= keyframe.co.x <= frame_end:
                    new_keyframe = target_fcurve.keyframe_points.insert(
                        frame=keyframe.co.x - frame_start + target_start_frame, value=keyframe.co.y)
                    new_keyframe.interpolation = keyframe.interpolation  # الاحتفاظ بنوع الاستيفاء (interpolation type)
    else:
        message("لم يتم العثور على الحركة المطلوبة.")


def check_object_and_shape_key(object_name, shape_key_name):
    obj = bpy.data.objects.get(object_name)
    if obj is not None:
        if obj.data.shape_keys is not None:
            if shape_key_name in obj.data.shape_keys.key_blocks:
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0


def convert_to_lowercase(char):
    if char.isalpha() and char.isupper():
        return char.lower()
    else:
        return char


def past_copy():
        system_name = platform.system()  # الحصول على نوع النظام
        try:
            if system_name == "Windows":
                # استخدام PowerShell للحصول على النص من الحافظة في Windows
                clipboard_text = subprocess.run(['powershell', '-command', 'Get-Clipboard'], capture_output=True,text=True,encoding='utf-8',check=True)
                return clipboard_text.stdout.strip()
            elif system_name == "Darwin":
                # استخدام pbpaste للحصول على النص من الحافظة في macOS
                clipboard_text = subprocess.run(['pbpaste'], capture_output=True, text=True)
                return clipboard_text.stdout.strip()
            elif system_name == "Linux":
                # استخدام xclip للحصول على النص من الحافظة في Linux
                clipboard_text = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True)
                return clipboard_text.stdout.strip()
            else:
               message("النظام غير مدعوم")
               return ""
        except Exception as e:
            message (f"حدث خطأ: {e}")
            return ""



def Shape_key(shape_key_name, key_value, frames, object_name):
    checks = check_object_and_shape_key(object_name, shape_key_name)
    if checks == 1:
        obj = bpy.data.objects.get(object_name)
        shape_key = obj.data.shape_keys.key_blocks.get(shape_key_name)
        shape_key.value = key_value
        shape_key.keyframe_insert(data_path="value", frame=frames)

def Shape_keys(shape_key_name, velues, blus, object_name):
    current_frame = bpy.context.scene.frame_current
    Shape_key(shape_key_name, 0.0, current_frame - blus, object_name)
    Shape_key(shape_key_name, velues, current_frame, object_name)
    current_frame = current_frame + blus
    Shape_key(shape_key_name, 0.0, current_frame, object_name)


def AplayChar(key):
    return 0


def nextFrame():
    return 0


def Emoji(key, context):
    speed = bpy.context.scene.my_tool.sp_emoji
    names = bpy.context.scene.Bodys.name
    match key:
        case "😒":
            Shape_keys("Mouth_L", 1.0, speed, names)  # object name of shape key
        case '😊':
            Shape_keys("Mouth_Smile", 1.0, speed, names)
        case '☹️':
            Shape_keys("Mouth_Frown", 1.0, speed, names)

def Char(letter, context):  #
    letter = convert_to_lowercase(letter)
    for i in Charsx:
        if letter in Charsx[i].char:
            arm_object = bpy.data.objects.get(bpy.context.scene.Armature.name)
            if arm_object and arm_object.type == 'ARMATURE':
                namea_ction = get_action_name(arm_object.name)
                copy_ring_frame("Face", namea_ction, int(Charsx[i].frame), int(Charsx[i].frame),bpy.context.scene.frame_current)


def action_size(action_name):
    action = bpy.data.actions.get(action_name)
    if not action:
        raise ValueError(f"Action '{action_name}' not found")
    # Initialize min and max frames
    min_frame = float('inf')
    max_frame = float('-inf')
    # Iterate through all keyframes in the action to find the frame range
    for fcurve in action.fcurves:
        for keyframe in fcurve.keyframe_points:
            frame = keyframe.co.x
            if frame < min_frame:
                min_frame = frame
            if frame > max_frame:
                max_frame = frame
    # Check if there are no keyframes
    if min_frame == float('inf') or max_frame == float('-inf'):
        message("No keyframes found in the action")
        return 0,0
    else:
        return int(min_frame),int(max_frame)
        message(f"Action '{action_name}' has keyframes from frame {int(min_frame)} to frame {int(max_frame)}")


def random_face(action_name="woow_random",min=0,max=0):
        random_number = random.randint(min, max)
        arm_object = bpy.data.objects.get(bpy.context.scene.Armature.name)
        if arm_object and arm_object.type == 'ARMATURE':
            namea_ction = get_action_name(arm_object.name)
            copy_ring_frame(action_name, namea_ction, int(random_number), int(random_number), bpy.context.scene.frame_current)


def Arbic(word, context):
    if int(bpy.context.scene.my_tool.Text) == 2:
                exists = check_action_exists("Face")
                if exists:  # if action name in action or Action list load
                    for letter in word:
                        unicode_num = ord(letter)
                        if unicode_num < 1700:
                              Char(letter, context)
                              bpy.context.scene.frame_set(bpy.context.scene.frame_current + (bpy.context.scene.my_tool.sp_text * 2))
                              if letter == " ":
                                  bpy.context.scene.frame_set(bpy.context.scene.frame_current + (bpy.context.scene.my_tool.sp_text * 2))
                                  Char(letter, context)
                                  bpy.context.scene.frame_set(bpy.context.scene.frame_current + (bpy.context.scene.my_tool.sp_text * 2))
                        else:
                            Emoji(letter, context)
                            bpy.context.scene.frame_set(bpy.context.scene.frame_current + (bpy.context.scene.my_tool.sp_emoji * 2))
                    bpy.context.window_manager.progress_end()
                else:
                    message("Not action Face in file or Src load File")





def process_text(text, context):  # $Imant fors$
    minr=0
    maxr=0
    ac_ran = check_action_exists("woow_random")
    exists = check_action_exists("Face")
    if ac_ran and bpy.context.scene.my_tool.random_frame:
       minr, maxr = action_size("woow_random")
    if exists:  # if action name in action or Action list load
        xc = True
        word = ""
        step = 0
        ligen = len(text)
        rnd = 0
        for i in text:
            rnd = rnd + 1
            step = step + 1

            if rnd == bpy.context.scene.my_tool.wo_random and maxr>0:
                rnd = 0
                random_face("woow_random",minr,maxr)
            print_progress_bar(step, ligen, 30, ligen, step, word)

            if i == " " and xc:
                Arbic(word, context)
                word = ""
            elif i == "$":
                if xc:
                    xc = False
                else:
                    xc = True
                    eppend = copy_action_from_file(bpy.context.scene.woow_src_action.file_src, word, context)
                    copy_key_frame(eppend, context)
                    word = ""
            else:
                word = word + i

        if word != "":
            if xc:
                Arbic(word, context)
            else:
                eppend = copy_action_from_file(bpy.context.scene.woow_src_action.file_src, word, context)
                copy_key_frame(eppend, context)
        if bpy.context.scene.my_tool.end_frame:
            bpy.context.scene.frame_end = bpy.context.scene.frame_current
    message("\nProcess completed!")
    bpy.context.window_manager.progress_end()



def Selecte_BonesIn_Frame_On(frame=1):
    obj = bpy.context.object
    if obj and obj.type == 'ARMATURE' and obj.mode == 'POSE':
        bpy.ops.pose.select_all(action='DESELECT')
        for bone in obj.pose.bones:
            bone_data_path = f'pose.bones["{bone.name}"]'
            for channel in ['location', 'rotation_quaternion', 'rotation_euler', 'scale']:
                fcurve = obj.animation_data.action.fcurves.find(bone_data_path + "." + channel)
                if fcurve:
                    for keyframe in fcurve.keyframe_points:
                        if keyframe.co.x == frame:
                            bone.bone.select = True
                            break
    else:
        message("Please make sure you are in Pose Mode and have an Armature selected.")


def insert_key_frame(frame_number):
    obj = bpy.context.object
    if obj and obj.type == 'ARMATURE' and obj.mode == 'POSE':
        for bone in obj.pose.bones:
            if bone.bone.select:
                bone.keyframe_insert(data_path="location", frame=frame_number)
                bone.keyframe_insert(data_path="rotation_quaternion", frame=frame_number)
                bone.keyframe_insert(data_path="scale", frame=frame_number)
    else:
        message("Please make sure you are in Pose Mode and have an Armature selected.")
