from fileinput import filename
import plistlib

def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' % fileName)
    # read in a playlist
    plist = plistlib.readPlist(fileName)
    print("plist['Tracks']:",plist['Tracks'])
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
    # a list of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        plist = plistlib.readPlist(fileName)
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
    print('*trackNameSets:',*trackNameSets)
    # get the set of common tracks
    commonTracks = set.intersection(*trackNameSets) # intersection() 方法用于返回两个或更多集合中都包含的元素，即交集
    # write to file
    if len(commonTracks) > 0: # alternative: if commonTracks
        f = open("common.txt",'w')
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found. Track names weitten to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    # read in a playlist
    plist = plistlib.readPlist(fileName)
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
        print('No valid Album Rating/Total Time data in %s.' %filename)
        return