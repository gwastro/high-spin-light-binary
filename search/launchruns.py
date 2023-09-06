#!/usr/env python
import subprocess
import sys
import glob

run = sys.argv[1]
chunk = sys.argv[2]
print(run, chunk)

if run == 'O1':
    data = 'data/data_O1.ini'
elif run == 'O2' and chunk == '15p':
    data = 'data/data_15p.ini'
elif run == 'O2' and int(chunk) <= 18:
    data = 'data/data_O2_twoifo.ini'
elif run == 'O2' and int(chunk) >= 19:
    data = 'data/data_O2.ini'
elif run == 'O3':
    data = 'data/data_O3.ini'
elif run == 'O3b':
    data = 'data/data_O3b.ini'

configs = glob.glob("config/*.ini")
configs.append("bank_highspin_bns.ini")
configs.append("times/gps_times_{}_analysis_{}.ini".format(run, chunk))
configs.append(data)
outdir = 'runs/{}/{}'.format(run, chunk)

print(outdir)
print(configs)
subprocess.run(["pycbc_make_coinc_search_workflow",
                "--workflow-name", "gw",
                "--output-dir", "{}".format(outdir),
		"--config-overrides", "results_page:output-path:{}/html/".format(outdir),
                "--config-files"] + configs)
