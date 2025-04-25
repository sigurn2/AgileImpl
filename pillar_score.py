import pandas as pd

from util.clip import clipper

dimension = {
    'd1.1': [
        'p1.i',
        'p1.p.ii'
    ],
    'd1.2': [
        'p2.i',
        'p2.p.ii',
        'p3.i',
        'p3.p.ii',
        'p4.i',
        'p4.p.ii',
        'p5.i',
        'p5.p.ii',
    ],
    'd1.3': [
        'p6.i',
        'p6.p.ii',
        'p7.i',
        'p7.p.ii',
    ],
    'd1.4': [
        'g1.i',
        'g1.p.ii',

    ],
    'd2.1':[
        'p8.i',
        'p8.p.ii',
    ],
    'd2.2': [
        'p9.i',
        'p9.p.ii',
        'p10.i',
        'p10.p.ii',
    ],
    'd3.1':[
        'g2.i',
        'g2.p.ii',
    ],
    'd3.2': [
        'g3.i',
        'g3.p.ii',
    ],
    # ----------------- 202504221 add sum of investment on ai ----------------  #
    'd3.3': [
        'g6.i',
        'g6.p.ii',
    ],
    'd3.4': [
        'g7.i',
        'g7.p.ii',
    ],
    # ----------------- end of comment --------------------------------------- #
    'd4.1':[
        'g4.i',
        'g4.p.ii',
    ],
    'd6.5':[
        'g5.i',
        'g5.p.ii',
    ],
    'd9.2':[
        'u1.i',
    ],
    'd12.1':[
        'u2.i',
    ],
    'd13.1':[
        'u3.i',
        'u4.i',
        'p11.i',
        'p11.p.ii',
    ],
    'd13.2':[
        'u5.i',
    ],
    'd13.3':[
        'u6.i',
        'u7.i',
        'u8.i',
    ],
    'd14.1':[
        'u9.i',
        'u10.i',
        'u11.i',
    ],
    'd14.2':[
        'u12.i',
        'u13.i',
        'u14.i',
        'u15.i',
        'u16.i',
        'u17.i',
        'u18.i',
        'u19.i',
        'u20.i',
        'u21.i',
        'u22.i',
        'u23.i',
        'u24.i',
        'u25.i',
        'u26.i',
    ],
    'd14.3':[
        'u27.i',
        'u28.i',
    ],
    'd14.4':[
        'u29.i',
        'u30.i',
    ],
    'd15.1':[
        'u31.i',
    ],
    'd15.2':[
        'u32.i',
        'u33.i',
        'u34.i',
    ],
    'd15.3':[
        'u35.i',
    ],
    'd15.4':[
        'u36.i',
    ],
    'd15.5':[
        'u37.i',
    ],
    'd16.1':[
        'u38.i',
        'u39.i',
    ],
    'd16.2':[
        'u40.i',
    ],
    'd17.1':[
        'w1.i',
        'w1.p.ii',
    ],
    'd17.2':[
        'w2.i',
        'w2.p.ii',
    ],
    'd17.3':[
        'w3.i',
        'w3.p.ii',
    ]
}
a_dimension = {
    'a1': [
        'd1.1',
        'd1.2',
        'd1.3',
        'd1.4'
    ],
    'a2': [
        'd2.1',
        'd2.2',
        'd2.3',
    ],
    'a3': [
        'd3.1',
        'd3.2',
        'd3.3',
        'd3.4',
    ],
    'a4': [
        'd4.1',
    ],
    'a5': [
        'd5.1',
        'd5.2',
        'd5.3',
    ],
    'a6': [
        'd6.1',
        'd6.2',
        'd6.3',
        'd6.4',
        'd6.5',
    ],
    'a9': [
        'd9.1',
        'd9.2',
    ],
    'a11':[
        'd11.1',
        'd11.2',
        'd11.3',
    ],
    'a12': [
        'd12.1',
        'd12.2',
    ],
    'a13': [
        'd13.1',
        'd13.2',
        'd13.3',
    ],
    'a14': [
        'd14.1',
        'd14.2',
        'd14.3',
        'd14.4',
    ],
    'a15': [
        'd15.1',
        'd15.2',
        'd15.3',
        'd15.4',
        'd15.5'
    ],
    'a16': [
        'd16.1',
        'd16.2',
    ],
    'a17': [
        'd17.1',
        'd17.2',
        'd17.3',
    ]
}
f_dimension = {
    'a1':'m1',
    'a2':'m2',
    'a3':'m3',
    'a4':'m4',
    'a5':'m5',
    'a6':'m6',
    'a9':'m9',
    'a11':'m11',
    'a12':'m12',
    'a13':'m13',
    'a14':'m14',
    'a15':'m15',
    'a16':'m16',
    'a17':'m17',
}
pillar = {
    'pillar1':[
        'm1',
        'm2',
        'm3',
    ],
    'pillar2':[
        'm4',
        'm5'
    ],
    'pillar3':[
        'm6',
        'm7',
        'm8',
        'm9',
        'm10',
        'm11',
        'm12',
    ],
    'pillar4':[
        'm13',
        'm14',
        'm15',
        'm16',
        'm17',
    ]
}
agile = {
    'agile':[
        'pillar1',
        'pillar2',
        'pillar3',
        'pillar4',
    ]
}
input_file = 'final_score_mean.xlsx'
output_file = 'pillar_score.xlsx'

if __name__ == '__main__':
    f = pd.read_excel(input_file)
    cp = f.copy()
    for dim,itm in dimension.items():
        total = 0
        for i in itm:
            total += cp[i]

        cp[dim] = total/len(itm)
    for av, itm in a_dimension.items():
        total = 0
        for i in itm:
            total += cp[i]
        cp[av] = total/len(itm)
    for a,m in f_dimension.items():
        data = cp[a]
        cp[m] = clipper(data)
        if m == 'm4':
            cp[m] = 100 - cp[m]
    for p, m in pillar.items():
        total = 0
        for i in m:
            total += cp[i]
        cp[p] = total/len(m)
    for k, v in agile.items():
        total = 0
        for i in v:
            total += cp[i]
        cp[k] = total/len(v)
    cp.to_excel(output_file)


