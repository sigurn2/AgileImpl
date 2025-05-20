import  pandas as pd
import  re

input_file = 'raw.xlsx'



condition = {
    'ppl' : [
        'p1', # D1.1 AI相关期刊会议发表数量&人均比例
        'p2', # AI相关文章作者数目
        'p3', # 全球AI人才undergraduate
        'p4', # graduate school
        'p5', # post-grad work
        'p6', # D1.3 AI专利授权数量&人均比例
        'p7', # D1.3 AI专利授权数量&人均比例
        'p8', # D2.1 托管数据中心数量&人均比例
        'p9', # D2.2非分布式超级计算机每秒浮点运算次数RMAX&人均比例
        'p10', # D2.2非分布式超级计算机每秒浮点运算次数RPEAK&人均比例
        'p11', # Coursera 技能报告 - 学习者数量（m）
    ],
    'gdp' : [
        'g1', # D1.4 AI系统研发数量&GDP比例 our world data
        'g2', # D3.1AI公司的资金规模2023年
        'g3', # D3.2AI初创公司数量2023年
        'g4', # 案例求和
        'g5', # D6.5 AI专项支出预算规模&GDP比例
        'g6', # D3.3 Global private investment in AI by geographic area, 2013–24 (sum)
        'g7', # Number of newly funded AI companies by geographic area, 2013–24 (sum)
    ],
    'art' : [
        'w1', # D17.1 AI治理主题的文献数量&总数比例
        'w2', # D17.2人工智能安全相关文献发表数数目
        'w3', # D17.3 AI与可持续发展主题的文献数量&文献总数比例
    ]
}
condition_1 = r"^[pgw]\d+$"

output_file = 'output/processed.xlsx'

def find_divisor(string):
    for k, v in condition.items():
        if string in v:
            return k
    return 1
if __name__ == '__main__':
    file = pd.read_excel(input_file)

    cp = file.copy()
    cp = cp.drop(cp.index[0])
    # cp = cp.drop(cp.index[-1])

    for col in cp.columns:
        s = col.lower()
        if re.match(condition_1, s):
            divisor = find_divisor(s)
            if divisor != 1:
                q = cp[s] / cp[divisor]
                if s[0] == 'w':
                    q *= 100
                cp[f'{s}.p'] = q
            else:
                continue

    cp.to_excel(output_file)


