import argparse
import plistlib
import numpy as np
import matplotlib.pyplot as pyplot

def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' % fileName)
    # read in a playlist
    with open(r'D:\Python\PlayGround\PlayGroundCode\iTunes\test-data'+ '\\' + fileName,'r') as f:
        plist = plistlib.load(f)
    # print("plist['Tracks']:",plist['Tracks'])
    # get the tracks from the Tracks dictionary
    tracks = plist['Tracks']
    # create a track name dictionary,save duplicate tracks
    trackNames = {}
    # iterate through the tracks
    for trackId,track in tracks.items():
        print('trackId,track :',trackId,track)
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                # if a name and duration match,increment the count 
                # round the track length to the nearest second
                if duration // 1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration,count+1)
            else:
                # add dictionary entry as tuple (duration,count)
                trackNames = (duration,1)
        except:
            # ignore
            pass
    
    # store duplicates as (name,count) tuples
    dups = []
    for k,v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1],k))
        
        # save duplicates to a file
        if len(dups) > 0:
            print('Found %d duplicates. Track names saved to dup.txt' % len(dups))
        else:
            print('No duplicate tracks found!')
        
        # The following lines should be written into the if statement ?
        f = open('dups.txt','w')
        for val in dups:
            f.write('[%d] %s\n' %[val[0],val[1]])
        f.close()

def findCommonTracks(fileNames):
    """
    Find common tracks in given playlist files,
    and save them to common.txt
    """
    # a list of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # print('fileName:',fileName)
        # fileName = dict(fileName)
        # read in playlist
        with open(r'D:\Python\PlayGround\PlayGroundCode\iTunes\test-data'+ '\\' + fileName,'rb') as f:
            plist = plistlib.load(f)
        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # add the rack name to a set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
    # add to list
    trackNameSets.append(trackNames) # 这一句是否要包含在for fileName in fileNames中
    # print('*trackNameSets:',*trackNameSets)
    # get the set of common tracks
    commonTracks = set.intersection(*trackNameSets) # intersection() 方法用于返回两个或更多集合中都包含的元素，即交集
    # write to file
    if len(commonTracks) > 0: # alternative: if commonTracks
        f = open("common.txt",'w')
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s)
        f.close()
        print("%d common tracks found. Track names weitten to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    """
    Plot some statistics by reading track information from playlist
    """
    # read in a playlist
    with open(r'D:\Python\PlayGround\PlayGroundCode\iTunes\test-data'+ '\\' + fileName,'rb') as f:
        plist = plistlib.load(f)
    # get the racks from the playlist
    tracks = plist['Tracks']
    ratings = []
    durations = []
    # iterate through the tracks
    for trackId,track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass
    # ensure that valid data was collected
    if ratings ==[] or durations == []:
        print('No valid Album Rating/Total Time data in %s.' %fileName)
        return

    # scatter plot
    x = np.array(durations,np.int32)
    # covert to minutes
    x = x/60000.0
    y = np.array(ratings,np.int32)
    pyplot.subplot(2,1,1)
    pyplot.plot(x,y,'o')
    pyplot.axis([0,1.05*np.max(x),-1,110]) # axis( [xmin xmax ymin ymax] )    设置当前坐标轴 x轴 和 y轴的限制范围
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2,1,2)
    pyplot.hist(x,bins=20) # 在x最小值和最大值中间分成20份
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()

def main():
    # create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes
    """
    parser = argparse.ArgumentParser(description = descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common',nargs='*',dest='plFiles',required=False)
    group.add_argument('--stats',dest='plFile',required=False)
    group.add_argument('--dup',dest='plFileD',required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print('These are not the tracks you are looking for.')

if __name__ == '__main__':
    main()