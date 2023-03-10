# Classes

Python belongs to the family of object-oriented languages. In OOP, the basic building block is a **Class**. Classes provide a means of bundling data and functionality (or behavior) together. Creating a new class creates a new **type** of object, allowing new **instances** of that type to be made. Each class instance can have **attributes** attached to it for maintaining its **state**. Class instances can also have **methods** (defined by its class) for modifying its state.

Take some time to read [9.3 - A first look at classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes) until the `9.4`.

## Getting Started

```bash
cd ~/code/<user.github_nickname>/engineering-basics
cd 01-OOP/08-Classes
subl .
```

## Your first class

Open the `vehicle.py` file and implement a simple class following these specs:

- A vehicle has a brand and a color
- A vehicle is started or stopped
- A vehicle can be started or stopped _via_ a call

To help you through this task, we implemented some tests you can run:

```bash
nosetests
```

Do not hesitate to open and **read** the test file in `tests/test_vehicle.py`!
It will help you figure out how the `Vehicle` class is called, which is the
spec of what you should do translated to code.

💡 If you want to use the debugger introduced earlier with `nosetests`, you need to run the tests with the [`--no-capture` flag](http://nose.readthedocs.io/en/latest/man.html#cmdoption-s) (shortcut: `-s`).

## (Optional) PowerShell Classes

Since inception, PowerShell uses the .Net framework, an object-oriented platform, allowing the developer access to a collection of types.

Since PowerShell 5.0, there is a formal syntax to define classes and other user-defined types. It goes like this:

```powershell
# Defining the class:
class Device {
    [string]$Brand # An instance variable
}

# Creating an instance of the new `Device` class
$dev = [Device]::new()

# And setting/calling instance variables:
$dev.Brand = "Microsoft"
$dev
```

The difference with Python here is that you are invited to specify the type of each instance variable in the class definition (`[string]` for the `$Brand` instance variable).

You can read the [whole Microsoft Docs article](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_classes) to dive into PowerShell user-defined classes.
