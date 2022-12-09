---
title: "Home Network"
description: "Lorem ipsum dolor sit amet"
date: 2022-05-21
draft: false
type: "project"
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

# Hardware

## Cable Modem

Lorem ipsum dolor sit amet.

## Router

TP-Link Archer C5

### SSH

`ssh root:password@10.0.0.1`

## Switch

Lorem ipsum dolor sit amet.

## Wireless AP

TP-Link EAP610 V2

## NAS

Lorem ipsum dolor sit amet.

# Network

## Static IPs

| IP Address | Hostname          | Description     |
| ---------- | ----------------- | --------------- |
| 10.0.0.1   | openwrt.lan       | Router          |
| 10.0.0.125 | homeassistant.lan | Home automation |
| 10.0.0.102 | nas.lan           | NAS             |

## Trusted VNET

|                        |                                     |
| ---------------------- | ----------------------------------- |
| IP Address             | 10.0.0.1                            |
| Network Address        | 10.0.0.0                            |
| Usable Host IP Range   | 10.0.0.1 - 10.0.255.254             |
| Broadcast Address      | 10.0.255.255                        |
| Total Number of Hosts  | 65,536                              |
| Number of Usable Hosts | 65,534                              |
| Subnet Mask            | 255.255.0.0                         |
| Wildcard Mask          | 0.0.255.255                         |
| Binary Subnet Mask     | 11111111.11111111.00000000.00000000 |
| IP Class               | B                                   |
| CIDR Notation          | /16                                 |
| IP Type                | Private                             |

## Untrusted VNET

|                        |                                     |
| ---------------------- | ----------------------------------- |
| IP Address             | 10.1.0.1                            |
| Network Address        | 10.1.0.0                            |
| Usable Host IP Range   | 10.1.0.1 - 10.1.255.254             |
| Broadcast Address      | 10.1.255.255                        |
| Total Number of Hosts  | 65,536                              |
| Number of Usable Hosts | 65,534                              |
| Subnet Mask            | 255.255.0.0                         |
| Wildcard Mask          | 0.0.255.255                         |
| Binary Subnet Mask     | 11111111.11111111.00000000.00000000 |
| IP Class               | B                                   |
| CIDR Notation          | /16                                 |
| IP Type                | Private                             |

# Configuration

## Router

### `/etc/config/system`

```
config system
	option hostname 'OpenWrt'
	option timezone 'UTC'
	option ttylogin '0'
	option log_size '64'
	option urandom_seed '0'

config timeserver 'ntp'
	option enabled '1'
	option enable_server '0'
	list server '0.openwrt.pool.ntp.org'
	list server '1.openwrt.pool.ntp.org'
	list server '2.openwrt.pool.ntp.org'
	list server '3.openwrt.pool.ntp.org'
```

### `/etc/config/network`

```
config interface 'loopback'
	option device 'lo'
	option proto 'static'
	option ipaddr '127.0.0.1'
	option netmask '255.0.0.0'

config globals 'globals'
	option ula_prefix 'fdbe:7046:3929::/48'

config device
	option name 'br-lan'
	option type 'bridge'
	list ports 'eth1.1'

config interface 'lan'
	option device 'br-lan'
	option proto 'static'
	option ipaddr '10.0.0.1'
	option netmask '255.255.0.0'
	option ip6assign '60'
	list dns '10.0.0.125'

config interface 'wan'
	option device 'eth0.2'
	option proto 'dhcp'

config interface 'wan6'
	option device 'eth0.2'
	option proto 'dhcpv6'

config interface 'iot'
	option device 'br-iot'
	option proto 'static'
	option ipaddr '10.1.0.1'
	option netmask '255.255.0.0'
	option ip6assign '60'

config switch
	option name 'switch0'
	option reset '1'
	option enable_vlan '1'

config switch_vlan
	option device 'switch0'
	option vlan '1'
	option vid '1'
	option ports '0t 2 3 4'
	option description 'LAN'

config switch_vlan
	option device 'switch0'
	option vlan '3'
	option vid '3'
	option ports '0t 5'
	option description 'IoT'

config switch_vlan
	option device 'switch0'
	option vlan '2'
	option ports '6t 1'
	option vid '2'
	option description 'WAN'

config device
	option name 'eth1.3'
	option type '8021q'
	option ifname 'eth1'
	option vid '3'

config device
	option type 'bridge'
	option name 'br-iot'
	list ports 'eth1.3'
```

### `/etc/config/dhcp`

```
config dnsmasq
	option domainneeded '1'
	option localise_queries '1'
	option rebind_protection '1'
	option rebind_localhost '1'
	option local '/lan/'
	option domain 'lan'
	option expandhosts '1'
	option readethers '1'
	option leasefile '/tmp/dhcp.leases'
	option resolvfile '/tmp/resolv.conf.d/resolv.conf.auto'
	option ednspacket_max '1232'
	option sequential_ip '1'
	option authoritative '1'
	option localservice '1'

config dhcp 'lan'
	option interface 'lan'
	option start '100'
	option limit '150'
	option leasetime '12h'
	option dhcpv4 'server'
	option dhcpv6 'server'
	option ra 'server'
	list ra_flags 'managed-config'
	list ra_flags 'other-config'

config dhcp 'wan'
	option interface 'wan'
	option ignore '1'

config odhcpd 'odhcpd'
	option maindhcp '0'
	option leasefile '/tmp/hosts/odhcpd'
	option leasetrigger '/usr/sbin/odhcpd-update'
	option loglevel '4'

config dhcp 'iot'
	option interface 'iot'
	option start '100'
	option limit '150'
	option leasetime '12h'
	option dhcpv4 'server'
	option dhcpv6 'server'
	option ra 'server'
	option ra_slaac '1'
	list ra_flags 'managed-config'
	list ra_flags 'other-config'

config host
	option ip '10.0.0.134'
	option mac '2C:AA:8E:2C:63:9A'

# Wyze Cam 1
config host
	option ip '10.0.0.136'
	option mac '2C:AA:8E:2F:7A:15'

# Wyze Cam 2
config host
	option ip '10.0.0.138'
	option mac '2C:AA:8E:2E:D8:86'

# Wyze Cam 3
config host
	option ip '10.0.0.167'
	option mac '2C:AA:8E:2F:7A:A8'

config host
	option name 'homeassistant'
	option ip '10.0.0.125'
	option mac 'DC:A6:32:D0:7D:0B'
```

### `/etc/config/wireless`

```
config wifi-device 'radio0'
	option type 'mac80211'
	option path 'pci0000:00/0000:00:00.0'
	option channel '36'
	option band '5g'
	option htmode 'VHT80'
	option cell_density '0'
	option disabled '1'

config wifi-device 'radio1'
	option type 'mac80211'
	option path 'platform/ahb/18100000.wmac'
	option channel '1'
	option band '2g'
	option htmode 'HT20'
	option cell_density '0'

config wifi-iface 'wifinet2'
	option device 'radio0'
	option mode 'ap'
	option ssid 'OpenWrt'
	option encryption 'sae-mixed'
	option key '0n0kd1n8'
	option network 'lan'
	option disabled '1'

config wifi-iface 'wifinet1'
	option device 'radio1'
	option mode 'ap'
	option network 'iot'
	option encryption 'psk-mixed'
	option key '0n0kd1n8'
	option ssid 'K IoT'
	option hidden '1'
```

### `/etc/config/firewall`

```
config defaults
	option input 'ACCEPT'
	option output 'ACCEPT'
	option forward 'REJECT'
	option synflood_protect '1'

config zone
	option name 'lan'
	list network 'lan'
	option input 'ACCEPT'
	option output 'ACCEPT'
	option forward 'ACCEPT'

config zone
	option name 'iot'
	option input 'ACCEPT'
	list network 'iot'
	option output 'ACCEPT'
	option forward 'ACCEPT'

config zone
	option name 'wan'
	list network 'wan'
	list network 'wan6'
	option input 'REJECT'
	option output 'ACCEPT'
	option forward 'REJECT'
	option masq '1'
	option mtu_fix '1'

config forwarding
	option src 'lan'
	option dest 'wan'

config rule
	option name 'Block Wyze'
	option dest 'wan'
	option target 'REJECT'
	option src 'lan'
	list src_mac '2C:AA:8E:2C:63:9A'
	list src_mac '2C:AA:8E:2E:D8:86'
	list src_mac '2C:AA:8E:2F:7A:15'
	list src_mac '2C:AA:8E:2F:7A:A8'

config rule
	option name 'Allow-DHCP-Renew'
	option src 'wan'
	option proto 'udp'
	option dest_port '68'
	option target 'ACCEPT'
	option family 'ipv4'

config rule
	option name 'Allow-Ping'
	option src 'wan'
	option proto 'icmp'
	option icmp_type 'echo-request'
	option family 'ipv4'
	option target 'ACCEPT'

config rule
	option name 'Allow-IGMP'
	option src 'wan'
	option proto 'igmp'
	option family 'ipv4'
	option target 'ACCEPT'

config rule
	option name 'Allow-DHCPv6'
	option src 'wan'
	option proto 'udp'
	option src_ip 'fc00::/6'
	option dest_ip 'fc00::/6'
	option dest_port '546'
	option family 'ipv6'
	option target 'ACCEPT'

config rule
	option name 'Allow-MLD'
	option src 'wan'
	option proto 'icmp'
	option src_ip 'fe80::/10'
	list icmp_type '130/0'
	list icmp_type '131/0'
	list icmp_type '132/0'
	list icmp_type '143/0'
	option family 'ipv6'
	option target 'ACCEPT'

config rule
	option name 'Allow-ICMPv6-Input'
	option src 'wan'
	option proto 'icmp'
	list icmp_type 'echo-request'
	list icmp_type 'echo-reply'
	list icmp_type 'destination-unreachable'
	list icmp_type 'packet-too-big'
	list icmp_type 'time-exceeded'
	list icmp_type 'bad-header'
	list icmp_type 'unknown-header-type'
	list icmp_type 'router-solicitation'
	list icmp_type 'neighbour-solicitation'
	list icmp_type 'router-advertisement'
	list icmp_type 'neighbour-advertisement'
	option limit '1000/sec'
	option family 'ipv6'
	option target 'ACCEPT'

config rule
	option name 'Allow-ICMPv6-Forward'
	option src 'wan'
	option dest '*'
	option proto 'icmp'
	list icmp_type 'echo-request'
	list icmp_type 'echo-reply'
	list icmp_type 'destination-unreachable'
	list icmp_type 'packet-too-big'
	list icmp_type 'time-exceeded'
	list icmp_type 'bad-header'
	list icmp_type 'unknown-header-type'
	option limit '1000/sec'
	option family 'ipv6'
	option target 'ACCEPT'

config rule
	option name 'Allow-IPSec-ESP'
	option src 'wan'
	option dest 'lan'
	option proto 'esp'
	option target 'ACCEPT'

config rule
	option name 'Allow-ISAKMP'
	option src 'wan'
	option dest 'lan'
	option dest_port '500'
	option proto 'udp'
	option target 'ACCEPT'

config rule
	option name 'Support-UDP-Traceroute'
	option src 'wan'
	option dest_port '33434:33689'
	option proto 'udp'
	option family 'ipv4'
	option target 'REJECT'
	option enabled '0'

config include
	option path '/etc/firewall.user'

config forwarding
	option src 'lan'
	option dest 'iot'

config rule
	option name 'Allow mDNS'
	list proto 'udp'
	option src '*'
	option src_port '5353'
	list dest_ip '224.0.0.251'
	option dest_port '5353'
	option target 'ACCEPT'

config forwarding
	option src 'iot'
	option dest 'lan'
```

# Misc.

## WiFi QR Codes

Install the `qrencode` package.

```
qrencode "WIFI:T:WPA;S:ssid;P:password;;" -o qr.png
```