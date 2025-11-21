import  pandas as pd
import  re
import numpy as np
input_file = 'raw.xlsx'

# These are the exact column names in your file that contain the denominators
POPULATION_COL = 'ppl'    # population
GDP_COL        = 'gdp'    # GDP
ART_COL        = 'art'

pattern = re.compile(r'^[gpw]\d+$',re.IGNORECASE)

output_file = 'output/processed.xlsx'


if __name__ == '__main__':
    file = pd.read_excel(input_file)

    cp = file.copy()
    cp = cp.drop(cp.index[0])
    # cp = cp.drop(cp.index[-1])

    # for col in cp.columns:
    #     s = col.lower()
    #     if re.match(pattern, s):
    #         divisor = find_divisor(s)
    #         if divisor != 1:
    #             q = cp[s] / cp[divisor]
    #             if s[0] == 'w':
    #                 q *= 100
    #             cp[f'{s}.p'] = q
    #         else:
    #             continue
    base_cols = [col for col in cp.columns if pattern.match(col)]
    for col in base_cols:
        prefix = col[0].lower()
        target_col = f"{col}.p"

        if target_col not in cp.columns:
            print(f"Warning: Target col{target_col} not created")
            break
        
        if prefix == 'p':
            divisor_col = POPULATION_COL
        elif prefix == 'g':
            divisor_col = GDP_COL
        elif prefix == 'w':
            divisor_col = ART_COL
        else:
            continue

        divisor = cp[divisor_col]
        # cp[target_col] = cp[col] / divisor
        # Critical part: create a mask where divisor is zero or NaN → result will be NaN
        valid_divisor = divisor.copy()
        valid_divisor = valid_divisor.replace(0, np.nan)        # 0  → NaN
        valid_divisor = valid_divisor.fillna(np.nan)           # real NaN stays NaN

        # Perform division: anywhere divisor is NaN → result becomes NaN automatically
        cp[target_col] = cp[col] / valid_divisor

        # Optional: explicitly force NaN where original divisor was bad (extra safety)
        bad_divisor_rows = divisor.isin([0]) | divisor.isna()
        cp.loc[bad_divisor_rows, target_col] = np.nan

    cp.to_excel(output_file)


