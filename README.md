# DON: Diagnosing OpenVswitch Networking

> This work was [presented in the OpenStack Liberty Summit held in Vancouver in May, 2015]
(https://www.openstack.org/summit/vancouver-2015/summit-videos/presentation/don-diagnosing-ovs-in-neutron "DON Presentation at OpenStack Liberty Summit, Vancouver, May 2015").

Neutron provides Networking-as-a-service in the OpenStack ecosystem. Networking
functionalities are provided by plugins that implement well-defined Neutron
APIs. Among many, the Open vSwitch plugin (OVS) is possibly the most widely
used. Any practical OpenStack installation has complicated networking
configuration and verifying it manually is time consuming and error prone.
DON, a [django](https://www.djangoproject.com/) app, provides a
completely automated service for verifying and diagnosing the
networking functionality provided by OVS. This service verifies (or points out
deviations) that the user configuration is indeed reflected in the underlying
infrastructure and presents the results in an intuitive graphical display.

As an example, given the following Neutron network topology:
![Neutron: Network Topology](/don/static/net_topology.PNG "Neutron: Network Topology")

DON generates the following view of the networking internals,
![DON: Internal View](/don/static/don_internal.PNG "DON: Internal View")

does OVS tests and ping tests,
![DON: Analysis](/don/static/don_analysis.PNG "DON: Analysis")

and also allows the user to do ping tracing
![DON: Ping Tracer](/don/static/don_ping_notworking.PNG "DON: Ping Tracer")

The project is in beta status and owing to overwhelming response at the
OpenStack Liberty Summit, we will be moving this to
[stackforge](https://github.com/stackforge) sometime soon.

## How to Run:

0. You must have a [devstack setup running on a single VM](http://docs.openstack.org/developer/devstack/guides/single-vm.html).
1. [Download and source the project specific rc file](http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html).
2. `cd don; python collector.py` - this generates don.json. Update the `myenv` dictionary in
   don/collector.py to match the settings in the file downloaded in the previous
   step. **This step is soon going to be automated and integrated with the next
   step.**
3. DON runs as a  application.
   `python manage.py runserver 0.0.0.0:8000.` This runs the django server that
   accepts requests on port 8000 from any IP address. For more understanding of
   how to start the django server, please look at official django documentation.
   If you get an error "Error: That port is already in use." and you are sure
   that there is nothing listening on the port, then use `sudo fuser -k 8000/tcp`
   to kill any process that might still be listening on that port.

### TODO:
- **Move to [stackforge](https://github.com/stackforge)**
- integrate with Horizon
- multi-thread for faster ping test
- Handle floating ips (br-ex on network node has to be updated)
- add legend
- figure out public network (since it does not have qdhcp associated with it)
- admin-openrc.sh file as input
- Get eth0/eth1 of each interface
- Invisible edges - to make figure have similar ordering of nodes even if there
  are no edges
- Clickable SVG (to get more detail). Will need javascript.
- Multi node setup

## Issues/Comments:
If you have questions, bugs, or feature requests, file an issue or send email
to:

* Amit Saha (amisaha+don@cisco.com)

