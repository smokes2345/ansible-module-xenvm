#!/usr/bin/python
import XenAPI
import provision
import difflib

class XenVM:

	name = ""
	desired['state'] = 'absent'
	current['state'] = 'absent'
	desired['power_state'] = 'halted'
	current['power_state'] = 'halted'
	desired['cpu'] = 1
	current['cpu'] = 0
	desired['ram'] = {128, 512}
	current['ram'] = 0
	desired['net'] = []
	current['net'] = []

	_xen = None
	_hv_ref = None
	_hv_data = None

	def __init__(self,xen,desired_state='present',name,cpu,ram,net):
		self.desired['name'] = name
		self.desired['cpu'] = cpu
		self.desired['ram'] = ram
		self.desired['net'] = net
		self._xen = xen
		get_current_state()

	def get_current_state(self):
		_get_hv_ref()
		if self.current['state'] == 'present':
			try:
				self._get_net_names()
				self.current['power_state'] = self._hv_data['power_state']


    def _get_net_names(self):
        for nic_ref in self._hv_data['VIFs']:
            nic_data = self._xen.xenapi.VIF.get_record(nic_ref)
            net_data = self._xen.xenapi.network.get_record(self._xen.xenapi.network.get_by_name_label(nic_data['network'])[0])
            self.current['net'].append(net_data['name_label'])

    def _create_vif(self,net,device_num=0):
        #print "Device: " + str(device_num)
        vif = { 'device': str(device_num),
            'network': net,
            'VM': self._hv_ref,
            'MAC': "",
            'MTU': "1500",
            "qos_algorithm_type": "",
            "qos_algorithm_params": {},
            "other_config": {} }
        session.xenapi.VIF.create(vif)

	def _get_hv_ref(self):
		try:
			self._hv_ref = self._xen.xenapi.VM.get_by_name_label(self.name)[0]
			self._hv_data = self._xen.xenapi.VM.get_record(self._hv_ref)
			self.current['state'] = 'present'
		except Exception as e:
			self.current['state'] = 'absent'

	def create(self,template=None):
		self._xen.xenapi.VM.clone(template,self.desired['name'])

	def get_diff(self):
		difflib.SequenceMatcher(self.current,self.desired)

if __name__ == "__main__":
	session = XenAPI.Session(module.params['url'])
    try:
        session.xenapi.login_with_password(module.params['username'], module.params['password'])
        print "Connected to xenserver"
    except:
    	print "Could not connect"
        #module.fail_json(failed=True,msg="Could not login to server!")

    try:
    	vm = XenVM(session,'present',"xenvm_class_test",1,256,"Private1")
    	print "Created VM"
