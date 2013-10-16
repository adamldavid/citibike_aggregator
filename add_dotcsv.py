
def main():
    f=openFileAsReadLines("all_stations.info")
    outfile=open("all_stations_csv.info","w")
    for line in f:
        s="1.0hourAvg_"+line.strip() +".csv"+"\n"
        outfile.write(s)
    outfile.close()
    print "done"
    




def openFileAsReadLines(filename=""):
    # if no file is given, ask user
    if filename=="":
        filename=raw_input("Enter the source file name>")

    #Open file, then read lines
    infile=open(filename,"r")
    fileAsLines = infile.readlines()

    infile.close()

    return fileAsLines

main()
