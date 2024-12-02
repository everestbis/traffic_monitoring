import random
import time
import threading

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://benjamin:2is_george@cluster.iwa9w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.traffic.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# hello write a function to add two numbers


class TrafficLight:
    def __init__(self, name, green_duration, red_duration):
        self.name = name
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.state = "RED"
        self.time_in_state = 0

    def switch_state(self):
        if self.state == "GREEN":
            self.state = "RED"
            self.time_in_state = 0
            print(f"{self.name} traffic light is RED.")
        else:
            self.state = "GREEN"
            self.time_in_state = 0
            print(f"{self.name} traffic light is GREEN.")

    def is_green(self):
        return self.state == "GREEN"


class Intersection:
    def __init__(self, ns_green_duration, ns_red_duration, ew_green_duration, ew_red_duration):
        # Initialize traffic lights
        self.ns_light = TrafficLight("North-South", ns_green_duration, ns_red_duration)
        self.ew_light = TrafficLight("East-West", ew_green_duration, ew_red_duration)

        # Car queues
        self.ns_queue = []
        self.ew_queue = []
        self.ns_cars_passed = 0
        self.ew_cars_passed = 0
        self.total_cars_arrived = 0


    def car_arrival(self, direction):
        """Simulate car arrivals to the queues."""
        while True:
            time.sleep(random.randint(1, 3))  # Car arrives every 1-3 seconds
            self.total_cars_arrived += 1
            if direction == "North-South":
                self.ns_queue.append(f"Car-{len(self.ns_queue) + 1}")
                print(f"A car arrived at North-South queue. Queue length: {len(self.ns_queue)}")
            else:
                self.ew_queue.append(f"Car-{len(self.ew_queue) + 1}")
                print(f"A car arrived at East-West queue. Queue length: {len(self.ew_queue)}")

        # insert ew_queue and ns_queue to db 
        


    def manage_traffic(self):
        """Manage traffic based on the light states."""
        # Handle North-South traffic if the light is GREEN
        if self.ns_light.is_green() and self.ns_queue:
            print(f"North-South light is GREEN. A car passes!")
            self.ns_queue.pop(0)  # A car passes
            self.ns_cars_passed += 1
            time.sleep(1)  # 1 second per car

        # Handle East-West traffic if the light is GREEN
        if self.ew_light.is_green() and self.ew_queue:
            print(f"East-West light is GREEN. A car passes!")
            self.ew_queue.pop(0)  # A car passes
            self.ew_cars_passed += 1
            time.sleep(1)  # 1 second per car

    def run(self):
        """Run the traffic simulation for a set duration."""
        # Start car arrivals in separate threads for North-South and East-West queues
        threading.Thread(target=self.car_arrival, args=("North-South",), daemon=True).start()
        threading.Thread(target=self.car_arrival, args=("East-West",), daemon=True).start()

        # Run the traffic light cycle and manage traffic flow
        simulation_duration = 60  # seconds
        start_time = time.time()

        while time.time() - start_time < simulation_duration:
            # Simulate the switching of traffic lights
            if self.ns_light.time_in_state >= self.ns_light.green_duration:
                self.ns_light.switch_state()

            if self.ew_light.time_in_state >= self.ew_light.green_duration:
                self.ew_light.switch_state()

            # Update time in state for each light
            self.ns_light.time_in_state += 1
            self.ew_light.time_in_state += 1

            # Call manage_traffic to handle car passing based on the light states
            self.manage_traffic()

            # Simulate real-time with 1-second delay between each cycle
            time.sleep(1)

        # Print statistics at the end of the simulation
        print("\nSimulation ended.")
        print(f"Total cars arrived: {self.total_cars_arrived}")
        print(f"Cars passed North-South: {self.ns_cars_passed}")
        print(f"Cars passed East-West: {self.ew_cars_passed}")


# Real-time simulation without SimPy
if __name__ == "__main__":
    intersection = Intersection(ns_green_duration=5, ns_red_duration=5, ew_green_duration=5, ew_red_duration=5)

    # Start the simulation
    intersection.run()
