from typing import *

class OUIVendor(object):

    oui: List[str]
    company_id: str
    organization: str
    address: str
    
    def __init__(self, oui: str, company_id: str, organization: str, address: str):
        super().__init__()

        self.oui = oui
        self.company_id = company_id
        self.organization = organization
        self.address = address

    def __dict__(self) -> dict:
        return vars(self)