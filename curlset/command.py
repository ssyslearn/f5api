class command:

    def __init__(self):
        pass

    virtuals = '/mgmt/tm/ltm/virtual'
    pools = '/mgmt/tm/ltm/pool'
    create_virtual_server = """ -d '{"name": "", "destination": ""}'"""
    enable_virtual_server = """ -d '{"enabled":""}'"""


#    @classmethod
#    def get_virtuals(cls):
#        curl = '/mgmt/tm/ltm/virtual'
#        return curl
#
#    @classmethod
#    def get_pools(cls):
#        curl = '/mgmt/tm/ltm/pool'
#        return curl
