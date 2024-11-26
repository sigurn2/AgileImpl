import  pandas as pd


input_file = 'raw.xlsx'


df = pd.read_excel(input_file)

condition = {
    'ppl' : [
        'pa','pa.i','pa.p','pa.ii', # 论文发表数量
        'pb','pb.i','pb.p','pb.ii', # AI相关文章作者数目
        'pc','pc.i','pc.p','pc.ii', # AI专利授权数量
        'pd','pd.i','pd.p','pd.ii', # 托管数据中心数量、人均比例
        'pd','pd.i','pd.p','pd.ii', # AI与可持续发展主题的文献数量&人均比例

    ],
    'gdp' : [
        'ga','ga.i','ga.p','ga.ii', # AI公司企业融资规模&GDP比例；
        'gb','gb.i','gb.p','gb.ii', # AI初创公司数量、发展水平，GDP比例
        'gc','gc.i','gc.p','gc.ii', # AI初创公司数量、发展水平，GDP比例
        'gd','gd.i','gd.p','gd.ii', # 风险案例事故数量&GDP比例
        'ge','ge.i','ge.p','ge.ii', # 风险案例事故数量&GDP比例
    ],
    'pro' : [
        'ra','ra.i','ra.p','ra.ii' # 开放AI模型以及数据集
        'rb','rb.i','rb.p','rb.ii' # AI开发者社区
    ],
    'art' : [
        'aa','aa.i','aa.p','aa.ii' # AI治理，伦理与政策相关论文数目

    ],
    'util' : [
        'ua','ua.i', # 性别比例
        'ub','ub.i', # 公众信任度
        'uc','uc.i', # 公众对AI应用与影响的了解水平
    ]
}

input_file = 'raw.xlsx'
output_file = 'processed.xlsx'
if __name__ == '__main__':
    file = pd.read_excel(input_file)
    cp = file.copy()
    for col in cp.columns:
        pass
