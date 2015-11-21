import sys
import json
from subprocess import check_output

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom

def create_item(attrs, contents):
    item = Element('item')
    for k in attrs: item.set(k, attrs[k])
    for k in contents:
        content = Element(k)
        content.text = contents[k]
        item.append(content)
    return(item)

def search_ec2_instances(query):
    output = check_output(['aws', 'ec2', 'describe-instances', '--instance-ids=%s' % query])
    response = json.loads(output.decode('utf-8'))
    return([i for r in response['Reservations'] for i in r['Instances']])

query = sys.argv[1].strip()

items = Element('items')
for i in search_ec2_instances(query):
    for k in ['PublicDnsName', 'PublicIpAddress', 'PrivateIpAddress', 'InstanceId', 'PrivateDnsName']:
        if k not in i: continue

        v = i[k]

        item = create_item(
            { 'uid': v, 'valid': 'YES', 'type': 'default' },
            { 'title': v, 'subtitle': k, 'arg': v }
        )
        items.append(item)

doc = minidom.parseString(ElementTree.tostring(items, 'utf-8'))
print(doc.toprettyxml())
