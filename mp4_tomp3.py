''' code to convert mp4 to mp3'''


path1 = "/media/shruti/Data/Internship_data/data/Fire_alram-20200916T183630Z-001/Fire_alram/Industrial/"
out_path = "/media/shruti/Data/Internship_data/data/Industrial/"
if not os.path.exists(out_path):
    os.makedirs(out_path)

for filename in os.listdir(path1):
    print(filename)
    mp4_file = os.path.join(path1, filename)
    print( mp4_file)
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio
    name, ext = os.path.splitext(filename)
    print(name, ext)
    mp3_file1 = os.path.join(out_path, name)
    print(mp3_file1)
    mp3_file = (mp3_file1 + '.mp3')
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoclip.close()
