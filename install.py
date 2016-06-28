import argparse
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import ansible.constants as CONSTANTS
import sys

CONSTANTS.HOST_KEY_CHECKING = False

class Installer:
	def __init__(self,host_ip,username,password):
		self.host_ip = host_ip
		self.username = username
		self.password = password
		try:
			self.host_info = ansible.inventory.host.Host(
			    name = host_ip,
			    )
			#this group name mapped to playbook host info
			group = ansible.inventory.group.Group(
			    name = 'don'
			    )
			group.add_host(self.host_info)

			#setting up inventory
			self.inventory = ansible.inventory.Inventory()
			self.inventory.add_group(group)
			self.inventory.subset('don')
		except Exception,err:
			print "Installer Initiation failed"
			sys.exit()
		print "Installer Init successful"

	def execute_playbook(self,playbook_file='don_playbook.yaml'):
		playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
		stats = callbacks.AggregateStats()
		runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
		# inventory = Inventory(host)
		pb = ansible.playbook.PlayBook(
		    playbook=playbook_file,
		    remote_user=self.username,
		    remote_pass=self.password,
		    callbacks=playbook_cb,
		    runner_callbacks=runner_cb,
		    inventory=self.inventory,     
		    stats=stats,
		    # private_key_file='/path/to/key.pem'
		)
		results = pb.run()
		playbook_cb.on_stats(pb.stats)
		return results



if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-host', action='store', dest='host_ip',
        	            help='Provide Host IP address')
	parser.add_argument('-u', action='store', dest='username',
						help="Username of Host")
	parser.add_argument('-p', action='store', dest='password',
						help='Password of Host')
	args = parser.parse_args()

	if not args.host_ip or not args.username or not args.password:
		parser.print_help()
	else:
		install = Installer(args.host_ip, args.username, args.password)
		response = install.execute_playbook()
		if response[args.host_ip]['failures'] != 0:
			print "Installation failed"
		else:
			print "Installation Successful!!"
		#print results.host_name
	

