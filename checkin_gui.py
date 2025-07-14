import tkinter as tk
from tkinter import ttk, messagebox
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from gpt_client import GPTClient
from audio_manager import AudioManager

class CheckInApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daily AI Check-In")
        self.geometry("600x500")

        # Initialize GPT and Audio managers
        self.gpt = GPTClient()
        self.audio = AudioManager()

        # Scheduler setup
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler_job = None

        # --- Schedule Frame ---
        sched_frame = ttk.LabelFrame(self, text="Schedule Settings")
        sched_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(sched_frame, text="Call Time (24h HH:MM):").grid(row=0, column=0, padx=5, pady=5)
        self.hour_var = tk.StringVar(value="08")
        hour_spin = ttk.Spinbox(sched_frame, from_=0, to=23, width=3, textvariable=self.hour_var, format="%02.0f")
        hour_spin.grid(row=0, column=1, pady=5)
        ttk.Label(sched_frame, text=":").grid(row=0, column=2)
        self.minute_var = tk.StringVar(value="00")
        minute_spin = ttk.Spinbox(sched_frame, from_=0, to=59, width=3, textvariable=self.minute_var, format="%02.0f")
        minute_spin.grid(row=0, column=3, pady=5)

        ttk.Label(sched_frame, text="Voice:").grid(row=1, column=0, padx=5, pady=5)
        # Use a default list of voices until AudioManager implements list_voices()
        self.voice_choice = ttk.Combobox(sched_frame, values=self.audio.list_voices(), state="readonly")
        self.voice_choice.current(0)
        self.voice_choice.grid(row=1, column=1, columnspan=3, sticky="ew", pady=5)

        self.test_button = ttk.Button(sched_frame, text="Test Call Now", command=self.test_call)
        self.test_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.start_button = ttk.Button(sched_frame, text="Start Schedule", command=self.start_schedule)
        self.start_button.grid(row=2, column=2, padx=5, pady=10)
        self.stop_button = ttk.Button(sched_frame, text="Stop Schedule", command=self.stop_schedule, state="disabled")
        self.stop_button.grid(row=2, column=3, padx=5, pady=10)

        # --- Transcript Frame ---
        trans_frame = ttk.LabelFrame(self, text="Conversation Transcript")
        trans_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.transcript_text = tk.Text(trans_frame, wrap="word", height=15, state="disabled")
        self.transcript_text.pack(fill="both", expand=True, padx=5, pady=5)

    def append_transcript(self, speaker: str, message: str):
        self.transcript_text.config(state="normal")
        self.transcript_text.insert("end", f"{speaker}: {message}\n")
        self.transcript_text.see("end")
        self.transcript_text.config(state="disabled")

    def test_call(self):
        # Generate dynamic prompt
        date_str = datetime.now().strftime('%Y-%m-%d')
        script = self.gpt.generate_checkin_script(date_str)
        # Display in transcript
        self.append_transcript("AI", script)
        # Convert to speech
        voice = self.voice_choice.get()
        audio_file = self.audio.text_to_speech(script, voice)
        # Play audio
        self.audio.play_audio(audio_file)
        # After playback, listen and continue conversation
        user_reply = self.audio.record_and_transcribe()
        self.append_transcript("You", user_reply)
        # Generate follow-up
        follow_up = self.gpt.generate_followup(script, user_reply)
        self.append_transcript("AI", follow_up)
        audio_file2 = self.audio.text_to_speech(follow_up, voice)
        self.audio.play_audio(audio_file2)

    def _scheduled_call(self):
        """Internal wrapper to call test_call from scheduler."""
        self.test_call()

    def start_schedule(self):
        # Parse time from GUI
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        # Schedule daily job
        if self.scheduler_job:
            self.scheduler.remove_job(self.scheduler_job.id)
        self.scheduler_job = self.scheduler.add_job(
            self._scheduled_call,
            'cron',
            hour=hour,
            minute=minute,
            id='daily_call'
        )
        time_str = f"{hour:02d}:{minute:02d}"
        messagebox.showinfo("Schedule", f"Daily call scheduled at {time_str}")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_schedule(self):
        if self.scheduler_job:
            self.scheduler.remove_job(self.scheduler_job.id)
            self.scheduler_job = None
        messagebox.showinfo("Schedule", "Scheduled calls stopped.")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    app = CheckInApp()
    app.mainloop()
