# State Count

Counts the number of monotone Boolean models (MBMs) supporting each steady state for the given topologies.

## Usage: 
```bash
state_count [-h] [--topodir TOPODIR] [--output OUTPUT] [topo]
```
- Count MBMs for the topology `EMT6N.topo` and save results in `Counts_EMT6N.csv`. Only supported if the in-degree of any of the nodes in the network is <6.
```bash
uv run state_count --output Counts_EMT6N.csv EMT6N.topo
```
- Count MBMs for all the topology files in `Inputs/Topo/topofiles_4` and save results in `Output/Count/4-node_count.csv`. If you are counting over multiple topofiles, make sure that they all have same number of nodes.
```bash
uv run state_count --topodir Input/topofiles_4 --output Output/Count/4-node_count.csv 
```

## Positional arguments:
- `topo` topo file name

## Options:
- `-h, --help` show this help message and exit
- `--topodir TOPODIR` topo file directory
- `--output OUTPUT` output file