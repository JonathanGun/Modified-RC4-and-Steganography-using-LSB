with open('StarWars60.wav', 'rb') as fd:
    audio = fd.read()

aa = list(audio)

with open('StarWars60-edit.wav', 'wb') as fd:
    fd.write(bytes(aa))