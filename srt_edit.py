import pysrt
import random
import datetime


def times_to_seconds(time_tuples):

    second_tuples = []
    # Extract the two time objects from the tuple
    for time_tuple in time_tuples:
        time1, time2 = time_tuple

        # Convert time intervals to timedelta objects
        delta1 = datetime.timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second, microseconds=time1.microsecond)
        delta2 = datetime.timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second, microseconds=time2.microsecond)

        # Convert timedelta objects to seconds and cast to integers
        seconds1 = int(delta1.total_seconds())-2
        seconds2 = int(delta2.total_seconds())+2

    # Return the durations as a tuple
        second_tuples.append((seconds1, seconds2))
    return second_tuples



def convert_timestamp_to_seconds(timestamp):
    # Split the timestamp into hours, minutes, seconds, and milliseconds
    hours, minutes, rest = timestamp.split(':')
    seconds, milliseconds = rest.split(',')

    # Calculate the total duration in seconds
    total_seconds = (
        int(hours) * 3600 +  # Convert hours to seconds
        int(minutes) * 60 +   # Convert minutes to seconds
        int(seconds) +        # Add seconds
        int(milliseconds) / 1000  # Convert milliseconds to seconds
    )

    return total_seconds

def search_word_in_srt(file_path, search_word):
    # Open the SRT file using pysrt
    subs = pysrt.open(file_path, encoding='windows-1252')

    found_timestamps = []

    # Iterate through each subtitle in the SRT file
    for sub in subs:
        # Check if the search word is in the subtitle text (case-insensitive)
        if search_word.lower() in sub.text.lower():
            # Append the start and end timestamps to the list
            found_timestamps.append((sub.start.to_time(), sub.end.to_time()))

    return found_timestamps

def find_timestamp_sentence(word):
    file_path = 'oss.srt'  # Replace with your SRT file path
    timestamps = []
    found_timestamps = "##"
    found_timestamps = search_word_in_srt(file_path, word)
    if found_timestamps:
        return found_timestamps
    else:
        return 0
