from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging
import logging.config
import time
import sys
import os


class Watcher:
    def __init__(self):
        self.observer = Observer()
        self.watchDir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    def run(self):
        logging.config.fileConfig(os.path.dirname(__file__) + '/logging.conf')
        self.observer.schedule(Handler(), self.watchDir, recursive=True)
        self.observer.start()
        
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            
        self.observer.join()
  
        
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        logger = logging.getLogger("mainApp")
        message = f"[{time.asctime()}] noticed: Watchdog received {event.event_type} event on {event.src_path}"
        print(message)
        logger.info(message)
            



    