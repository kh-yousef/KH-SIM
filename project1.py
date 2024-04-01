import numpy as np
import random
from scipy.stats import truncnorm
import matplotlib.pyplot as plt

class Politician:
    def __init__(self, age, office=None, years_in_office=0):
        self.age = age
        self.office = office
        self.years_in_office = years_in_office
        self.life_expectancy = generate_life_expectancy()

office_limits = {
    'Quaestor': 20,
    'Aedile': 10,
    'Praetor': 8,
    'Consul': 2,
}

def generate_life_expectancy(mu=55, sigma=10, lower=25, upper=80):
    return int(truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs())

def annual_influx_of_candidates(mu=15, sigma=5):
    return int(np.random.normal(mu, sigma))

def is_eligible_for_office(politician, office):
    age_requirements = {'Quaestor': 30, 'Aedile': 36, 'Praetor': 39, 'Consul': 42}
    if office == 'Quaestor':  # New candidates are only directly eligible for Quaestor
        return True
    elif office == 'Aedile' and politician.office == 'Quaestor' and politician.years_in_office >= 2:
        return True
    elif office == 'Praetor' and politician.office == 'Aedile' and politician.years_in_office >= 2:
        return True
    elif office == 'Consul' and politician.office == 'Praetor' and politician.years_in_office >= 2:
        return True
    return False

def initialize_political_landscape():
    landscape = {
        'Quaestor': [Politician(age=random.randint(30, 34), office='Quaestor') for _ in range(20)],
        'Aedile': [Politician(age=random.randint(36, 39), office='Aedile') for _ in range(10)],
        'Praetor': [Politician(age=random.randint(39, 42), office='Praetor') for _ in range(8)],
        'Consul': [Politician(age=random.randint(42, 45), office='Consul') for _ in range(2)]
    }
    return landscape, 100

def age_and_mortality(landscape):
    for office in landscape:
        landscape[office] = [p for p in landscape[office] if p.age + 1 <= p.life_expectancy]
        for politician in landscape[office]:
            politician.age += 1
            politician.years_in_office += 1

def generate_new_candidates():
    num_candidates = annual_influx_of_candidates()
    return [Politician(age=30) for _ in range(num_candidates)]

def conduct_elections(landscape, new_candidates):
    for office in ['Consul', 'Praetor', 'Aedile', 'Quaestor']:
        if office == 'Quaestor':  # Special case for Quaestors where new candidates can be considered
            candidates = new_candidates + [p for p in landscape['Quaestor'] if is_eligible_for_office(p, office)]
        else:
            candidates = [p for p in landscape[office] if is_eligible_for_office(p, office)]
        random.shuffle(candidates)  # Randomize the candidate list
        for candidate in candidates:
            if len(landscape[office]) < office_limits[office]:
                landscape[office].append(candidate)
                if office == 'Quaestor':  # Remove newly elected Quaestors from the candidate pool
                    if candidate in new_candidates:
                        new_candidates.remove(candidate)
            else:
                break

def update_PSI(landscape, PSI):
    for office in office_limits:
        unfilled_positions = office_limits[office] - len(landscape[office])
        PSI -= unfilled_positions * 5
    return PSI

def simulate_year(landscape, PSI):
    age_and_mortality(landscape)
    new_candidates = generate_new_candidates()
    conduct_elections(landscape, new_candidates)
    PSI = update_PSI(landscape, PSI)
    return landscape, PSI

def run_simulation():
    landscape, PSI = initialize_political_landscape()
    fill_rates = {office: [] for office in office_limits}  # Initialize fill rate tracking
    
    for year in range(1, 201):
        landscape, PSI = simulate_year(landscape, PSI)
        # Calculate and record fill rate for each office
        for office in office_limits:
            fill_rate = len(landscape[office]) / office_limits[office]
            fill_rates[office].append(fill_rate)
    
    # Calculate average fill rates for the simulation period
    avg_fill_rates = {office: sum(rates) / len(rates) for office, rates in fill_rates.items()}
    return PSI, avg_fill_rates, landscape



def plot_age_distributions(landscape):
    offices = list(landscape.keys())
    num_offices = len(offices)
    fig, axs = plt.subplots(1, num_offices, figsize=(5 * num_offices, 4))  # Adjust figure size as needed

    for i, office in enumerate(offices):
        ages = [p.age for p in landscape[office]]
        axs[i].hist(ages, bins=range(25, 81, 5), alpha=0.7, label=office)
        axs[i].set_xlabel('Age')
        axs[i].set_ylabel('Number of Politicians')
        axs[i].set_title(f'Age Distribution in {office}')
        axs[i].legend()

    plt.tight_layout()
    plt.show()

# Adjusted to just calculate and return the fill rates and PSI
PSI_final, avg_fill_rates, final_landscape = run_simulation()
print("Final PSI:", PSI_final)
print("Average Annual Fill Rates:")
for office, rate in avg_fill_rates.items():
    print(f"{office}: {rate:.2f}")

# Plotting
plot_age_distributions(final_landscape)