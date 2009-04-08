from moksha.lib.helpers import CategoryEnum

updates_links = CategoryEnum('updates_links',
                             ('PACKAGE',
                              '/package_maintenance/packages/package/updates'
                             ),
                             ('ALL_UPDATES',
                              '/package_maintenance/updates'
                             ),
                             ('STABLE_UPDATES',
                              '/package_maintenance/updates/stable_updates'
                             ),
                             ('TESTING_UPDATES',
                              '/package_maintenance/updates/testing_updates'
                             ),
                             ('UNPUSHED_UPDATES',
                              '/package_maintenance/updates/unpushed_updates'
                             )
                           )
