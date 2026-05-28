import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading

from make_furigana_video import load_config, build_ass_from_srt, burn_subtitles


def run_job():
    video = video_var.get().strip()
    srt = srt_var.get().strip()

    if not video or not srt:
        messagebox.showerror("Missing files", "Please choose both a video file and an SRT file.")
        return

    video_path = Path(video)
    srt_path = Path(srt)

    if not video_path.exists():
        messagebox.showerror("Video not found", video)
        return

    if not srt_path.exists():
        messagebox.showerror("SRT not found", srt)
        return

    run_button.config(state="disabled")
    status_var.set("Working... creating furigana subtitles and rendering video.")

    def worker():
        try:
            config = load_config(Path("config.json"))

            ass_path = srt_path.with_name(config["output_ass_name"])
            output_path = video_path.with_name(
                video_path.stem + config["output_video_suffix"] + video_path.suffix
            )

            build_ass_from_srt(srt_path, ass_path, config)
            burn_subtitles(video_path, ass_path, output_path)

            status_var.set(f"Done! Created: {output_path.name}")
            messagebox.showinfo("Done", f"Finished!\n\nCreated:\n{output_path}")

        except Exception as e:
            status_var.set("Error")
            messagebox.showerror("Something went wrong", str(e))

        finally:
            run_button.config(state="normal")

    threading.Thread(target=worker, daemon=True).start()


def choose_video():
    path = filedialog.askopenfilename(
        title="Choose video file",
        filetypes=[("Video files", "*.mp4 *.mkv *.mov"), ("All files", "*.*")]
    )
    if path:
        video_var.set(path)


def choose_srt():
    path = filedialog.askopenfilename(
        title="Choose subtitle file",
        filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
    )
    if path:
        srt_var.set(path)


root = tk.Tk()
root.title("Furigana Assist")
root.geometry("620x260")
root.resizable(False, False)

video_var = tk.StringVar()
srt_var = tk.StringVar()
status_var = tk.StringVar(value="Choose a video and SRT file, then click Create Video.")

tk.Label(root, text="Furigana Assist", font=("Yu Gothic", 18, "bold")).pack(pady=(18, 8))

frame = tk.Frame(root)
frame.pack(padx=20, pady=10, fill="x")

tk.Label(frame, text="Video file:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=video_var, width=58).grid(row=1, column=0, padx=(0, 8), pady=(2, 10))
tk.Button(frame, text="Browse", command=choose_video).grid(row=1, column=1, pady=(2, 10))

tk.Label(frame, text="SRT subtitle file:").grid(row=2, column=0, sticky="w")
tk.Entry(frame, textvariable=srt_var, width=58).grid(row=3, column=0, padx=(0, 8), pady=(2, 10))
tk.Button(frame, text="Browse", command=choose_srt).grid(row=3, column=1, pady=(2, 10))

run_button = tk.Button(root, text="Create Furigana Video", command=run_job, height=2, width=28)
run_button.pack(pady=8)

tk.Label(root, textvariable=status_var, wraplength=560).pack(pady=(6, 0))

root.mainloop()
