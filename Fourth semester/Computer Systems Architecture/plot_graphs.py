import csv
import matplotlib.pyplot as plt

def load_data(filename):
    iterations = []
    times = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            iterations.append(int(row['iterations']))
            times.append(float(row['time_ns']))
    return iterations, times

iter_with, time_with = load_data('1_with.csv')
iter_without, time_without = load_data('1_without.csv')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(iter_with, time_with, 'b-', linewidth=1.5)
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Time (ns)')
ax1.set_title('With Hyper-Threading')
ax1.grid(True, alpha=0.3)

ax2.plot(iter_without, time_without, 'r-', linewidth=1.5)
ax2.set_xlabel('Iterations')
ax2.set_ylabel('Time (ns)')
ax2.set_title('Without Hyper-Threading')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cpu_benchmark.png', dpi=300)
plt.show()