
> Method Resolution Order (MRO) refers to the order in which Python searches for methods and attributes in a class hierarchy. It's particularly relevant in multiple inheritance scenarios, where a subclass inherits from multiple parent classes.
##### Example 

<image src='./assets/mro.png'>
<br></br>

```python
class A: 
	def ping(self): 
		print('ping:', self) 

class B(A): 
	def pong(self): 
		print('pong:', self)

class C(A): 
	def pong(self):
		print('PONG:', self) 
		
class D(B, C): 
	def ping(self): 
		super().ping() 
		print('post-ping:', self) 
	
	def pingpong(self): 
		self.ping() 
		super().ping() 
		self.pong() 
		super().pong() 
		C.pong(self)
```
*Note that both classes B and C implement a pong method. The only difference is that C.pong outputs the word PONG in uppercase.*

The ambiguity of a call like d.pong() is resolved because Python follows a specific order when traversing the inheritance graph. That order is called MRO: Method Resolution Order. Classes have an attribute called `__mro__` holding a tuple of references to the superclasses in MRO order, from the current class all the way to the object class. For the D class, this is the `__mro__`
```bash
>>> D.__mro__  
(<class 'mro.D'>, <class 'mro.B'>, <class 'mro.C'>, <class 'mro.A'>, <class 'object'>)

>>> d.pingpong()
ping: <mro.D object at 0x000002026BB37910>
post-ping <mro.D object at 0x000002026BB37910>
ping: <mro.D object at 0x000002026BB37910>
pong: <mro.D object at 0x000002026BB37910>
pong: <mro.D object at 0x000002026BB37910>
PONG: <mro.D object at 0x000002026BB37910>
```

**The MRO takes into account not only the inheritance graph but also the order in which superclasses are listed in a subclass declaration**. In other words, in the given example, the D class was declared as class D(C, B), the `__mro__` of class D would be different: C would be searched before B.