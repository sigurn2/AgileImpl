import numpy as np
import pandas as pd

distribution = [1,0.75,0.5,0.25]


def compute_mean_std(raw):
    mean = np.mean(raw)
    std = np.std(raw,ddof=1)
    return mean, std


def standardize_with_clip(raw, mean, std):
    standardized = [25 * (x - mean) / std + 50 for x in raw]
    clipped = np.clip(standardized,0,100)
    return clipped

def filter_distribution(raw,score,bound):
    filtered = [x for x,score in zip(raw,score) if score <= bound * 100]
    assert isinstance(filtered,list)
    return filtered

class QuantileAdaption:
    def __init__(self, raw):
        self.raw = raw
        self.scoring = pd.DataFrame({})
        self.mid = pd.DataFrame()
        self.final = pd.DataFrame()
        self.alphabet = {value:index for index,value in enumerate(raw)}

    def compute(self):
        filtered = self.raw
        mean, std = compute_mean_std(filtered)
        scores = standardize_with_clip(filtered,mean,std)
        for d in distribution:
            filtered = filter_distribution(filtered,scores,d)
            f_mean, f_std = compute_mean_std(filtered)
            scores = standardize_with_clip(filtered,f_mean,f_std) * d
            scoring_sheet = pd.DataFrame(
                {
                    "name":f'within_{d}_data',
                    'data':[filtered],
                    'mean':[f_mean],
                    'std':[f_std],
                    'score':[scores]
                 }
            )
            self.scoring = pd.concat([self.scoring,scoring_sheet]).reset_index(drop=True)

    def format(self):
        mid = pd.DataFrame()
        mid['raw'] = self.raw
        for index, row in self.scoring.iterrows():
            data = row['data']
            score = row['score']
            if len(data) == len(score):
                for d, s in zip(data,score):
                    posi = self.alphabet[d]
                    mid.loc[posi,index] = s
        self.mid = mid

    def create_final_score(self):
        final = pd.DataFrame()
        final['raw'] = self.raw
        final['final_score'] = self.mid.apply(
            lambda row: row.dropna().iloc[-1].round(0).astype(int), axis=1
        )
        final.loc[final['raw'] == 0,'final_score'] = 0
        self.final = final
        print(final)

if __name__ == '__main__':
    data = [1352481,957616,308276,416706,182837,154795,205201,176252,22956,130407,78402,10810,50307,11401]
    q = QuantileAdaption(data)
    q.compute()
    q.format()
    q.create_final_score()