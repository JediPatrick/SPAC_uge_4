from bisect import bisect_right
import csv
from datetime import datetime
from Median import writeToTempFiles

def parse_time(time_str):
    time_formats = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]
    for fmt in time_formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time format not recognized for: {time_str}")

def read_large_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            yield row  # Yield each row as a list of values

class dataObject:
    def __init__(self):
        self.meanTotal = 0
        self.row_count = 0
        self.lowerLimitValue = float('inf')  # Largest possible float
        self.upperLimitValue = float('-inf')   # Smallest possible float
        self.fileSplitSize = 10 # 1000000
        self.limitOfdataInMemory = 100000
        self.intervals = []
  
class intervalObject:
    def __init__(self, interval):
        self.interval = interval
        self.fileName = f"file_{interval[0]}_{interval[1]}.txt"
        self.data = []
        self.numberOfValues = 0
        self.totalNumberOfValues = 0
    
    def resetData(self):
        self.data = []
        self.totalNumberOfValues += self.numberOfValues
        self.numberOfValues = 0

def createRangesUpper(start, end, data, depth):    
    # Calculate midpoint of the current range
    midpoint = (start + end) / 2
    if depth != data.fileSplitSize // 2:
        depth += 1
        createRangesUpper(start, midpoint, data, depth)
    else:   
        data.intervals.append(intervalObject((start, end)))
    data.intervals.append(intervalObject((midpoint, end)))

def createRangesLower(start, end, data, depth):    
    # Calculate midpoint of the current range
    midpoint = (start + end) / 2
    data.intervals.append(intervalObject((start, midpoint)))
    if depth != data.fileSplitSize // 2:
        depth += 1
        createRangesLower(midpoint, end, data, depth)
    else:
        data.intervals.append(intervalObject((start, end)))


data = dataObject()

#data.intervals.append(intervalObject((0, 10)))
#data.intervals.append(intervalObject((10, 20)))
#data.intervals.append(intervalObject((20, 30)))

    
# Use binary search to find the position where x would fit in the intervals
#pos = bisect_right(lower_bounds, x_values[0]) - 1

#        x_values = [5, 12, 25, 8, 18, 29, 35]
#        for x in x_values:
#        #    pos = bisect_right(lower_bounds, x) - 1
#        #    data.intervals[pos].data.append(x)
#        #    data.intervals[pos].numberOfValues += 1
#            if x < data.lowerLimitValue:
#                data.lowerLimitValue = x
#            elif x > data.upperLimitValue:
#                data.upperLimitValue = x
#            data.meanTotal += x
#            data.row_count += 1
#        
#        average = data.meanTotal / data.row_count
#        
#        createRangesLower(data.lowerLimitValue, average, data, 1)
#        createRangesUpper(average, data.upperLimitValue, data, 1)
#        lower_bounds = [obj.interval[0] for obj in data.intervals]
#        
#        for x in x_values:
#            pos = bisect_right(lower_bounds, x) - 1
#            data.intervals[pos].data.append(x)
#            data.intervals[pos].numberOfValues += 1
#        
#        for interval in data.intervals:
#            print(f"lowerlimit {interval.interval[0]} upperlimit {interval.interval[1]}")
#        writeToTempFiles(data.intervals)

# Example usage
for row in read_large_csv(r"C:\Users\spac-36\Downloads\daily_rent_detail.csv"):
    startTime = parse_time(row[2])
    endTime = parse_time(row[3])
    if endTime > startTime:
        data.row_count += 1
        # Calculate the difference
        time_difference = endTime - startTime
        timePassed = float(time_difference.total_seconds() / 3600)
        data.meanTotal += timePassed
        if timePassed < data.lowerLimitValue:
            data.lowerLimitValue = timePassed
        elif timePassed > data.upperLimitValue:
            data.upperLimitValue = timePassed
   
average = data.meanTotal / data.row_count

createRangesLower(data.lowerLimitValue, average, data, 1)
createRangesUpper(average, data.upperLimitValue, data, 1)
lower_bounds = [obj.interval[0] for obj in data.intervals]

for row in read_large_csv(r"C:\Users\spac-36\Downloads\daily_rent_detail.csv"):
   # data.row_count += 1
    startTime = parse_time(row[2])
    endTime = parse_time(row[3])
    if endTime > startTime:
        # Calculate the difference
        time_difference = endTime - startTime
        timePassed = float(time_difference.total_seconds() / 3600)
        data.meanTotal += timePassed
        pos = bisect_right(lower_bounds, timePassed) - 1
        data.intervals[pos].data.append(timePassed)
        data.intervals[pos].numberOfValues += 1

writeToTempFiles(data.intervals)

print("hello")