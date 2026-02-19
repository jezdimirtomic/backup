"""
Backup GUI - Modern CustomTkinter interface
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from backup_engine import BackupEngine
from scheduler import BackupScheduler
import os


class BackupGUI:
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Advanced Backup Tool")
        self.root.geometry("900x700")

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize backend
        self.backup_engine = BackupEngine(progress_callback=self.update_progress)
        self.scheduler = BackupScheduler(self.backup_engine)
        self.backup_thread = None

        # Variables
        self.source_dir = ctk.StringVar()
        self.dest_dir = ctk.StringVar()
        self.include_ext = ctk.StringVar()
        self.exclude_ext = ctk.StringVar()
        self.schedule_enabled = ctk.BooleanVar(value=False)
        self.schedule_type = ctk.StringVar(value="daily")
        self.schedule_time = ctk.StringVar(value="12:00")

        # Build UI
        self.create_widgets()

        # Start scheduler checker
        self.check_scheduler()

    def create_widgets(self):
        """Create all GUI components"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🗄️ Advanced Backup Tool",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Source Directory Section
        source_frame = ctk.CTkFrame(main_frame)
        source_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(source_frame, text="Source Directory:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        source_input_frame = ctk.CTkFrame(source_frame)
        source_input_frame.pack(fill="x", padx=10, pady=(0, 10))

        source_entry = ctk.CTkEntry(source_input_frame, textvariable=self.source_dir, width=500)
        source_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(source_input_frame, text="Browse", command=self.browse_source, width=100).pack(side="left")

        # Destination Directory Section
        dest_frame = ctk.CTkFrame(main_frame)
        dest_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(dest_frame, text="Destination Directory:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        dest_input_frame = ctk.CTkFrame(dest_frame)
        dest_input_frame.pack(fill="x", padx=10, pady=(0, 10))

        dest_entry = ctk.CTkEntry(dest_input_frame, textvariable=self.dest_dir, width=500)
        dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(dest_input_frame, text="Browse", command=self.browse_destination, width=100).pack(side="left")

        # Filter Section
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(filter_frame, text="File Filters:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        # Include extensions
        include_frame = ctk.CTkFrame(filter_frame)
        include_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(include_frame, text="Include Extensions:", width=150).pack(side="left", padx=(0, 5))
        ctk.CTkEntry(include_frame, textvariable=self.include_ext, placeholder_text=".txt, .pdf, .docx").pack(side="left", fill="x", expand=True)

        # Exclude extensions
        exclude_frame = ctk.CTkFrame(filter_frame)
        exclude_frame.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(exclude_frame, text="Exclude Extensions:", width=150).pack(side="left", padx=(0, 5))
        ctk.CTkEntry(exclude_frame, textvariable=self.exclude_ext, placeholder_text=".tmp, .log").pack(side="left", fill="x", expand=True)

        # Scheduling Section
        schedule_frame = ctk.CTkFrame(main_frame)
        schedule_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(schedule_frame, text="Scheduling:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        schedule_toggle_frame = ctk.CTkFrame(schedule_frame)
        schedule_toggle_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkCheckBox(
            schedule_toggle_frame,
            text="Enable Automatic Backup",
            variable=self.schedule_enabled,
            command=self.toggle_schedule
        ).pack(side="left")

        self.schedule_config_frame = ctk.CTkFrame(schedule_frame)
        self.schedule_config_frame.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(self.schedule_config_frame, text="Frequency:", width=100).pack(side="left", padx=(0, 5))

        ctk.CTkRadioButton(
            self.schedule_config_frame,
            text="Daily",
            variable=self.schedule_type,
            value="daily"
        ).pack(side="left", padx=5)

        ctk.CTkRadioButton(
            self.schedule_config_frame,
            text="Weekly",
            variable=self.schedule_type,
            value="weekly"
        ).pack(side="left", padx=5)

        ctk.CTkRadioButton(
            self.schedule_config_frame,
            text="Monthly",
            variable=self.schedule_type,
            value="monthly"
        ).pack(side="left", padx=5)

        ctk.CTkLabel(self.schedule_config_frame, text="Time:", width=50).pack(side="left", padx=(20, 5))
        ctk.CTkEntry(self.schedule_config_frame, textvariable=self.schedule_time, width=80, placeholder_text="HH:MM").pack(side="left")

        self.schedule_config_frame.pack_forget()  # Hidden by default

        # Progress Section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(progress_frame, text="Progress:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=800)
        self.progress_bar.pack(padx=10, pady=5)
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready to backup", font=ctk.CTkFont(size=12))
        self.progress_label.pack(padx=10, pady=(0, 10))

        # Action Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)

        self.backup_button = ctk.CTkButton(
            button_frame,
            text="Start Backup",
            command=self.start_backup,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.backup_button.pack(side="left", padx=(10, 5))

        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel_backup,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.cancel_button.pack(side="left", padx=5)

        # Log/Status Section
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=5)

        ctk.CTkLabel(log_frame, text="Status Log:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self.log_text = ctk.CTkTextbox(log_frame, width=800, height=150)
        self.log_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    def toggle_schedule(self):
        """Toggle schedule configuration visibility"""
        if self.schedule_enabled.get():
            self.schedule_config_frame.pack(fill="x", padx=10, pady=(5, 10))
        else:
            self.schedule_config_frame.pack_forget()

    def browse_source(self):
        """Browse for source directory"""
        directory = filedialog.askdirectory(title="Select Source Directory")
        if directory:
            self.source_dir.set(directory)

    def browse_destination(self):
        """Browse for destination directory"""
        directory = filedialog.askdirectory(title="Select Destination Directory")
        if directory:
            self.dest_dir.set(directory)

    def parse_extensions(self, ext_string: str):
        """Parse comma-separated extension string"""
        if not ext_string.strip():
            return []

        extensions = [ext.strip() for ext in ext_string.split(",")]
        # Ensure all extensions start with a dot
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        return extensions

    def log(self, message: str):
        """Add message to log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def update_progress(self, current: int, total: int, filename: str):
        """Update progress bar and label"""
        progress = current / total if total > 0 else 0
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"Backing up: {filename} ({current}/{total})")
        self.root.update_idletasks()

    def perform_backup(self):
        """Perform backup operation (runs in separate thread)"""
        try:
            # Get parameters
            source = self.source_dir.get()
            destination = self.dest_dir.get()
            include_ext = self.parse_extensions(self.include_ext.get())
            exclude_ext = self.parse_extensions(self.exclude_ext.get())

            # Validate
            if not source or not destination:
                self.log("❌ Error: Please select both source and destination directories")
                return

            # Log start
            self.log(f"🚀 Starting backup from {source} to {destination}")
            if include_ext:
                self.log(f"   Including: {', '.join(include_ext)}")
            if exclude_ext:
                self.log(f"   Excluding: {', '.join(exclude_ext)}")

            # Perform backup
            result = self.backup_engine.backup(
                source_dir=source,
                destination_dir=destination,
                include_extensions=include_ext,
                exclude_extensions=exclude_ext
            )

            # Show result
            if result["success"]:
                self.log(f"✅ Backup completed successfully!")
                self.log(f"   Files copied: {result['copied']}")
                self.log(f"   Files skipped: {result['skipped']}")
                self.log(f"   Timestamp: {result['timestamp']}")

                if result.get('errors'):
                    self.log(f"   Errors: {len(result['errors'])}")

                messagebox.showinfo("Success", f"Backup completed!\n\nCopied: {result['copied']} files\nSkipped: {result['skipped']} files")
            else:
                self.log(f"❌ Backup failed: {result['error']}")
                messagebox.showerror("Error", f"Backup failed:\n{result['error']}")

        except Exception as e:
            self.log(f"❌ Exception: {e}")
            messagebox.showerror("Error", f"An error occurred:\n{e}")

        finally:
            # Reset UI
            self.progress_bar.set(0)
            self.progress_label.configure(text="Ready to backup")
            self.backup_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")

    def start_backup(self):
        """Start backup in separate thread"""
        self.backup_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")

        self.backup_thread = threading.Thread(target=self.perform_backup, daemon=True)
        self.backup_thread.start()

        # Setup scheduling if enabled
        if self.schedule_enabled.get():
            self.setup_schedule()

    def cancel_backup(self):
        """Cancel ongoing backup"""
        self.backup_engine.cancel()
        self.log("⚠️ Backup cancelled by user")
        self.cancel_button.configure(state="disabled")

    def setup_schedule(self):
        """Setup scheduled backups"""
        schedule_type = self.schedule_type.get()
        schedule_time = self.schedule_time.get()

        # Get backup parameters
        source = self.source_dir.get()
        destination = self.dest_dir.get()
        include_ext = self.parse_extensions(self.include_ext.get())
        exclude_ext = self.parse_extensions(self.exclude_ext.get())

        # Setup schedule
        self.scheduler.schedule_backup(
            schedule_type=schedule_type,
            time_str=schedule_time,
            source_dir=source,
            destination_dir=destination,
            include_extensions=include_ext,
            exclude_extensions=exclude_ext
        )

        self.log(f"⏰ Scheduled {schedule_type} backup at {schedule_time}")

    def check_scheduler(self):
        """Check and run pending scheduled tasks"""
        self.scheduler.run_pending()
        self.root.after(1000, self.check_scheduler)  # Check every second

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = BackupGUI()
    app.run()
