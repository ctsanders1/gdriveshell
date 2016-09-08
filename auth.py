def get_credentials(csf, scopes, app_name, app_ver):
    import os
    from oauth2client import client,file,tools
    from argparse import ArgumentParser

    flags = ArgumentParser(parents=[tools.argparser]).parse_args()
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gdriveshell_credentials.json')

    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(csf, scopes)
        flow.user_agent = app_name + '/' + app_ver
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials
