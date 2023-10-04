from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep

# Observer Pattern: Define an abstract Observer class
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# Concrete Observer class: DeviceStatusObserver
class DeviceStatusObserver(Observer):
    def __init__(self, device):
        self.device = device

    def update(self, message):
        print(f"Device {self.device.device_id}: {message}")

# Define the abstract Device class using the Factory Method Pattern
class Device(ABC):
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.observers = []

    def status_report(self):
        pass

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

# Concrete Light class
class Light(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "light")
        self.status = "off"

    def turn_on(self):
        self.status = "on"
        self.notify_observers(f"Light is turned on ({self.status})")

    def turn_off(self):
        self.status = "off"
        self.notify_observers(f"Light is turned off ({self.status})")

    def status_report(self):
        return f"Light {self.device_id} is {self.status}."

# Concrete Thermostat class
class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "thermostat")
        self.temperature = 70

    def set_temperature(self, temperature):
        self.temperature = temperature
        self.notify_observers(f"Thermostat temperature set to {self.temperature} degrees")

    def status_report(self):
        return f"Thermostat is set to {self.temperature} degrees."

# Concrete DoorLock class
class DoorLock(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "door")
        self.status = "locked"

    def lock(self):
        self.status = "locked"
        self.notify_observers(f"Door is locked")

    def unlock(self):
        self.status = "unlocked"
        self.notify_observers(f"Door is unlocked")

    def status_report(self):
        return f"Door is {self.status}."

# Proxy Pattern: Define a Proxy class for controlling access to devices
class DeviceProxy:
    def __init__(self, device):
        self.device = device

    def turn_on(self):
        self.device.turn_on()

    def turn_off(self):
        self.device.turn_off()

    def set_temperature(self, temperature):
        if isinstance(self.device, Thermostat):
            self.device.set_temperature(temperature)
        else:
            print("This device does not support temperature control.")

    def lock(self):
        if isinstance(self.device, DoorLock):
            self.device.lock()
        else:
            print("This device does not support locking.")

    def unlock(self):
        if isinstance(self.device, DoorLock):
            self.device.unlock()
        else:
            print("This device does not support unlocking.")

    def status_report(self):
        return self.device.status_report()

# Define a Smart Home Hub as the Subject in the Observer Pattern
class SmartHomeHub:
    def __init__(self):
        self.devices = {}
        self.scheduled_tasks = []
        self.automated_triggers = []

    # Factory Method for creating instances of different smart devices
    def create_device(self, device_id, device_type, initial_status=None, initial_temperature=None):
        if device_id in self.devices:
            print(f"Device with ID {device_id} already exists.")
            return

        if device_type == "light":
            device = Light(device_id)
        elif device_type == "thermostat":
            device = Thermostat(device_id)
            if initial_temperature is not None:
                device.set_temperature(initial_temperature)
        elif device_type == "door":
            device = DoorLock(device_id)
            if initial_status is not None:
                if initial_status == "locked":
                    device.lock()
                elif initial_status == "unlocked":
                    device.unlock()
        else:
            raise ValueError("Invalid device type")
        self.devices[device_id] = device
        return DeviceProxy(device)  # Return a proxy for controlled access

    def turn_on(self, device_id):
        if device_id in self.devices:
            self.devices[device_id].turn_on()
        else:
            print(f"Device with ID {device_id} not found.")

    def turn_off(self, device_id):
        if device_id in self.devices:
            self.devices[device_id].turn_off()
        else:
            print(f"Device with ID {device_id} not found.")

    def set_schedule(self, device_id, time, action):
        self.scheduled_tasks.append({"device": device_id, "time": time, "action": action})
        print(f"Scheduled Task: [{time}] - {action}")

    def add_trigger(self, condition, action):
        self.automated_triggers.append({"condition": condition, "action": action})
        print(f"Automated Trigger: [{condition}] - {action}")

    def add_device(self, device_id, device_type, initial_status=None, initial_temperature=None):
        if device_id in self.devices:
            print(f"Device with ID {device_id} already exists.")
            return

        device = self.create_device(device_id, device_type, initial_status, initial_temperature)
        self.devices[device_id] = device
        print(f"Added new {device_type} with ID {device_id}.")

    def remove_device(self, device_id):
        if device_id in self.devices:
            device = self.devices[device_id]
            del self.devices[device_id]
            print(f"Removed {device.device_type} with ID {device_id}.")
        else:
            print(f"Device with ID {device_id} not found.")

    def run_scheduled_tasks(self):
        while True:
            current_time = datetime.now().strftime("%H:%M")
            for task in self.scheduled_tasks:
                if task["time"] == current_time:
                    self.execute_command(task["action"])
            sleep(60)  # Check every minute

    def execute_command(self, command):
        try:
            eval(f"self.{command}")
        except Exception as e:
            print(f"Error executing command: {e}")

    def status_report(self):
        report = []
        for device_id, device in self.devices.items():
            report.append(device.status_report())
        return " ".join(report)

    def get_scheduled_tasks(self):
        return self.scheduled_tasks

    def get_automated_triggers(self):
        return self.automated_triggers
    # ... (previous code remains the same)

# Function to format scheduled tasks as a string
def format_scheduled_tasks(tasks):
    formatted_tasks = []
    for task in tasks:
        formatted_task = {
            "device": task["device"],
            "time": task["time"],
            "command": task["action"]
        }
        formatted_tasks.append(formatted_task)
    return str(formatted_tasks)

# Function to format automated triggers as a string
def format_automated_triggers(triggers):
    formatted_triggers = []
    for trigger in triggers:
        formatted_trigger = {
            "condition": trigger["condition"],
            "action": trigger["action"]
        }
        formatted_triggers.append(formatted_trigger)
    return str(formatted_triggers)

    

# Example usage of adding and removing devices
if __name__ == "__main__":
    hub = SmartHomeHub()
    
    # Adding devices with provided initial states
    hub.add_device(1, "light", initial_status="off")
    hub.add_device(2, "thermostat", initial_temperature=70)
    hub.add_device(3, "door", initial_status="locked")

    # User commands from provided input
    hub.turn_on(1)
    hub.set_schedule(2, "06:00", "turn_on(1)")
    hub.add_trigger("device.temperature > 75", "turn_off(1)")

    # Status report
    print(hub.status_report())

    # Scheduled tasks and automated triggers
    print("Scheduled Tasks:", hub.get_scheduled_tasks())
    print("Automated Triggers:", hub.get_automated_triggers())

    # Simulate running scheduled tasks
    hub.run_scheduled_tasks()
    hub = SmartHomeHub()

    # Adding devices
    hub.add_device(1, "light", initial_status="off")
    hub.add_device(2, "thermostat", initial_temperature=70)
    hub.add_device(3, "door", initial_status="")
