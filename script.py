import os
import yt_dlp
import subprocess

def download_video(url, output_dir):
    # yt-dlp options for downloading the best quality video
    ydl_opts = {
        'format': 'best',  # best video format
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Save with video title in the output directory
        'quiet': True,  # make it verbose for debugging
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        # Return the video title and the downloaded path
        return result['title'], os.path.join(output_dir, f"{result['title']}.mp4")

def convert_to_webm(input_video_path, output_dir):
    # Define output path for the WebM file
    output_webm_path = os.path.join(output_dir, os.path.basename(input_video_path).replace('.mp4', '.webm'))

    # Path to the bundled ffmpeg executable
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg.exe')

    # ffmpeg command to convert to webm
    command = [
        ffmpeg_path, '-i', input_video_path,  # Input video file
        '-c:v', 'libvpx', '-crf', '10', '-b:v', '1M',  # Video codec settings for webm
        '-an',  # No audio
        output_webm_path  # Output path
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Conversion complete: {output_webm_path}")
        os.remove(input_video_path)  # Optionally remove the original video
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def main():
    # Save the current working directory (where the script is run from)
    script_folder = os.getcwd()

    # Loop to continuously ask for YouTube URL and process the video
    while True:
        # Prompt the user for the YouTube URL
        youtube_url = input("Enter a YouTube URL (or 'exit' to quit): ").strip()
        
        # If the user types 'exit', break the loop and stop
        if youtube_url.lower() == 'exit':
            print("Exiting program.")
            break

        # Download the video
        print("Downloading video...")
        video_title, downloaded_video_path = download_video(youtube_url, script_folder)
        
        print(f"Video downloaded: {downloaded_video_path}")

        # Convert the downloaded video to webm
        print("Converting to webm...")
        convert_to_webm(downloaded_video_path, script_folder)
        
        print(f"Video converted and saved as: {os.path.basename(downloaded_video_path).replace('.mp4', '.webm')}")
        
        # Ask again for the next video
        print("\n---\n")

if __name__ == "__main__":
    main()
