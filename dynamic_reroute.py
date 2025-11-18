import traci
import sumolib

# === Configuration ===
SUMO_BINARY = "sumo-gui"   # use "sumo" for GUI mode; "sumo" for CLI mode
CONFIG_FILE = "grid.sumocfg"
THRESHOLD_SPEED = 5  # km/h threshold to consider congestion

# === Start SUMO simulation ===
traci.start([SUMO_BINARY, "-c", CONFIG_FILE])
print("🚀 SUMO simulation started...")

# Load the SUMO network
net = sumolib.net.readNet("grid.net.xml")

# === Helper: reroute vehicle ===
def reroute_vehicle(vehicle_id):
    current_edge = traci.vehicle.getRoadID(vehicle_id)
    if current_edge.startswith(":"):  # Skip internal junction edges
        return

    # Get outgoing edges from the current edge
    outgoing_edges = net.getEdge(current_edge).getOutgoing()
    if not outgoing_edges:
        return

    # Find the best next edge based on mean speed
    best_edge = None
    best_speed = 0
    for edge in outgoing_edges:
        edge_id = edge.getID()  # Edge object directly
        mean_speed = traci.edge.getLastStepMeanSpeed(edge_id)
        if mean_speed > best_speed:
            best_speed = mean_speed
            best_edge = edge_id

    # Reroute the vehicle if a faster edge is found
    if best_edge:
        try:
            traci.vehicle.changeTarget(vehicle_id, best_edge)
            print(f"🚗 Vehicle {vehicle_id} rerouted → {best_edge} (avg speed: {best_speed:.2f} km/h)")
        except traci.TraCIException:
            pass

# === Simulation Loop ===
try:
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for vehicle_id in traci.vehicle.getIDList():
            speed = traci.vehicle.getSpeed(vehicle_id)
            if speed < THRESHOLD_SPEED:  # Congested
                reroute_vehicle(vehicle_id)
        step += 1

except traci.exceptions.FatalTraCIError:
    print("✅ SUMO simulation ended normally.")

finally:
    traci.close()
    print("🔚 TraCI connection closed successfully.")
