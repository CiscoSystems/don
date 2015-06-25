## DON: Diagnosing OVS in Neutron

> [Presented in the OpenStack Liberty Summit, Vancouver, May, 2015]
(https://www.openstack.org/summit/vancouver-2015/summit-videos/presentation/don-diagnosing-ovs-in-neutron "DON Presentation at OpenStack Liberty Summit, Vancouver, May 2015").

Neutron provides Networking-as-a-service in the OpenStack ecosystem. Networking
functionalities are provided by plugins that implement well-defined Neutron
APIs. Among many, the Open vSwitch plugin (OVS) is possibly the most widely
used. Any practical OpenStack installation has complicated networking
configuration and verifying it manually is time consuming and error prone.
DON, written in [django](https://www.djangoproject.com/), is a network analysis
and diagnostic system and provides a
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
3. `python manage.py runserver 0.0.0.0:8000.` This runs the django server that
   accepts requests on port 8000 from any IP address. For a better understanding of
   how to start the django server, please look at official django documentation.
   If you get an error "Error: That port is already in use." and you are sure
   that there is nothing listening on the port, then use `sudo fuser -k 8000/tcp`
   to kill any process that might still be listening on that port.

### TODO/Known Issues:
- **Move to [stackforge](https://github.com/stackforge)**
- Remove hardcoded "cirros" and "cubswin:)" password (default ones used in
  OpenStack Cirros VMs). Ideally, the user should be prompted for this or a
  config file should have this.
- integrate with Horizon
- multi-thread for faster ping test
- Handle floating ips (br-ex on network node has to be updated)
- add legend - low priority
- figure out public network (since it does not have qdhcp associated with it)
- admin-openrc.sh file as input
- Get eth0/eth1 of each interface
- Invisible edges - to make figure have similar ordering of nodes even if there
  are no edges
- Clickable SVG (to get more detail). Will need javascript.
- Multi node setup
- ~~ping with tcpdump for vms attached to different network - visualize~~
- ~~ping with tcpdump for vms attached to same network - visualize~~
- ~~Anomalies to be displayed~~
- ~~display ping and ovs-appctl results~~
- ~~ovs-appctl commands~~
- ~~ping test~~
- ~~Plot the port ids (makes it easier to debug)~~
- ~~Combine compute and network figures~~
- ~~Collect network node related commands~~
- ~~Draw network node~~
- ~~Draw compute node~~
- ~~Get IP of each interface~~
- ~~Get network name (private0, private1, ...) for each port~~
- ~~Color code the vlans. same color for the same vlan tag.~~
- ~~Get VLAN tags for br-int~~

## Issues/Comments:
If you have questions, bugs, or feature requests, file an issue or send email
to:

* Amit Saha (amisaha+don@cisco.com)
* Pritesh Kothari (pritkoth+don@cisco.com)

