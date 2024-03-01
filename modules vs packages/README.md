# Modules vs Packages

> [!NOTE] Definition
In short, modules provide an easy way to organize components into a system by serving as self-contained packages of variables known as namespaces. Ultimately, Python’s modules allow us to link individual files into a larger program system

Python fosters a modular program structure that groups functionality into coherent and reusable units, in ways that are natural, and almost automatic

##### Importance

###### 1. Code reuse
- Modules let you save code in files permanently. 
- Code in module files is persistent—it can be reloaded and rerun as many times as needed. Just as importantly, *modules are a place to define names, known as attributes*, which may be referenced by multiple external clients. 
- When used well, this supports a modular program design that groups functionality into reusable units. 

###### 2. System namespace partitioning 
- Modules are also the highest-level program organization unit in Python. 
- Although they are fundamentally just packages of names, these packages are also self-contained—you can never see a name in another file, unless you explicitly import that file. 
	- Much like the local scopes of functions, this helps avoid name clashes across your programs. 
	- In fact, you can’t avoid this feature—everything “lives” in a module, both the code you run and the objects you create are always implicitly enclosed in modules. 
	- Because of that, modules are natural tools for grouping system components. 

###### 3. Implementing shared services or data
- From an operational perspective, modules are also useful for implementing components that are shared across a system and hence require only a single copy. 
- For instance, if you need to provide a global object that’s used by more than one function or file, you can code it in a module that can then be imported by many clients.