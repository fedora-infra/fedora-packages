from basesearch import BaseSearch

import os

class PackageSearch(BaseSearch):
    def __init__(self):
        BaseSearch.__init__(self)
        self.set_search_shortcut('pkg')

    def search(self, search_str):
        # FIXME: this is just a demo, don't use yum
        split_results = []
        for result in os.popen('yum search ' + search_str).readlines():
            split_results.append(result.split(':'))

        pkg_hash = {}
        for result in split_results:
            name = result[0][0:result[0].rindex('.')]
            # last one wins :)
            pkg_hash[name] = result[1] # description
            
        pkg_list = pkg_hash.keys()
        pkg_list.sort()
        
        # we should figure out how to template these
        mylist=[]
        for pkg in pkg_list:
            mylist.append((pkg, pkg_hash[pkg])) 

        return mylist 

