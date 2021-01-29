import datetime
from catalog.models import TemporalLink

def removeLinks():
    datetime_object = datetime.datetime.now()
    ten_minute = datetime.timedelta(minutes=10)
    time_filter = datetime_object - ten_minute
    queryItems = TemporalLink.objects.filter(created_at__lte = time_filter)
    numItems = queryItems.count()
    print( 'Removed : ' + str(numItems))
    queryItems.delete()
    print('--------')