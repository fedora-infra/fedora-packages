from turbogears import controllers, expose

from myfedora.urlhandler import KojiURLHandler
import koji
import re

def _mock_error_code_to_log_file(err_code):
    log_file = ''
    if err_code == 1:
        log_file = 'build.log'
    elif err_code == 10 or err_code == 30:
        log_file = 'root.log'

    return log_file

class KojiReleaseTagsQuery(controllers.Controller):
    @expose("json", allow_json=True)
    def index(self, *args, **kw):
        build_id = int(kw.get('build_id', '0'))

        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())

        tags = cs.listTags(build = build_id)

        return {'tags': tags}

class KojiGetErrorLogQuery(controllers.Controller):
    @expose("json", allow_json=True)
    def index(self, *args, **kw):
        results = {'log_url':'', 'log_name':'', 'task_id':''}
        task_id = int(kw.get('task_id', '0'))

        koji_url_handler = KojiURLHandler()
        cs = koji.ClientSession(koji_url_handler.get_xml_rpc_url())

        decendents = cs.getTaskDescendents(task_id)
        for task in decendents.keys():
            task_children = decendents[task]
            for child in task_children:
                if child['state'] == koji.TASK_STATES['FAILED']:
                    child_task_id = child['id']

                    error_code = 0
                    try:
                        # this should throw an error 
                        child_result = cs.getTaskResult(child_task_id)
                    except koji.BuildrootError, e:
                        error = str(e)
                        r = re.compile('mock exited with status (\d*)')
                        s = r.search(error)
                        error_code = int(s.group(1))

                    child_files = cs.listTaskOutput(child_task_id)

                    log_file = _mock_error_code_to_log_file(error_code)

                    if log_file not in child_files:
                        continue

                    log_url = koji_url_handler.get_file_url(child_task_id, log_file)

                    results['log_url'] = log_url
                    results['log_name'] = log_file 
                    results['task_id'] = child_task_id
                    # break out of loop since only one task should fail
                    # and the others should be canceled or succeed
                    # of course there is a race condition but first
                    # failure wins in the rare case there are more than one
                    break

        return results



class KojiFilesQuery(controllers.Controller):
    @expose("json", allow_json=True)
    def index(self, *args, **kw):
        results = {'logs':{}, 'downloads':{}}
        task_id = int(kw.get('task_id', '0'))
        state = int(kw.get('state', '0'))

        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())

        decendents = cs.getTaskDescendents(task_id)
        for task in decendents.keys():
            task_children = decendents[task]
            for child in task_children:
                child_task_id = child['id']
                child_label = child['label']
                child_files = cs.listTaskOutput(child_task_id, stat=True)
                
                last_log = (None, None)

                cf_keys = [] 
                if isinstance(child_files, dict):
                    cf_keys = child_files.keys()

                for f_name in cf_keys:
                    f_info = child_files[f_name]

                    f_type = 'downloads'
                    if not f_name.endswith('rpm'):
                        f_type = 'logs'

                        output = {'name': f_name, 
                                  'm_time': f_info['st_mtime'],
                                  'is_last': False}

                        f_type = 'logs'
                        if  f_info['st_mtime'] > last_log[1]:
                            if last_log[0]:
                                last_log[0]['is_last'] = False

                            output['is_last'] = True
                            last_log = (output, f_info['st_mtime'])
                    else:
                        output = {'name': f_name, 
                                  'm_time': f_info['st_mtime']}

                    if not results[f_type].has_key(child_label):
                        results[f_type][child_label] = []

                    results[f_type][child_label].append(output)

        return {'files': results}


