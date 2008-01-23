class BaseSearch:
    def __init__(self):
        self.search_shortcut = None

    def get_search_shortcut(self):
        return self.search_shortcut

    def set_search_shortcut(self, shortcut):
        return self.search_shortcut

    def search(self, search_str):
        raise NotImplementedError
