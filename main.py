from datetime import datetime
import os
import string
from typing import List
import PySimpleGUI as sg

import cv2

from modified_rc4 import ModifiedRC4
from steganography.stego_image import Image
from steganography.stego_audio import Audio
from steganography.stego_video import Video

from helpers import audio
import wave


class Config:
    APP_NAME = "Tucil 3 Kriptografi"
    SUCCESS_COLOR = "#90EE90"
    FAIL_COLOR = "#d9534f"
    ABOUT = """
Created by:
- Hengky Surya Angkasa / 13518048
- Michael Hans / 13518056
- Jonathan Yudi Gunawan / 13518084
"""


sg.theme("Reddit")
layout = [
    [sg.T(Config.APP_NAME, font="Any 20")],
    [sg.T("", key="debug")],
    [sg.TabGroup([[
        sg.Tab("Input", [
            [sg.TabGroup([[
                sg.Tab("Modified RC4", [
                    [sg.T("Action", size=(10, 1)), sg.DropDown(["Encrypt", "Decrypt"], key="action_rc4", default_value="Encrypt", size=(10, 1))],
                    [sg.TabGroup([[
                        sg.Tab("From Text", [
                            [sg.Multiline(key="in_text", size=(70, 7))]
                        ], key="text"),
                        sg.Tab("From File", [
                            [sg.T("Select File", size=(10, 1)), sg.FileBrowse("Choose a file", key="in_file", target=(sg.ThisRow, 2)), sg.T("", size=(40, 2))],
                        ], key="file"),
                    ]], key="source")],
                ], key="modified_rc4"),
                sg.Tab("Steganography", [
                    [sg.T("Select Secret File", size=(20, 1)), sg.FileBrowse("Choose a file", key="secret_file", target=(sg.ThisRow, 2)), sg.T("", size=(30, 2))],
                    [sg.T("Select Stego File", size=(20, 1)), sg.FileBrowse("Choose a file", key="stego_file", target=(sg.ThisRow, 2)), sg.T("", size=(30, 2))],
                    [sg.Radio("Image", "stego_type", key="image", default=True), sg.Radio("Audio", "stego_type", key="audio"), sg.Radio("Video", "stego_type", key="video")],
                    [sg.T("Action", size=(10, 1)), sg.DropDown(["Hide", "Extract"], key="action_stego", default_value="Hide", size=(10, 1))],
                    [sg.Checkbox("With encryption?", key="is_msg_encrypted")],
                    [sg.Checkbox("Insert randomly?", key="is_insert_random")],
                ], key="steganography"),
            ]], key="method")],
            [sg.T("Cipher Key", size=(10, 1)), sg.In(key="cipher_key", size=(60, 1))],
            [sg.Button("Run", pad=(5, 10))],
        ], key="input"),
        sg.Tab("Output", [
            [sg.TabGroup([[
                sg.Tab("Text", [
                    [sg.Multiline(key="out_preview_text", write_only=True, size=(70, 10))],
                ], key="out_text"),
                sg.Tab("Image", [
                    [
                        sg.Image(key="out_preview_image_orig", filename=""),
                        sg.Image(key="out_preview_image_hidden", filename=""),
                    ],
                    [sg.T("PSNR", size=(10, 1)), sg.T("", key="psnr")],
                ], key="out_image"),
                sg.Tab("Audio", [
                    [
                        sg.Button("Play/Pause Original", key="listen_orig", size=(15,)),
                        sg.Button('Stop', key="stop_orig"),
                        sg.ProgressBar(10000, orientation="h", size=(25, 20), key="audio_prog_orig"),
                    ],
                    [
                        sg.Button("Play/Pause Hidden", key="listen_hidden", size=(15,)),
                        sg.Button('Stop', key="stop_hidden"),
                        sg.ProgressBar(10000, orientation="h", size=(25, 20), key="audio_prog_hidden"),
                    ],
                    [sg.T("Fidelity", size=(10, 1)), sg.T("", key="fidelity")],
                ], key="out_audio"),
            ]], key="output_type")],
            [sg.T("Output File", size=(10, 1)), sg.In(key="filename", size=(60, 1))],
            [sg.Button("Export", pad=(5, 10))],
        ], key="output"),
        sg.Tab("About", [[sg.T(txt)] for txt in Config.ABOUT.strip().split("\n")], key="about"),
    ]], key="current_tab")],
]


def load_file(filepath: str) -> List[int]:
    # return list of bytes
    file_byte = []
    with open(filepath, "rb") as f:
        file_byte += f.read()
    return file_byte


def byte_to_str(byte_list: List[int]) -> str:
    printable_chars = set(bytes(string.printable, "ascii"))
    printable = all(char in printable_chars for char in byte_list)
    return "".join(map(chr, byte_list)) if printable else "NOT_TEXT"


def write_file(filepath: str, content: List[int]) -> bool:
    with open(filepath, "wb") as f:
        f.write(content)


def byte_to_img(byte_list, target_size=(245, 245)):
    scale = min(target_size[1] / byte_list.shape[1], target_size[0] / byte_list.shape[0])
    resized = cv2.resize(byte_list, (int(byte_list.shape[1] * scale), int(byte_list.shape[0] * scale)), interpolation=cv2.INTER_AREA)
    final = cv2.imencode(".png", resized)[1].tobytes()
    return final


window = sg.Window(Config.APP_NAME, layout)
event, values = window.read()

out_text = ""
stego_object = None
while event not in (sg.WIN_CLOSED, "Exit"):
    event = event.lower()
    debug_text, debug_color = "", None
    print(event, values)

    if event == "run":
        out_text = ""
        print("Method:", values["method"])
        if values["method"] == "modified_rc4":
            # Read input
            in_bytes = list(str.encode(values["in_text"]))
            action = values["action_rc4"].lower()
            if values["source"] == "file":
                try:
                    in_bytes = load_file(values["in_file"])
                    window["filename"].update(os.path.basename(values["in_file"]) + "." + action[:3])
                except Exception as e:
                    debug_text, debug_color = str(e), Config.FAIL_COLOR
            else:
                window["filename"].update(datetime.now().strftime("%Y%m%d-%H%M%S") + "." + action[:3])

            if debug_color != Config.FAIL_COLOR:
                # Process (decrypt / encrypt)
                out_bytes = getattr(ModifiedRC4(in_bytes, values["cipher_key"]), action)()
                debug_text, debug_color = f"Succesfully {action}ed!", Config.SUCCESS_COLOR

                window["out_text"].select()
                out_text = byte_to_str(out_bytes)
        else:
            out_text = "NOT_TEXT"
            action = values["action_stego"].lower()

            # Read input
            try:
                stego_bytes = load_file(values["stego_file"])
                secret_bytes = []
                if action == "hide":
                    secret_bytes = load_file(values["secret_file"])
            except Exception as e:
                debug_text, debug_color = str(e), Config.FAIL_COLOR

            if debug_color != Config.FAIL_COLOR:
                # Process
                stego_class = Image if values["image"] else Audio if values["audio"] else Video
                print(stego_class)
                try:
                    stego_object = stego_class(
                        secret_bytes, stego_bytes,
                        key=values["cipher_key"],
                        is_msg_encrypted=values["is_msg_encrypted"],
                        is_insert_random=values["is_insert_random"],
                        stego_filepath=values["stego_file"],
                        secret_filepath=values["secret_file"],
                    )
                    out_bytes = getattr(stego_object, action)()
                    if action == "hide":
                        if values["image"]:
                            window["out_preview_image_orig"].update(data=byte_to_img(stego_object.image))
                            window["out_preview_image_hidden"].update(data=byte_to_img(out_bytes))
                            window["out_image"].select()
                            debug_text, debug_color = "Succesfully insert secret file to image", Config.SUCCESS_COLOR
                            window["psnr"].update(stego_object.calculate_psnr(stego_object.image, out_bytes))
                        if values["audio"]:
                            window["out_audio"].select()
                            debug_text, debug_color = "Succesfully insert secret file to audio", Config.SUCCESS_COLOR
                        if values["video"]:
                            debug_text, debug_color = "Not implemented yet", Config.FAIL_COLOR
                        outname = list(os.path.splitext(stego_object.stego_filename))
                        outname.insert(-1, ".hide")
                        window["filename"].update("".join(outname))
                        if values["audio"]:
                            filename = "out/" + "".join(outname)
                            stego_object.stego_out_filepath = filename
                            write_file(filename, bytes(out_bytes))
                            window["fidelity"].update(stego_object.calculate_psnr())
                    else:
                        out_text = byte_to_str(out_bytes)
                        debug_text, debug_color = f"Succesfully extract secret file from {stego_class.__name__.lower()}", Config.SUCCESS_COLOR
                        window["filename"].update(stego_object.secret_filename)
                except Exception as e:
                    print(e)
                    debug_text, debug_color = f"Fail to {action}. Reason: {str(e)}", Config.FAIL_COLOR

    elif event == "export":
        filename = "out/" + values["filename"]
        if values["filename"]:
            try:
                if values["image"] and values["method"] != "modified_rc4" and action == "hide":
                    cv2.imwrite(filename, out_bytes)
                else:
                    write_file(filename, bytes(out_bytes))
                debug_text, debug_color = f"Succesfully saved as {filename}", Config.SUCCESS_COLOR
            except Exception as e:
                print(e)
                debug_text, debug_color = f"Failed to save as {filename}", Config.FAIL_COLOR
        else:
            debug_text, debug_color = "Output filename cannot be empty", Config.FAIL_COLOR
    elif event == "listen_orig" and values["audio"] and stego_object is not None:
        original_audio = wave.open(stego_object.stego_filepath, 'rb')
        audio.listen(original_audio, "orig")
        # audio.play_song(stego_object.audio, "orig")
    elif event == "stop_orig" and values["audio"]:
        audio.stop("orig")
        window["audio_prog_orig"].update(0)
    elif event == "listen_hidden" and values["audio"]:
        hidden_audio = wave.open(stego_object.stego_out_filepath, 'rb')
        audio.listen(hidden_audio, "hidden")
        # audio.play_song(out_bytes, "hidden")
    elif event == "stop_hidden" and values["audio"]:
        audio.stop("hidden")
        window["audio_prog_hidden"].update(0)

    # Output
    if event == "run" and debug_color == Config.SUCCESS_COLOR:
        #print(f"out_bytes: {out_bytes[:3]}... (len: {len(out_bytes)})")
        window["out_preview_text"].update(out_text)
        window["output"].select()
    window["debug"].update(debug_text)
    window["debug"].update(background_color=debug_color)

    # Get next value
    event, values = window.read()

audio.pAud.terminate()
window.close()
