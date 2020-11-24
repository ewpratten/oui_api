from typing import *
from .vendor import OUIVendor
import re

def parse_oui_table(data: str) -> Generator[OUIVendor, None, None]:
    """Generates a list of vendors from an IEEE-format OUI database

    Args:
        data (str): OUI database file contents

    Yields:
        Generator[OUIVendor, None, None]: List of vendors
    """

    # Split OUI table up by entry
    raw_entries: List[str] = data.split("\r\n\r\n")

    # Construct each entry into a vendor object
    for entry in raw_entries[1:]:
        entry = re.sub(" +", entry.replace("\t"," ").strip()).split("\r\n")
        
        # Split out first two lines
        line_1 = entry[0].split(" ")
        line_2 = entry[1].split(" ")

        # Get needed data
        oui = line_1[0]
        company_name = line_1[2]
        company_id = line_2[0]
        address = "\n".join(entry[2:])

        # Build vendor obj
        yield OUIVendor(oui, company_id, company_name, address)

