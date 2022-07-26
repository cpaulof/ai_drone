#!/usr/bin/env python3

"""
This example shows how to use the manual controls plugin.
Note: Manual inputs are taken from a test set in this example to decrease complexity. Manual inputs
can be received from devices such as a joystick using third-party python extensions
Note: Taking off the drone is not necessary before enabling manual inputs. It is acceptable to send
positive throttle input to leave the ground. Takeoff is used in this example to decrease complexity
"""

import asyncio
import random
from mavsdk import System


async def print_gps_info(drone):
    async for pos in drone.telemetry.position():
        print(f"\rGPS info: {pos}\t\t\t\t\t\t\t\t", end="")

# Test set of manual inputs. Format: [roll, pitch, throttle, yaw]
manual_inputs = [
    [0, 0, 0.5, 0],  # no movement
    [-1, 0, 0.5, 0],  # minimum roll
    [1, 0, 0.5, 0],  # maximum roll
    [0, -1, 0.5, 0],  # minimum pitch
    [0, 1, 0.5, 0],  # maximum pitch
    [0, 0, 0.5, -1],  # minimum yaw
    [0, 0, 0.5, 1],  # maximum yaw
    [0, 0, 1, 0],  # max throttle
    [0, 0, 0, 0],  # minimum throttle
]
drone = System(mavsdk_server_address='localhost', port=50051)

async def manual_controls():
    """Main function to connect to the drone and input manual controls"""
    # Connect to the Simulation
    
    await drone.connect()

    # This waits till a mavlink based drone is connected
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Checking if Global Position Estimate is ok
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    # set the manual control input after arming
    
    # Arming the drone
    print("-- Arming")
    await drone.action.arm()

    # Takeoff the vehicle
    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    # set the manual control input after arming
    
    

    # start manual control
    print("-- Starting manual control")
    await drone.manual_control.start_position_control()

    

    for i in range(50):
        await drone.manual_control.set_manual_control_input(-1.0, 0., 1.0, 0.)

        

        await asyncio.sleep(0.1)

async def print_position(drone=drone):
    """
    Default print_position command seperated and taken from telemetry.py
    :param drone:
    :return:
    """

    async for position in drone.telemetry.position():
        print(position)
        return position

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(manual_controls())
    loop.run_until_complete(print_position())