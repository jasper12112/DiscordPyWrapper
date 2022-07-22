class accessobj():
    def __init__(self, accessobj):
        """
        Variables for user
        """
        
        self.token = accessobj['access_token']
        self.refresh_token = accessobj['refresh_token']
        self.expires = accessobj['expires_in']
        self.token_type = accessobj['token_type']