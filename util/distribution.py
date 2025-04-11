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

def fill_zero(data):
    temp = [0 if np.isnan(x) else x for x in data]
    return np.array(temp).tolist()

def fill_mean(data):
    ar = np.array(data)
    mean = np.nanmean(data)
    ar = np.where(np.isnan(data),mean,ar)
    return ar.tolist()

class QuantileAdaption:
    def __init__(self, raw, method = fill_mean):
        self.raw = method(raw)
        self.scoring = pd.DataFrame()
        self.mid = pd.DataFrame()
        self.final = pd.DataFrame()
        # self.alphabet = {value:index for index,value in enumerate(self.country)}

    def compute(self):
        mid = pd.DataFrame({'raw_data':self.raw})
        filtered = self.raw
        mean, std = compute_mean_std(filtered)
        scores = standardize_with_clip(filtered,mean,std)
        for d in distribution:
            filtered = filter_distribution(filtered,scores,d)
            f_mean, f_std = compute_mean_std(filtered)
            scores = standardize_with_clip(filtered,f_mean,f_std) * d
            scores = scores.tolist()
            for i in range(len(filtered)):
                mid.loc[mid['raw_data'] == filtered[i], f'{d}_quantile'] = scores[i]
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
        self.mid = mid

    def create_final_score(self):
        final = pd.DataFrame()
        final['raw'] = self.raw
        final['final_score'] = self.mid.apply(
            lambda row: row.dropna().iloc[-1].round(0).astype(int), axis=1
        )
        final.loc[final['raw'] == 0,'final_score'] = 0
        self.final = final

if __name__ == '__main__':
    data = [
        10.0,
        9.0,
        7.0,
        5.0,
        6.0,
        9.0,
        4.0,
        7.0,
        1.0,
        3.0,
        2.0,
        1.0,
        2.0,
        0.0,
        4.0,
        7.0,
        1.0,
        2.0,
        2.0,
        3.0,
        8.0,
        1.0,
        5.0,
        1.0,
        3.0,
        1.0,
        3.0,
        1.0,
        3.0,
        1.0,
        0.0,
        1.0,
        3.0,
        1.0,
        1.0,
        1.0,
        5.0,
        0.0,
        0.0,
        0.0,
    ]
    q = QuantileAdaption(data)
    q.compute()
    q.create_final_score()
    pass