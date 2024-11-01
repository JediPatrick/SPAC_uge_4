
def writeToTempFiles(intervals):
    # The code goes through all the intervals and write it to files 
    for interval in intervals:
        if interval.numberOfValues > 0:
            file = open(interval.fileName, "a")
            data = "\n".join(str(x) for x in interval.data)
            file.write(data + "\n")
            file.close()