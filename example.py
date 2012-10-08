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