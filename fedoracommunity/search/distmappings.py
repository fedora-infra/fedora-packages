# Global list of koji tags we care about
tags = ({'name': 'Rawhide', 'tag': 'f20'},
        {'name': 'Fedora 19', 'tag': 'f16-updates'},
        {'name': 'Fedora 19', 'tag': 'f16'},
        {'name': 'Fedora 19 Testing', 'tag': 'f16-updates-testing'},
        {'name': 'Fedora 18', 'tag': 'f16-updates'},
        {'name': 'Fedora 18', 'tag': 'f16'},
        {'name': 'Fedora 18 Testing', 'tag': 'f16-updates-testing'},
        {'name': 'Fedora 17', 'tag': 'f16-updates'},
        {'name': 'Fedora 17', 'tag': 'f16'},
        {'name': 'Fedora 17 Testing', 'tag': 'f16-updates-testing'},
        {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
        {'name': 'EPEL 6', 'tag': 'dist-6E-epel-testing'},
        {'name': 'EPEL 5', 'tag': 'dist-5E-epel'},
        {'name': 'EPEL 5', 'tag': 'dist-5E-epel-testing'},
       )

tags_to_name_map = {}
for t in tags:
    tags_to_name_map[t['tag']] = t['name']
