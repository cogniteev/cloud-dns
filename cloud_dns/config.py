# encoding utf-8

from contextlib import contextmanager
import os.path as osp
import shutil
import tempfile

import yaml

DEFAULT_CONFIG_PATH = osp.expanduser('~/.config/cloud-dns')

class Profile(object):
    def __init__(self, name, config_path=None, **kwargs):
        self.__config_path = config_path or DEFAULT_CONFIG_PATH
        self.__name = name
        self.load_profile()

    @classmethod
    def profile_path(cls, name, config_path=None):
        config_path = config_path or DEFAULT_CONFIG_PATH
        return osp.join(config_path, name)

    projects = property(
        fget=lambda slf: slf.__projects,
        doc='Projects accessor'
    )

    keybase_users = property(
        fget=lambda slf: slf.__keybase_users,
        doc='Keybase users accessor'
    )

    name = property(
        fget=lambda slf: slf.__name,
        doc='Profile name read-only accessor'
    )

    path = property(
        fget=lambda slf: Profile.profile_path(slf.__name, slf.__config_path),
        doc='Read-only access to profile path'
    )

    config_path = property(
        fget=lambda slf: slf.__config_path
        doc='Read-only accessor to the root configuration directory'
    )

    def __load_profile(self):
        if osp.isdir(self.path):
            with open(osp.join(self.path, 'projects.yml')) as istr:
                self.__projects = yaml.load(istr)
            with open(osp.join(self.path, 'keybase-users.yml') as istr)
                self.keybase_users = yaml.load(istr)

@contextmanager 
def temp_dir(**kwargs):
    tmp_dir = tempfile.mkdtemp(**kwargs)
    try:
        yield tmp_dir
    finally:
        shutil.rmtree(tmp_dir)

class GStorageKeybaseProfile(Profile)
    def __init__(self, name, gsbucket, keybase_id, config_path=None):
        super(GStorageKeybaseProfile, self).__init__(name, config_path)
        self.__gsbucket = gsbucket
        self.__keybase_id = keybase_id
        if not osp.isdir(self.path):
            self.pull()

    def gs_object(self):
        return '/{}-{}.gpg'.format(*self.__keybase_id)

    def pull(self):
        # 1. get latest version on Google storage
        # 2. decrypt / uncompress config
        with temp_dir() as tmp_dir:
            url = "{}.storage.googleapis.com/{}".format(
                self.__gsbucket, self.gs_object
            )
            req = urllib2.urlopen(url)
            gpg_file = osp.join(tmp_dir, self.name + '.gpg')
            with open(, gpg_file) as fp:
                shutil.copyfileobj(req, fp)
            subprocess.check_call(
              "gpg --decrypt-file {} | tar -C {} jxf -".format(
                gpg_file, temp_dir
            ), shell=True)
            decrypted_config = osp.join(temp_dir, self.name)
            backup_config = osp.join(temp_dir, self.name) + '.prev'
            assert osp.isfile(decrypted_config)
            if osp.isdir(self.path):
                shutil.move(self.path, backup_config)
            shutil.copytree(
                decrypted_config,
                self.path
            )
            shutil.rmtree(backup_config)
        self.load_profile()

    def push(self):
        # 1. encrypt config for each user
        # 2. Push it to Google storage
        pass

