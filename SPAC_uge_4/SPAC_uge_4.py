from bisect import bisect_right
import csv
from datetime import datetime
from Median import dataObject

path = r"C:\Users\spac-36\Downloads\daily_rent_detail.csv"

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


data = dataObject()

for row in read_large_csv(path):
    startTime = parse_time(row[2])
    endTime = parse_time(row[3])
    if endTime > startTime: # some data has a negative time duration so the are not used 
        data.row_count += 1
        # Calculate the difference
        time_difference = endTime - startTime
        timePassed = float(time_difference.total_seconds() / 3600)
        data.meanTotal += timePassed
        if timePassed < data.lowerLimitValue:
            data.lowerLimitValue = timePassed
        elif timePassed > data.upperLimitValue:
            data.upperLimitValue = timePassed
   
lower_bounds = data.getIntervals()

counter = 0
for row in read_large_csv(path):
    startTime = parse_time(row[2])
    endTime = parse_time(row[3])

    if endTime > startTime: # some data has a negative time duration so the are not used
        # Calculate the difference
        time_difference = endTime - startTime
        timePassed = float(time_difference.total_seconds() / 3600)
        data.meanTotal += timePassed
        pos = bisect_right(lower_bounds, timePassed) - 1
        data.intervals[pos].data.append(timePassed)
        data.intervals[pos].numberOfValues += 1
    
    counter += 1
    if counter % data.limitOfdataInMemory == 0:
        data.writeToTempFiles()

data.writeToTempFiles()
median = data.calculateMedian()

print(median)