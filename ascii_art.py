from PIL import Image
import numpy as np
import os
import cv2
from time import sleep

density = " `.-'_,^=:;><+!rc*/z?sLTv#$itbg0BMNWQ%&@"

def FrameCapture(path, max_frames, directory): 
    vidObj = cv2.VideoCapture(path) 
    count = 0
    success, image = vidObj.read()

    for count in range(max_frames):
        if not success:
            break
        cv2.imwrite(f"{directory}/frame{count}.jpg", image) 
        success, image = vidObj.read()

    vidObj.release()

def get_image_data(filename):
    img = Image.open(filename).convert('L')  # Convert image to grayscale
    terminal_size = os.get_terminal_size()
    new_width = terminal_size.columns
    new_height = terminal_size.lines
    img = img.resize((new_width, new_height))
    return np.asarray(img).tolist()

def render_ascii_img(filename):
    img_data = get_image_data(filename)
    density_len = len(density)
    return [[density[int((pixel / 255) * (density_len - 1))] for pixel in row] for row in img_data]

def render_ascii_video(filename_list):
    ascii_video = []
    for i in range(len(filename_list)):
        # print(f"Progress: {int(i / len(filename_list)) * 100 }%", end="\r", flush=True) this doesn't work
        filename = filename_list[i]
        ascii_video.append(render_ascii_img(filename))
    return ascii_video

def play_rendered_ascii_video(filename_list, sleep_secs):
    video = render_ascii_video(filename_list=filename_list)
    for frame in video:
        for row in frame:
            print("".join(row))
        sleep(sleep_secs)

def play_rendered_ascii_video_frame_by_frame(filename_list, sleep_secs):
    video = render_ascii_video(filename_list=filename_list)
    for frame in video:
        asci_frame = "\n".join( ["".join(row) for row in frame] )
        print(asci_frame)
        sleep(sleep_secs)

def play_ascii_video_no_render(filename_list, sleep_sec):
    density_len = len(density)
    clear_command = "cls" if os.name == "nt" else "clear"
    for filename in filename_list:
        os.system(clear_command)
        img_data = get_image_data(filename)
        for row in img_data:
            print("".join([density[int((col / 255) * (density_len - 1))] for col in row]))
        sleep(sleep_sec)

def get_filenames(direc):
    content = os.listdir(direc)
    return [os.path.join(direc, f) for f in content if os.path.isfile(os.path.join(direc, f)) and f.split(".")[-1].lower() in ["jpg", "jpeg", "bmp", "png"]]

def main():
    frames_directory = "frames"
    video_file = "C:/Users/DELL/Desktop/me_at_zoo.mp4" if os.name == 'nt' else "/mnt/c/Users/DELL/Desktop/me_at_zoo.mp4"
    
    if not os.path.isdir(frames_directory):
        os.makedirs(frames_directory)
    
    # Extract frames
    FrameCapture(video_file, 1000, frames_directory)
    
    # Get filename list
    filenames = get_filenames(frames_directory)

    # Play video (uncomment only one at a time):

    play_ascii_video_no_render(filenames, 1/60)
    # play_rendered_ascii_video(filenames, 1/60)
    # play_rendered_ascii_video_frame_by_frame(filenames, 1/30)

if __name__ == "__main__":
    main()
