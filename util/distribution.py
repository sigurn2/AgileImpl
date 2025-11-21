import numpy as np
import pandas as pd

distribution = [1,0.75,0.5,0.25]


def compute_mean_std(raw):
    mean = np.nanmean(raw)
    std = np.nanstd(raw,ddof=1)
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

# class QuantileAdaption:
#     def __init__(self, raw, method = fill_mean):
#         self.raw = raw
#         self.scoring = pd.DataFrame()
#         self.mid = pd.DataFrame()
#         self.final = pd.DataFrame()
#         # self.alphabet = {value:index for index,value in enumerate(self.country)}

#     def compute(self):
#         mid = pd.DataFrame({'raw_data':self.raw})
#         filtered = self.raw
#         mean, std = compute_mean_std(filtered)
#         scores = standardize_with_clip(filtered,mean,std)
#         for d in distribution:
#             filtered = filter_distribution(filtered,scores,d)
#             f_mean, f_std = compute_mean_std(filtered)
#             scores = standardize_with_clip(filtered,f_mean,f_std) * d
#             scores = scores.tolist()
#             for i in range(len(filtered)):
#                 mid.loc[mid['raw_data'] == filtered[i], f'{d}_quantile'] = scores[i]
#             scoring_sheet = pd.DataFrame(
#                 {
#                     "name":f'within_{d}_data',
#                     'data':[filtered],
#                     'mean':[f_mean],
#                     'std':[f_std],
#                     'score':[scores]
#                  }
#             )
#             self.scoring = pd.concat([self.scoring,scoring_sheet]).reset_index(drop=True)
#         self.mid = mid

#     def create_final_score(self):
#         final = pd.DataFrame()
#         final['raw'] = self.raw

#         # Get all quantile columns (they have names like '1_quantile', '0.75_quantile', etc.)
#         quantile_cols = [col for col in self.mid.columns if '_quantile' in col]

#         if not quantile_cols:
#             # No quantiles computed at all (edge case)
#             final['final_score'] = np.nan
#         else:
#             # Sort columns by distribution value descending so the "last" one is the smallest bucket
#             quantile_cols = sorted(quantile_cols, key=lambda x: float(x.split('_')[0]), reverse=True)

#             def get_last_quantile_score(row):
#                 # Look only at quantile columns
#                 quantile_values = row[quantile_cols]
#                 # Drop NaN, then take the last valid one (which corresponds to deepest surviving bucket)
#                 valid = quantile_values.dropna()
#                 if valid.empty:
#                     # Never survived any filter → treat as worst / 0
#                     return 0
#                 else:
#                     return int(round(valid.iloc[-1]))

#             final['final_score'] = self.mid.apply(get_last_quantile_score, axis=1)

#         # Optional: explicitly set score 0 for raw == 0
#         final.loc[final['raw'] == 0, 'final_score'] = 0

#         self.final = final
#         print(final)
class QuantileAdaption:
    def __init__(self, raw):
        self.raw = list(raw)                     # keep original order + NaNs
        self.mid = pd.DataFrame({'raw': self.raw})
        self.scoring = pd.DataFrame()
        self.final = pd.DataFrame()

    def compute(self):
        values = np.array(self.raw, dtype=float)   # support NaN
        valid_mask = ~np.isnan(values)             # True where value is real

        # Initial standardization on all valid data
        mean, std = compute_mean_std(values[valid_mask])
        scores = standardize_with_clip(values, mean, std)

        for d in distribution:
            # Which values survive this quantile (top d*100% by current score)
            survive_mask = (scores <= d * 100) & valid_mask

            # Update the surviving values for next iteration
            current_values = values[survive_mask]

            # Re-standardize only the survivors
            mean, std = compute_mean_std(current_values)
            new_scores = standardize_with_clip(current_values, mean, std) * d

            # Write scores back to the original positions
            col_name = f'{d}_quantile'
            self.mid[col_name] = np.nan                     # default: no score
            survived_indices = np.where(survive_mask)[0]     # original positions
            self.mid.loc[survived_indices, col_name] = new_scores

            # Optional: track intermediate stats
            self.scoring = pd.concat([self.scoring, pd.DataFrame([{
                "quantile": d,
                "count": len(current_values),
                "mean": mean,
                "std": std,
            }])], ignore_index=True)

            # Update scores and mask for next round
            scores = scores.copy()
            scores[~survive_mask] = np.inf   # non-survivors get infinite score → won't pass next filter
            valid_mask = survive_mask        # only survivors remain valid

    def create_final_score(self):
        quantile_cols = [f'{d}_quantile' for d in distribution]

        final_scores = (
            self.mid[quantile_cols]
            .bfill(axis=1)      # deepest surviving score fills leftward
            .iloc[:, 0]         # take the score from the tightest bucket the value entered
            # ← NO .fillna(), NO .round(), NO .astype(int)
        )

        # Only override raw == 0 values (your original rule)
        final_scores = final_scores.where(self.mid['raw'] != 0, 0)

        self.final = pd.DataFrame({
            'raw': self.raw,
            'final_score': final_scores
        })

        print(self.final)

if __name__ == '__main__':
    data = [
400,
238,
141,
320,
205,
281.3333333,
130,
248,
328,
184,
230,
132,
206,
184,
218,
238,
176,
62,
150,
154.6666667,
63,
40,
89,
212,
48,
154,
130,
216,
133,
156,
149,
222,
156,
150,
220,
84,
107,
30,
124,
58,

    ]
    q = QuantileAdaption(data)
    q.compute()
    q.create_final_score()
    pass