
from codenamize import codenamize as cd 
from uuid import uuid4 as uuid


def codename():
    """Generate random codename"""
    i = str(uuid())
    return {'uuid':i, 'name':cd(i)}

