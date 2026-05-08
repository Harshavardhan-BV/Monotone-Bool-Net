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
@article{10.1371/journal.pcsy.0000103,
    doi = {10.1371/journal.pcsy.0000103},
    author = {Adigwe, Sarah AND BV, Harshavardhan AND Jolly, Mohit Kumar AND Gedeon, Tomáš},
    journal = {PLOS Complex Systems},
    publisher = {Public Library of Science},
    title = {Characterization of monotone Boolean models supporting fixed points and multistability in balanced networks},
    year = {2026},
    month = {05},
    volume = {3},
    url = {https://doi.org/10.1371/journal.pcsy.0000103},
    pages = {1-28},
    number = {5},
}
```
