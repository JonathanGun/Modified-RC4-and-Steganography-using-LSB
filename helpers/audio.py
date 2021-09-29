import io
import pyaudio

CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen

pAud = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    data = cur_wave_file.readframes(frame_count)
    # TODO possibly visualize (?)
    return (data, pyaudio.paContinue)


streams = {
    "orig": False,
    "hidden": False,
}
cur_wave_file = False


def stop(channel: str):
    if streams[channel]:
        streams[channel].stop_stream()
        streams[channel].close()
        streams[channel] = False

<<<<<<< HEAD
=======

def play_song(data, channel: str):
    song = AudioSegment.from_file(io.BytesIO(data), format="wav")
    play(song)


>>>>>>> d84c596eb806824092f46787d4f3bbf5839a2b8d
def listen(wave_file, channel: str):
    global cur_wave_file
    for k in streams.keys():
        if k != channel:
            stop(k)
            continue
        if streams[k] and not streams[k].is_stopped():
            streams[channel].stop_stream()
            continue
        streams[k] = pAud.open(
            format=pAud.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True,
            stream_callback=callback,
        )
        streams[k].start_stream()
    cur_wave_file = wave_file
