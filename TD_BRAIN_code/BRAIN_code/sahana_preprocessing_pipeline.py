#!/usr/bin/env python3

from autopreprocessing import dataset as ds
import os
from pathlib import Path
import numpy as np
import copy
import sys


def autopreprocess_standard(source, dest):
    subs = [s for s in os.listdir(source) if os.path.isdir(os.path.join(
        source, s)) if not any([e in s for e in ['preprocessed', 'results', 'DS']])]
    subs = np.sort(subs)
    print(str(len(subs))+' subjects')
    k = 0
    for i, sub in enumerate(subs):
        print(f'[INFO]: processing subject: {i} of {len(subs)}')
        # sessions = [session for session in os.listdir(os.path.join(source, sub)) if not any([e in session for e in ['preprocessed', 'results', 'DS']])]
        conditions = []
        allconds = np.array([conds for conds in os.listdir(os.path.join(source, sub)) if not any([e in conds for e in ['preprocessed', 'results', 'DS']])])
        reqconds = "all"
        if reqconds == 'all':
            conditions = allconds
        else:
            conditions = np.array([conds for conds in allconds if any([a.upper() in conds for a in reqconds])])

        for cond in conditions:
            print(cond)
            inname = os.path.join(source, sub, cond)
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

            trllength = 'all'
            npy = copy.deepcopy(tmpdat)
            npy.segment(trllength=trllength, remove_artifact='no')
            # subpath = os.path.join(preprocpath,s)
            # Path(subpath).mkdir(parents=True, exist_ok=True)
            sesspath = os.path.join(dest, sub)
            Path(sesspath).mkdir(parents=True, exist_ok=True)
            npy.save(sesspath)

            rawreport = True
            if rawreport:  # for the raw data report
                lengthtrl = 10
                pdf = copy.deepcopy(tmpdat)
                pdf.segment(trllength=lengthtrl, remove_artifact='no')
                pdf.save_pdfs(sesspath)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        raise RuntimeError(f"Please specify input and output path, i.e. {sys.argv[0]} [INPUT_PATH] [OUTPUT_PATH]")
    autopreprocess_standard(sys.argv[1], sys.argv[2])
