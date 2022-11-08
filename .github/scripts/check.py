'''
Check if ENVs in deploy are in Vault Engine for backen-monorepo
'''
import os
import sys
import hvac
import yaml

vault_url = os.environ['ADDR']
client = hvac.Client(url=vault_url)
client.token = os.environ['TOKEN']
rootEngine = os.environ['ROOT_ENGINE']

changedFiles = []
for fileName in sys.argv[1:]:
    if fileName.startswith("deploy/"):
        changedFiles.append(fileName)

if client.is_authenticated():
    missingSecrets = []
    for file in changedFiles:
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
                            missingSecrets.append(
                                f"{rootEngine}/{service}/{environment}/{env['secret']}")
            except yaml.YAMLError as exc:
                print(exc)
    if len(missingSecrets) > 0:
        print("::"*40)
        print(':: There are differences in Environment Variables and Vault Secrets')
        print(':: Missing Secrets')
        for item in missingSecrets:
            print(item)
        print("::"*40)
        sys.exit(1)
else:
    print("::"*40)
    print(":: Error in Vault authentication")
    print("::"*40)
    sys.exit(1)
