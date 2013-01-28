# Global list of koji tags we care about
tags = ({'name': 'Rawhide', 'tag': 'f17'},
        {'name': 'Fedora 16', 'tag': 'f16-updates'},
        {'name': 'Fedora 16', 'tag': 'f16'},
        {'name': 'Fedora 16 Testing', 'tag': 'f16-updates-testing'},
        {'name': 'Fedora 15', 'tag': 'dist-f15-updates'},
        {'name': 'Fedora 15', 'tag': 'dist-f15'},
        {'name': 'Fedora 15 Testing', 'tag': 'dist-f15-updates-testing'},
        {'name': 'Fedora 14', 'tag': 'dist-f14-updates'},
        {'name': 'Fedora 14', 'tag': 'dist-f14'},
        {'name': 'Fedora 14 Testing', 'tag': 'dist-f14-updates-testing'},
        {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
        {'name': 'EPEL 6', 'tag': 'dist-6E-epel-testing'},
        {'name': 'EPEL 5', 'tag': 'dist-5E-epel'},
        {'name': 'EPEL 5', 'tag': 'dist-5E-epel-testing'},
       )

tags_to_name_map = {}
for t in tags:
    tags_to_name_map[t['tag']] = t['name']
