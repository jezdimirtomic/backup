"""
Backup Engine - Core backup functionality with filtering
"""
import os
import shutil
from pathlib import Path
from typing import List, Callable, Optional
from datetime import datetime


class BackupEngine:
    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        Initialize backup engine

        Args:
            progress_callback: Function to call with progress updates (current, total, filename)
        """
        self.progress_callback = progress_callback
        self.cancelled = False

    def cancel(self):
        """Cancel the ongoing backup operation"""
        self.cancelled = True

    def reset_cancel(self):
        """Reset cancel flag for new operation"""
        self.cancelled = False

    def should_include_file(self, file_path: str, include_extensions: List[str],
                           exclude_extensions: List[str]) -> bool:
        """
        Determine if file should be included based on extension filters

        Args:
            file_path: Path to the file
            include_extensions: List of extensions to include (e.g., ['.txt', '.pdf'])
            exclude_extensions: List of extensions to exclude

        Returns:
            True if file should be included, False otherwise
        """
        file_ext = Path(file_path).suffix.lower()

        # If exclude list has this extension, skip it
        if exclude_extensions and file_ext in [ext.lower() for ext in exclude_extensions]:
            return False

        # If include list is empty, include all (except excluded)
        if not include_extensions:
            return True

        # If include list exists, only include matching extensions
        return file_ext in [ext.lower() for ext in include_extensions]

    def count_files(self, source_dir: str, include_extensions: List[str],
                   exclude_extensions: List[str]) -> int:
        """
        Count total files to be backed up

        Args:
            source_dir: Source directory path
            include_extensions: Extensions to include
            exclude_extensions: Extensions to exclude

        Returns:
            Total number of files to backup
        """
        total = 0
        try:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.should_include_file(file_path, include_extensions, exclude_extensions):
                        total += 1
        except Exception as e:
            print(f"Error counting files: {e}")
        return total

    def backup(self, source_dir: str, destination_dir: str,
              include_extensions: List[str] = None,
              exclude_extensions: List[str] = None) -> dict:
        """
        Perform backup operation with filtering

        Args:
            source_dir: Source directory to backup
            destination_dir: Destination directory for backup
            include_extensions: List of file extensions to include (None = all)
            exclude_extensions: List of file extensions to exclude

        Returns:
            Dictionary with backup statistics
        """
        self.reset_cancel()

        include_extensions = include_extensions or []
        exclude_extensions = exclude_extensions or []

        # Validate directories
        if not os.path.exists(source_dir):
            return {"success": False, "error": "Source directory does not exist"}

        # Create destination if it doesn't exist
        try:
            os.makedirs(destination_dir, exist_ok=True)
        except Exception as e:
            return {"success": False, "error": f"Cannot create destination directory: {e}"}

        # Count total files first
        total_files = self.count_files(source_dir, include_extensions, exclude_extensions)

        if total_files == 0:
            return {"success": False, "error": "No files match the filter criteria"}

        # Perform backup
        copied_files = 0
        skipped_files = 0
        errors = []

        try:
            for root, dirs, files in os.walk(source_dir):
                if self.cancelled:
                    return {
                        "success": False,
                        "error": "Backup cancelled by user",
                        "copied": copied_files,
                        "skipped": skipped_files
                    }

                for file in files:
                    source_file = os.path.join(root, file)

                    # Check if file matches filter
                    if not self.should_include_file(source_file, include_extensions, exclude_extensions):
                        skipped_files += 1
                        continue

                    # Calculate relative path and destination
                    rel_path = os.path.relpath(source_file, source_dir)
                    dest_file = os.path.join(destination_dir, rel_path)

                    # Create destination subdirectories
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                    # Copy file
                    try:
                        shutil.copy2(source_file, dest_file)
                        copied_files += 1

                        # Report progress
                        if self.progress_callback:
                            self.progress_callback(copied_files, total_files, file)

                    except Exception as e:
                        errors.append(f"Failed to copy {source_file}: {e}")
                        skipped_files += 1

        except Exception as e:
            return {
                "success": False,
                "error": f"Backup failed: {e}",
                "copied": copied_files,
                "skipped": skipped_files
            }

        # Generate report
        result = {
            "success": True,
            "copied": copied_files,
            "skipped": skipped_files,
            "total": total_files,
            "errors": errors,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return result
