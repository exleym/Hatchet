from datetime import date
from hatchet.db.models import Season

SEASONS = [
    Season(id=2019, start_date=date(2019, 8, 24), end_date=date(2020, 1, 13)),
    Season(id=2018, start_date=date(2018, 8, 25), end_date=date(2019, 1, 7)),
    Season(id=2017, start_date=date(2017, 8, 26), end_date=date(2018, 1, 8)),
    Season(id=2016, start_date=date(2016, 8, 26), end_date=date(2017, 1, 9)),
    Season(id=2015, start_date=date(2015, 9, 3), end_date=date(2016, 1, 11)),
    Season(id=2014, start_date=date(2014, 8, 27), end_date=date(2015, 1, 12)),
    Season(id=2013, start_date=date(2013, 8, 29), end_date=date(2014, 1, 6)),
    Season(id=2012, start_date=date(2012, 8, 30), end_date=date(2013, 1, 7)),
    Season(id=2011, start_date=date(2011, 9, 1), end_date=date(2012, 1, 9)),
    Season(id=2010, start_date=date(2010, 9, 2), end_date=date(2011, 1, 10)),
    Season(id=2009, start_date=date(2009, 9, 3), end_date=date(2010, 1, 7)),
    Season(id=2008, start_date=date(2008, 8, 28), end_date=date(2009, 1, 8)),
    Season(id=2007, start_date=date(2007, 8, 30), end_date=date(2008, 1, 7)),
    Season(id=2006, start_date=date(2006, 8, 31), end_date=date(2007, 1, 8)),
    Season(id=2005, start_date=date(2005, 9, 1), end_date=date(2006, 1, 4)),
    Season(id=2004, start_date=date(2004, 8, 28), end_date=date(2005, 1, 4)),
    Season(id=2003, start_date=date(2003, 8, 23), end_date=date(2004, 1, 4)),
    Season(id=2002, start_date=date(2002, 8, 22), end_date=date(2003, 1, 3)),
    Season(id=2001, start_date=date(2001, 8, 23), end_date=date(2002, 1, 3)),
    Season(id=2000, start_date=date(2000, 8, 26), end_date=date(2001, 1, 3)),
]