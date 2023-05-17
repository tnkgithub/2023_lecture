#%%
from ortools.sat.python import cp_model

#%%
num_nurses = 10 # ナースの人数
num_shifts_pattern = 3 # 勤務パターン数、日勤、夜勤、深夜勤
num_days = 7 # 日数
num_nurses_per_day = 7 # 1日に必要な看護師の人数(日勤3人＋夜勤2人＋深夜勤2人)

nurses = range(num_nurses) # ナースのリスト
shifts_patterns = range(num_shifts_pattern) # 勤務パターンのリスト(日勤：0, 夜勤：1, 深夜勤：2)
days = range(num_days) # 日数のリスト

shift_requests = [
    [[0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 0]], # 看護師0
    [[0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]], # 看護師1
    [[0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1]], # 看護師2
    [[1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 1], [0, 1, 0], [0, 1, 0], [1, 0, 0]], # 看護師3
    [[0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 0]], # 看護師4
    [[0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 1, 0], [0, 1, 0], [1, 0, 1], [0, 0, 1]], # 看護師5
    [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 0], [0, 1, 0], [1, 0, 0]], # 看護師6
    [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 0]], # 看護師7
    [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, 1]], # 看護師8
    [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [1, 0, 0]]  # 看護師9
]

#%%
# モデルの作成
model = cp_model.CpModel()

#%%
'''
shifts[(n, d, s)]: 看護師nが日dにシフトsに割り当てられているかどうかを表す変数
# 割り当てられている場合は1、割り当てられていない場合は0
'''
shifts = {} # シフトの変数を格納する辞書
for n in nurses:
    for d in days:
        for s in shifts_patterns:
            shifts[(n, d, s)] = model.NewBoolVar(f"shift_n{n}_d{d}_s{s}")

#%%
# 制約条件の作成
'''
各時間帯に必要な看護師の人数の制約を追加
1日に3人の日勤、2人の夜勤、2人の深夜勤が必要とする
'''
for d in days:
    model.Add(sum(shifts[(n, d, 0)] for n in nurses) == 3) # 日勤の人数
    model.Add(sum(shifts[(n, d, 1)] for n in nurses) == 2) # 夜勤の人数
    model.Add(sum(shifts[(n, d, 2)] for n in nurses) == 2) # 深夜勤の人数

#%%
'''
各看護師が1日に1つのシフトしか割り当てられない制約を追加
'''
for n in nurses:
    for d in days:
        model.Add(sum(shifts[(n, d, s)] for s in shifts_patterns) == 1)

#%%
'''
(日勤３人＋夜勤２人＋深夜勤２人)×7日＝49コマ
ナースの人数10人×各人の勤務日数5日＝50コマ
よって、ナース9人は5日働き、1人は4日働く
'''
min_shifts_per_nurse = (num_nurses_per_day * num_days) // num_nurses # 最低勤務日数
print(min_shifts_per_nurse)
#%%
'''
各ナースの最低勤務日数と最大勤務日数を設定
今回は最低勤務日数が4日、最大勤務日数が5日
勤務日数が5日のナースが9人、4日のナースが1人となる
'''
not_enough_nurses = num_shifts_pattern * num_days % num_nurses # 全員が最低勤務日数を満たす場合の足りない人数
if not_enough_nurses == 0: # 全員が最低勤務日数を満たす場合
    max_shifts_per_nurse = min_shifts_per_nurse # 最大勤務日数も最低勤務日数と同じ
else: # 全員が最低勤務日数を満たさない場合
    max_shifts_per_nurse = min_shifts_per_nurse + 1 # 最大勤務日数(ナースによって勤務日数が異なる)

#%%
'''
各ナースの最低勤務日数と最大勤務日数の制約を追加
'''
for n in nurses:
    shifts_worked = []
    for d in days:
        for s in shifts_patterns:
            shifts_worked.append(shifts[(n, d, s)])
    model.Add(sum(shifts_worked) >= min_shifts_per_nurse) # 最低勤務日数の制約
    model.Add(sum(shifts_worked) <= max_shifts_per_nurse) # 最大勤務日数の制約

#%%
'''
目的関数のを作成
'''
model.Minimize(sum(shifts[(n, d, s)] * shift_requests[n][d][s] for n in nurses for d in days for s in shifts_patterns))

#%%
'''
ソルバーの作成と実行
'''
# Creates the solver and solve.
solver = cp_model.CpSolver()
status = solver.Solve(model)

#%%
if status == cp_model.OPTIMAL:
    print('Solution:')
    for d in days:
        print('Day', d)
        for n in nurses:
            for s in shifts_patterns:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    if shift_requests[n][d][s] == 1:
                        if s == 0:
                            print('Nurse', n, 'works shift', s, '(day).')
                        elif s == 1:
                            print('Nurse', n, 'works shift', s, '(night).')
                        else:
                            print('Nurse', n, 'works shift', s, '(late night).')
                    else:
                        print('Nurse', n, 'works shift', s, '(not requested).')
        print()
    print(f'Number of shift requests met = {solver.ObjectiveValue()}',
            f'(out of {num_nurses * min_shifts_per_nurse})')
else:
    print('No optimal solution found !')

#%%
