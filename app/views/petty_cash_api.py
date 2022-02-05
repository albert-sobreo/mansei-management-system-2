from ..models import *
import datetime
from decimal import Decimal
from .notificationCreate import *

def pCashChecker(request, amount):
    pCashRemaining = request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.amount
    return True if (pCashRemaining - Decimal(amount)) >= 0 else False