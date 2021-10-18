import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from filelogic import parse_name, parse_numerics, move_files
from filelogic import startPath


class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):

    def on_created(self, event):

        print("New files found! Sorting...")

        for j in os.listdir(startPath):
            if j.lower().endswith(('.asf', '.avi', '.mov', '.mp4', '.mpeg', '.mpegts', '.ts', '.mkv', '.wmv', '.srt', '.txt')):
                move_files(parse_name(j), parse_numerics(j), j)

        print("Done")


if __name__ == "__main__":
    w = Watcher(startPath, MyHandler())
    w.run()
