#%%
from ortools.sat.python import cp_model

# %%
num_nurses = 10 # ナースの人数
num_shifts = 3 # 勤務パターン数、日勤、夜勤、深夜勤
num_days = 7 # 日数

# 各ナースのシフト要望 [日勤, 夜勤, 深夜勤]
shift_requests = [
    [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1]],
    [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1]],
    [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[0, 0, 1], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0]],
    [[1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 0, 0]],
    [[1, 1, 0], [0, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 1]],
    [[0, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]],
    [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0]]
]

# モデルの作成
model = cp_model.CpModel()

# 各ナースの各日の各シフトの割り当てを表すブール変数を作成
# shifts[10人のナース、7日間、3つのシフト]

shifts = {}
for n in range(num_nurses):
    for d in range(num_days):
        for s in range(num_shifts):
            shifts[(n, d, s)] = model.NewBoolVar("shift_bool")

print(shifts)

#%%
# 各シフトの人数の制約
for d in range(num_days):
    model.Add(sum(shifts[(n, d, 0)] for n in range(num_nurses)) == 3)
    model.Add(sum(shifts[(n, d, 1)] for n in range(num_nurses)) == 2)
    model.Add(sum(shifts[(n, d, 2)] for n in range(num_nurses)) == 2)

# 各看護師は1日に1つのシフトしか担当しない
for n in range(num_nurses):
    for d in range(num_days):
        model.Add(sum(shifts[(n, d, s)] for s in range(num_shifts)) <= 1)

# 各ナースの出勤日数の制約
for n in range(num_nurses):
    model.Add(sum(shifts[(n, d, s)]
                  for d in range(num_days)
                  for s in range(num_shifts)) >= 4)

    model.Add(sum(shifts[(n, d, s)]
                  for d in range(num_days)
                  for s in range(num_shifts)) <= 5)


# 目的関数を最大化
model.Maximize(
    sum(shift_requests[n][d][s] * shifts[(n, d, s)]
        for n in range(num_nurses)
        for d in range(num_days)
        for s in range(num_shifts))
)

# ソルバーの作成と解の探索
solver = cp_model.CpSolver()
result = solver.Solve(model)

# 結果の出力
if result == cp_model.OPTIMAL:
    print('Solution:')
    for d in range(num_days):
        print('Day', d+1)
        for s in range(num_shifts):
            if s == 0:
                print('Shift: day')
            elif s == 1:
                print('Shift: night')
            else:
                print('Shift: midnight')
            for n in range(num_nurses):
                if solver.Value(shifts[(n, d, s)]) == 1: # シフトが割り当てられている場合
                    if shift_requests[n][d][s] == 1: # 希望シフトの場合
                            print('  Nurse', n, '(requested).')
                    else: # 希望シフトでない場合
                            print('  Nurse', n, '(not requested).')
        print()
else:
    print('No optimal solution found !')

# Statistics.
print('\nStatistics')
print('  - conflicts: %i' % solver.NumConflicts()) # コンフリクト数
print('  - branches : %i' % solver.NumBranches()) # ブランチ数
print('  - wall time: %f s' % solver.WallTime()) # 実行時間

# %%
