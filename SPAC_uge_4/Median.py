
class dataObject:
    def __init__(self):
        self.meanTotal = 0
        self.row_count = 0
        self.lowerLimitValue = float('inf')  # Largest possible float
        self.upperLimitValue = float('-inf')   # Smallest possible float
        self.fileSplitSize = 10
        self.limitOfdataInMemory = 54
        self.intervals = []

    def getMedianPosition(self):
        postions = []
   
        if self.row_count % 2 == 1:
             position = {
                "index": self.row_count // 2,
                "value": None
             }
             postions.append(position)
        else:
            position = {
                "index": self.row_count // 2,
                "value": None
             }
            position2 = {
                "index": self.row_count // 2,
                "value": None
             }
            postions.append(position)
            postions.append(position2)
        
        return postions 

    def calculateMedian(self):
        positions = self.getMedianPosition()
        positions = self.getMedianFromFile(positions)
        
        if len(positions) == 1:
            median = positions[0]["value"]
        else:
            median = (positions[0]["value"] + positions[1]["value"]) / 2
        
        return median
    
    def getMedianFromFile(self, positions):
        currentIndex = 0
        for interval in self.intervals:
            interval.totalStartIndex = currentIndex
            interval.totalEndIndex = interval.totalNumberOfValues + currentIndex
            currentIndex += interval.totalNumberOfValues + 1
    
            shouldIntervalFileBeSortet = False
            for position in positions:
                if position["index"] > interval.totalStartIndex and position["index"] < interval.totalEndIndex:
                   shouldIntervalFileBeSortet = True
                   break
            
            if shouldIntervalFileBeSortet:
                file = getFile(interval.fileName)
                file.sort()
                for position in positions:
                    if position["index"] > interval.totalStartIndex and position["index"] < interval.totalEndIndex:
                       position["value"] = file[position["index"]]
            
            medianFound = all(position.get("value") is not None for position in positions)
            if medianFound:
                break
        return positions

    def createRangesUpper(self, start, end, depth):    
        # Calculate midpoint of the current range
        midpoint = (start + end) / 2
        if depth != self.fileSplitSize // 2:
            depth += 1
            self.createRangesUpper(start, midpoint, depth)
        else:   
            self.intervals.append(intervalObject((start, end)))
        self.intervals.append(intervalObject((midpoint, end)))
    
    def createRangesLower(self, start, end, depth):    
        # Calculate midpoint of the current range
        midpoint = (start + end) / 2
        self.intervals.append(intervalObject((start, midpoint)))
        if depth != self.fileSplitSize // 2:
            depth += 1
            self.createRangesLower(midpoint, end, depth)
        else:
            self.intervals.append(intervalObject((start, end)))
    
    def getIntervals(self):
        average = self.meanTotal / self.row_count

        self.createRangesLower(self.lowerLimitValue, average, 1)
        self.createRangesUpper(average, self.upperLimitValue, 1)

        return [obj.interval[0] for obj in self.intervals]

    def writeToTempFiles(self):
        for interval in self.intervals:
            if interval.numberOfValues > 0:
                file = open(interval.fileName, "a")
                data = "\n".join(str(x) for x in interval.data)
                file.write(data + "\n")
                file.close()
            interval.resetData()
 
            
class intervalObject:
    def __init__(self, interval):
        self.interval = interval
        self.fileName = f"file_{interval[0]}_{interval[1]}.txt"
        self.data = []
        self.numberOfValues = 0
        self.totalNumberOfValues = 0
        self.totalStartIndex = 0
        self.totalEndIndex = 0
    
    def resetData(self):
        self.data = []
        self.totalNumberOfValues += self.numberOfValues
        self.numberOfValues = 0


def getFile(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]  # Remove newline characters
    return lines