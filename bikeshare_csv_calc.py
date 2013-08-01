#bikeshare_csv_calc.py
#Change station names on line 77

import sys, os, string, urllib, urllib2, datetime

class bikeshare:
    #DockSize=0
    def __init__(self,name="Unnamed",Docks=0):
        self.bikeSum, self.lastbike,self.OpenDocks,self.undocked, \
                self.docked, self.empty, self.full, self.bikeAvg, \
                self.minutes = (0,)*9
        self.DockSize=Docks
        self.name=name

    def updateCounter(self, bikes=0):
        self.minutes +=1
        self.bikeSum += float(bikes)
        self.OpenDocks=self.DockSize-bikes

        bike_change = bikes- self.lastbike
        if bike_change < 0:
            self.undocked +=bike_change
        elif bike_change > 0:
            self.docked +=bike_change
        
        if bikes<=3:
            self.empty +=1
        elif bikes >= self.DockSize-1:
            self.full +=1
            
        self.bikeAvg=float(self.bikeSum/self.minutes)
       
        self.lastbike = bikes
        return self.bikeAvg
    
    def getBikes(self):
        return self.lastbike
    def getBikeAvg (self):
        return self.bikeAvg
    def getOpenDocks(self):
        return self.OpenDocks
    def getDockSize(self):
        return self.DockSize
    def setDockSize(self, n):
        DockSize=n
    def getName(self):
        return self.name
    def setName(self,name=""):
        self.name=name
    def minEmpty(self):
        return self.empty
    def minFull(self):
        return self.full
    def getMinutes (self):
        return self.minutes
    
    def resetCounter(self):
        self.bikeSum=0
        self.undocked=0
        self.docked=0
        self.empty=0
        self.full=0
        self.bikeAvg=0
        self.minutes=0
        self.OpenDocks=0
        
    def getStats(self):
        return self.name, self.bikeAvg, self.undocked, self.docked,self.empty,self.full
       

def main():
    arg=sys.argv

    interval=[.5,1,3,8,12,24,72,168]
    if len(arg)==1:
        station_list=["W-26-St-&-8-Ave", "Pike-St-&-E-Broadway" ] ##### Station names at bottom of document
        for station in station_list:
            dirname =os.path.dirname(sys.argv[0])
            new_dir=dirname+"\\"+station+"\\"
            csv = new_dir+station+".csv"
            print "-"*75
            if os.path.isfile(csv) is False:
                csv=createBikeCSV(station)
            else:
                print "File '"+station+".csv' found in:\n " +new_dir+"\n"
            for hour in interval:
                ReadBikeCount(csv, float(hour))
            print "\n" +str(len(interval))+" files now available in:\n "+new_dir+"\n"
    elif len(arg)>1:
        try:
            print arg, len(arg)
            if len(arg)==3:
                ReadBikeCount(arg[1], float(arg[2]))
            elif len(arg)==2:
                ReadBikeCount(arg[1], interval)

        except:
            print "Error in argument %n." %(arg[1])
            
    x=raw_input ("\n"+ str(len(interval)*len(station_list))+\
                 " files created.\nProgram Completed.\nPress <ENTER> to exit>>")

     
def createBikeCSV(file_input, startDate="20130615", endDate=None,\
                  startTime="0:00", endTime=None):
    now = datetime.datetime.now()
    if endDate==None:
        endDate="%04d%02d%02d" % (now.year,now.month,now.day)
    if endTime==None:
        #endTime = "%02d:%02d" % (now.hour,now.minute)
        endTime = "%02d:00" % (now.hour)
        
    dirfilestation=file_input.split(",")
    station_dir=dirfilestation[0]
    station=dirfilestation[-1]
    fileName=station+".csv"
    print (station_dir+", "+ station+", "+ fileName)
        
    url=buildCitibikesURL(station, startDate, startTime, endDate, endTime)
    x=raw_input(url)
    return "done"

    dirname =os.path.dirname(sys.argv[0])
    directory = dirname+"\\"+station_dir+"\\"

    CSVfile=directory+fileName
    if os.path.isfile(CSVfile) is False:
        if not os.path.exists(directory):
            os.makedirs(directory)
        print "Downloading data from station", station+"... \nThis may take a few minutes."
        urllib.urlretrieve (url, CSVfile)
        #downloadFile(url, CSVfile)
        print "Done downloading!\n"
    else:
        print "\nFile already exists:\n", CSVfile,"\n"
    return CSVfile
    
def buildCitibikesURL(station,startDate,startTime,endDate,endTime):
#http://data.citibik.es/render/?target=Montague-St-%26-Clinton-St.available_bikes&from=0:00_20130615&until=0:00_20130715&format=csv
    url=r"http://data.citibik.es/render/?target="
    url = url+station.replace("&",r"%26")+".available_bikes&from="+startTime+"_"+\
           startDate+"&until="+endTime+"_"+endDate+"&format=csv"
    return url

def downloadStationList (stationList):
    stationList=["downtown_fulton_area, Cliff-St-&-Fulton-St","downtown,Cleveland-Pl-&-Spring-St"]
    for station in stationList:
        csv=createBikeCSV(station)
        ReadBikeCount(csv,3)
    

def downloadFile(url,file_name):
    #file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    try:
        file_size = int(meta.getheaders("Content-Length")[0])
    except:
        file_size=-1
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

      
def openFileAsReadLines(filename=""):
    # if no file is given, ask user
    if filename=="":
        filename=raw_input("Enter the source file name>")

    #Open file, then read lines
    infile=open(filename,"r")
    fileAsLines = infile.readlines()

    infile.close()

    return fileAsLines

def FindDockSize (dockData=None):
    DockSize=0
    if dockData is not None:
        for x in dockData:
            record=x.split(",")
            try:
                docks= float(record[2])
            except:
                None
            DockSize=max(DockSize,docks)
    else:
        DockSize=-1
    return DockSize
        
 
def ReadBikeCount(csv, hours):
    bikecsv=openFileAsReadLines(csv)
    DockSize=FindDockSize(bikecsv)
    name=bikecsv[0].split(",")[0].replace(".available_bikes","")
    bikeStation=bikeshare(name, DockSize)

    directory,filename = os.path.split(os.path.abspath(csv))
    outfile=open(directory+"\\"+str(hours)+ "hourAvg_"+filename,"w")

    header="Station,Start Date & Time,End Date & Time,Avg. Available Bikes,"+\
            "Undocked, Docked, Minutes Empty, Minutes Full, %d Docks \n" %(DockSize)
    outfile.writelines(header)

    time_interval=hours*60 #time interval in minutes
    time_count, timestart = 0, None
    print "Station: "+bikeStation.getName()+" Time Interval: "+\
          str(hours)+" hours...",
    for i in bikecsv:
        record=i.split(",")
        timeend=record[1]
        try:
            bikes= float(record[2])
        except:
            None
          
        if bikeStation.getMinutes()+1==time_interval:
            bikeStation.updateCounter(bikes)
            name, bikeavg, undocked, docked, empty, full = bikeStation.getStats()
            output = name+","+str(timestart)+","+str(timeend)+","+str(bikeavg)\
                     +","+str(undocked)+","+str(docked)+","+str(empty)+","+str(full)+"\n"
            outfile.writelines(output)
            timestart= None
            bikeStation.resetCounter()
            
        else:
            if timestart==None:
                timestart=timeend
            bikeStation.updateCounter(bikes)

    outfile.close()
    print " completed!"

def getRawCSVFiles (directory):
    f = openFileAsReadLines("stations.info")
    for station in f:
        station=station.replace("\n","")
        b = createBikeCSV(directory+","+station)
    

getRawCSVFiles("All_stations")   
#main()

###downloadStationList("x")



############# Copy from below without "##"
#Station Names
##
##1-Ave-&-18-St
##1-Ave-&-E-15-St
##1-Ave-&-E-30-St
##1-Ave-&-E-44-St
##10-Ave-&-W-28-St
##11-Av-&-59-St
##11-Ave-&-W-41-St
##11-Ave-&-W-59-St
##12-Ave-&-W-40-St
##2-Ave-&-E-30-St
##2-Ave-&-E-58-St
##3-Ave-&-Flatbush-Ave
##5-Ave-&-E-29-St
##52-St-&-9-Ave
##6-Ave-&-Canal-St
##6-Ave-&-W-33-St
##7th-Ave-&-Farragut-St
##8--Ave-&-W-52-St
##8--Ave-&-W-57-St
##8-Ave-&-W-31-St
##9-Ave-&-W-14-St
##9-Ave-&-W-16-St
##9-Ave-&-W-18-St
##9-Ave-&-W-22-St
##9-Ave-&-W-45-St
##Adelphi-St-&-Myrtle-Ave
##Allen-St-&-E-Houston-St
##Allen-St-&-Hester-St
##Allen-St-&-Rivington-St
##Ashland-Pl-&-Hanson-Pl
##Atlantic-Ave-&-Fort-Greene-Pl
##Atlantic-Ave-&-Furman-St
##Avenue-D-&-E-12-St
##Avenue-D-&-E-3-St
##Avenue-D-&-E-8-St
##Bank-St-&-Hudson-St
##Bank-St-&-Washington-St
##Barclay-St-&-Church-St
##Barrow-St-&-Hudson-St
##Bayard-St-&-Baxter-St
##Bedford-Ave-&-S-9-St
##Bialystoker-Pl-&-Delancey-St
##Bond-St-&-Schermerhorn-St
##Broad-St-&-Bridge-St
##Broadway-&-Battery-Pl
##Broadway-&-Berry-St
##Broadway-&-E-14-St
##Broadway-&-E-22-St
##Broadway-&-W-24-St
##Broadway-&-W-29-St
##Broadway-&-W-32-St
##Broadway-&-W-36-St
##Broadway-&-W-37-St
##Broadway-&-W-39-St
##Broadway-&-W-41-St
##Broadway-&-W-49-St
##Broadway-&-W-51-St
##Broadway-&-W-53-St
##Broadway-&-W-55-St
##Broadway-&-W-57-St
##Broadway-&-W-60-St
##Cadman-Plaza-E-&-Red-Cross-Pl
##Cadman-Plaza-E-&-Tillary-St
##Cadman-Plaza-W-&-Middagh-St
##Canal-St-&-Rutgers-St
##Carlton-Ave-&-Park-Ave
##Carmine-St-&-6-Ave
##Catherine-St-&-Monroe-St
##Central-Park-S-&-6-Ave
##Centre-St-&-Chambers-St
##Centre-St-&-Worth-St
##Cherry-St
##Christopher-St-&-Greenwich-St
##Church-St-&-Leonard-St
##Clark-St-&-Henry-St
##Clermont-Ave-&-Lafayette-Ave
##Clermont-Ave-&-Park-Ave
##Cleveland-Pl-&-Spring-St
##Cliff-St-&-Fulton-St
##Clinton-Ave-&-Flushing-Ave
##Clinton-Ave-&-Myrtle-Ave
##Clinton-St-&-Grand-St
##Clinton-St-&-Joralemon-St
##Clinton-St-&-Tillary-St
##Columbia-Heights-&-Cranberry-St
##Columbia-St-&-Rivington-St
##Concord-St-&-Bridge-St
##Cooper-Square-&-E-7-St
##Cumberland-St-&-Lafayette-Ave
##DeKalb-Av-&-Skillman-St
##DeKalb-Ave-&-Hudson-Ave
##DeKalb-Ave-&-S-Portland-Ave
##DeKalb-Ave-&-Skillman-St
##DeKalb-Ave-&-Vanderbilt-Ave
##Dean-St-&-4-Ave
##Dekalb-Ave-&-Skillman-St
##Division-St-&-Bowery
##Duane-St-&-Greenwich-St
##Duffield-St-&-Willoughby-St
##E-10-St-&-5-Ave
##E-10-St-&-Avenue-A
##E-11-St-&-1-Ave
##E-11-St-&-Broadway
##E-11-Street-&-2-Avenue
##E-12-St-&-3-Ave
##E-13-St-&-Avenue-A
##E-14-St-&-Avenue-B
##E-15-St-&-3-Ave
##E-16-St-&-5-Ave
##E-16-St-&-Irving-Pl
##E-17-St-&-Broadway
##E-19-St-&-3-Ave
##E-2-St-&-2-Ave
##E-2-St-&-Avenue-B
##E-2-St-&-Avenue-C
##E-20-St-&-2-Ave
##E-20-St-&-FDR-Drive
##E-20-St-&-Park-Ave
##E-23-St-&-1-Ave
##E-24-St-&-Park-Ave-S
##E-25-St-&-1-Ave
##E-25-St-&-2-Ave
##E-27-St-&-1-Ave
##E-3-St-&-1-Ave
##E-30-St-&-Park-Ave-S
##E-31-St-&-3-Ave
##E-32-St-&-Park-Av
##E-33-St-&-1-Ave
##E-33-St-&-5-Ave
##E-37-St-&-Lexington-Ave
##E-39-St-&-2-Ave
##E-39-St-&-3-Av
##E-4-St-&-2-Ave
##E-40-St-&-5-Ave
##E-43-St-&-2-Ave
##E-43-St-&-Vanderbilt-Ave
##E-45-St-&-3-Ave
##E-47-St-&-1-Ave
##E-47-St-&-2-Ave
##E-47-St-&-Park-Av
##E-48-St-&-3-Ave
##E-5-St-&-Avenue-C
##E-51-St-&-1-Ave
##E-51-St-&-Lexington-Ave
##E-52-St-&-2-Ave
##E-53-St-&-Madison-Ave
##E-53-St-and-Lexington-Ave
##E-55-St-&-2-Ave
##E-55-St-&-5-Ave
##E-55-St-&-Lexington-Ave
##E-56-St-&-3-Ave
##E-58-St-and-3-Ave
##E-59-St-&-Sutton-Pl
##E-6-St-&-Avenue-B
##E-6-St-&-Avenue-D
##E-7-St-&-Avenue-A
##E-9-St-&-Avenue-C
##Elizabeth-St-&-Hester-St
##FDR-Drive-&-E-35-St
##Flatbush-Ave-&-Fulton-St
##Flushing-Ave-&-Carlton-Ave
##Forsyth-St-&-Broome-St
##Forsyth-St-&-Canal-St
##Franklin-Ave-&-Myrtle-Ave
##Franklin-St-&-W-Broadway
##Front-St-&-Gold-St
##Front-St-&-Maiden-Ln
##Front-St-&-Washington-St
##Fulton-St-&-Clermont-Ave
##Fulton-St-&-Grand-Ave
##Fulton-St-&-Waverly-Ave
##Fulton-St-&-William-St
##Gallatin-Pl-&-Livingston-St
##Gouverneur-St-&-Madison-St
##Grand-Army-Plaza-&-Central-Park-S
##Grand-St-&-Greene-St
##Grand-St-&-Havemeyer-St
##Great-Jones-St
##Greenwich-Ave-&-7-Ave
##Greenwich-Ave-&-8-Ave
##Greenwich-St-&-N-Moore-St
##Greenwich-St-&-Warren-St
##Hancock-St-&-Bedford-Ave
##Hanover-Pl-&-Livingston-St
##Harrison-St-&-Hudson-St
##Henry-St-&-Atlantic-Ave
##Henry-St-&-Grand-St
##Henry-St-&-Poplar-St
##Hicks-St-&-Montague-St
##Howard-St-&-Centre-St
##Hudson-St-&-Reade-St
##Jay-St-&-Tech-Pl
##John-St-&-William-St
##Johnson-St-&-Gold-St
##Joralemon-St-&-Adams-St
##Kent-Ave-&-S-11-St
##LaGuardia-Pl-&-W-3-St
##Lafayette-Ave-&-Classon-Ave
##Lafayette-Ave-&-Fort-Greene-Pl
##Lafayette-St-&-E-8-St
##Lafayette-St-&-Jersey-St
##Laight-St-&-Hudson-St
##Lawrence-St-&-Willoughby-St
##Lefferts-Pl-&-Franklin-Ave
##Lexington-Ave-&-Classon-Ave
##Lexington-Ave-&-E-24-St
##Lexington-Ave-&-E-26-St
##Lexington-Ave-&-E-37-St
##Liberty-St-&-Broadway
##Lispenard-St-&-Broadway
##Little-West-St-&-1-Pl
##MacDougal-St-&-Prince-St
##MacDougal-St-&-Washington-Sq
##Macon-St-&-Nostrand-Ave
##Madison-St-&-Clinton-St
##Madison-St-&-Montgomery-St
##Maiden-Ln-&-Pearl-St
##Market-St-&-Cherry-St
##Mercer-St-&-Bleecker-St
##Mercer-St-&-Spring-St
##Metropolitan-Ave-&-Bedford-Ave
##Monroe-St-&-Bedford-Ave
##Monroe-St-&-Classon-Ave
##Montague-St-&-Clinton-St
##Mott-St-&-Prince-St
##Murray-St-&-West-St
##Myrtle-Ave-&-Emerson-Pl
##Myrtle-Ave-&-St-Edwards-St
##Nassau-St-&-Navy-St
##Norfolk-St-&-Broome-St
##Old-Fulton-St
##Old-Slip-&-Front-St
##Park-Ave-&-St-Edwards-St
##Park-Pl-&-Church-St
##Pearl-St-&-Anchorage-Pl
##Pearl-St-&-Hanover-Square
##Perry-St-&-Bleecker-St
##Pershing-Square-N
##Pershing-Square-S
##Pike-St-&-E-Broadway
##Pike-St-&-Monroe-St
##Pitt-St-&-Stanton-St
##Railroad-Ave-&-Kay-Ave
##Reade-St-&-Broadway
##Rivington-St-&-Chrystie-St
##Rivington-St-and-Ridge-St
##S-3-St-&-Bedford-Ave
##S-4-St-&-Wythe-Ave
##S-5-Pl-&-S-4-St
##S-Portland-Ave-&-Hanson-Pl
##Sands-St-&-Gold-St
##South-End-Av-&-Liberty-St
##South-End-and-Liberty
##South-St-&-Gouverneur-Ln
##South-St-&-Whitehall-St
##Spring-St-&-6-Ave
##Spruce-St-&-Nassau-St
##St-James-Pl-&-Lafayette-Ave
##St-James-Pl-&-Oliver-St
##St-James-Pl-&-Pearl-St
##St-Marks-Pl-&-1-Ave
##St-Marks-Pl-&-2-Ave
##Stanton-St-&-Chrystie-St
##Stanton-St-&-Mangin-St
##State-St
##State-St-&-Smith-St
##Suffolk-St-&-Stanton-St
##Sullivan-St-&-Washington-Sq
##University-Pl-&-E-14-St
##Vesey-Pl-&-River-Terrace
##W-11-St-&-6-Ave
##W-13-St-&-5-Ave
##W-13-St-&-6-Ave
##W-13-St-&-7-Ave
##W-14-St-&-The-High-Line
##W-15-St-&-7-Ave
##W-16-St-&-The-High-Line
##W-17-St-&-8-Ave
##W-18-St-&-11-Ave
##W-18-St-&-6-Av
##W-20-St-&-7-Ave
##W-20-St-&-8-Ave
##W-21-St-&-6-Ave
##W-22-St-&-10-Ave
##W-22-St-&-11-Ave
##W-22-St-&-8-Ave
##W-24-St-&-7-Ave
##W-25-St-&-6-Ave
##W-26-St-&-10-Ave
##W-26-St-&-8-Ave
##W-27-St-&-7-Ave
##W-29-St-&-9-Ave
##W-31-St-&-7-Ave
##W-33-St-&-7-Ave
##W-33-St-&-8-Ave
##W-34-St-&-11-Ave
##W-37-St-&-10-Ave
##W-37-St-&-5-Ave
##W-38-St-&-8-Ave
##W-39-St-&-9-Ave
##W-4-St-&-7-Ave-S
##W-41-St-&-8-Ave
##W-42-St-&-8-Ave
##W-43-St-&-10-Ave
##W-43-St-&-6-Ave
##W-44-St-&-5-Ave
##W-45-St-&-6-Ave
##W-45-St-&-8-Ave
##W-46-St-&-11-Ave
##W-47-St-&-10-Ave
##W-49-St-&-5-Ave
##W-49-St-&-8-Ave
##W-51-St-&-6-Ave
##W-52-St-&-11-Ave
##W-52-St-&-5-Ave
##W-53-St-&-10-Ave
##W-54-St-&-9-Ave
##W-56-St-&-10-Ave
##W-56-St-&-6-Ave
##W-59-St-&-10-Ave
##W-Broadway-&-Spring-St
##W-Houston-St-&-Hudson-St
##Warren-St-&-Church-St
##Washington-Ave-&-Greene-Ave
##Washington-Ave-&-Park-Ave
##Washington-Park
##Washington-Pl-&-6-Ave
##Washington-Pl-&-Broadway
##Washington-Square-E
##Washington-St-&-Gansevoort-St
##Water---Whitehall-Plaza
##Watts-St-&-Greenwich-St
##West-St-&-Chambers-St
##West-Thames-St
##William-St-&-Pine-St
##Willoughby-Ave-&-Hall-St
##Willoughby-Ave-&-Walworth-St
##Wiloughby-St-&-Fleet-St
##Wythe-Ave-&-Metropolitan-Ave
##York-St-&-Jay-St
##DeKalb-Ave-&-S-Portland-Ave
