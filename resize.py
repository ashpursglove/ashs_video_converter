
import sys
import os
import re
import subprocess

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QProgressBar,
    QPlainTextEdit,
)
from PyQt5.QtCore import Qt, QProcess


class VideoConverterGUI(QMainWindow):
    """
    Ash's Video Converter

    Features
    --------
    - Accepts (almost) any input video format supported by FFmpeg.
    - Lets the user choose:
        * Input file
        * Output resolution (scaled using FFmpeg's scale filter)
        * Output container format (mp4, mkv, mov, avi, webm)
        * Output file name (without extension)
    - Runs FFmpeg through QProcess so the GUI stays responsive.
    - Shows progress bar (based on ffprobe duration + ffmpeg stderr "time=" lines).
    - Shows a scrolling log of FFmpeg output.
    """

    def __init__(self):
        super().__init__()
        self.process: QProcess | None = None
        self.total_duration_seconds: float | None = None
        self.initUI()

    def initUI(self):
        # Window title and geometry
        self.setWindowTitle("Ash's Video Converter")
        self.setGeometry(200, 200, 650, 420)

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # -----------------------------
        # File selection row
        # -----------------------------
        file_title_label = QLabel("Input video file:")
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet("color: #9aa3b5;")
        self.file_path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.browse_button = QPushButton("Browse…")
        self.browse_button.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_label, stretch=1)
        file_layout.addWidget(self.browse_button, stretch=0)

        main_layout.addWidget(file_title_label)
        main_layout.addLayout(file_layout)

        # -----------------------------
        # Resolution selection
        # -----------------------------
        resolution_label = QLabel("Output resolution:")
        self.resolution_dropdown = QComboBox()
        self.resolution_dropdown.addItems(
            [
                "1920x1080 (Full HD)",
                "1280x720 (HD)",
                "854x480 (SD)",
                "640x360 (Low)",
                "426x240 (Very Low)",
            ]
        )

        main_layout.addWidget(resolution_label)
        main_layout.addWidget(self.resolution_dropdown)

        # -----------------------------
        # Output format + file name
        # -----------------------------
        format_label = QLabel("Output format (container):")
        self.format_dropdown = QComboBox()
        # Common containers that work well with H.264
        self.format_dropdown.addItems(["mp4", "mkv", "mov", "avi", "webm"])

        main_layout.addWidget(format_label)
        main_layout.addWidget(self.format_dropdown)

        output_name_label = QLabel("Output file name (without extension):")
        self.output_name_edit = QLineEdit()
        self.output_name_edit.setPlaceholderText("Leave blank to auto-generate")

        main_layout.addWidget(output_name_label)
        main_layout.addWidget(self.output_name_edit)

        # -----------------------------
        # Convert button
        # -----------------------------
        self.convert_button = QPushButton("Convert")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.convert_video)
        main_layout.addWidget(self.convert_button, alignment=Qt.AlignHCenter)

        # -----------------------------
        # Progress + status
        # -----------------------------
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.status_label = QLabel("Ready.")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignLeft)

        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)

        # -----------------------------
        # Log window (FFmpeg output)
        # -----------------------------
        log_label = QLabel("Conversion log:")
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumBlockCount(5000)

        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_output, stretch=1)

        # Finalise layout
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply dark blue theme
        self.apply_dark_blue_theme()

    # ------------------------------------------------------------------
    # Theming
    # ------------------------------------------------------------------
    def apply_dark_blue_theme(self):
        """
        Apply a dark blue theme similar to the style you've been using:
        - Dark navy backgrounds
        - Soft borders and subtle hover effects
        - High-contrast text for readability
        """
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #050b15;
            }
            QWidget {
                background-color: #050b15;
                color: #e0e4f0;
                font-family: "Segoe UI", "Roboto", Arial;
                font-size: 10pt;
            }
            QLabel {
                color: #e0e4f0;
            }
            QLabel#statusLabel {
                color: #9ad29a;
                font-weight: 500;
            }
            QPushButton {
                background-color: #1b3458;
                border: 1px solid #264670;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #25446f;
            }
            QPushButton:pressed {
                background-color: #182b44;
            }
            QPushButton:disabled {
                background-color: #262c3c;
                color: #7a8294;
                border: 1px solid #1d2330;
            }
            QComboBox, QLineEdit {
                background-color: #0b1324;
                border: 1px solid #2b3c5a;
                border-radius: 3px;
                padding: 4px 8px;
                selection-background-color: #2b6bbd;
                selection-color: #ffffff;
            }
            QComboBox::drop-down {
                background-color: #1b3458;
                width: 20px;
                border-left: 1px solid #2b3c5a;
            }
            QComboBox QAbstractItemView {
                background-color: #050b15;
                selection-background-color: #2b6bbd;
                selection-color: #ffffff;
            }
            QProgressBar {
                background-color: #0b1324;
                border: 1px solid #2b3c5a;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2b6bbd;
                margin: 0px;
            }
            QPlainTextEdit {
                background-color: #050b15;
                border: 1px solid #2b3c5a;
                border-radius: 3px;
                color: #c7ccdd;
            }
            """
        )

    # ------------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------------
    def browse_file(self):
        """
        Let the user select a video file.
        We accept most common containers; FFmpeg will handle the rest.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mov *.mp4 *.mkv *.avi *.wmv *.flv *.m4v *.webm);;All Files (*)",
            options=options,
        )

        if file_path:
            self.file_path_label.setText(file_path)
            self.file_path_label.setStyleSheet("color: #e0e4f0;")
            self.convert_button.setEnabled(True)

            # Auto-suggest an output base name
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            self.output_name_edit.setText(f"{base_name}_converted")

            self.status_label.setText("Ready to convert.")
            self.status_label.setStyleSheet("")  # keep theme styling
        else:
            self.file_path_label.setText("No file selected")
            self.file_path_label.setStyleSheet("color: #9aa3b5;")
            self.convert_button.setEnabled(False)
            self.status_label.setText("Please select an input file.")

    # ------------------------------------------------------------------
    # Conversion helpers
    # ------------------------------------------------------------------
    def get_total_duration(self, input_file: str) -> float | None:
        """
        Use ffprobe to find the total duration of the input video in seconds.
        Returns None if ffprobe fails for any reason.
        """
        try:
            # ffprobe command: returns duration in seconds (float)
            cmd = [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nokey=1:noprint_wrappers=1",
                input_file,
            ]
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            duration_str = output.decode("utf-8").strip()
            duration = float(duration_str)
            return duration
        except Exception as e:
            # If ffprobe not available or fails, we just won't show percentage progress
            self.append_log(f"[ffprobe] Unable to determine duration: {e}")
            return None

    def parse_time_from_ffmpeg_output(self, text: str) -> float | None:
        """
        Parse a 'time=HH:MM:SS.xx' pattern from FFmpeg stderr output and
        return the time in seconds. Returns None if no match.
        """
        match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", text)
        if not match:
            return None

        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = float(match.group(3))
        return hours * 3600 + minutes * 60 + seconds

    def append_log(self, text: str):
        """
        Append a line to the log window, scrolling to the bottom.
        """
        self.log_output.appendPlainText(text)
        cursor = self.log_output.textCursor()
        cursor.movePosition(cursor.End)
        self.log_output.setTextCursor(cursor)

    # ------------------------------------------------------------------
    # Conversion start
    # ------------------------------------------------------------------
    def convert_video(self):
        """
        Start the conversion process using QProcess and FFmpeg.
        """
        input_file = self.file_path_label.text()
        if not input_file or input_file == "No file selected":
            self.status_label.setText("No input file selected.")
            return

        input_file = input_file.strip('"')

        # Extract resolution
        resolution_text = self.resolution_dropdown.currentText()
        resolution = resolution_text.split(" (")[0]  # "1920x1080 (Full HD)" -> "1920x1080"

        # Output format
        output_format = self.format_dropdown.currentText().lower()

        # Base name & directory
        directory = os.path.dirname(input_file)
        base_name_text = self.output_name_edit.text().strip()

        if not base_name_text:
            base_name_text = os.path.splitext(os.path.basename(input_file))[0] + "_converted"

        output_file = os.path.join(directory, f"{base_name_text}.{output_format}")

        # Clear log and reset progress
        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Preparing conversion...")
        self.status_label.setStyleSheet("")  # keep global style

        # Disable controls while converting
        self.convert_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.resolution_dropdown.setEnabled(False)
        self.format_dropdown.setEnabled(False)
        self.output_name_edit.setEnabled(False)

        # Get total duration for progress calculation (if possible)
        self.total_duration_seconds = self.get_total_duration(input_file)

        # Build FFmpeg command
        # We standardize on H.264 video; this works well for mp4/mkv/mov/webm (webm can also handle H.264 nowadays).
        ffmpeg_args = [
            "-y",  # overwrite output without asking
            "-i",
            input_file,
            "-vf",
            f"scale={resolution}",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_file,
        ]

        self.append_log("Starting FFmpeg with arguments:")
        self.append_log("ffmpeg " + " ".join(f'"{a}"' if " " in a else a for a in ffmpeg_args))

        # Run FFmpeg via QProcess
        self.process = QProcess(self)
        self.process.setProgram("ffmpeg")
        self.process.setArguments(ffmpeg_args)

        # Connect signals
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.handle_finished)
        self.process.errorOccurred.connect(self.handle_error)

        # Start process
        self.process.start()
        self.status_label.setText("Converting…")

    # ------------------------------------------------------------------
    # QProcess signal handlers
    # ------------------------------------------------------------------
    def handle_stdout(self):
        """
        Read standard output from FFmpeg (rarely used, but we log it anyway).
        """
        if not self.process:
            return
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if data.strip():
            for line in data.strip().splitlines():
                self.append_log(line)

    def handle_stderr(self):
        """
        Read FFmpeg stderr and update progress / log.
        FFmpeg writes progress info (including 'time=') to stderr.
        """
        if not self.process:
            return
        data = self.process.readAllStandardError().data().decode("utf-8", errors="replace")
        if data.strip():
            for line in data.strip().splitlines():
                self.append_log(line)

        # Try to extract current time and update progress bar
        if self.total_duration_seconds:
            current_time = self.parse_time_from_ffmpeg_output(data)
            if current_time is not None:
                progress = int((current_time / self.total_duration_seconds) * 100)
                progress = max(0, min(100, progress))
                self.progress_bar.setValue(progress)

    def handle_finished(self, exit_code: int, exit_status: QProcess.ExitStatus):
        """
        Called when FFmpeg finishes (successfully or not).
        """
        # Re-enable controls
        self.convert_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.resolution_dropdown.setEnabled(True)
        self.format_dropdown.setEnabled(True)
        self.output_name_edit.setEnabled(True)

        if exit_status == QProcess.NormalExit and exit_code == 0:
            self.progress_bar.setValue(100)
            self.status_label.setText("Conversion completed successfully.")
            self.append_log("Conversion completed successfully.")
        else:
            self.status_label.setText("Error: Conversion failed.")
            # Make the status text red while keeping theme otherwise
            self.status_label.setStyleSheet("color: #ff6b6b;")
            self.append_log(f"FFmpeg exited with code {exit_code}, status {exit_status}.")

        self.process = None

    def handle_error(self, process_error: QProcess.ProcessError):
        """
        Called when QProcess encounters an error (e.g., FFmpeg not found).
        """
        # Re-enable controls
        self.convert_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.resolution_dropdown.setEnabled(True)
        self.format_dropdown.setEnabled(True)
        self.output_name_edit.setEnabled(True)

        self.status_label.setText("Error: Could not start FFmpeg.")
        self.status_label.setStyleSheet("color: #ff6b6b;")
        self.append_log(f"QProcess error: {process_error}")
        self.process = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = VideoConverterGUI()
    converter.show()
    sys.exit(app.exec_())
