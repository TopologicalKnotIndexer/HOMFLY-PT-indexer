# HOMFLY-PT polynomial list

A static catalog of mirror-image HOMFLY-PT polynomials for 1,871 named knots
used by the TopologicalKnotIndexer tools. “Mirror-image” means that the stored
polynomial is evaluated on the mirror of the named diagram under the
organization's convention.

## Files and format

- `data/combined_knot_name.txt` lists names in source order.
- `data/HOMFLY-PT.txt` contains the corresponding polynomial/name records.
- `data/sorted_HOMFLY-PT.txt` contains the same records sorted
  lexicographically by polynomial text.

Every record has the form:

```text
[POLYNOMIAL|KNOT_NAME]
```

All three files contain 1,871 lines. The unknot is represented by `K0a1` and
polynomial `1`.

## Consuming the data

```python
from pathlib import Path

line = Path("data/HOMFLY-PT.txt").read_text(encoding="utf-8").splitlines()[0]
polynomial, name = line[1:-1].rsplit("|", 1)
print(name, polynomial)
```

The polynomial field is stored as Sage-compatible text; this repository does
not evaluate it and has no runtime dependency. Consumers should preserve the
text exactly when using it as an index key.

## License

MIT. See `LICENSE`.

