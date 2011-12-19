import os
import tempfile
import shutil
import fnmatch

class RPMCache(object):
    def __init__(self, pkg, yum_base, cache_dir='cache', max_retry=10):
        rpm_envra = pkg.ui_envra
        if ':' in rpm_envra:
            rpm_envra = rpm_envra.split(':')[1]

        self.rpm_file_name = "%s.rpm" % rpm_envra
        self.rpm_envra = rpm_envra
        self.cache_dir = os.path.join(cache_dir, 'rpms')
        self.retry = 0
        self.pkg = pkg
        self.yum_base = yum_base
        self.max_retry = max_retry

        # create cache dir if it does not exist
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        self.tmp_dir = None

    def open(self):
        self.tmp_dir = tempfile.mkdtemp()

    def _download_rpm(self):
        self.rpm_path = os.path.join(self.cache_dir, self.rpm_file_name)
        if not os.path.exists(self.rpm_path):
            repo = self.yum_base.repos.getRepo(self.pkg.repoid)
            repo.cache = 0
            self.pkg.localpath = self.rpm_path
            print "Downloading %s" % self.rpm_path
            path = repo.getPackage(self.pkg)

    def _extract_file(self, file_path):
        os.chdir(self.tmp_dir)

        if self.decompress_filter == None:
            decompress_filter =  os.path.basename(file_path)
        else:
            decompress_filter = self.decompress_filter

        cmd = 'rpm2cpio %s | cpio -idmv --no-absolute-filenames %s' % (self.rpm_path, decompress_filter)
        print cmd
        os.system(cmd)
        os.chdir(self.cache_dir)

    def prep_file(self, file_path, decompress_filter=None):
        self._download_rpm()
        self.decompress_filter = decompress_filter
        full_path = self.tmp_dir + '/' + file_path

        if not os.path.exists(full_path):
            self._extract_file(file_path)

        # retry if file did not get extracted
        if not os.path.exists(full_path):
            print "Retrying for file %s" % full_path
            retry = True
            exists = False
            while retry and not exists:
                retry = self._retry(file_path)
                exists = os.path.exists(full_path)

            if exists:
                return full_path
            else:
                return None

        else:
            return full_path

    def open_file(self, file_path, access='r', decompress_filter=None):
        full_path = self.prep_file(file_path, decompress_filter)
        if full_path == None:
            return None

        return open(full_path, access)

    def find_file(self, filename, file_glob="*"):
        """ Finds the first file that matches the filename and
            file_glob and extracts it

            Returns the complete path to that file or None
        """
        for filepath in self.pkg.filelist:
            basename = os.path.basename(filepath)
            if basename == filename:
                if fnmatch.fnmatch(filepath, file_glob):
                    return self.prep_file(filepath, file_glob)

        return None

    def find_files(self, filename, file_glob="*"):
        """ Finds the all file that matches the filename and
            file_glob and extracts them

            Returns the complete path to all files as a list
        """
        results = []
        for filepath in self.pkg.filelist:
            basename = os.path.basename(filepath)
            if basename == filename:
                if fnmatch.fnmatch(filepath, file_glob):
                    found_file = self.prep_file(filepath, file_glob)
                    if found_file:
                        results.append(found_file)
        return results


    def _retry(self, file_path):
        if self.retry <= self.max_retry:
            self.retry += 1
            try:
                os.remove(self.rpm_path)
            except OSError:
                pass
            self._download_rpm()
            self._extract_file(file_path)
            return True
        return False

    def close(self):
        shutil.rmtree(self.tmp_dir)
