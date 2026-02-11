import os
import glob
import pandas as pd
import mbnet as mn
import argparse
from multiprocessing import Pool

def tot_mbm(topo):
    adjmat = mn.utils.topo_to_adj(topo)
    nMBM = mn.tl.n_mbm(adjmat)
    return nMBM['Total']

def main():
    parser = argparse.ArgumentParser(
        prog="state_count",
        description="Counts the number of monotone Boolean models (MBMs) supporting each steady state for the given topologies",
    )
    parser.add_argument(
        "topo", type=str, help="topo file name", default="all", nargs="?"
    )
    parser.add_argument(
        "--topodir", type=str, help="topo file directory", default=None
    )
    parser.add_argument(
        "--output", type=str, help="output file", default="Counts.csv"
    )
    args = parser.parse_args()
    
    # if no topo file is provided, use iterate over all the topo files
    if args.topo == "all":
        topos = sorted(glob.glob(f"*.topo",root_dir = args.topodir))
        topo_full = [os.path.join(args.topodir,topo) for topo in topos]
    else:
        topo_full = topos = [args.topo]
    # Print the parameters
    print(f"Number of topology files: {len(topos)}")
    # Iterate over each topofile and get the total counts
    with Pool() as p:
        df = p.map(tot_mbm,topo_full)
    # Concat and save
    df = pd.concat(df,axis=1)
    df.columns = topos
    df.T.to_csv(args.output)

if __name__ == "__main__":
    main()