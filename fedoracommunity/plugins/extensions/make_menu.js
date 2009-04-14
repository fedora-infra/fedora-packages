{
  info: {
    consumes:['make_menu'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Menu Creator',
    summary: 'Async creation of menus used inside of templates',
    description: 'Since jQuery templates can\'t have javascript in \
                  them we use this to create a javascript menu'
  },

  run: function (data) {
    $('#' + data.placeholder_id).moksha_popup();

    return null;
  }
 }
