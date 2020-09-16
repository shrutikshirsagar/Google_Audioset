''' code to convert mp3 to wav '''
path1 = "/media/shruti/Data/Internship_data/data/Industrial/"
out_path = "/media/shruti/Data/Internship_data/data/Industrial_wav/"
if not os.path.exists(out_path):
    os.makedirs(out_path)

for filename in os.listdir(path1):
    print(filename)
    mp3_file = os.path.join(path1, filename)
    print( mp3_file)
    
    name, ext = os.path.splitext(filename)
    print(name, ext)
    wav_file1 = os.path.join(out_path, name)
    print(wav_file1)
    wav_file = (wav_file1 + '.wav')
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

