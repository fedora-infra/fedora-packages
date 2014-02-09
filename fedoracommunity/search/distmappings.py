# Global list of koji tags we care about
tags = ({'name': 'Rawhide', 'tag': 'f21'},

        {'name': 'Fedora 20', 'tag': 'f20-updates'},
        {'name': 'Fedora 20', 'tag': 'f20'},
        {'name': 'Fedora 20 Testing', 'tag': 'f20-updates-testing'},

        {'name': 'Fedora 19', 'tag': 'f19-updates'},
        {'name': 'Fedora 19', 'tag': 'f19'},
        {'name': 'Fedora 19 Testing', 'tag': 'f19-updates-testing'},

        {'name': 'Fedora 18', 'tag': 'f18-updates'},
        {'name': 'Fedora 18', 'tag': 'f18'},
        {'name': 'Fedora 18 Testing', 'tag': 'f18-updates-testing'},

        {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
        {'name': 'EPEL 6 Testing', 'tag': 'dist-6E-epel-testing'},

        {'name': 'EPEL 5', 'tag': 'dist-5E-epel'},
        {'name': 'EPEL 5 Testing', 'tag': 'dist-5E-epel-testing'},

        {'name': 'EPEL 7', 'tag': 'epel7'},
        {'name': 'EPEL 7 Testing', 'tag': 'epel7-testing'},
        )

tags_to_name_map = {}
for t in tags:
    tags_to_name_map[t['tag']] = t['name']
