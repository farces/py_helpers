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
    ActionTree(key_str, subkey_str, lambda k, i: _winreg.DeleteKey(k, i))


def ActionTree(key_str, subkey_str, cb):
    """Perform action in callback for each child subkey, then finally
    on the parent key"""
    _action_subkeys(key_str, subkey_str, cb)
    cb(key_str, subkey_str)


def _action_subkeys(key_str, subkey_str, cb):
    """Internal:
    Recursively steps down tree, performing the provided callback for
    each key found, starting at the deepest child subkey."""
    l = []
    current_key = _winreg.OpenKey(key_str, subkey_str)
    try:
        i = 0
        while True:
            next = _winreg.EnumKey(current_key, i)
            next_str = "%s\\%s" % (subkey_str, next)
            l.append(next_str)
            _action_subkeys(key_str, next_str, cb)
            i += 1
    except WindowsError:
        for item in l:
            cb(key_str, item)
