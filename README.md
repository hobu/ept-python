# ept-python

Python library for making queries against [Entwine Point Tile](https://entwine.io/) data.

## Install

Using git and pip:

```bash
git clone https://github.com/hobu/ept-python.git
cd ept-python
pip install .
```

Using just pip:

```bash
pip install git+https://github.com/hobu/ept-python.git
```

## Usage

Example query and output to LasData object:

```python
import ept

url = 'https://na-c.entwine.io/red-rocks'
bounds = ept.Bounds(
    482298, #xmin
    4390602, #ymin
    1762, #zmin
    482421, #xmax
    4390690, #ymax
    2113 #zmax
)

query = ept.EPT(url, bounds=bounds)
las = query.as_laspy()
print(las)
```
```
<LasData(1.2, point fmt: <PointFormat(3, 4 bytes of extra dims)>, 98050 points, 4 vlrs)>
```


## Uninstall

```
pip uninstall ept-python
```
