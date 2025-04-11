import pandas as pd
import re
from util.distribution import QuantileAdaption
input_file = 'processed.xlsx'
final_file = 'final_score_mean.xlsx'
condition_1 = r"^[pgwu]\d+$"  # 得到未除过系数的列
condition_2 = r".*\.p$" # 得到除过系数的列

if __name__ == '__main__':
    f = pd.read_excel(input_file)
    cp = f.copy()
    for row in cp.columns:
        s = row.lower()
        try:
            if re.match(condition_1, s):
                if s == 'u5':
                    pass
                q = QuantileAdaption(cp[row].tolist())
                q.compute()
                q.create_final_score()
                score = q.final['final_score']
                cp[f'{s}.i'] = score
            if re.match(condition_2, s):
                q = QuantileAdaption(cp[row])
                q.compute()
                q.create_final_score()
                score = q.final['final_score']
                cp[f'{s}.ii'] = score
        except Exception as e:
            print(s)
            pass
    cp.to_excel(final_file)
