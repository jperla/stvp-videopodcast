import os
import re
import commands

def convert(id):
    file_in = '/mnt/stvp/repository/%s.flv' % id
    file_out = '/mnt/stvp/transcoded/%s.xvid.avi' % id

    if os.path.exists(file_out):
        print 'transcoded file already exists for %s' % id
    else:
        command = 'ffmpeg -i %s -vcodec xvid -acodec mp3 %s' % (file_in, file_out)
        print commands.getoutput(command)
    
ids = [re.match('([0-9]+).flv', filename).group(1) for filename in os.listdir('/mnt/stvp/repository/')]

for id in ids:
    convert(id)
    print 'just transcoded %s' % id

'''ffmpeg -i I_KRmU2dO2M.flv -ab 56 -ar 22050 -b 500 -s 320x240 -vcodec xvid -acodec mp3 video.avi'''

