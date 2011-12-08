
import os
import tg

from paste.deploy import appconfig

import tw2.core.command

# hack to get all the tw2 widgets since we don't care about tw1
config = appconfig('config:build.ini', relative_to=os.getcwd())
tg.config = config
print config.get('moksha.use_tw2')
archive_fedoracommunity_resources = tw2.core.command.archive_tw2_resources
