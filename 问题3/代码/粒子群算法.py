import numpy as np
import pandas as pd


sales_data = pd.read_excel("filtered_combine_sales_data.xlsx")
sensitivity_info = pd.read_excel("sensitivity_info.xlsx")

class Particle:
    def __init__(self, dimension):
        self.position = np.random.uniform(low=5, high=20, size=dimension)  # Initialize position within a realistic price range
        self.velocity = np.random.uniform(low=-0.1, high=0.1, size=dimension)  # Initialize velocity
        self.best_position = np.copy(self.position)
        self.best_score = -np.inf

def fitness(position):
    if position.sum() < 27 or position.sum() > 33:
        return -np.inf

    profit = compute_profit(position, sales_data, sensitivity_info)
    
    return profit

def compute_profit(prices, sales_data, sensitivity_info):

    merged_data = sales_data.merge(sensitivity_info, on="单品名称", how="left")
    
    merged_data["estimated_sales"] = np.where(
        merged_data["销售单价(元/千克)"] <= merged_data["销售单价(元/千克)_max"],
        merged_data["销量(千克)_max"],
        merged_data["销量(千克)_min"]
    )

    profit = (merged_data["estimated_sales"] * prices - 2.5 * prices).sum()
    
    return profit

def pso(num_particles, dimension, num_iterations, alpha=0.5, beta=0.5, gamma=0.5):
    particles = [Particle(dimension) for _ in range(num_particles)]
    g_best_position = np.random.uniform(low=5, high=20, size=dimension)
    g_best_score = -np.inf
    velocities = []
    positions = []

    for _ in range(num_iterations):
        iteration_velocities = []
        iteration_positions = []
        for particle in particles:

            f = fitness(particle.position)
            if f > particle.best_score:
                particle.best_score = f
                particle.best_position = particle.position

            if f > g_best_score:
                g_best_score = f
                g_best_position = particle.position

        for particle in particles:
            inertia = alpha * particle.velocity
            personal_attraction = beta * np.random.rand() * (particle.best_position - particle.position)
            global_attraction = gamma * np.random.rand() * (g_best_position - particle.position)

            particle.velocity = inertia + personal_attraction + global_attraction
            particle.position += particle.velocity

            iteration_velocities.append(particle.velocity)
            iteration_positions.append(particle.position)

        velocities.append(iteration_velocities)
        positions.append(iteration_positions)

    return velocities, positions


dimension = 43
velocities, positions = pso(43, dimension, 100)


particle_to_product_mapping = {}
for particle_number in range(1, 44): 

    product_name = sales_data.loc[particle_number - 1, "单品名称"]
    particle_to_product_mapping[particle_number] = product_name


result_df = pd.DataFrame({
    "Particle": list(range(1, 44)),
    "Velocity": [v for v in velocities[-1]],
    "Position": [p for p in positions[-1]]
})
result_df["Particle"] = result_df["Particle"].map(particle_to_product_mapping)

result_df.to_excel("PSO_Results_With_Product_Names.xlsx", index=False)
