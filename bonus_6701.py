import simpy
import random

# Constants
CRITICAL_RATE = 3
SERIOUS_RATE = 5
FAIR_RATE = 10
GOOD_RATE = 15
RECEPTION_RATE = 35

SIMULATION_TIME = 1000

# Patient generator
def patient_generator(env, reception):
    patient_id = 0
    while True:
        condition = random.choices(
            ["critical", "serious", "fair", "good"],
            weights=[CRITICAL_RATE, SERIOUS_RATE, FAIR_RATE, GOOD_RATE],
        )[0]

        patient_id += 1
        env.process(patient(env, patient_id, condition, reception))
        yield env.timeout(random.expovariate(sum([CRITICAL_RATE, SERIOUS_RATE, FAIR_RATE, GOOD_RATE])))

# Patient process
def patient(env, patient_id, condition, reception):
    arrival_time = env.now
    with reception.request(priority=get_priority(condition)) as req:
        yield req
        wait_time = env.now - arrival_time
        response_times[condition].append(wait_time)
        yield env.timeout(random.expovariate(RECEPTION_RATE))

# Helper function to get priority
def get_priority(condition):
    if condition == "critical":
        return 0
    elif condition == "serious":
        return 1
    elif condition == "fair":
        return 2
    else:
        return 3

# Simulation
env = simpy.Environment()
reception = simpy.PriorityResource(env, capacity=1)
response_times = {"critical": [], "serious": [], "fair": [], "good": []}
env.process(patient_generator(env, reception))
env.run(until=SIMULATION_TIME)

# Results
for condition in response_times:
    avg_response_time = sum(response_times[condition]) / len(response_times[condition])
    print(f"Average response time for {condition} patients: {avg_response_time:.2f} hours")

total_patients = sum([len(response_times[condition]) for condition in response_times])
print(f"Average number of patients in the system: {total_patients / SIMULATION_TIME:.2f} patients/hour")
