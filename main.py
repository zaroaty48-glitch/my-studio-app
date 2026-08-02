import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess, os, threading

def run_ffmpeg(cmd, progress_label, process_button):
    progress_label.config(text="⏳ Processing...", fg="#f39c12")
    process_button.config(state="disabled")
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            progress_label.config(text="✅ Finished!", fg="#2ecc71")
            messagebox.showinfo("Success", "Video exported successfully!")
        else:
            progress_label.config(text="❌ Error", fg="#e74c3c")
            messagebox.showerror("Error", res.stderr[-200:])
    except Exception as e:
        progress_label.config(text="❌ Failed", fg="#e74c3c")
        messagebox.showerror("Error", str(e))
    finally:
        process_button.config(state="normal")

def select_input():
    fn = filedialog.askopenfilename(initialdir="/sdcard/Download", title="Select Video")
    if fn:
        input_var.set(fn)
        b, e = os.path.splitext(fn)
        output_var.set(f"{b}_edited{e}")

def apply_canvas_blur():
    if not input_var.get():
        messagebox.showwarning("Warning", "Select input video first!")
        return
    cmd = [
        'ffmpeg', '-i', os.path.abspath(input_var.get()),
        '-vf', "split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=20[bg];[b]scale=1080:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2",
        '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
        os.path.abspath(output_var.get()), '-y'
    ]
    threading.Thread(target=run_ffmpeg, args=(cmd, progress_label, btn_blur), daemon=True).start()

def apply_trim():
    if not input_var.get():
        messagebox.showwarning("Warning", "Select input video first!")
        return
    start = start_var.get().strip() or "00:00:00"
    duration = duration_var.get().strip() or "10"
    cmd = [
        'ffmpeg', '-ss', start, '-i', os.path.abspath(input_var.get()),
        '-t', duration, '-c', 'copy',
        os.path.abspath(output_var.get()), '-y'
    ]
    threading.Thread(target=run_ffmpeg, args=(cmd, progress_label, btn_trim), daemon=True).start()

def apply_4k_filter():
    if not input_var.get():
        messagebox.showwarning("Warning", "Select input video first!")
        return
    filter_chain = "unsharp=5:5:1.0:5:5:0.0,eq=contrast=1.15:saturation=1.2:brightness=0.02"
    cmd = [
        'ffmpeg', '-i', os.path.abspath(input_var.get()),
        '-vf', filter_chain,
        '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
        '-c:a', 'copy',
        os.path.abspath(output_var.get()), '-y'
    ]
    threading.Thread(target=run_ffmpeg, args=(cmd, progress_label, btn_4k), daemon=True).start()

root = tk.Tk()
root.title("My Studio Pro")
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{sw}x{sh}+0+0")
root.configure(bg='#0f172a')

input_var, output_var = tk.StringVar(), tk.StringVar()
start_var, duration_var = tk.StringVar(value="00:00:00"), tk.StringVar(value="10")

tk.Label(root, text="🎬 My Studio Pro", font=("Arial", 18, "bold"), bg='#0f172a', fg='#38bdf8').pack(pady=15)
tk.Label(root, text="Source Video:", bg='#0f172a', fg='#94a3b8').pack()
tk.Entry(root, textvariable=input_var, width=32).pack(pady=4)
tk.Button(root, text="📁 Select Video", command=select_input, bg='#3b82f6', fg='white', font=("Arial", 10, "bold")).pack(pady=6)

tk.Label(root, text="Output Path:", bg='#0f172a', fg='#94a3b8').pack()
tk.Entry(root, textvariable=output_var, width=32).pack(pady=4)

tk.Frame(root, height=2, bg="#334155").pack(fill="x", pady=10)

tk.Label(root, text="✂️ Trim Options:", font=("Arial", 11, "bold"), bg='#0f172a', fg='#e2e8f0').pack(pady=2)
frame_trim = tk.Frame(root, bg='#0f172a')
frame_trim.pack(pady=3)

tk.Label(frame_trim, text="Start:", bg='#0f172a', fg='white').grid(row=0, column=0, padx=5)
tk.Entry(frame_trim, textvariable=start_var, width=10).grid(row=0, column=1, padx=5)
tk.Label(frame_trim, text="Duration (s):", bg='#0f172a', fg='white').grid(row=1, column=0, padx=5, pady=5)
tk.Entry(frame_trim, textvariable=duration_var, width=10).grid(row=1, column=1, padx=5, pady=5)

btn_blur = tk.Button(root, text="✨ Canvas Blur (Reels)", command=apply_canvas_blur, bg="#10b981", fg="white", font=("Arial", 11, "bold"), padx=10, pady=4)
btn_blur.pack(pady=5)

btn_trim = tk.Button(root, text="✂️ Cut Video", command=apply_trim, bg="#f59e0b", fg="white", font=("Arial", 11, "bold"), padx=10, pady=4)
btn_trim.pack(pady=5)

btn_4k = tk.Button(root, text="💎 Apply 4K / Sharp Filter", command=apply_4k_filter, bg="#8b5cf6", fg="white", font=("Arial", 11, "bold"), padx=10, pady=4)
btn_4k.pack(pady=5)

progress_label = tk.Label(root, text="", bg='#0f172a', fg='white', font=("Arial", 11, "bold"))
progress_label.pack(pady=10)

root.mainloop()
