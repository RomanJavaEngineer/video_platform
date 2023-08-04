from logging import Logger
from timeit_decorator import timeit
import json
import yt_dlp as ydl
from utils import return_video_download_location, return_video_folder_name
from datetime import timedelta
import ffmpeg
import os
from typing import Dict

class ImportVideo:
    def __init__(self, video_runner_obj: Dict[str, int]):
        """
        Initialize ImportVideo object.
        
        Parameters:
        video_runner_obj (Dict[str, int]): A dictionary that contains the information of the video.
            The keys are "video_id", "video_start_time", and "video_end_time", and their values are integers.
        """
        self.video_runner_obj = video_runner_obj
    
    @timeit
    def download_video(self):
        """
        Download the video from YouTube
        
        Returns:
        None
        """
        # Download video from YouTube
        print("Downloading video from YouTube")
        video_id = self.video_runner_obj.get("video_id")
        video_start_time = self.video_runner_obj.get("video_start_time",None)
        video_end_time = self.video_runner_obj.get("video_end_time",None)
        logger: Logger = self.video_runner_obj.get("logger")
        
        ydl_opts = {'outtmpl': return_video_download_location(self.video_runner_obj), "format": "best" }
        vid = ydl.YoutubeDL(ydl_opts).extract_info(
            url='https://www.youtube.com/watch?v=' + video_id, download=True)

        # Get Video Duration
        duration = vid.get('duration')

        # Get Video Title
        title = vid.get('title')
        logger.info(f"Video Title: {title}")
        print("Video Title: ", title)

        # Save metadata to json file
        with open(return_video_folder_name(self.video_runner_obj) + '/metadata.json', 'w') as f:
            f.write(json.dumps({'duration': duration, 'title': title}))
        if video_start_time and video_end_time:
            # Convert start and end time to timedelta
            start_time = timedelta(seconds=int(video_start_time))
            end_time = timedelta(seconds=int(video_end_time))
            
            print("start time: ", start_time)
            logger.info(f"start time: {start_time}")
            print("end time: ", end_time)
            logger.info(f"end time: {end_time}")

            # Trim video and audio based on start and end time
            input_stream = ffmpeg.input(return_video_download_location(self.video_runner_obj))
            vid = (
                input_stream.video
                .trim(start=video_start_time, end=video_end_time)
                .setpts('PTS-STARTPTS')
            )
            aud = (
                input_stream.audio
                .filter_('atrim', start=video_start_time, end=video_end_time)
                .filter_('asetpts', 'PTS-STARTPTS')
            )

            # Join trimmed video and audio
            joined = ffmpeg.concat(vid, aud, v=1, a=1).node

            # Output trimmed video
            logger.info(f"Trimming video {return_video_folder_name(self.video_runner_obj)}")
            print("Trimming video",return_video_folder_name(self.video_runner_obj))
            output = ffmpeg.output(joined[0], joined[1], return_video_folder_name(self.video_runner_obj) + '/trimmed.mp4')
            output.run(overwrite_output=True)

            # Delete original video
            if os.path.exists(return_video_download_location(self.video_runner_obj)):
                os.remove(return_video_download_location(self.video_runner_obj))

            # Rename trimmed video to original name
            os.rename(return_video_folder_name(self.video_runner_obj) + '/trimmed.mp4', return_video_download_location(self.video_runner_obj))
            
        logger.info(f"Video downloaded to {return_video_download_location(self.video_runner_obj)}")
        return
    
    
    
    # rsync -aZP sfsu_me:/home/datasets/pipeline/wzh0EuLhRhE_files ./