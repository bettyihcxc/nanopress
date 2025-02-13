import psutil
import os
import subprocess
import time

def list_processes():
    """List all running processes."""
    print("Listing all running processes:")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, "
                  f"CPU: {proc.info['cpu_percent']}%, "
                  f"Memory: {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def kill_process(pid):
    """Kill a process by PID."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        print(f"Process {pid} terminated successfully.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
        print(f"Failed to terminate process {pid}: {e}")

def optimize_resources():
    """Optimize system resources by cleaning temporary files and freeing up memory."""
    print("Optimizing system resources...")
    
    # Clear temporary files
    temp_path = os.getenv('TEMP')
    if temp_path:
        for filename in os.listdir(temp_path):
            file_path = os.path.join(temp_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    # Free up memory using Windows Management Instrumentation Command-line (WMIC)
    try:
        subprocess.run('wmic os get FreePhysicalMemory', check=True)
        print("Freed up memory.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to free up memory: {e}")

def main():
    while True:
        print("\nNanoPress - System Optimizer")
        print("1. List running processes")
        print("2. Kill a process")
        print("3. Optimize resources")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            list_processes()
        elif choice == '2':
            pid = int(input("Enter PID of the process to kill: "))
            kill_process(pid)
        elif choice == '3':
            optimize_resources()
        elif choice == '4':
            print("Exiting NanoPress.")
            break
        else:
            print("Invalid choice. Please try again.")

        time.sleep(1)

if __name__ == "__main__":
    main()