import config, random
from outline_vpn.outline_vpn import OutlineVPN


class Outline:
    def __init__(self) -> None:
        self.api_url = config.OUTLINE_SERVER.get("apiUrl")
        self.cert_sha256 = config.OUTLINE_SERVER.get("certSha256")
        self.client = OutlineVPN(self.api_url, self.cert_sha256)

    def create_key(self, data_limit=None):
        name = f"{config.CONFIG_START_NAME}-{random.randint(10000, 99999)}"
        key = self.client.create_key(name=name, data_limit=data_limit)
        return key
    
    def get_keys(self):
        keys = self.client.get_keys()
        return keys
    
    def edit_key(self, key_id):
        self.client
    
    def limit_key(self, key_id, limit_bytes):
        status = self.client.add_data_limit(key_id, limit_bytes)
        return status

    def get_key(self, key_id):
        key = self.client.get_key(key_id)
        return key
    
    def delete_key(self, key_id):
        status = self.client.delete_key(key_id)
        return status
    #def
