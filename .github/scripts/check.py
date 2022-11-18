'''
Check if ENVs in deploy are in Vault Engine for backen-monorepo
'''
import os
import sys
import hvac
import yaml


def promote():
    '''
    Check for promote workflow
    '''
    service = sys.argv[2]
    environment = sys.argv[3]
    all_secrets = client.secrets.kv.v1.read_secret(
        path=service + '/' + environment, mount_point=rootEngine)
    file = f'deploy/{environment}/{service}.yaml'
    missing_secrets = []
    with open(file, "r", encoding="utf-8") as stream:
        try:
            for env in yaml.safe_load(stream)['env']:
                if 'secret' in env.keys():
                    if env['secret'] in all_secrets['data'].keys():
                        pass
                    else:
                        missing_secrets.append(
                            f"{rootEngine}/{service}/{environment}/{env['secret']}")
        except yaml.YAMLError as exc:
            print(exc)
    if len(missing_secrets) > 0:
        print("::"*40)
        print(':: There are differences in Environment Variables and Vault Secrets')
        print(':: Missing Secrets')
        for item in missing_secrets:
            print(item)
        print("::"*40)
        sys.exit(1)

def envs():
    '''
    Check for env workflow
    '''
    changed_files = []
    for file_name in sys.argv[2:]:
        if file_name.startswith("deploy/"):
            changed_files.append(file_name)

    if client.is_authenticated():
        missing_secrets = []
        for file in changed_files:
            splitted = file.split('/')
            environment = splitted[1]
            service = splitted[2].split('.')[0]
            all_secrets = client.secrets.kv.v1.read_secret(
                path=service + '/' + environment, mount_point=rootEngine)
            with open(file, "r", encoding="utf-8") as stream:
                try:
                    for env in yaml.safe_load(stream)['env']:
                        if 'secret' in env.keys():
                            if env['secret'] in all_secrets['data'].keys():
                                pass
                            else:
                                missing_secrets.append(
                                    f"{rootEngine}/{service}/{environment}/{env['secret']}")
                except yaml.YAMLError as exc:
                    print(exc)
        if len(missing_secrets) > 0:
            print("::"*40)
            print(':: There are differences in Environment Variables and Vault Secrets')
            print(':: Missing Secrets')
            for item in missing_secrets:
                print(item)
            print("::"*40)
            sys.exit(1)
    else:
        print("::"*40)
        print(":: Error in Vault authentication")
        print("::"*40)
        sys.exit(1)


vault_url = os.environ['ADDR']
client = hvac.Client(url=vault_url)
client.token = os.environ['TOKEN']
rootEngine = os.environ['ROOT_ENGINE']
if sys.argv[1] == 'env':
    envs()
elif sys.argv[1] == 'promote':
    promote()
else:
    print("::Wrong Workflow Name (not \'env\' neither \'promote\')")
