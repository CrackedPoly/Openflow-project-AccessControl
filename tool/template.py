# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     template
   Description :
   Author :       unstoppable
   date：          8/1/2022
-------------------------------------------------
   Change Activity:
                   8/1/2022:
-------------------------------------------------
"""
flow_template = """
                {
                    "flow": {
                        "id": "%s-%s-%s-%s-%s",
                        "priority": 200,
                        "table_id": 0,
                        "match": {
                        },
                        "instructions": {
                            "instruction": [
                                {
                                    "order": 0,
                                    "apply-actions": {
                                        "action": [
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
                """

arp_match_template = """
                    {
                        "arp-source-hardware-address": {
                            "address": "%s"
                        },
                        "arp-target-hardware-address": {
                            "address": "%s"
                        },
                        "arp-op": %d, 
                        "ethernet-match": {
                            "ethernet-type": {
                                "type": 2054
                            }
                        }
                    } 
                    """

arp_request_match_template = """
                    {
                        "arp-target-hardware-address": {
                            "address": "00:00:00:00:00:00"
                        },
                        "arp-op": 1, 
                        "ethernet-match": {
                            "ethernet-type": {
                                "type": 2054
                            }
                        }
                    } 
                    """

icmp_match_template = """{
                             "ip-match": {
                                 "ip-protocol": 1
                             },
                             "ethernet-match": {
                                 "ethernet-type": {
                                     "type": 2048
                                 },
                                 "ethernet-source": {
                                     "address": "%s"
                                 },
                                 "ethernet-destination": {
                                     "address": "%s"
                                 }
                            }
                        }
                        """

ipv4_match_template = """{
                             "ethernet-match": {
                                 "ethernet-type": {
                                     "type": 2048
                                 },
                                 "ethernet-source": {
                                     "address": "%s"
                                 },
                                 "ethernet-destination": {
                                     "address": "%s"
                                 }
                            }
                        }
                        """

all_from_match_template = """{
                             "ethernet-match": {
                                 "ethernet-source": {
                                     "address": "%s"
                                 }
                            }
                        }
                        """

all_to_match_template = """{
                             "ethernet-match": {
                                 "ethernet-destination": {
                                     "address": "%s"
                                 }
                            }
                        }
                        """

action_template = """
                        {
                            "order": 0,
                            "output-action": {
                                "output-node-connector": "%s"
                            }
                        }
                    """