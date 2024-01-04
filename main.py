import whisper_timestamped as whisper
from moviepy.editor import VideoFileClip,AudioFileClip,concatenate_videoclips
from srt_edit import *
import numpy as np 
import os

def concatenate_video_clips(video_clips):

    # Concatenate video clips
    final_clip = concatenate_videoclips(video_clips)
    
    # Write the final video to the output file
    final_clip.write_videofile("final.mp4", codec='libx264')

def save_audios(timestamp,imput_file_path):
    
    directory = "temp"
    if not os.path.exists(directory):
        os.makedirs(directory)
    start,end = timestamp
    video = get_cut_video(input_file_path, start, end)
    audio = video.audio
    audio.write_audiofile(f"temp/audio_clip.wav")
    return video  

def get_cut_video(input_file, start_time, end_time):

    # Load the video clip
    video_clip = VideoFileClip(input_file)
    # Get the subclip from start_time to end_time
    cut_clip = video_clip.subclip(start_time, end_time)

    return cut_clip

def get_audio_file_paths(directory):
    return os.path.join(directory,os.listdir(directory)[0])

def get_timestamps_word(structure,word):
    for segment in structure['segments']:
        segment_text = segment['words']
        a = 0
        for words in segment_text:
            if word == words["text"]:
                return words['start'], words['end']
    return -1,-1
    
input_file_path = "OSS/OSS.mp4"  # Replace with your input video path

words = ["vous","avez","de","beaux","yeux"]
model = whisper.load_model("NbAiLab/whisper-large-v2-nob", device="cpu")
print("loaded!")
videos = []
for word in words:
    
    timestamps = 0
    while timestamps ==0:
        timestamps = find_timestamp_sentence(word)
    timestamps = times_to_seconds(timestamps)
    random.shuffle(timestamps)
    a = False
    i = 0
    start, end = -1, -1
    video = 0
    while a == False and i<len(timestamps):
        video = save_audios(timestamps[i],input_file_path)
        audio_file = get_audio_file_paths("temp")
        result = whisper.transcribe(audio = audio_file ,language="french",model = model,beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),remove_punctuation_from_words=True)
        start,end = get_timestamps_word(result,word)
        if start > 0 and start<video.duration and end<=video.duration and start < end:
            a = True
            start-=0.1
            end+=0.1
            os.remove(os.path.join("temp",os.listdir("temp")[0]))
        i+=1
    if a == False:
        print(f"ERROOOOOOOOOR for word {word}")
    else:
        print(f"word {word} done in {i} steps! next word")
        newvid = video.subclip(start, end)
        videos.append(newvid)

concatenate_video_clips(videos)