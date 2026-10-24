import csv
from collections import defaultdict
import matplotlib.pyplot as plt

def load_csv_multi_core(path):
    data = defaultdict(list)
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            core = int(row['core'].strip())
            iters = int(row['iterations'].strip())
            time = float(row['time_ns'].strip())
            data[core].append((iters, time))
    return data

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

data_with = load_csv_multi_core('2_with.csv')
cores_with = sorted(data_with.keys())
for core in cores_with:
    pts = sorted(data_with[core], key=lambda x: x[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax1.plot(xs, ys, linewidth=1.5, label=f'core {core}')
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Time (ns)')
ax1.set_title('Multi-core with Hyper-Threading')
ax1.grid(True, alpha=0.3)
ax1.legend(ncol=2, fontsize=8)

data_without = load_csv_multi_core('2_without.csv')
cores_without = sorted(data_without.keys())
for core in cores_without:
    pts = sorted(data_without[core], key=lambda x: x[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax2.plot(xs, ys, linewidth=1.5, label=f'core {core}')
ax2.set_xlabel('Iterations')
ax2.set_ylabel('Time (ns)')
ax2.set_title('Multi-core without Hyper-Threading')
ax2.grid(True, alpha=0.3)
ax2.legend(ncol=2, fontsize=8)

plt.tight_layout()
plt.savefig('multi_core_benchmark.png', dpi=300)
plt.show()