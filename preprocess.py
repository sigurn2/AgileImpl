import  pandas as pd
import  re

input_file = 'raw.xlsx'



condition = {
    'ppl' : [
        'pa', # 论文发表数量
        'pb', # AI相关文章作者数目
        'pc', # AI专利授权数量
        'pd', # 托管数据中心数量、人均比例
        'pe', # AI与可持续发展主题的文献数量&人均比例

    ],
    'gdp' : [
        'ga', # AI公司企业融资规模&GDP比例；
        'gb', # AI初创公司数量、发展水平，GDP比例
        'gc', # AI初创公司数量、发展水平，GDP比例
        'gd', # 风险案例事故数量&GDP比例
        'ge', # 风险案例事故数量&GDP比例
    ],
    'pro' : [
        'ra', # 开放AI模型以及数据集
        'rb', # AI开发者社区
    ],
    'art' : [
        'aa' # AI治理，伦理与政策相关论文数目

    ],
    # 'util' : [
    #     'ua','ua.i', # 性别比例
    #     'ub','ub.i', # 公众信任度
    #     'uc','uc.i', # 公众对AI应用与影响的了解水平
    # ]
}
condition_1 = r'[pgura][abcde](?!\S)'

input_file = 'raw.xlsx'
output_file = 'processed.xlsx'

def find_divisor(string):
    for k, v in condition.items():
        if string in v:
            return k
    return 1
if __name__ == '__main__':
    file = pd.read_excel(input_file)

    cp = file.copy()
    cp = cp.drop(cp.index[0])
    cp = cp.drop(cp.index[-1])

    for col in cp.columns:
        s = col.lower()
        if re.match(condition_1, s):
            divisor = find_divisor(s)
            if divisor != 1:
                cp[f'{s}.p'] = cp[s] / cp[divisor]
            else:
                continue

    cp.to_excel(output_file)


