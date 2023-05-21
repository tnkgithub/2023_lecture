#%%
"""ナーススケジューリング問題"""
from ortools.sat.python import cp_model


def main():
    num_nurses = 10 # ナースの人数
    num_shifts = 3 # 勤務パターン数、日勤、夜勤、深夜勤
    num_days = 7 # 日数
    num_shifts_per_day = 7 # 1日に必要な看護師の人数(日勤3人＋夜勤2人＋深夜勤2人)
    all_nurses = range(num_nurses) # ナースのリスト
    all_shifts = range(num_shifts) # 勤務パターンのリスト(日勤：0, 夜勤：1, 深夜勤：2)
    all_days = range(num_days) # 日数のリスト
    # 各ナースのシフト要望 [日勤, 夜勤, 深夜勤]
    shift_requests = [[[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1]],
                        [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],[0, 0, 0], [0, 0, 1]],
                        [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],[0, 1, 0], [0, 0, 0]],
                        [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],[1, 0, 0], [0, 0, 0]],
                        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],[0, 1, 0], [0, 0, 0]],
                        [[1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0],[0, 0, 1], [0, 1, 0]],
                        [[0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0],[0, 0, 0], [1, 0, 0]],
                        [[0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 1, 0],[0, 0, 0], [0, 0, 1]],
                        [[0, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],[0, 1, 0], [0, 0, 0]],
                        [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0],[0, 0, 0], [0, 1, 0]]
                        ]

    # モデルの作成
    model = cp_model.CpModel()

    # 各ナースの各日の各シフトの割り当てを表すブール変数を作成
    # shifts[10人のナース、7日間、3つのシフト]
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # 各シフトの人数の制約
    # 日勤：3人、夜勤：2人、深夜勤：2人
    for d in all_days:
        model.Add(sum(shifts[(n, d, 0)] for n in all_nurses) == 3)
        model.Add(sum(shifts[(n, d, 1)] for n in all_nurses) == 2)
        model.Add(sum(shifts[(n, d, 2)] for n in all_nurses) == 2)

    # 各看護師は1日に1つのシフトしか担当しない
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # 各看護師は1週間に5日以上働かない
    #for n in all_nurses:
    #    model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_shifts) <= 5)


    # 各ナースは、最低限必要なシフト数以上、最大限必要なシフト数以下で働く
    min_shifts_per_nurse = (num_shifts_per_day * num_days) // num_nurses # 1日に必要な看護師の人数×日数÷看護師の人数の商
    if num_shifts * num_days % num_nurses == 0: # 割り切れる場合
        max_shifts_per_nurse = min_shifts_per_nurse # 最大限必要なシフト数＝最低限必要なシフト数
    else: # 割り切れない場合
        max_shifts_per_nurse = min_shifts_per_nurse + 1 # 最大限必要なシフト数＝最低限必要なシフト数＋１
    for n in all_nurses:
        num_shifts_worked = 0
        for d in all_days:
            for s in all_shifts:
                num_shifts_worked += shifts[(n, d, s)] # 各ナースの各日の各シフトの割り当てを表すブール変数を足し合わせる
        model.Add(min_shifts_per_nurse <= num_shifts_worked) # 最低限必要なシフト数以上
        model.Add(num_shifts_worked <= max_shifts_per_nurse) # 最大限必要なシフト数以下

    # 目的関数を最大化
    model.Maximize(
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_nurses
            for d in all_days for s in all_shifts))

    # ソルバーの作成と解の探索
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 結果の出力
    if status == cp_model.OPTIMAL:
        print('Solution:')
        for d in all_days:
            print('Day', d+1)
            for s in all_shifts:
                for n in all_nurses:
                    if solver.Value(shifts[(n, d, s)]) == 1: # 割り当てられたシフトの場合
                        if shift_requests[n][d][s] == 1: # 希望シフトの場合
                            if s == 0:
                                print('Nurse', n, 'works shift day (requested).')
                            elif s == 1:
                                print('Nurse', n, 'works shift night (requested).')
                            else:
                                print('Nurse', n, 'works shift midnight (requested).')
                        else: # 希望シフトでない場合
                            if s == 0:
                                print('Nurse', n, 'works shift day (not requested).')
                            elif s == 1:
                                print('Nurse', n, 'works shift night (not requested).')
                            else:
                                print('Nurse', n, 'works shift midnight (not requested).')
            print() # 改行
        # 各ナースの各日の各シフトの割り当てを表すブール変数を足し合わせる
        print(f'Number of shift requests met = {solver.ObjectiveValue()}',
              f'(out of {num_nurses * min_shifts_per_nurse})')
    else:
        print('No optimal solution found !')

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts()) # コンフリクト数
    print('  - branches : %i' % solver.NumBranches()) # ブランチ数
    print('  - wall time: %f s' % solver.WallTime()) # 実行時間


if __name__ == '__main__':
    main()
# %%
