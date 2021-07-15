
from ..logic.find_TILTs import *

class Logic(object):

    def getRiskScore(self, domain):
        find = FindTILTs()

        return { "RiskScore": len(find.findTILTs(domain)) }