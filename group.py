URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
    config={}
    config['resources'] = []

    itName = context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-it'
    it = {
        'name': itName,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'properties': {
                'machineType': context.properties['nodeType'],
                'networkInterfaces': [{
                    'network': URL_BASE + context.env['project'] + '/global/networks/default',
                    'accessConfigs': [{
                        'name': 'External NAT',
                        'type': 'ONE_TO_ONE_NAT'
                    }]
                }],
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': URL_BASE + 'ubuntu-os-cloud/global/images/ubuntu-1404-trusty-v20170424'
                    },
                    'diskType': 'pd-ssd',
                    'diskSizeGb': context.properties['diskSize']
                }],
                'metadata': {'items': [{'key':'startup-script', 'value':GenerateStartupScript(context)}]},
            }
        }
    }
    config['resources'].append(it)

    igm = {
        'name': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-igm',
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'region': context.properties['region'],
            'baseInstanceName': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-instance',
            'instanceTemplate': '$(ref.' + itName + '.selfLink)',
            'targetSize': context.properties['nodeCount'],
            'autoHealingPolicies': [{
                'initialDelaySec': 60
            }]
        }
    }
    config['resources'].append(igm)

    return config

def GenerateStartupScript(context):
    script = '#!/usr/bin/env bash\n\n'
    script += 'couchbaseUsername="' + context.properties['couchbaseUsername'] + '"\n'
    script += 'couchbasePassword="' + context.properties['couchbasePassword'] + '"\n'

    services=context.properties['services']
    servicesParameter=''
    for service in services:
        servicesParameter += service + ','
    servicesParameter=servicesParameter[:-1]
    script += 'services="' + servicesParameter + '"\n\n'

    if 'syncGateway' in services or 'accelerator' in services:
        script+=context.imports['scripts/installMobile.sh']
#        script+= context.imports['scripts/configureMobile.sh']
    else:
        script+= context.imports['scripts/installServer.sh']
#        script+= context.imports['scripts/configureServer.sh']
    return script
