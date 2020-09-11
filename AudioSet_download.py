
import pafy, os, shutil, time, ffmpy
import pandas as pd
import soundfile as sf 
import pafy, os, shutil, time, ffmpy
from natsort import natsorted
import pandas as pd
import soundfile as sf 
from tqdm import tqdm 

#function to clean labels 
def convertlabels(sortlist,labels,textlabels):
    
    clabels=list()

    for i in range(len(sortlist)):
        
        #find index in list corresponding
        index=labels.index(sortlist)
       
        clabel=textlabels[index]
        #pull out converted label
        clabels.append(clabel)

    return clabels 

def download_audio(link):
    listdir=os.listdir()
    os.system("youtube-dl -f 'bestaudio[ext=m4a]' '%s'"%(link))
    listdir2=os.listdir()
    filename=''
    for i in range(len(listdir2)):
        if listdir2[i] not in listdir and listdir2[i].endswith('.m4a'):
            filename=listdir2[i]
            break

    return filename

defaultdir=os.getcwd()
os.chdir(defaultdir)

#load labels of the videos

#number, label, words
loadfile=pd.read_excel('labels.xlsx')

number=loadfile.iloc[:,0].tolist()
labels=loadfile.iloc[:,1].tolist()
textlabels=loadfile.iloc[:,2].tolist()
#remove spaces for folders 
for i in range(len(textlabels)):
    textlabels[i]=textlabels[i].replace(' ','')

#now load data for youtube
loadfile2=pd.read_excel('unbalanced_train_segments.xlsx')

# ylabels have to be cleaned to make a good list (CSV --> LIST) 
yid=loadfile2.iloc[:,0].tolist()[2:]
ystart=loadfile2.iloc[:,1].tolist()[2:]
yend=loadfile2.iloc[:,2].tolist()[2:]
ylabels=loadfile2.iloc[:,3].tolist()[2:]
 
#make folders

try:
    defaultdir2=os.getcwd()+'/audiosetdata/'
    os.chdir(os.getcwd()+'/audiosetdata')
except:
    defaultdir2=os.getcwd()+'/audiosetdata/'
    os.mkdir(os.getcwd()+'/audiosetdata')
    os.chdir(os.getcwd()+'/audiosetdata')

existing_wavfiles=list()
for i in range(len(textlabels)):
    try:
        os.mkdir(textlabels[i])
    except:
        os.chdir(textlabels[i])
        listdir=os.listdir()
        for j in range(len(listdir)):
            if listdir[j].endswith('.wav'):
                existing_wavfiles.append(listdir[j])
        os.chdir(defaultdir2)

# get last file checkpoint to leave off 
existing_wavfiles=natsorted(existing_wavfiles)
print(existing_wavfiles)
try:
    lastfile=int(existing_wavfiles[-1][7:][0:-4])
except:
    lastfile=0


slink='https://www.youtube.com/watch?v='

for i in tqdm(range(len(yid))):
    print(len(yid))
    print(lastfile)
    if i < lastfile:
        print('skipping, already downloaded file...')
    else:
        link=slink+yid[i]
        print(link)
        start=float(ystart[i])
        end=float(yend[i])
        print('label', labels)
        print('text', textlabels)
        print('ylabel', ylabels[i])
        if not ylabels[i] in labels :
        #if clabels is not in :
            continue
        clabels=convertlabels(ylabels[i],labels,textlabels)
        
        
        print('clabel', clabels)

        if clabels != []:

            #change to the right directory
            newdir=defaultdir2+clabels[0]+'/'
            os.chdir(newdir)
            #if it is the first download, pursue this path to download video 
            lastdir=os.getcwd()+'/'

            if 'snipped'+str(i)+'.wav' not in os.listdir():

                try:
                    # use YouTube DL to download audio
                    filename=download_audio(link)
                    extension='.m4a'
                    #get file extension and convert to .wav for processing later 
                    os.rename(filename,'%s%s'%(str(i),extension))
                    filename='%s%s'%(str(i),extension)
                    if extension not in ['.wav']:
                        xindex=filename.find(extension)
                        filename=filename[0:xindex]
                        ff=ffmpy.FFmpeg(
                            inputs={filename+extension:None},
                            outputs={filename+'.wav':None}
                            )
                        ff.run()
                        os.remove(filename+extension)

                    file=filename+'.wav'
                    data,samplerate=sf.read(file)
                    totalframes=len(data)
                    totalseconds=totalframes/samplerate
                    startsec=start
                    startframe=samplerate*startsec
                    endsec=end
                    endframe=samplerate*endsec
                    # print(startframe)
                    # print(endframe)
                    sf.write('snipped'+file, data[int(startframe):int(endframe)], samplerate)
                    snippedfile='snipped'+file
                    os.remove(file)

                except:
                    print('no urls')

                #sleep 3 second sleep to prevent IP from getting banned 
                time.sleep(2) 
            else:
                print('skipping, already downloaded file...')
