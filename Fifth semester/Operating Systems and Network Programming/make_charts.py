import matplotlib.pyplot as plt

# ==============================================================================
# 1. ЭМПИРИЧЕСКИЕ ДАННЫЕ ИЗ ВАШЕГО ЗАПУСКА
# ==============================================================================
counts = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Потоки (Thread)
thread_total_ms = [0.261, 1.547, 2.992, 3.741, 5.743, 5.398, 7.349, 7.713, 7.990, 14.323, 9.694]
thread_avg_us = [261.10, 154.66, 149.58, 124.71, 143.57, 107.95, 122.48, 110.19, 99.87, 159.15, 96.94]

# Процессы (Process)
process_total_ms = [23.451, 93.638, 144.293, 237.146, 288.285, 368.165, 459.586, 585.242, 655.175, 710.450, 655.674]
process_avg_us = [23450.60, 9363.82, 7214.65, 7904.87, 7207.12, 7363.31, 7659.76, 8360.60, 8189.69, 7893.88, 6556.74]

# Общие настройки оформления (ГОСТ / Академический стиль)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10

# ==============================================================================
# ГРАФИК 1: ОБЩЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ (мс)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# --- Потоки ---
ax1.plot(counts, thread_total_ms, marker='o', color='#1f77b4', linewidth=2, markersize=6, label='Thread')
ax1.set_title('Общее время: Потоки (Thread)', fontweight='bold', pad=10)
ax1.set_xlabel('Количество потоков (N)')
ax1.set_ylabel('Время выполнения (мс)')
ax1.set_xticks(counts)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_ylim(0, max(thread_total_ms) * 1.15)

# Подписи ключевых точек для потоков (каждая 2-я точка, чтобы не сливалось)
for i in range(len(counts)):
    if i == 0 or i == len(counts) - 1 or i % 2 == 1:
        ax1.annotate(f"{thread_total_ms[i]:.2f}", (counts[i], thread_total_ms[i]),
                     textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)

# --- Процессы ---
ax2.plot(counts, process_total_ms, marker='s', color='#d62728', linewidth=2, markersize=6, label='Process')
ax2.set_title('Общее время: Процессы (Process)', fontweight='bold', pad=10)
ax2.set_xlabel('Количество процессов (N)')
ax2.set_ylabel('Время выполнения (мс)')
ax2.set_xticks(counts)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.set_ylim(0, max(process_total_ms) * 1.15)

for i in range(len(counts)):
    if i == 0 or i == len(counts) - 1 or i % 2 == 1:
        ax2.annotate(f"{process_total_ms[i]:.1f}", (counts[i], process_total_ms[i]),
                     textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)

plt.tight_layout()
chart1_name = 'chart_total_time.png'
plt.savefig(chart1_name, dpi=300)
plt.close()
print(f"[ОК] График 1 успешно сохранен: {chart1_name}")

# ==============================================================================
# ГРАФИК 2: СРЕДНЕЕ ВРЕМЯ НА 1 ОБЪЕКТ (мкс)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# --- Потоки ---
ax1.plot(counts, thread_avg_us, marker='o', color='#2ca02c', linewidth=2, markersize=6)
ax1.set_title('Удельное время: Потоки (Thread)', fontweight='bold', pad=10)
ax1.set_xlabel('Размер серии (N)')
ax1.set_ylabel('Время на 1 поток (мкс)')
ax1.set_xticks(counts)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_ylim(0, max(thread_avg_us) * 1.2)

for i in range(len(counts)):
    if i == 0 or i == len(counts) - 1 or i % 2 == 1:
        ax1.annotate(f"{thread_avg_us[i]:.1f}", (counts[i], thread_avg_us[i]),
                     textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)

# --- Процессы ---
ax2.plot(counts, process_avg_us, marker='s', color='#ff7f0e', linewidth=2, markersize=6)
ax2.set_title('Удельное время: Процессы (Process)', fontweight='bold', pad=10)
ax2.set_xlabel('Размер серии (N)')
ax2.set_ylabel('Время на 1 процесс (мкс)')
ax2.set_xticks(counts)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.set_ylim(0, max(process_avg_us) * 1.2)

for i in range(len(counts)):
    if i == 0 or i == len(counts) - 1 or i % 2 == 1:
        ax2.annotate(f"{int(process_avg_us[i])}", (counts[i], process_avg_us[i]),
                     textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)

plt.tight_layout()
chart2_name = 'chart_avg_time.png'
plt.savefig(chart2_name, dpi=300)
plt.close()
print(f"[ОК] График 2 успешно сохранен: {chart2_name}")