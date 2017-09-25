class command:

    def __init__(self):
        pass

    virtuals = '/mgmt/tm/ltm/virtual'
    pools = '/mgmt/tm/ltm/pool'
    monitor = '/mgmt/tm/ltm/monitor'

    create_monitor = """ -d '{"name": "", "destination": ""}'"""
    create_pool = """ -d '{"name": "", "members": "", "monitor": ""}'"""
    create_virtual_server = """ -d '{"name": "", "destination": "", "pool": ""}'"""

    change_pool = """ -d '{"pool":""}'"""
    change_members = """ -d '{"members":""}'"""


#    @classmethod
#    def get_virtuals(cls):
#        curl = '/mgmt/tm/ltm/virtual'
#        return curl
#
#    @classmethod
#    def get_pools(cls):
#        curl = '/mgmt/tm/ltm/pool'
#        return curl
