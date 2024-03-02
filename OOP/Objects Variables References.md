<image src='assets/vor.png'>

# Variables
```python
a = 3 
```

1. Create an object to represent the value 3. 
2. Create the variable a, if it does not yet exist. 
3. Link the variable a to the new object 3.

In sum, variables are created when assigned, can reference any type of object, and must be assigned before they are referenced. This means that you never need to declare names used by your script, but you must initialize names before you can update them

**In typical code, a given variable usually will reference just one kind of object**

**Variable Creation**:
   - In Python, variables (or names) are created when they are first assigned a value.
   - For example, when you write `a = 10`, you are creating a variable named `a` and assigning it the value `10`.
   - Subsequent assignments to the same variable change the value it refers to.
   - Technically, Python performs some name binding before your code runs, but for practical purposes, you can consider the initial assignments as creating variables.

**Variable Types**:
   - In Python, variables do not have type information or constraints associated with them.
   - The concept of types is associated with objects, not names. Variables are generic; they simply refer to objects at a given point in time.
   - For example, `a = 10` assigns the integer object `10` to the variable `a`, but the variable `a` itself does not have any inherent type.
   
**Variable Use**:
   - When a variable appears in an expression, it is immediately replaced with the object it currently refers to.
   - For instance, if you have `b = a`, `b` will refer to the same object as `a`.
   - All variables must be explicitly assigned before they can be used. Referencing unassigned variables results in errors (e.g., `NameError`).
   - For instance, trying to use a variable before it's assigned will lead to an error, like `x = y + 5` when `y` hasn't been assigned any value.

# Objects
Each time you generate a new value in your script by running an expression, Python creates a new object (i.e., a chunk of memory) to represent that value

Objects have more structure than just enough space to represent their values. Each object also has two standard header fields: 
1. A type designator used to mark the type of the object
2. A reference counter used to determine when it’s OK to reclaim the object

**Objects, know what type they are. Each object contains a header field that tags the object with its type**. The integer object 3, for example, will contain the value 3, plus a designator that tells Python that the object is an integer (strictly speaking, a pointer to an object called int, the name of the integer type). The type designator of the 'spam' string object points to the string type (called str) instead. *Because objects know their types, variables don’t have to*

# References

These links from variables to objects are called references in Python—that is, a reference is a kind of association, implemented as a pointer in memory. Whenever the variables are later used (i.e., referenced), Python automatically follows the variable-to-object links