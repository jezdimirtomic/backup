"""
Demo script - Test backup functionality without GUI
"""
from backup_engine import BackupEngine
import os
import tempfile


def demo_backup():
    """Demonstrate backup functionality"""
    print("🗄️ Backup Engine Demo\n")

    # Create temporary test directories
    with tempfile.TemporaryDirectory() as temp_source:
        with tempfile.TemporaryDirectory() as temp_dest:
            # Create test files
            print("📁 Creating test files...")

            test_files = {
                "document.txt": "This is a text file",
                "image.jpg": "Fake image data",
                "video.mp4": "Fake video data",
                "temp.tmp": "Temporary file",
                "log.log": "Log file data"
            }

            for filename, content in test_files.items():
                filepath = os.path.join(temp_source, filename)
                with open(filepath, 'w') as f:
                    f.write(content)

            print(f"   Created {len(test_files)} test files in {temp_source}\n")

            # Initialize backup engine
            def progress_callback(current, total, filename):
                print(f"   [{current}/{total}] Backing up: {filename}")

            backup_engine = BackupEngine(progress_callback=progress_callback)

            # Test 1: Backup all files
            print("🚀 Test 1: Backup ALL files")
            result = backup_engine.backup(temp_source, temp_dest)

            if result["success"]:
                print(f"✅ Success! Copied {result['copied']} files\n")
            else:
                print(f"❌ Failed: {result['error']}\n")

            # Test 2: Backup only .txt and .jpg files
            print("🚀 Test 2: Backup only .txt and .jpg files")
            temp_dest2 = tempfile.mkdtemp()

            result = backup_engine.backup(
                temp_source,
                temp_dest2,
                include_extensions=['.txt', '.jpg']
            )

            if result["success"]:
                print(f"✅ Success! Copied {result['copied']} files (should be 2)")
                print(f"   Skipped: {result['skipped']} files\n")
            else:
                print(f"❌ Failed: {result['error']}\n")

            # Test 3: Exclude .tmp and .log files
            print("🚀 Test 3: Exclude .tmp and .log files")
            temp_dest3 = tempfile.mkdtemp()

            result = backup_engine.backup(
                temp_source,
                temp_dest3,
                exclude_extensions=['.tmp', '.log']
            )

            if result["success"]:
                print(f"✅ Success! Copied {result['copied']} files (should be 3)")
                print(f"   Skipped: {result['skipped']} files\n")
            else:
                print(f"❌ Failed: {result['error']}\n")

            print("✨ Demo completed!\n")
            print("To run the full GUI application, execute:")
            print("   python backup_gui.py")


if __name__ == "__main__":
    demo_backup()
