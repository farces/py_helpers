"""
Wrapper for _winreg.DeleteKey to recursively delete a key and all
subkeys. _winreg does not provide this feature and requires any key
contain no subkeys, though values are fine.
Usage:
 import reghelper, _winreg
 reghelper.DeleteTree(_winreg.HKEY_CURRENT_USER,
                      "SOFTWARE\\KeyName")

 reghelper.ActionTree(_winreg.HKEY_CURRENT_USER,
                      "SOFTWARE\\KeyName",
                      lambda k,i: action(k,i))

 Callback is provided two arguments, the _winreg.HKEY_* parent key
 and the string representation of the subkey to be acted on.
"""
import _winreg


def DeleteTree(key_str, subkey_str):
    """Wrapper for ActionTree(key,subkey,delete callback)"""
    ActionTree(key_str, subkey_str, _winreg.DeleteKey)


def ActionTree(key_str, subkey_str, callback):
    """Perform action in callback for each child subkey, then finally
    on the parent key"""
    _action_subkeys(key_str, subkey_str, callback)
    callback(key_str, subkey_str)


def _action_subkeys(key_str, subkey_str, callback):
    """Internal:
    Recursively steps down tree, performing the provided callback for
    each key found, starting at the deepest child subkey."""
    l = []
    current_key = _winreg.OpenKey(key_str, subkey_str)
    try:
        i = 0
        while True:
            next_key = _winreg.EnumKey(current_key, i)
            next_str = "%s\\%s" % (subkey_str, next_key)
            l.append(next_str)
            _action_subkeys(key_str, next_str, callback)
            i += 1
    except WindowsError:
        for item in l:
            callback(key_str, item)
