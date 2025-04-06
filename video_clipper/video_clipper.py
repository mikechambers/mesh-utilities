import os
import argparse
import ffmpeg

def cut_videos_into_clips(input_folder, output_folder, clip_duration=5):
    """
    Takes a folder of videos and cuts each video into clips of specified duration using ffmpeg
    
    Args:
        input_folder (str): Path to folder containing input videos
        output_folder (str): Path to folder where clips will be saved
        clip_duration (int): Duration of each clip in seconds (default: 5)
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    
    # Get all video files in the input folder
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    video_files = [f for f in os.listdir(input_folder) if any(f.lower().endswith(ext) for ext in video_extensions)]
    
    if not video_files:
        print(f"No video files found in {input_folder}")
        return
    
    print(f"Found {len(video_files)} video files to process")
    
    # Process each video
    for video_file in video_files:
        input_path = os.path.join(input_folder, video_file)
        
        try:
            # Get video information
            probe = ffmpeg.probe(input_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            
            if video_stream is None:
                print(f"No video stream found in {video_file}")
                continue
                
            # Get video duration
            duration = float(probe['format']['duration'])
            num_clips = int(duration // clip_duration)
            
            print(f"Video duration: {duration:.2f} seconds, creating {num_clips} clips")
            
            # Extract the filename without extension
            filename_base = os.path.splitext(video_file)[0]
            
            # Create clips
            for i in range(num_clips):
                start_time = i * clip_duration
                
                # Generate output filename
                output_filename = f"{filename_base}_clip_{i+1:03d}.mp4"
                output_path = os.path.join(output_folder, output_filename)
                
                # Create ffmpeg command
                print(f"Saving clip {i+1}/{num_clips}: {output_filename}")
                
                try:
                    # Use ffmpeg-python to generate the clip
                    (
                        ffmpeg
                        .input(input_path, ss=start_time, t=clip_duration)
                        .output(output_path, c='copy')
                        .run(quiet=True, overwrite_output=True)
                    )
                except ffmpeg.Error as e:
                    print(f"Error creating clip {i+1} from {video_file}: {e}")
            
            print(f"Finished processing {video_file}")
            
        except Exception as e:
            print(f"Error processing {video_file}: {str(e)}")
    
    print("All videos processed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut videos into clips of specified duration")
    parser.add_argument("input_folder", help="Path to folder containing input videos")
    parser.add_argument("output_folder", help="Path to folder where clips will be saved")
    parser.add_argument("--duration", type=int, default=5, help="Duration of each clip in seconds (default: 5)")
    
    args = parser.parse_args()
    
    cut_videos_into_clips(args.input_folder, args.output_folder, args.duration)