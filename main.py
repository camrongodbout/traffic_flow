import os
import sys
import traci

# Add SUMO_HOME/tools to Python PATH
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable 'SUMO_HOME' not set.")

# Define SUMO command and config
sumoCmd = ["sumo-gui", "-c", "your_config.sumocfg"]

# Custom lane-changing logic
def custom_lane_changing():
    for vehicle_id in traci.vehicle.getIDList():
        if traci.vehicle.getTypeID(vehicle_id) == "slowTruck":
            current_lane = traci.vehicle.getLaneIndex(vehicle_id)
            if current_lane == 0:
                # Slowly move to the left lane
                traci.vehicle.changeLane(vehicle_id, 1, 1)
            elif current_lane == 1:
                # Return to the right lane if left is clear
                traci.vehicle.changeLane(vehicle_id, 0, 1)

# Main simulation loop
def run_simulation():
    traci.start(sumoCmd)
    step = 0
    while step < 1000:
        traci.simulationStep()
        custom_lane_changing()
        step += 1

    traci.close()

# Run the simulation
if __name__ == "__main__":
    run_simulation()