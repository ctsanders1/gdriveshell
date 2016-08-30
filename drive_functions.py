import httplib2
import os
import logging

from apiclient import discovery

from config import APPLICATION_NAME, CLIENT_SECRET_FILE, DRIVE_ROOT_FOLDER, SCOPES
from auth import get_credentials

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

conn = None
path = ['']
path_id = [DRIVE_ROOT_FOLDER]
cwd_subdirs = None
cwd_id = None
spaces = {'drive',
          'appDataFolder',
          'photos'}
space = 'drive'
subdir_map = {}

#
#
#
def debug_info():
    global conn
    global path
    global cwd_subdirs
    global subdir_map
    
    return {'conn':conn,
            'path':path,
            'cwd_subdirs':cwd_subdirs,
            'subdir_map':subdir_map}

#
# 
#
def execute_request(request, params):

    res = request(**params).execute()
    files = res.get('files', [])

    while res.get('nextPageToken', False):
        params['pageToken'] = res['nextPageToken']
        res = request(**params).execute()
        files += res.get('files', [])

    return files


def file_exists(name, only_in_cwd=True):
    global conn
    global path_id

    params = {'pageSize':1,
              'fields':'nextPageToken, files(name)'}
    q = 'name = "{0}"'.format(name)

    if (only_in_cwd):
        q += ' and "{0}" in parents'.format(path_id[-1])

    params['q'] = q

    return execute_request(conn.files().list, params)

#
#
#
def change_dir(name):
    global path
    global cwd_subdirs
    global cwd_id

    if(name == '..'):
        if(len(path) > 1):
            path.pop()
            cwd_subdirs = fetch_subdirs(path_id[-1])
    else:
        path_id.append(cwd_subdirs[name][0])
        path.append(name)
        cwd_subdirs = fetch_subdirs(path_id[-1],path_id[-2])

    return path


def change_space(n_space):
    global space
    global spaces
    
    if ({n_space}.issubset(spaces)):
        space = n_space
        return True
    else:
        return False
    

def copy_file(source, target):
    pass

def create_file(name, mime_type):
    params = {'body':{'name':name,
                      'mimeType':mime_type},
              'fields':'id'}
    return conn.files().create(**params).execute()

def enumerate_directories():
    global conn
    global dir_tree

    q_tmpl = 'mimeType = "application/vnd.google-apps.folder" and "{0}" in parents'
    params = {'pageSize':1000,
              'spaces':'drive',
              'fields':'nextPageToken, files(id, name)'}
    stack = [DRIVE_ROOT_FILDER]
    retval = {'..':None}
    retval['..'] = retval
    cwd = retval

    while (stack):
        node = stack.pop(0)
        cwd = cwd.get(node,cwd)
        q = q_tmpl.format(node)
        params['q'] = q

        for folder in execute_request(conn.files().list, params):
            stack.append(folder['id'])
            f_dict = {'..':cwd}
            cwd[folder['name']] = f_dict
            cwd[folder['id']] = f_dict


def fetch_shared_dirs():
    global conn
    q = 'mimeType = "application/vnd.google-apps.folder" and sharedWithMe = true'.format(dir)
    params = {'pageSize':1000,
              'spaces':'drive',
              'q':q,
              'fields':'nextPageToken, files(id, name)'}

    name_id_map = {}
    files = filter(lambda x: x.get('parents', True),
                   conn.files().list(**params).execute().get('files', []))

    for file in files:
        name_id_map[file['name']] = [file['id']]
   
    return name_id_map


def fetch_subdirs(dir,parent=None):
    global conn
    global subdir_map

    if(subdir_map.get(dir,None)):
        return subdir_map[dir]
    else:
        q = 'mimeType = "application/vnd.google-apps.folder" and "{0}" in parents'.format(dir)
        params = {'pageSize':1000,
                  'spaces':'drive',
                  'fields':'nextPageToken, files(id, name)'}
        params['q'] = q
        name_id_map = {}
        files = execute_request(conn.files().list, params)

        for file in files:
            name_id_map[file['name']] = [file['id']]

        if (dir == DRIVE_ROOT_FOLDER):
            name_id_map.update(fetch_shared_dirs())
        else:
            name_id_map['..'] = subdir_map[parent]

        subdir_map[dir] = name_id_map
        
        return name_id_map


def get_file(**kwargs):
    pass

def get_file_by_id(id):
    q = ''
    params = {'pageSize':1000,
              'spaces':'drive',
              'fields':'nextPageToken, files(id, owners, size, modifiedTime, version, name,' \
              'parents, mimeType, shared, capabilities)'}

    if(len(cwd) > 0):
        q += '{0} in parents'.format(cwd)
    else:
        q += '{0} in parents'.format(DRIVE_ROOT_FOLDER)

    if(qstring):
        q += ' and ' + qstring

    params['q'] = q
    
    return conn.files().list(**params).execute()


def get_file_by_name(name):
    global conn
    global path_id

    q_tmpl = '{0} in parents and name = {1}'
    params = {'pageSize':1000,
              'spaces':'drive',
              'fields':'nextPageToken, files(id, owners, size, modifiedTime, version, name,' \
              'parents, mimeType, shared, capabilities)'}

    if(len(cwd) > 0):
        q += '{0} in parents'.format(cwd)
    else:
        q += '{0} in parents'.format(DRIVE_ROOT_FOLDER)

    if(qstring):
        q += ' and ' + qstring

    params['q'] = q


def make_directory(name):
    global cwd_subdirs
    res = file_exists(name)
    print('make_directory:file_exists:res: {0}'.format(res))
    if(res): #file_exists(name)):
        print('make_directory:false')
        return False
    else:
        res = create_file(name, 'application/vnd.google-apps.folder')
        print('make_directory:create_file:res: {0}'.format(res))
        cwd_subdirs[name] = [res['id']]
        return res

def move_file(source, target):
    pass

def link_file(source, target):
    pass

def list(cwd, qstring=None):
    global conn

    q = ''
    params = {'pageSize':1000,
              'spaces':space,
              'fields':'nextPageToken, files(id, owners, size, modifiedTime, version, name,' \
              'parents, mimeType, shared, capabilities)'}

    if(len(cwd) > 0):
        q += '"{0}" in parents'.format(path_id[-1])
    else:
        q += '"{0}" in parents'.format(DRIVE_ROOT_FOLDER)

    if(qstring):
        q += ' and ' + qstring

    params['q'] = q

    return  execute_request(conn.files().list, params)

def list_shared_folders():
    global conn

    params = {'pageSize':1000,
              'spaces':space,
              'q':'mimeType = "application/vnd.google-apps.folder" and sharedWithMe = true',
              'fields':'nextPageToken, files(id, owners, size, modifiedTime, version, name,' \
              'parents, mimeType, shared, capabilities)'}
    
    return conn.files().list(**params).execute()


def remove_directory(name):
    # application/vnd.google-apps.folder
    pass

def rename_file(old_name, new_name):
    global conn
    global path_id

    q_tmpl = '"{0}" in parents and name = "{1}"'
    params = {'pageSize':1000,
              'spaces':'drive',
              'fields':'files(id)'}

    params['q'] = q_tmpl.format(path_id[-1], old_name)

    res = execute_request(conn.files().list, params)

    if (len(res) == 0):
        return -1
    elif (len(res) > 1):
        return -2
    else:
        res = conn.files().update(fileId=res[0]['id'],
                                  body={'name':new_name},
                                  fields='name').execute()
        return 0


    
#
#
#
def generate_drive_connection():
    credentials = get_credentials(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME)
    http = credentials.authorize(httplib2.Http())

    return discovery.build('drive', 'v3', http=http)

conn = generate_drive_connection()
cwd_subdirs = fetch_subdirs(DRIVE_ROOT_FOLDER)
