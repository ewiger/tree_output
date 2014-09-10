tree_output
===========

[![Build Status](https://travis-ci.org/ewiger/tree_output.svg?branch=master)](https://travis-ci.org/ewiger/tree_output)


Python library to simplify building of tree output with command-line interfaces.

Supported output format options are:

- json
- ascii
- ansi
- null

examples
--------


```python
tree_output = HierarchicalOutput.factory('ansi')
import colorama

tree_output.emit('foo')
tree_output.add_level()
tree_output.emit('foO')
tree_output.add_level()
tree_output.emit('bar')

tree_output.add_level()
for num in range(10):
    tree_output.emit(num)
tree_output.emit(10, closed=True)
tree_output.remove_level()

tree_output.emit('baz', closed=True)
tree_output.emit('foo2')


```

this will draw a colorful ANSI output like this

```
.
├── foo
│   ├── foO
│   │   ├── bar
│   │   │   ├── 0
│   │   │   ├── 1
│   │   │   ├── 2
│   │   │   ├── 3
│   │   │   ├── 4
│   │   │   ├── 5
│   │   │   ├── 6
│   │   │   ├── 7
│   │   │   ├── 8
│   │   │   ├── 9
│   │   │   └── 10
│   └── baz
├── foo2

```

logging
-------

Another option is to integrate with logging and pass hierarchical meta instructions via optional **extra** argument, e.g.

```python
houtput = HierarchicalOutput.factory(format='json')
#houtput = HierarchicalOutput.factory(format='ansi')
handler = HierarchicalOutputHandler(houtput=houtput)
logger = logging.getLogger('foo')
logging.root.addHandler(handler)
# Emission.
logger.info('foo')
logger.info('bar', extra={'add_hlevel': True})
logger.info('foo2')
logger.info('bar', extra={'add_hlevel': True})
logger.info('foo2')
logger.info('Numbers', extra={'add_hlevel': True})
for num in range(10):
    logger.warn(num)
logger.warn('end of numbers', extra={'hclosed': True})
logger.debug('level up', extra={'remove_hclosed': True})
```

produces

```json
["foo", [
	"bar", "foo2", ["
		bar", "foo2", [
			"Numbers", 
			"0", 
            "1", 
            "2", 
            "3", 
            "4", 
            "5", 
            "6", 
            "7", 
            "8", 
            "9", 
            "end of numbers"
        ], 
    "level up"]
    ]
]
```

tests
-----

For tests we use *nose*, i.e. usage would be:

```bash
cd tests && nosetests
```
