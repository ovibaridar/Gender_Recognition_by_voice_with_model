from pydub import AudioSegment

if __name__ == "__main__":
    for i in range(2311, 2312):
        if i == 163:
            continue

        else:
            input_file = "audio file/Female2/" + str(i) + ".m4a"
            output_file = "audio file/Female/" + str(i) + ".wav"

            # Load the M4A file
            audio = AudioSegment.from_file(input_file, format="m4a")

            # Export the audio to the desired format
            audio.export(output_file, format="wav")
            print(input_file)
