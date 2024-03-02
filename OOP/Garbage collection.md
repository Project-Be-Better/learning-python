
Whenever a name is assigned to a new object, the space held by the prior object is reclaimed if it is not referenced by any other name or object. This automatic reclamation of objects’ space is known as garbage collection. The main garbage collection algorithm used by CPython is reference counting

```python
a = 3 
a = 'spam'
```

Internally, Python accomplishes garbage collection by keeping a counter in every object that keeps track of the number of references currently pointing to that object. As soon as (and exactly when) this counter drops to zero, the object’s memory space is automatically reclaimed

>The most immediately tangible benefit of garbage collection is that it means you can use objects liberally without ever needing to allocate or free up space in your script. Python will clean up unused space for you as your program runs. In practice, this eliminates a substantial amount of bookkeeping code required in lower-level languages such as C and C++

#### Example 
```bash
>>> x = 42 
>>> x = 'shrubbery' # Reclaim 42 now (unless referenced elsewhere) 
>>> x = 3.1415 # Reclaim 'shrubbery' now 
>>> x = [1, 2, 3] # Reclaim 3.1415 now
```

First, notice that x is set to a different type of object each time. Again, though this is not really the case, the effect is as though the type of x is changing over time. Remember, in *Python types live with objects, not names*. Because names are just generic references to objects, this sort of code works naturally. Second, notice that references to objects are discarded along the way. 

*Each time x is assigned to a new object, Python reclaims the prior object’s space*. For instance, when it is assigned the string 'shrubbery', the object 42 is immediately reclaimed (assuming it is not referenced anywhere else) that is, the object’s space is automatically thrown back into the free space pool, to be reused for a future object
#### References
1. [Garbage collector design (python.org)](https://devguide.python.org/internals/garbage-collector/index.html)