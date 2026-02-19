"""
Scheduler - Handles scheduled backup operations
"""
import schedule
import threading
from typing import List, Optional
from datetime import datetime


class BackupScheduler:
    def __init__(self, backup_engine):
        """
        Initialize backup scheduler

        Args:
            backup_engine: BackupEngine instance to use for scheduled backups
        """
        self.backup_engine = backup_engine
        self.scheduled_jobs = []
        self.last_run = None

    def schedule_backup(self, schedule_type: str, time_str: str,
                       source_dir: str, destination_dir: str,
                       include_extensions: List[str] = None,
                       exclude_extensions: List[str] = None):
        """
        Schedule a backup operation

        Args:
            schedule_type: Type of schedule ('daily', 'weekly', 'monthly')
            time_str: Time in HH:MM format (24-hour)
            source_dir: Source directory to backup
            destination_dir: Destination directory
            include_extensions: Extensions to include
            exclude_extensions: Extensions to exclude
        """
        # Clear existing schedules
        schedule.clear()

        # Create backup job
        def backup_job():
            print(f"[Scheduler] Running scheduled backup at {datetime.now()}")
            result = self.backup_engine.backup(
                source_dir=source_dir,
                destination_dir=destination_dir,
                include_extensions=include_extensions,
                exclude_extensions=exclude_extensions
            )

            self.last_run = datetime.now()

            if result["success"]:
                print(f"[Scheduler] Backup completed: {result['copied']} files copied")
            else:
                print(f"[Scheduler] Backup failed: {result.get('error', 'Unknown error')}")

        # Schedule based on type
        try:
            if schedule_type == "daily":
                schedule.every().day.at(time_str).do(backup_job)
                print(f"[Scheduler] Scheduled daily backup at {time_str}")

            elif schedule_type == "weekly":
                # Weekly backup on Monday at specified time
                schedule.every().monday.at(time_str).do(backup_job)
                print(f"[Scheduler] Scheduled weekly backup (Mondays) at {time_str}")

            elif schedule_type == "monthly":
                # Monthly backup on 1st of each month at specified time
                # Note: schedule library doesn't have native monthly support,
                # so we use daily check and only run on 1st
                def monthly_backup_job():
                    if datetime.now().day == 1:
                        backup_job()

                schedule.every().day.at(time_str).do(monthly_backup_job)
                print(f"[Scheduler] Scheduled monthly backup (1st of month) at {time_str}")

            else:
                print(f"[Scheduler] Unknown schedule type: {schedule_type}")

        except Exception as e:
            print(f"[Scheduler] Error scheduling backup: {e}")

    def run_pending(self):
        """Run pending scheduled jobs"""
        schedule.run_pending()

    def get_next_run(self) -> Optional[datetime]:
        """Get next scheduled run time"""
        jobs = schedule.get_jobs()
        if jobs:
            return jobs[0].next_run
        return None

    def clear_all(self):
        """Clear all scheduled jobs"""
        schedule.clear()
        print("[Scheduler] All schedules cleared")
