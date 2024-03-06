import numpy as np

np.random.seed(42)  # For reproducible results


# Initialize a row x column array with random initial populations between 1000 and 255000
def generate_env(no_rows, no_cols):
    return np.random.randint(1000, 255000, size=(no_rows, no_cols))


K = 1000000  # Carrying capacity -> the max limit of fish per cell
r_annual = 0.1  # Annual intrinsic rate of increase
months = 24  # Simulate growth over 24 months (2 years)

# Convert annual growth rate to monthly growth rate
r_monthly = (1 + r_annual) ** (1/12) - 1


# Logistic growth function
def logistic_growth(initial_population, monthly_growth, max_population, month):
    return max_population / (1 + ((K - initial_population) / initial_population) * np.exp(-monthly_growth * month))

def population_growth():
    # Simulate growth over 24 months
    population_growth_monthly = np.zeros((rows, columns, months+1))  # +1 to include the initial month
    population_growth_monthly[:, :, 0] = initial_populations  # Set initial populations

for month in range(1, months+1):
    population_growth_monthly[:, :, month] = logistic_growth(initial_populations, r_monthly, K, month)

# Define which months to display
months_to_show = [0, 3, 6, 9, 12, 15, 18, 21, 24]
