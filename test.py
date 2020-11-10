import dateutil
from dateutil import parser



def Time(value):
    datetime_obj = dateutil.parser.parse(value)
    time = datetime_obj.strftime('%H:%M:%S')
    t = int(time.split(":")[0])
    m = int(time.split(":")[1])
    if t > 12:
        hm = "{}:{} pm".format(t-12, m)
        return hm
    else:
        hm = "{}:{} am".format(t, m)
        return hm
print(Time("2020-11-09T14:15:00.000+05:30"))