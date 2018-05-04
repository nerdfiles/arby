so the tree might engage with the world rhizopathically or geonominally in such
a way as to produce effects that are reflective of the gravitational signature 
at which there was some recording of photo-aspective imprint. 


★  Answer from https://stackoverflow.com/questions/38130453/difference-between-bare-metal-hypervisor-based-and-host-virtualization-types ★
I've done some documentation. From multiple sources I've managed to gather the following information:
1. Type I Hypervisor: Bare-metal virtualization hypervisors






Is deployed as a bare-metal installation (the first thing to be installed on a server as the operating system will be the hypervisor).


The hypervisor will communicate directly with the underlying physical server hardware, manages all hardware resources and support execution of VMs.


Hardware support is typically more limited, because the hypervisor usually has limited device drivers built into it.


Well suited for enterprise data centers, because it usually comes with advanced features for resource management, high availability and security.


Bare-metal virtualization hypervisors examples: VMware ESX and ESXi, Microsoft Hyper-V, Citrix Systems XenServer.


2. Type II Hypervisor - Hosted virtualization hypervisors






The software is not installed onto the bare-metal, but instead is loaded on top of an already live operating system, so it requires you to first install an OS(Host OS).


The Host OS integrates a hypervisor that is responsible for providing the virtual machines(VMs) with their virtual platform interface and for managing all context switching scheduling, etc.


The hypervisor will invoke drivers or other component of the Host OS as needed.


On the Host OS you may run Guest VMs, but you can also run native applications


This approach provides better hardware compatibility than bare-metal virtualization, because the OS is responsible for the hardware drivers instead of the hypervisor.


A hosted virtualization hypervisor does not have direct access to hardware and must go through the OS, which increases resource overhead and can degrade virtual machine (VM) performance.


The latency is minimal and with today’s modern software enhancements, the hypervisor can still perform optimally.


Common for desktops, because they allow you to run multiple OSes. These virtualization hypervisor types are also popular for developers, to maintain application compatibility on modern OSes.


Because there are typically many services and applications running on the host OS, the hypervisor often steals resources from the VMs running on it


The most popular hosted virtualization hypervisors are: VMware Workstation, Server, Player and Fusion; Oracle VM VirtualBox; Microsoft Virtual PC; Parallels Desktop


