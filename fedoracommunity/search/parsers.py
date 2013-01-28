import re

class KeyValueParser(object):
    key_value_re = None # you need to sublass this and define the regex
    case_insensitive_keys = False

    def __init__(self, file_obj):
        object.__init__(self)
        self._entries = {}
        self.parse(file_obj)

    def get(self, entry_key, default=''):
        if self.case_insensitive_keys:
            entry_key = entry_key.lower()
        return self._entries.get(entry_key, default)

    def parse(self, file_obj):
        dfile = file_obj
        for line in dfile:
            if line.startswith('#') or line.startswith(' ') or line.startswith('['):
                continue
            m = self.key_value_re.match(line)
            if m:
                key = m.group(1)
                value = m.group(2)
                if self.case_insensitive_keys:
                   key = key.lower()
                self._entries[key] = value

class DesktopParser(KeyValueParser):
    key_value_re = re.compile('([A-Za-z0-9-]*)[ ]*=[ ]*(.*)')

class SimpleSpecfileParser(KeyValueParser):
    """SimpleSpecfileParser - A simple parser that parses the header from
       rpm spec files.  This does not expand macros (yet) and only reads
       header keys.
    """
    key_value_re = re.compile('([A-Za-z0-9-]*)[ ]*:[ ]*(.*)')
    case_insensitive_keys = True

