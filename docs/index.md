# Monotone-Bool-Net
Python code for the analysis of Monotone Boolean Functions and Models across Network Topologies. 

## Usage
Requires `uv`
```bash
uv sync
```
The scripts can be run directly using uv
```bash
uv run state_counts --arguments ...
```
Otherwise, the .venv can be used to import the codes as a python module
```python
import mbnet as mn
mn.function_name
```

## Documentation
You can access the  documentation at [hbv.io.in/Monotone-Bool-Net](https://www.hbv.io.in/Monotone-Bool-Net/)

## Citation
If you found this useful please cite the associated manuscript
```
@article {Adigwe2025.10.16.682751,
	author = {Adigwe, Sarah and Harshavardhan, BV and Jolly, Mohit Kumar and Gedeon, Tom{\'a}{\v s}},
	title = {Fixed points and multistability in monotone Boolean network models},
	elocation-id = {2025.10.16.682751},
	year = {2025},
	doi = {10.1101/2025.10.16.682751},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2025/10/16/2025.10.16.682751},
	eprint = {https://www.biorxiv.org/content/early/2025/10/16/2025.10.16.682751.full.pdf},
	journal = {bioRxiv}
}
```