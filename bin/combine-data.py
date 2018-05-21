#!/usr/bin/python2

import collections, json, locale

locale.setlocale(locale.LC_ALL, 'en_US')

all_sysnames = ('\\\\sys-bypass', 'ext4-bypass', '\\\\sys-log', 'ext4-log')
sysname_map = {
    '\\\\sys-bypass'  : 'fscq-bypass',
    '\\\\sys-log'     : 'fscq-log',
    'ext4-bypass'     : 'ext4-async-bypass',
    'ext4-log'        : 'ext4-async-log',
}

data_files = {
    'largefile': 'data/largefile.json',
    'mailbench': 'data/mailbench.json',
    'largefile-ssd': 'data/largefile-ssd.json',
    'mailbench-ssd': 'data/mailbench-ssd.json',
}

fig_fields = ('largefile/largefile', 'mailbench/time')
ssd_fields = ('largefile-ssd/largefile', 'mailbench-ssd/time')
tbl_fields = ('largefile/avgwrite', 'largefile/avgsync', 
              'mailbench/avgwrite', 'mailbench/avgsync')

data = {}

def sel_data(data, s, n):
    (app, f) = n.split('/')
    return data[app][sysname_map[s]][f]

def pretty(n):
    if isinstance(n, int) or n.is_integer():
        return locale.format('%d', n, grouping=True)
    else:
        return locale.format('%.1f', n, grouping=True)

for (k, v) in data_files.iteritems():
    with open(v) as f:
      data[k] = json.loads(f.read())

with open('data/app.data', 'w') as f:
  f.write('"system" ' + ' '.join(['"%s"' % n for n in all_sysnames]) + '\n')
  for n in fig_fields:
    f.write('"\\\\cc{%s}" ' % n.split('/')[0] + \
        ' '.join(['%f' % sel_data(data, s, n) for s in all_sysnames]) + '\n')

with open('data/ssd.data', 'w') as f:
  f.write('"system" ' + ' '.join(['"%s"' % n for n in all_sysnames]) + '\n')
  for n in ssd_fields:
    f.write('"\\\\cc{%s}" ' % n.split('/')[0] + \
        ' '.join(['%f' % sel_data(data, s, n) for s in all_sysnames]) + '\n')


with open('data/io.tex', 'w') as f:
  f.write("""\\begin{tabular}{lrrrr}
\\toprule
  & \\multicolumn{2}{c}{\\bf \cc{largefile}}
  & \\multicolumn{2}{c}{\\bf \cc{mailbench}}
  \\\\
  & writes & syncs & writes & syncs \\\\
\midrule
""")
  for s in all_sysnames:
    f.write('%-12s & ' % s.replace('\\\\', '\\') + \
            ' & '.join(['%6s' % pretty(sel_data(data, s, n)) for n in tbl_fields]) + ' \\\\ \n')
  f.write("""\\bottomrule
\\end{tabular}
""")

