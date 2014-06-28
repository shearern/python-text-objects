
import os
import unittest

from txtobjs.text_parsers.YamlTextParser import YamlTextParser
from txtobjs.TextObjectLoader import TextOjbectLoader

from SiteSchema import SiteSchema

class ServersUseCaseTests(unittest.TestCase):
    '''A use case where the structure of a network of servers is described'''

    def setUp(self):
        parser = YamlTextParser()
        loader = TextOjbectLoader()
        self.site = loader.parse_single_object_file(
            path = os.path.join(os.path.dirname(__file__), 'site.yml'),
            parser = parser,
            schema = SiteSchema())
        loader.link()


    def testSiteTextClass(self):
        self.assertEqual(self.site.txt_class, 'Site')


    def testSiteName(self):
        self.assertEqual(self.site.name, 'Home')


    def testCollectionsIterable(self):
        self.assertEqual(set([x.name for x in self.site.networks]),
                         set(['Home_Internal', 'Home_Wireless', 'Home_External']))
        self.assertEqual(set([x.name for x in self.site.machines]),
                         set(['Workstation', 'FileServer']))
        self.assertEqual(set([x.name for x in self.site.services]),
                         set(['Samba', ]))


    def testRetrieveNetworks(self):
        for name in ['Home_Internal', 'Home_Wireless', 'Home_External']:
            network = self.site.get_network(name)
            self.assertIsNotNone(network,
                                 "Failed to retrieve network %s" % (name))


    def testNetworkAttributes(self):
        network = self.site.networks['Home_Internal']
        self.assertEqual(network.name, 'Home_Internal')
        self.assertEqual(network.ip, '192.168.1.0')
        self.assertEqual(network.netmask, '255.255.255.0')
        self.assertEqual(network.vlan, 2)
        self.assertEqual(network.gateway, '192.168.1.1')


    def testRetrieveMachines(self):
        for name in ['Workstation', 'FileServer']:
            machine = self.site.get_machine(name)
            self.assertIsNotNone(machine,
                                 "Failed to retrieve machine %s" % (name))


    def testMachineName(self):
        for name in ['Workstation', 'FileServer']:
            machine = self.site.get_machine('Workstation')
            self.assertEqual(machine.name, name)


    def testRetrieveMachinesLikeDict(self):
        for name in ['Workstation', 'FileServer']:
            machine = self.site.machines[name]
            self.assertIsNotNone(machine,
                                 "Failed to retrieve machine %s" % (name))



    def testMachinePrimaryInterface(self):
        self.assertEqual(self.site.machines['Workstation'].primary_interface,
                         "eth0")
        self.assertIsNone(self.site.machines['FileServer'].primary_interface)


    def testMachineInterfaces(self):
        iface = self.site.machines['Workstation'].interfaces['eth0']
        self.assertIsNotNone(iface)
        self.assertEqual(iface.ip, '192.168.1.10')
        self.assertEqual(iface.mac, '01:50:56:A9:00:A4')
        self.assertEqual(iface.provisioned, 'dhcp')


    def testMachineInterfaceNetworkLinked(self):
        iface = self.site.machines['Workstation'].interfaces['eth0']
        self.assertEqual(iface.network.name, 'Home_Internal')
        self.assertEqual(iface.network,
                         self.site.networks['Home_Internal'])


    def testMachineGroups(self):
        self.assertEqual(self.site.machines['FileServer'].groups,
                         ['servers', 'home_server', 'file_server'])


    def testServiceRoleName(self):
        self.assertEqual(self.services['Samba'].role_name, 'home_samba')


    def testServiceHostsLinked(self):
        self.assertEqual(self.services['Samba'].hosts['FileServer'].hostname,
                         'fs')


    def testServiceFirewallPorts(self):
        self.assertEqual(set(self.services['Samba'].firewall['allow_http'].ports),
                         set([80, 443]))

    def testServiceNetsLinked(self):
        self.assertEqual([n.name for n in self.services['Samba'].firewall['allow_http'].allowed_nets],
                         ['Home_Internal', 'Home_Wireless'])




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()