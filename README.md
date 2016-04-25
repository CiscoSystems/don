# DON: Diagnosing OVS in Neutron

> [Presented in the OpenStack Liberty Summit, Vancouver, May, 2015]
(https://www.openstack.org/summit/vancouver-2015/summit-videos/presentation/don-diagnosing-ovs-in-neutron "DON Presentation at OpenStack Liberty Summit, Vancouver, May 2015").

[quote]
## Notice
DON is now integrated with Horizon. See #how-to-run.
[/quote]

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
![Neutron: Network Topology](/openstack_dashboard/don/ovs/static/net_topology.PNG "Neutron: Network Topology")

DON generates the following view of the networking internals,
![DON: Internal View](/openstack_dashboard/don/ovs/static/don_internal.PNG "DON: Internal View")

does OVS tests and ping tests,
![DON: Analysis](/openstack_dashboard/don/ovs/static/don_analysis.PNG "DON: Analysis")

and also allows the user to do ping tracing
![DON: Ping Tracer](/openstack_dashboard/don/ovs/static/don_ping_notworking.PNG "DON: Ping Tracer")

The project is in beta status and owing to overwhelming response at the
OpenStack Liberty Summit, we will be moving this to
[stackforge](https://github.com/stackforge) sometime soon.

## How to Run:

### Prerequisites:

* Django version must be 1.7 or later.

### Steps:

0. You must have a [devstack setup running on a single VM](http://docs.openstack.org/developer/devstack/guides/single-vm.html).
1. [Download and source the project specific rc file](http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html).
2. Copy the DON source to Horizon directory.(/opt/stack/horizon/)
3. Restart Horizon by executing `sudo service apache2 restart`

## TODO/Known Issues:
Please look at issues in the github repo. If you have questions, bugs, or feature requests, file an issue or send email
to:

* Amit Saha (amisaha+don@cisco.com)
