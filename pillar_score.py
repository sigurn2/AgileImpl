import pandas as pd
import data_mapping
import numpy as np
from util.distribution import QuantileAdaption


input_file = 'output/final_score_mean.xlsx'
output_file = 'output/pillar_score.xlsx'

if __name__ == '__main__':
    f = pd.read_excel(input_file)
    df = f.copy()
# Helper: apply "benefit of doubt" imputation + averaging
    def impute_and_average(group_cols, result_col):
        # Ensure all columns exist
        valid_cols = [c for c in group_cols if c in df.columns]
        if not valid_cols:
            df[result_col] = np.nan
            print(f"  → {result_col}: no valid columns → NaN")
            return

        data = df[valid_cols].copy()

        # Check if there is ANY missing value in this group (across all rows and cols)
        had_missing = data.isna().any().any()   # True if at least one NaN existed

        constrains = [
            # data_mapping.indicator_mapping.keys(),
            # data_mapping.pillar_mapping.keys(),
            "pillar2",
            "pillar3",
            "pillar1",
            "pillar4",
            "m1",
            "m2",
            "m3",
            "m4",
            "m5",
            # "m3",
            # "m2",
            # "m5",
            # "d5.1"
        ]
        if not had_missing or result_col in constrains :
            # ------------------------------------------------------------------
            # CASE 1: No missing data → simple average, no imputation needed
            # ------------------------------------------------------------------
            df[result_col] = data.mean(axis=1)
            print(f"  → {result_col} = simple average (no missings)")
        else:
            # ------------------------------------------------------------------
            # CASE 2: There were missings → benefit-of-doubt + QuantileAdaption
            # ------------------------------------------------------------------
            # 1. First preliminary average (using available data only)
            first_avg = data.mean(axis=1, skipna=True)

            # 2. Impute all missing sub-scores with this preliminary average
            for col in valid_cols:
                missing_mask = df[col].isna()
                if missing_mask.any():
                    df.loc[missing_mask, col] = first_avg[missing_mask]

            # 3. Now compute the temporary equal-weighted average
            temp_avg = df[valid_cols].mean(axis=1, skipna=False)

            # 4. Apply your sophisticated QuantileAdaption method
            q = QuantileAdaption(temp_avg)
            q.compute()
            q.create_final_score()
            final_score = q.final['final_score']

            # 5. Store the quantile-adjusted score
            df[result_col] = final_score

            print(f"  → {result_col} = QuantileAdaption score (had missings → imputed + adjusted)")
        if result_col == 'm4':
            df[result_col] = 100 - df[result_col]

    for dim, cols in data_mapping.dimension_mapping.items():
        scored_cols = [c for c in cols]
        impute_and_average(scored_cols, dim)    

    for ind, dims in data_mapping.indicator_mapping.items():
        scored_cols = [c for c in dims]
        impute_and_average(scored_cols, ind)

    for pillar, inds in data_mapping.pillar_mapping.items():
        scored_cols = [c for c in inds]
        impute_and_average(scored_cols, pillar)


    df['agile'] = df[['pillar1', 'pillar2', 'pillar3', 'pillar4']].mean(axis=1, skipna=True)

    df.to_excel(output_file)



