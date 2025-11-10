import schedule
import time
from app.commands.autoclose_overdue import autoclose_overdue


def run_scheduler():
    """Run the scheduler to execute tasks periodically."""
    # Schedule the autoclose_overdue command to run every 15 minutes
    schedule.every(15).minutes.do(lambda: autoclose_overdue.main(standalone_mode=False))

    print("Scheduler started. Running autoclose_overdue every 15 minutes.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


if __name__ == "__main__":
    run_scheduler()
