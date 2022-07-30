#!/usr/bin/env python3

import copy
import sys
from pathlib import Path
import shutil

from preprocessing import dataset as ds


def main(source, dest):
    source = Path(source)
    dest = Path(dest).resolve()
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)
    files = [s for s in source.iterdir() if s.name.endswith(".set")]
    print(str(len(files)) + ' files')

    for i, f in enumerate(files, start=1):
        print(f"Processing ({i}/{len(files)}) {f}")
        inname = str(f.resolve())
        tmpdat = ds(inname)
        tmpdat.loaddata()
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
        npy.segment(trllength=trllength, remove_artifact='no')
        npy.save(str(dest))


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        raise RuntimeError(f"Please specify input and output path, i.e. {sys.argv[0]} [INPUT_PATH] [OUTPUT_PATH]")
    main(sys.argv[1], sys.argv[2])
