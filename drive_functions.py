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


#
#
#
def change_dir(name):
    global path
    global cwd_subdirs
    global cwd_id

    #print('debug-cd0: {0}'.format(name))

    if(name == '..'):
        if(len(path) > 1):
            #print('debug-cd00: {0}'.format(path))
            #print('debug-cd01: {0}'.format(path_id))
            path.pop()
            parent = path_id.pop()
            #print('debug-cd02: {0}'.format(path))
            #print('debug-cd03: {0}'.format(path_id))
            #print('debug-cd03: {0}'.format(path_id[-1]))
            
            cwd_subdirs = fetch_subdirs(path_id[-1])
    else:
        #print('debug-cd1: {0}'.format(path))
        #print('debug-cd2: {0}'.format(path_id))
        path_id.append(cwd_subdirs[name][0])
        path.append(name)
        #print('debug-cd3: {0}'.format(path))
        #print('debug-cd4: {0}'.format(path_id))
        #print('debug-cd5: {0}'.format(cwd_subdirs[path[-1]]))
        cwd_subdirs = fetch_subdirs(path_id[-1],path_id[-2]) #cwd_subdirs[path[-1]][0])

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

    #print('dir: ' + dir)

    if(subdir_map.get(dir,None)):
        #print('cache hit')
        return subdir_map[dir]
    
    else:
        #print('cache miss')
        q = 'mimeType = "application/vnd.google-apps.folder" and "{0}" in parents'.format(dir)
        params = {'pageSize':1000,
                  'spaces':'drive',
                  'fields':'nextPageToken, files(id, name)'}
        params['q'] = q
        name_id_map = {}
        files = execute_request(conn.files().list, params)
        #files = conn.files().list(**params).execute().get('files', [])

        for file in files:
            name_id_map[file['name']] = [file['id']]

        if (dir == DRIVE_ROOT_FOLDER):
            #print(fetch_shared_dirs())
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
    pass

def make_directory(name):
    pass

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
    pass

def rename_file(id, name):
    global conn
    
    return conn.files().update(fileId=id,name=name,fields='id, parents').execute()

    
#
#
#
def generate_drive_connection():
    credentials = get_credentials(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME)
    http = credentials.authorize(httplib2.Http())

    return discovery.build('drive', 'v3', http=http)

conn = generate_drive_connection()
cwd_subdirs = fetch_subdirs(DRIVE_ROOT_FOLDER)
