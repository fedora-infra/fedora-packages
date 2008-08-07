from myfedora.lib.base import Controller, BaseController
from tg import expose

import koji
import re
import urllib2

# FIXME: get from configuration
koji_url = 'http://koji.fedoraproject.org'
koji_xmlrpc = koji_url + '/kojihub'
koji_getfile = koji_url + '/koji/getfile'

cvs_url = 'http://cvs.fedoraproject.org/'

def _mock_error_code_to_log_file(err_code):
    log_file = ''
    if err_code == 1:
        log_file = 'build.log'
    elif err_code == 10 or err_code == 30:
        log_file = 'root.log'
    else:
        print "Unhandled error code :", err_code

    return log_file

class CvsQuery(Controller):
    @expose()
    def get_page(self, *path):
        return urllib2.urlopen(cvs_url + '/'.join(path)).read()

class KojiQuery(Controller):
    @expose("json")
    def get_tags(self, *args, **kw):
        build_id = int(kw.get('build_id', '0'))

        cs = koji.ClientSession(koji_xmlrpc)
        tags = cs.listTags(build = build_id)

        return {'tags': tags}

    @expose("json")
    def get_error_log(self, *args, **kw):
        results = {'log_url':'', 'log_name':'', 'task_id':''}
        task_id = int(kw.get('task_id', '0'))

        cs = koji.ClientSession(koji_xmlrpc)

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
                    
                    log_url = koji_getfile + '?taskID=' + str(child_task_id) + '&name=' + log_file

                    results['log_url'] = log_url
                    results['log_name'] = log_file 
                    results['task_id'] = child_task_id
                    # break out of loop since only one task should fail
                    # and the others should be canceled or succeed
                    # of course there is a race condition but first
                    # failure wins in the rare case there are more than one
                    break

        return results

    @expose("json")
    def get_files(self, *args, **kw):
        results = {'logs':{'count':0}, 'downloads':{'count':0}}
        task_id = int(kw.get('task_id', '0'))
        state = int(kw.get('state', '0'))

        cs = koji.ClientSession(koji_xmlrpc)

        decendents = cs.getTaskDescendents(task_id)
        for task in decendents.keys():
            task_children = decendents[task]
            for child in task_children:
                child_task_id = child['id']
                child_label = child['label']
                child_files = cs.listTaskOutput(child_task_id, stat=False)
                
                last_log = (None, None)

                cf_keys = child_files
                
                if isinstance(child_files, dict):
                    cf_keys = child_files.keys()

                for f_name in cf_keys:
                    f_type = 'downloads'
                    if not f_name.endswith('rpm'):
                        f_type = 'logs'

                    if not results[f_type].has_key(child_label):
                        results[f_type][child_label] = []

                    url = koji_getfile + '?taskID=' + str(child_task_id) + '&name=' + f_name
                    file_result = {'name': f_name, 'url': url}
 
                    results[f_type][child_label].append(file_result)
                    results[f_type]['count'] += 1

                    results[f_type][child_label].sort(lambda a, b: cmp(a['name'], b['name']))


        return {'files': results}

class ProxyController(Controller):
    koji = KojiQuery()
    cvs = CvsQuery()
    #bodhi = BodhiQuery()