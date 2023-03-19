import numpy as np

# Define the Poisson rates for each road
rates = np.array([0.2, 0.3])

# Define the duration range for traffic lights
min_duration = 5
max_duration = 45

# Define the number of time steps
num_steps = 10000

# Define the learning rate and discount factor for Q-learning
learning_rate = 0.05
discount_factor = 0.5

# Initialize Q-values for each state-action pair
Q_values = np.zeros((2, max_duration - min_duration + 1))

# Initialize the traffic light duration for each road
light_duration = np.random.randint(min_duration, max_duration + 1, size = 2)

# Initialize the total waiting time for each road
total_waiting_time = np.zeros(2)

# Initialize the number of vehicles that have passed through the intersection for each road
num_passed = np.zeros(2)

# Loop through each time step
for t in range(num_steps):
    # Simulate arrivals of vehicles using a Poisson distribution
    arrivals = np.random.poisson(rates)
    
    # Loop through each road
    for i in range(2):
        # Update the total waiting time for the current road
        total_waiting_time[i] += num_passed[i] * light_duration[i]
        
        # Update the number of vehicles that have passed through the intersection for the current road
        num_passed[i] = arrivals[i] + num_passed[i] - light_duration[i] / 2
        
        # Update the Q-value for the current state-action pair
        reward = -total_waiting_time[i]
        next_state = np.argmax(Q_values, axis=1)
        next_reward = -total_waiting_time[next_state[i]]
        Q_values[i, light_duration[i] - min_duration] += learning_rate * (reward + discount_factor * next_reward - Q_values[i, light_duration[i] - min_duration])
        
        # Update the duration of the traffic light for the current road using an epsilon-greedy policy
        if np.random.rand() < 0.1:
            light_duration[i] = np.random.randint(min_duration, max_duration + 1)
        else:
            light_duration[i] = np.argmin(Q_values[i]) + min_duration

        # Print the optimal traffic light durations for each road
        print("Optimal traffic light durations:")
        
        for i in range(2):
            print(f"Road {i}: {np.argmin(Q_values[i]) + min_duration}")

        # Print the total waiting time for each road
        print("Total waiting time:")
        
        for i in range(2):
            print(f"Road {i}: {total_waiting_time[i]}")