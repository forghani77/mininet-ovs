# implement a flow based L3 switch using mininet and OVS
![[topo 2.png]]
This senario has the same concept for L2 switch but instead of MAC addresses flows are based upon IP addresses.
We want to have a biodirectional flow between h1 and h2.
Any trafic from/to h3 will be ignored.
## run: 
```bash
sudo python l3_switch.py
```
## test connections:
```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 X 
h2 -> h1 X 
h3 -> X X 
*** Results: 66% dropped (2/6 received)
mininet> 
```