Python Function Helpers
-----------------------
These are just some small methods and wrappers to implement useful features not found in the built-in library.

reghelper
---------
Implements _DeleteTree(key,subkey)_ using the _winreg package, to recursively delete a registry key and all subkeys.

Implements _ActionTree(key,subkey,callback)_ which accepts a callback to be called for each subkey within the key provided, and finally on the parent key. DeleteTree is a wrapper for this function.

Key argument must be a _winreg.HKEY* constant, or a key already opened through _winreg.OpenKey.

Subkey argument must be a string containing a subkey of key, and must not be None. 

Callback argument must be a function or lambda accepting 2 arguments: 
* Root key (as passed to ActionTree, e.g. _winreg.HKEY_CURRENT_USER) 
* Subkey (string representation of subkey within key e.g. SOFTWARE\test\Test Key #1)
These arguments can be passed directly into _winreg.* functions (such as DeleteKey).

```python
import _winreg, reghelper

def print_args(k,i):
    """Basic output function for callback"""
    print i

key_str = _winreg.HKEY_CURRENT_USER
subkey_str = "SOFTWARE\\test"

#print listing of child subkeys and finally parent key
reghelper.ActionTree(key_str, subkey_str, print_args)

#delete entire registry key and all children
reghelper.DeleteTree(key_str, subkey_str)
```
You can install the reg_sample.reg file to create a test registry tree in HKCU\SOFTWARE\test.