import numpy as np
import matplotlib.pyplot as plt

# --- 1. Membership Functions ---


def triangular_mf(x, a, b, c):
  """
  Computes the triangular membership function value.
  a: left foot, b: peak, c: right foot
  """
  return max(0, min((x - a) / (b - a) if b != a else 1, (c - x) / (c - b) if c != b else 1))


def trapezoidal_mf(x, a, b, c, d):
  """
  Computes the trapezoidal membership function value.
  a: left foot, b: left shoulder, c: right shoulder, d: right foot
  """
  if a == b:  # Handle left-shoulder (ramp up)
      val1 = 1
  else:
      val1 = (x - a) / (b - a)

  if c == d:  # Handle right-shoulder (ramp down)
      val2 = 1
  else:
      val2 = (d - x) / (d - c)

  return max(0, min(val1, 1, val2))


# --- 2. Define Fuzzy Sets and MFs for Temperature (Input) ---
# Universe of Discourse for Temperature: 0°C to 50°C
temp_domain = np.arange(0, 51, 1)


def temp_cold(x):
  # Trapezoidal: Fully cold below 10, ramps down to 0 at 20
  return trapezoidal_mf(x, 0, 0, 10, 20)


def temp_warm(x):
  # Triangular: Peaks at 25, starts at 15, ends at 35
  return triangular_mf(x, 15, 25, 35)


def temp_hot(x):
  # Trapezoidal: Starts ramping up at 30, fully hot above 40
  return trapezoidal_mf(x, 30, 40, 50, 50)


# --- 3. Define Fuzzy Sets and MFs for Fan Speed (Output) ---
# Universe of Discourse for Fan Speed: 0% to 100%
fan_speed_domain = np.arange(0, 101, 1)


def speed_slow(x):
  # Trapezoidal: Fully slow below 25, ramps down to 0 at 50
  return trapezoidal_mf(x, 0, 0, 25, 50)


def speed_medium(x):
  # Triangular: Peaks at 50, starts at 25, ends at 75
  return triangular_mf(x, 25, 50, 75)


def speed_fast(x):
  # Trapezoidal: Starts ramping up at 50, fully fast above 75
  return trapezoidal_mf(x, 50, 75, 100, 100)

# --- 4. Fuzzification ---


def fuzzify_temperature(crisp_temp):
  """
  Takes a crisp temperature value and returns the degree of membership
  for each fuzzy set (Cold, Warm, Hot).
  """
  return {
      "cold": temp_cold(crisp_temp),
      "warm": temp_warm(crisp_temp),
      "hot": temp_hot(crisp_temp)
  }

# --- 5. Rule Inference & Aggregation (Simplified) ---
# Rules:
# 1. IF Temperature is Cold THEN Fan Speed is Slow.
# 2. IF Temperature is Warm THEN Fan Speed is Medium.
# 3. IF Temperature is Hot THEN Fan Speed is Fast.


def apply_rules_and_aggregate(fuzzified_input):
  """
  Applies simple rules and aggregates the resulting output fuzzy sets.
  Uses the 'min' operator for implication and 'max' for aggregation.
  Returns a function representing the aggregated output membership.
  """
  # Get activation strengths from fuzzified input
  strength_slow = fuzzified_input['cold']
  strength_medium = fuzzified_input['warm']
  strength_hot = fuzzified_input['hot']

  # Apply implication (clipping the output MFs)
  # Create functions for the clipped output sets
  def clipped_slow(x): return min(strength_slow, speed_slow(x))
  def clipped_medium(x): return min(strength_medium, speed_medium(x))
  def clipped_fast(x): return min(strength_fast, speed_fast(x))

  # Aggregate the clipped output sets using MAX
  def aggregated_mf(x): return max(
      clipped_slow(x), clipped_medium(x), clipped_fast(x))

  return aggregated_mf


# --- 6. Defuzzification (Centroid Method) ---
def defuzzify_centroid(domain, aggregated_mf):
  """
  Calculates the defuzzified crisp value using the Centroid method.
  domain: The numpy array representing the universe of discourse (e.g., fan_speed_domain).
  aggregated_mf: The function representing the aggregated output membership.
  """
  # Calculate membership values for each point in the domain
  mf_values = np.array([aggregated_mf(x) for x in domain])

  # Calculate numerator and denominator for centroid formula
  numerator = np.sum(domain * mf_values)
  denominator = np.sum(mf_values)

  # Handle case where denominator is zero (no rules fired significantly)
  if denominator == 0:
    return 0  # Return a default value (e.g., 0 speed)

  return numerator / denominator

# --- 7. Simulation ---


def simulate_fuzzy_system(crisp_input_temp):
  """Runs the full fuzzification -> defuzzification process."""
  print(f"\n--- Simulating for Input Temperature: {crisp_input_temp}°C ---")

  # Step 1: Fuzzification
  fuzzified_temp = fuzzify_temperature(crisp_input_temp)
  print(f"Fuzzified Input:")
  print(f"  Membership 'Cold': {fuzzified_temp['cold']:.2f}")
  print(f"  Membership 'Warm': {fuzzified_temp['warm']:.2f}")
  print(f"  Membership 'Hot':  {fuzzified_temp['hot']:.2f}")

  # Step 2: Rule Application & Aggregation
  aggregated_output_mf = apply_rules_and_aggregate(fuzzified_temp)
  # Calculate aggregated values for plotting/defuzzification
  aggregated_values = np.array([aggregated_output_mf(x)
                               for x in fan_speed_domain])

  # Step 3: Defuzzification
  crisp_output_speed = defuzzify_centroid(
      fan_speed_domain, aggregated_output_mf)
  print(f"\nDefuzzified Output Fan Speed: {crisp_output_speed:.2f}%")

  return fuzzified_temp, aggregated_values, crisp_output_speed

# --- 8. Visualization ---


def plot_simulation(crisp_input_temp, fuzzified_temp, aggregated_values, crisp_output_speed):
  """Generates plots to visualize the fuzzy logic process."""
  fig, axs = plt.subplots(3, 1, figsize=(8, 10))
  fig.suptitle(
      f'Fuzzy Logic Simulation (Input Temp: {crisp_input_temp}°C)', fontsize=14)

  # Plot 1: Input Membership Functions
  axs[0].plot(temp_domain, [temp_cold(x) for x in temp_domain], label='Cold')
  axs[0].plot(temp_domain, [temp_warm(x) for x in temp_domain], label='Warm')
  axs[0].plot(temp_domain, [temp_hot(x) for x in temp_domain], label='Hot')
  axs[0].axvline(crisp_input_temp, color='k', linestyle='--',
                 label=f'Input Temp ({crisp_input_temp}°C)')
  # Mark fuzzified values
  axs[0].plot(crisp_input_temp, fuzzified_temp['cold'], 'ko', markersize=8)
  axs[0].plot(crisp_input_temp, fuzzified_temp['warm'], 'ko', markersize=8)
  axs[0].plot(crisp_input_temp, fuzzified_temp['hot'], 'ko', markersize=8)
  axs[0].set_title('1. Fuzzification (Input: Temperature)')
  axs[0].set_ylabel('Degree of Membership')
  axs[0].set_xlabel('Temperature (°C)')
  axs[0].legend()
  axs[0].grid(True, linestyle=':', alpha=0.6)

  # Plot 2: Output Membership Functions & Aggregated Result
  axs[1].plot(fan_speed_domain, [speed_slow(x)
              for x in fan_speed_domain], 'b--', alpha=0.5, label='Slow MF (Original)')
  axs[1].plot(fan_speed_domain, [speed_medium(x)
              for x in fan_speed_domain], 'g--', alpha=0.5, label='Medium MF (Original)')
  axs[1].plot(fan_speed_domain, [speed_fast(x)
              for x in fan_speed_domain], 'r--', alpha=0.5, label='Fast MF (Original)')
  # Plot the aggregated area
  axs[1].fill_between(fan_speed_domain, aggregated_values,
                      color='orange', alpha=0.7, label='Aggregated Output')
  axs[1].set_title('2. Rule Inference & Aggregation (Output: Fan Speed)')
  axs[1].set_ylabel('Degree of Membership')
  axs[1].set_xlabel('Fan Speed (%)')
  axs[1].legend()
  axs[1].grid(True, linestyle=':', alpha=0.6)

  # Plot 3: Defuzzification Result
  axs[2].fill_between(fan_speed_domain, aggregated_values,
                      color='orange', alpha=0.7, label='Aggregated Output')
  axs[2].axvline(crisp_output_speed, color='k', linestyle='-', linewidth=2,
                 label=f'Defuzzified Output ({crisp_output_speed:.2f}%)')
  axs[2].set_title(f'3. Defuzzification (Centroid Method)')
  axs[2].set_ylabel('Degree of Membership')
  axs[2].set_xlabel('Fan Speed (%)')
  axs[2].legend()
  axs[2].grid(True, linestyle=':', alpha=0.6)

  # Adjust layout to prevent title overlap
  plt.tight_layout(rect=[0, 0.03, 1, 0.96])
  plt.show()


# --- Main Execution ---
if __name__ == "__main__":
    # --- Test Cases ---
    test_temps = [5, 18, 25, 32, 45]

    for temp in test_temps:
        fuzz_in, agg_out_vals, defuzz_out = simulate_fuzzy_system(temp)
        plot_simulation(temp, fuzz_in, agg_out_vals, defuzz_out)
        print("-" * 40)

    # Example with a specific temperature
    # specific_temp = 28
    # fuzz_in, agg_out_vals, defuzz_out = simulate_fuzzy_system(specific_temp)
    # plot_simulation(specific_temp, fuzz_in, agg_out_vals, defuzz_out)
