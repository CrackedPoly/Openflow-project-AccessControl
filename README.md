# 基于 OpenFlow 的网络服务组策略防护

## 实验环境

虚拟机：Ubuntu 20.04.1 LTS(Focal Fossa)

虚拟机网络：NAT模式

控制器：[OpenDaylight karaf 0.13.1](https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.13.1/)

控制器插件：

- odl-openflowplugin-app-table-miss-enforcer

- odl-openflowplugin-app-forwardingrules-manager

- odl-openflowplugin-app-topology-lldp-discovery

- odl-openflowplugin-app-lldp-speaker

- odl-openflowplugin-app-table-miss-enforcer

- odl-openflowplugin-flow-services-rest

- odl-openflowplugin-app-topology-manager

## 实验命令

`sudo python3 net_start.py`生成实验网络

## 需要修改的地方

`config.py`文件中的ODL_ip和ODL_rest_addr

## 如何使用

见Releases里的幻灯片


