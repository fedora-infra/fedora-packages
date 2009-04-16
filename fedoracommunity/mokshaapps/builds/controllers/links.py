from moksha.lib.helpers import CategoryEnum

builds_links = CategoryEnum('build_link',
                             ('PACKAGE',
                              '/package_maintenance/packages/package/builds'
                             ),
                             ('ALL_BUILDS',
                              '/package_maintenance/builds'
                             ),
                             ('IN_PROGRESS',
                              '/package_maintenance/builds/inprogress',
                             ),

                             ('FAILED',
                              '/package_maintenance/builds/failed',
                             ),

                             ('SUCCESSFUL',
                              '/package_maintenance/builds/successful',
                             ),
                           )
