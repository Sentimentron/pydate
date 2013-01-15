#!/usr/bin/env python

from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime
import requests 
from pytz import timezone
import pytz
from timezones import is_timezone

def convert_time_dotsep(time_fragment):
    hour, sep, minute = time_fragment.partition('.')
    try:
        hour = int(hour)
        minute = int(minute)
    except ValueError:
        return time_fragment
    if hour >= 0 and hour <= 24:
        if minute >= 0 and minute <= 60:
            return ':'.join([str(x) for x in [hour, minute]])
    return time_fragment

def is_slashed_date(time_fragment):
    frags = time_fragment.split("/")
    if len(frags) != 3:
        return False
        
    for frag in frags:
        try:
            frag = int(frag)
        except ValueError:
            return False
    return True

def preprocess(text):
    ret = []
    add_counter = 0
    for frag in text.split(' '):
        
        frag = frag.strip()
        
        if len(frag) == 0:
            continue
        
        if is_slashed_date(frag):
            return frag, 3
        
        add = False
        if add_counter > 2:
            add_counter = 0
        
        frag = convert_time_dotsep(frag)
        
        for month_frag in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
            add = add or (month_frag in frag)
            add = add or (month_frag.lower() in frag)
            add = add or (month_frag.upper() in frag)
                
        add = add or "AM" in frag or "am" in frag
        add = add or "PM" in frag or "pm" in frag
        
        add = add or is_timezone(frag)
        
        for char in '0123456789':
            add = add or (char in frag)
        if is_slashed_date(frag):
            print add, frag
        if add:
            ret.append(frag)
            add_counter = 0
        else:
            add_counter += 1
    return ' '.join(ret), len(ret)
        

def get_dates(html):
    
    # Parse the HTML
    soup = BeautifulSoup(html, "lxml")
    
    # Set up a date dictionary
    dates = {}
    
    # Get standard timezone stuff
    utc = pytz.utc
    
    today_utc = datetime.now(utc)
    today_nom = datetime.now()
    
    # Search through all the text in the document body
    for position, text in enumerate(soup.body.findAll(text=True)):
        text = text.strip()
        if len(text) == 0:
            continue
        prep, prep_len = preprocess(text)
        if len(prep) == 0 or prep_len < 3:
            continue
        possibilities = set([])
        exceptions = set([])
        for day_first in [False, True]:
            # Try various fuzzy parameters
            for year_first in [False, True]:
                parsed = None
                # Parse the string
                try:
                    parsed = parse(prep, fuzzy = False, dayfirst = day_first, yearfirst = year_first)
                except Exception as ex:
                    exceptions.add((ex, text.encode('ascii', 'ignore')))
                sub_date = None
                if parsed is None:
                    continue
                if parsed.tzinfo is not None:
                    sub_date = today_utc 
                else:
                    sub_date = today_nom
                if (parsed - sub_date).seconds > 60:
                    possibilities.add((parsed, day_first, year_first))
        #raw_input()
        if len(possibilities) == 0:
            continue
        
        dates[position] = {'dates': possibilities, 'text': text, 'exceptions': exceptions, 'prep': prep}
    
    return dates

def get_page():
    
    url = raw_input("Enter a URL:")
    r = requests.get(url)
    return r.text 

if __name__ == "__main__":
    
    import pprint
    text = get_page()
    
    dates = get_dates(text)
    for item in dates:
        print item, dates[item]