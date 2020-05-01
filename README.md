# readi Collections
Dead simple class registration.

Often I find myself trying to implement generic class representations and then extending them to provide many different functional variants. I then want to be able to access those variants in a simple, automatic way, without having to write "switch-case" type class selection strategies.

This allows you to register classes at instantiation time and have them accessible using a simple dict interface, with some nice helper methods :)

## Install

```bash
pip install readi
```

## Usage

```python
# __init__.py
import readi
# this is just a dictionary with some fancy bits
collection = readi.Collection(entrypoints='myentrypoint')
```
```python
# setup.py
# this can allow other modules to register classes.
setuptools.setup(
    ...
    entry_points={'myentrypoint': ['C = module.for.thisclass:SomeClass']}
)
```
```python
# myclasses.py
# then just use it in your class
from . import collection

@collection.register
class A:
    pass

class B:
    pass

class B1(B):
    pass

class B2(B):
    pass

collection.register_subclasses(B, include=True)

# they're all available in the collection dictionary.
assert set(collection) == {'a', 'b', 'b1', 'b2', 'c'}

class D(B1): # works for nested subclasses
    pass

collection.refresh_subclasses() # can gather new subclasses
assert set(collection) == {'a', 'b', 'b1', 'b2', 'c', 'd'}
```
```python
# __main__.py
# now to see how they're used.
from . import collection

def main(**kw):
    processors = collection.gather(**kw)

    for data in data_generator():
        for func in processors: # assuming we defined __call__
            func(data)

main(fs=48000, channels=4, b1=False, b2=dict(nfft=2048))
```

Doing this will result in a processor list that looks like this:
```python
processors = [
    A(fs=48000, channels=4),
    B(fs=48000, channels=4),
    # B1 is omitted since it was set as False
    B2(fs=48000, channels=4, nfft=2048),
    C(fs=48000, channels=4),
    D(fs=48000, channels=4),
]
```

This is used if you have a bank of processors that you want to run and you want them to be enabled/disabled using keyword arguments.

Another use case is: you only need to select a single registered class. This is done very simply:
```python
# __main__.py
# now to see how they're used.
from . import collection

def main(proc_type='b', **kw):
    processor = collection.getone(proc_type, **kw)

    for data in data_generator():
        processor(data)

main(fs=48000, channels=4, proc_type='b2')

```

## Notes
 - There is nothing stopping you from adding things that return non function values (i.e. lists).


```python
@collection.register
def reds(saturation=92):
    c = '#FF0000'
    return [c] + calculate_colors(c, saturation)

@collection.register
def blues(saturation=92):
    c = '#0000FF'
    return [c] + calculate_colors(c, saturation)

@collection.register
def greens(saturation=92):
    c = '#00FF00'
    return [c] + calculate_colors(c, saturation)

colors = collection.gather(saturation=120, greens=False)
# colors = [
#     ['#FF0000', ...], # reds
#     ['#0000FF', ...], # blues
# ]
```

## TODO
