#!/usr/bin/env python3

import copy
import os
import sys
from multiprocessing import Pool
from pathlib import Path
import shutil

from preprocessing import dataset as ds

print(sys.argv)
if len(sys.argv) != 3:
    raise RuntimeError(f"Please specify input and output path, i.e. {sys.argv[0]} [INPUT_PATH] [OUTPUT_PATH]")
source = Path(sys.argv[1])
dest = Path(sys.argv[2]).resolve()
shutil.rmtree(dest, ignore_errors=True)


def process_file(f):
    inname = str(f.resolve())
    tmpdat = ds(inname)
    tmpdat.loaddata(data_ch_cnt=26)
    tmpdat.bipolarEOG()
    tmpdat.apply_filters()
    tmpdat.correct_EOG()
    tmpdat.detect_emg()
    tmpdat.detect_jumps()
    tmpdat.detect_kurtosis()
    tmpdat.detect_extremevoltswing()
    tmpdat.residual_eyeblinks()
    tmpdat.define_artifacts()

    trllength = 1
    npy = copy.deepcopy(tmpdat)
    npy.segment(trllength=trllength, remove_artifact=True)
    out_folder = dest / f.relative_to(source).parent
    out_folder.mkdir(parents=True, exist_ok=True)
    npy.save(str(out_folder.resolve()))


def main():
    # dest.mkdir(parents=True, exist_ok=True)
    files = list(source.rglob("*.edf"))
    print(f"Processing {len(files)} files")

    for f in files:
        process_file(f)
    # pool = Pool(min(len(files), os.cpu_count() // 2))
    # results = pool.imap_unordered(process_file, files)
    #
    # for i, res in enumerate(results, start=1):
    #     print(f"Processed ({i}/{len(files)}) {res}")
    # print("All done!")


if __name__ == "__main__":
    main()
