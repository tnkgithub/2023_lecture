'''
前提条件
・人数：10人
・勤務パターン：3パターン（日勤、夜勤、深夜勤）
・日数：7日
拘束条件
・1週間の勤務日数：5日
・各勤務パターンごとの必要人数：(日勤：3人, 夜勤：2人, 深夜勤：2人)
'''
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


#%%
# モデルの定義
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
'''
各時間帯に必要な看護師の人数の制約を追加
1日に3人の日勤、2人の夜勤、2人の深夜勤が必要とする
'''
for d in days:
    model.Add(sum(shifts[(n, d, 0)] for n in nurses) == 3) # 日勤の人数
    model.Add(sum(shifts[(n, d, 1)] for n in nurses) == 2) # 夜勤の人数
    model.Add(sum(shifts[(n, d, 2)] for n in nurses) == 2) # 深夜勤の人数

#%%
# 各日には1つのシフトしか割り当てられないという制約を追加
for n in nurses:
    for d in days:
        model.Add(sum(shifts[(n, d, s)] for s in shifts_patterns) <= 1)

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

# %%
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

# %%
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0 # 線形緩和のレベルを0に設定
solver.parameters.enumerate_all_solutions = True # 全ての解を列挙する

# %%
def print_shifts(shifts):
    '''
    ナースのシフト表を表示する関数
    '''
    for d in days:
        print(f"Day {d}")
        for n in nurses:
            is_working = False
            for s in shifts_patterns:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    is_working = True
                    if s == 0:
                        print(f"  Nurse {n} works shift {s} (day)")
                    elif s == 1:
                        print(f"  Nurse {n} works shift {s} (night)")
                    else:
                        print(f"  Nurse {n} works shift {s} (late night)")
            if not is_working:
                print(f"  Nurse {n} does not work")
        print()

# %%
status = solver.Solve(model)
if status == cp_model.OPTIMAL:
    print_shifts(shifts)
    print()
    print(f"Optimal Schedule Length: {solver.ObjectiveValue()}") # 最適なシフト表の長さ
    print(f"Time: {solver.WallTime()}ms") # 時間
else:
    print("No optimal solution found!")
# %%