#%%
from constraint import Problem

# 定数
NUM_NURSES = 10  # ナースの人数
NUM_SHIFTS = 3  # 勤務パターンの数
DAYS_PER_WEEK = 7  # 週の日数
DAYS_PER_SHIFT = DAYS_PER_WEEK // NUM_SHIFTS  # 勤務パターンごとの日数
WORKING_DAYS_PER_WEEK = 5  # 1人のナースの1週間の勤務日数
REQUIRED_NURSES_PER_SHIFT = [3, 3, 2]  # 勤務パターンごとに必要なナースの人数

# ナースごとのシフト要望
nurse_shift_requests = [
    [0, 1, 2, 0, 1, 2, 0],  # ナース0のシフト要望（0: 日勤, 1: 夜勤, 2: 深夜勤）
    [1, 0, 2, 1, 0, 2, 1],  # ナース1のシフト要望
    [2, 1, 0, 2, 1, 0, 2],  # ナース2のシフト要望
    [0, 1, 2, 0, 1, 2, 0],  # ナース3のシフト要望
    [1, 0, 2, 1, 0, 2, 1],  # ナース4のシフト要望
    [2, 1, 0, 2, 1, 0, 2],  # ナース5のシフト要望
    [0, 1, 2, 0, 1, 2, 0],  # ナース6のシフト要望
    [1, 0, 2, 1, 0, 2, 1],  # ナース7のシフト要望
    [2, 1, 0, 2, 1, 0, 2],  # ナース8のシフト要望
    [0, 1, 2, 0, 1, 2, 0],  # ナース9のシフト要望

    # 以下、ナース3からナース9までのシフト要望を追加
]

# 勤務パターンのリストを生成
shift_patterns = []
for nurse in range(NUM_NURSES):
    for day in range(DAYS_PER_WEEK):
        shift_patterns.append((nurse, day % NUM_SHIFTS))

# 問題の定義
problem = Problem()

# ナースの勤務パターン変数を定義
variables = []
for nurse in range(NUM_NURSES):
    for shift in range(NUM_SHIFTS):
        variable_name = f"nurse_{nurse}_shift_{shift}"  # ユニークな変数名を生成
        problem.addVariable(variable_name, [0, 1])
        variables.append(variable_name)

# 各勤務時間帯に必要なナースの人数の制約を追加
for shift in range(NUM_SHIFTS):
    shift_variables = [variable for variable in variables if variable.endswith(f"shift_{shift}")]
    problem.addConstraint(
        lambda *shift_variables: sum(value == 1 for value in shift_variables) == REQUIRED_NURSES_PER_SHIFT[shift],
        shift_variables
    )

# 各ナースの1週間の勤務日数の制約を追加
for nurse in range(NUM_NURSES):
    nurse_variables = [variable for variable in variables if variable.startswith(f"nurse_{nurse}")]
    problem.addConstraint(
        lambda *nurse_variables: sum(value == 1 for value in nurse_variables) == WORKING_DAYS_PER_WEEK,
        nurse_variables
    )

#ナースのシフト要望の制約を追加
for nurse in range(NUM_NURSES):
    for day in range(DAYS_PER_WEEK):
        shift = nurse_shift_requests[nurse][day]
        if shift != -1:
            variable_name = f"nurse_{nurse}shift{shift}"
            problem.addConstraint(lambda value, variable_name=variable_name: value == 1, [variable_name])

#解の検索
solutions = problem.getSolutions()

#結果の出力
if len(solutions) > 0:
    for i, solution in enumerate(solutions):
        print(f"Solution {i+1}:")
        for day in range(DAYS_PER_WEEK):
            print(f"Day {day+1}:")
            for shift in range(NUM_SHIFTS):
                nurses = [int(variable.split("")[1]) + 1 for variable, value in solution.items() if variable.endswith(f"shift{shift}") and value == 1]
                print(f"Shift {shift+1}: Nurses {', '.join(map(str, nurses))}")
            print()
else:
    print("No valid solutions found.")
# %%
