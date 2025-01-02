import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import whisper
import ffmpeg
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def extract_audio(video_path, audio_output):
    try:
        ffmpeg.input(video_path).output(audio_output, ac=1, ar='16k').run(overwrite_output=True, quiet=True)
    except ffmpeg.Error as e:
        print(f"Error in audio extraction: {e}")
        raise

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result


from moviepy.config import change_settings, get_setting
print(get_setting("IMAGEMAGICK_BINARY"))
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})  # Replace with your actual path

def generate_subtitles(text, video_path, font_color, whisper_result):
    video = VideoFileClip(video_path)
    audio = video.audio  # Preserve the original audio

    # Create subtitle clips for each segment
    subtitle_clips = []
    for segment in whisper_result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        segment_text = segment["text"]

        subtitle_clip = TextClip(
            segment_text,
            fontsize=24,
            color=font_color,
            method="caption",
            size=(video.size[0], None),
            align="center",
        ).set_start(start_time).set_end(end_time).set_position(("center", "bottom"))

        subtitle_clips.append(subtitle_clip)

    # Combine the video with the subtitle clips
    final_video = CompositeVideoClip([video, *subtitle_clips])
    final_video.audio = audio  # Add the original audio back to the final video

    # Write the final video
    output_path = os.path.splitext(video_path)[0] + "_with_subs.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video.fps, temp_audiofile="temp-audio.m4a",
    remove_temp=True)

    return output_path


def update_status(step_labels, step_index, status_text):
    for i, label in enumerate(step_labels):
        if i < step_index:
            label.config(foreground="green")  # Completed steps
        elif i == step_index:
            label.config(foreground="blue")  # Current step
        else:
            label.config(foreground="black")  # Upcoming steps
    status_text.set(f"Step {step_index + 1} ongoing...")

def main():
    # GUI setup
    root = tk.Tk()
    root.title("Subtitle Adder")
    root.geometry("400x400")

    # Status labels
    step_texts = ["Step 1: Select Video File", "Step 2: Choose Font Color", 
                  "Step 3: Extracting Audio", "Step 4: Transcribing Audio", 
                  "Step 5: Generating Subtitled Video"]
    step_labels = []
    for text in step_texts:
        label = ttk.Label(root, text=text, font=("Arial", 12))
        label.pack(pady=5)
        step_labels.append(label)

    status_text = tk.StringVar()
    status_label = ttk.Label(root, textvariable=status_text, font=("Arial", 12, "bold"))
    status_label.pack(pady=20)

    def run_process():
    # Step 1: Select video
     update_status(step_labels, 0, status_text)
     root.update()
     video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4;*.mov;*.avi")]
     )
     if not video_path:
        messagebox.showerror("Error", "No video file selected!")
        return

    # Step 2: Choose font color
     update_status(step_labels, 1, status_text)
     root.update()
     font_color = None
     color_window = tk.Toplevel(root)
     color_window.title("Choose Font Color")
     ttk.Label(color_window, text="Choose Subtitle Font Color").pack(pady=10)
     color_choice = ttk.Combobox(color_window, values=["white", "black", "yellow", "neon green"])
     color_choice.pack(pady=5)

     def select_color():
        nonlocal font_color
        font_color = color_choice.get()
        color_window.destroy()

     ttk.Button(color_window, text="Select", command=select_color).pack(pady=10)
     color_window.wait_window()

     if not font_color:
        messagebox.showerror("Error", "No font color selected!")
        return

    # Paths
     audio_path = os.path.splitext(video_path)[0] + "_temp_audio.wav"

     try:
        # Step 3: Extract audio
        update_status(step_labels, 2, status_text)
        root.update()
        extract_audio(video_path, audio_path)

        # Step 4: Transcribe audio
        update_status(step_labels, 3, status_text)
        root.update()
        whisper_result = transcribe_audio(audio_path)  # Get the transcription with segments

        # Step 5: Generate subtitled video
        update_status(step_labels, 4, status_text)
        root.update()
        output_video_path = generate_subtitles(whisper_result['text'], video_path, font_color, whisper_result)

        messagebox.showinfo("Success", f"Subtitled video saved at: {output_video_path}")
     except Exception as e:
        messagebox.showerror("Error", str(e))
     finally:
        # Clean up temp audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

    ttk.Button(root, text="Select Video", command=run_process).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
