from datetime import datetime as date
from dateutil.relativedelta import relativedelta as before


class Utils:

    @staticmethod
    def calculate_date(period=None) -> list :

        """
        Return
        - [1 year before today , date of today] 
        """
        _today = date.now()
        _from = _today - before(years=1)
        
        return [_from.strftime('%Y%m%d'), _today.strftime('%Y%m%d')]

if __name__ == "__main__":

    print(Utils.calculate_date())
    
