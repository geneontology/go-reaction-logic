# go-reaction-logic

## API

Example:

```python
engine = GOReactionEngine()
gmer = "GO:0047918"
gmd = "GO:0008446"
engine.compute_intermediates(gmer, gmd)
```

Returns:

```python
[ChemicalEntity(id='CHEBI:57527', label='GDP-alpha-D-mannose(2-)')]
```

## Installation

```bash
pip install go-reaction-logic
```

## UI

For demo purposes only: