
# Class Method
Definition
> A class method is a method that is bound to the class rather than to instances of the class. This means that class methods can be called on the class itself and can access or modify class-level attributes, but they cannot access or modify instance-specific attributes directly

>Python only allows one `__init__` method per class. Using class methods it’s possible to add as many alternative constructors as necessary. This can make the interface for your classes self-documenting (to a certain degree) and simplify their usage.

```python
class MyClass:
    @classmethod
    def class_method(cls, arg1, arg2):
        # Class method definition
        pass
```

```python
class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __repr__(self):
        return f'Pizza({self.ingredients!r})'

    @classmethod
    def margherita(cls):
        return cls(['mozzarella', 'tomatoes'])

    @classmethod
    def prosciutto(cls):
        return cls(['mozzarella', 'tomatoes', 'ham'])
```

```bash
>>> Pizza.margherita()
Pizza(['mozzarella', 'tomatoes'])

>>> Pizza.prosciutto()
Pizza(['mozzarella', 'tomatoes', 'ham'])
```
---
```python
class Car:
    total_cars = 0  # Class-level attribute to keep track of total cars
    
    def __init__(self, make, model):
        self.make = make
        self.model = model
        Car.total_cars += 1
    
    @classmethod
    def from_string(cls, car_string):
        make, model = car_string.split()
        return cls(make, model)
    
    @classmethod
    def display_total_cars(cls):
        print(f"Total cars created: {cls.total_cars}")
```
### Key Characteristics:
1. **Bound to the Class**: Class methods are bound to the class itself, not to instances of the class. This means they can be called on the class directly.
2. **Access Class Attributes**: Class methods can access and modify class-level attributes and methods through the `cls` parameter.
3. **Cannot Access Instance Attributes**: Since class methods are not bound to instances, they cannot directly access or modify instance-specific attributes.
4. **Use Cases**: Class methods are commonly used for tasks that involve operations on class-level data, class-level utility methods, or alternative constructors

Instead of accepting a `self` parameter, class methods take a `cls` parameter that points to the class—and not the object instance—when the method is called.

Because the class method only has access to this `cls` argument, it can’t modify object instance state. That would require access to `self`. However, class methods can still modify class state that applies across all instances of the class.

# Instance Method

> Definition
An instance method is a method that is bound to instances of a class. This means that instance methods can be called on individual instances of the class and have access to both the instance itself and its attributes

```python
class MyClass:
    def instance_method(self, arg1, arg2):
        # Instance method definition
        pass
```

Through the `self` parameter, instance methods can freely access attributes and other methods on the same object. This gives them a lot of power when it comes to modifying an object’s state.

Not only can they modify object state, instance methods can also access the class itself through the `self.__class__` attribute. This means instance methods can also modify class state.
### Key Characteristics:
1. **Bound to Instances**: Instance methods are bound to individual instances of the class. This means they can be called on instances of the class and have access to instance-specific attributes and methods.
2. **Access Instance Attributes**: Instance methods can access and modify instance-specific attributes and methods through the `self` parameter.
3. **Use Cases**: Instance methods are commonly used for tasks that involve operations on instance-specific data, behavior, or state.

# Static Method

Definition
> A static method is a method that is not bound to either the instance or the class. This means that static methods do not have access to instance attributes or class attributes and are essentially just like regular functions defined within the class namespace

```python
class MyClass:
    @staticmethod
    def static_method(arg1, arg2):
        # Static method definition
        pass
```
### Key Characteristics:
1. **Not Bound to Instances or Classes**: Static methods are not bound to either instances or classes. They are essentially standalone functions defined within the class namespace.
2. **No Access to Instance or Class Attributes**: Since static methods are not bound to instances or classes, they do not have access to instance attributes (`self`) or class attributes (`cls`).
3. **Use Cases**: Static methods are commonly used for utility functions that do not depend on instance-specific or class-specific data. They can be called directly on the class or instances of the class, but they do not receive any implicit arguments.

>Flagging a method as a static method is not just a hint that a method won’t modify class or instance state — this restriction is also enforced by the Python runtime.

```python
import math

class Pizza:
    def __init__(self, radius, ingredients):
        self.radius = radius
        self.ingredients = ingredients

    def __repr__(self):
        return (f'Pizza({self.radius!r}, '
                f'{self.ingredients!r})')

    def area(self):
        return self.circle_area(self.radius)

    @staticmethod
    def circle_area(r):
        return r ** 2 * math.pi
```
Static methods also have benefits when it comes to writing test code. Because the `circle_area()` method is completely independent from the rest of the class it’s much easier to test.

We don’t have to worry about setting up a complete class instance before we can test the method in a unit test. We can just fire away like we would testing a regular function. Again, this makes future maintenance easier.
#### References
1. [Python's Instance, Class, and Static Methods Demystified – Real Python](https://realpython.com/instance-class-and-static-methods-demystified/#:~:text=Instance%20methods%20need%20a%20class,access%20to%20cls%20or%20self%20.)