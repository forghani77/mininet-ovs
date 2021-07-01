# implement a flow based L2 switch with vlan support using mininet and OVS

![[topo.png]]

In this senario we want to have two vlans :
* h1 and h3: vlan 100
* h2 and h4: vlan 200

so we should write following flows for s1 and s2 switches :
* Any traffic from h1 to h3 must be tagged with id of 100
* Any traffic from h2 to h4 must be tagged with id of 200

Flows are based upon MAC addresses.
## run: 
```bash
sudo python l2_switch_vlan_support.py
```
## test connections:
```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> X h3 X 
h2 -> X X h4 
h3 -> h1 X X 
h4 -> X h2 X 
*** Results: 66% dropped (4/12 received)
mininet> 
```
