import threading

class WaitForUpdate:
    def __init__(self):
        self._updated_value = None
        self._event = threading.Event()

    def set_value(self, value):
        self._updated_value = value
        self._event.set()  # Unblock waiters

    def wait_for_update(self):
        print("Waiting for variable to be updated...")
        self._event.wait()  # Block until set_value() is called
        print(f"Variable updated to: {self._updated_value}")
        return self._updated_value

# Example usage:
if __name__ == "__main__":
    import time
    watcher = WaitForUpdate()

    def updater():
        time.sleep(5)
        watcher.set_value("Done!")

    threading.Thread(target=updater).start()
    watcher.wait_for_update()