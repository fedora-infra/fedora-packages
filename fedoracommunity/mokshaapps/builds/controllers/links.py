from moksha.lib.helpers import CategoryEnum

builds_links = CategoryEnum('build_link',
                             ('PACKAGE',
                              '/package_maint/packages/package'
                             ),
                             ('ALL_BUILDS',
                              '/package_maint/builds'
                             )
                           )
