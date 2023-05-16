#%%
import random

# ナースの名前と勤務パターンを定義
nurses = {
    'Nurse1': ['day', 'day', 'day', 'day', 'night', 'night', 'night'],
    'Nurse2': ['day', 'day', 'day', 'night', 'night', 'night', 'day'],
    'Nurse3': ['day', 'day', 'night', 'night', 'night', 'day', 'day'],
    'Nurse4': ['day', 'night', 'night', 'night', 'day', 'day', 'day'],
    'Nurse5': ['night', 'night', 'night', 'day', 'day', 'day', 'day'],
    'Nurse6': ['night', 'night', 'day', 'day', 'day', 'day', 'night'],
    'Nurse7': ['night', 'day', 'day', 'day', 'day', 'night', 'night'],
    'Nurse8': ['day', 'night', 'day', 'night', 'night', 'day', 'day'],
    'Nurse9': ['night', 'day', 'night', 'day', 'day', 'day', 'night'],
    'Nurse10': ['day', 'day', 'night', 'night', 'day', 'night', 'day']
}

# 各シフトに必要な人数
shift_requirements = {
    'day': 4,
    'night': 3,
    'late_night': 2
}

# 初期スケジュールを生成する関数
def generate_schedule(nurses, shift_requirements):
    schedule = {}
    shifts = list(shift_requirements.keys())
    # 各シフトに必要な人数を計算し、人数の多いシフトから順に優先度をつける
    sorted_shifts = sorted(shifts, key=lambda x: shift_requirements[x], reverse=True)
    for shift in sorted_shifts:
        # まだシフトが割り当てられていないナースを取得
        unassigned_nurses = [nurse for nurse in nurses if shift not in schedule.get(nurse, [])]
        while len(unassigned_nurses) > 0:
            # 未割り当てのシフトがあるナースをランダムに選び、そのナースにシフトを割り当てる
            nurse = random.choice(unassigned_nurses)
            schedule.setdefault(nurse, []).append(shift)
            # もしナースの勤務日数が５日を超える場合、そのナースの割り当てを取り消す
            if len(schedule[nurse]) > 5:
                schedule[nurse].remove(shift)
            # シフトが埋まったら、未割り当てのナースから削除する
            if len(schedule[nurse]) == len(shift_requirements):
                unassigned_nurses.remove(nurse)
    return schedule

schedule = generate_schedule(nurses, shift_requirements)
print(schedule)


# %%
# パッケージを利用したもの
from ortools.sat.python import cp_model
import random

# ナースの人数と勤務パターン
nurses = 10
shift_types = ["日勤", "夜勤", "深夜勤"]
shift_requirements = {"日勤": 4, "夜勤": 3, "深夜勤": 2}
days_per_week = 5
shifts_per_day = 3

model = cp_model.CpModel()

# 変数の定義
shifts = {}
for n in range(nurses):
    for d in range(days_per_week * shifts_per_day):
        shifts[(n, d)] = model.NewIntVar(0, len(shift_types) - 1, f"shift_n{n}_d{d}")

# 目的関数
model.Minimize(0)

# 一人が1日に1回しか勤務しない制約
for n in range(nurses):
    for d in range(shifts):
        model.Add(sum(shifts[(n, d)] for d in range(shifts)) <= 1)

# 1週間の勤務日数が5日である制約
for n in range(nurses):
    model.Add(sum(shifts[(n, d)] for d in range(shifts)) == days_per_week)

# 勤務希望の日数が5日である制約
for n in range(nurses):
    for d in range(shifts):
        model.Add(shifts[(n, d)] >= 0)
        model.Add(shifts[(n, d)] <= 1)

# 勤務人数が必要人数以上である制約
for d in range(shifts):
    for s in range(len(shift_types)):
        model.Add(sum(shifts[(n, d)] == s for n in range(nurses)) >= shift_requirements[shift_types[s]])

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    for n in range(nurses):
        nurse_shifts = [shift_types[solver.Value(shifts[(n, d)])] for d in range(shifts)]
        print(f"Nurse {n+1} shifts: {nurse_shifts}")
else:
    print("No solution found.")

# %%
