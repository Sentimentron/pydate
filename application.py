from flask import Flask, request, Response
import requests
import logging
from datetime import datetime
from parsing import get_dates

from lxml import etree


application = Flask(__name__)
debug = True
app = application

@app.route("/")
def hello():
    return r"""<html>
    
    <body>
        <form method="POST" action="/url">
            <p>Type a URL: <input type="text" name="url" /></p>
            <input type="submit" />
        </form>
    </body>
    
    
    </html>"""

@app.route("/url", methods=['POST'])
def from_url():
    
    # Validation
    if "url" not in request.form:
        return "Need a URL"
    
    # Get the page
    url = request.form['url']
    req = requests.get(url)
    
    # Extract dates
    par = get_dates(req.text)
    
    # Build XML response
    root = etree.Element('AutoDateResponse')
    info = etree.Element('BasicInfo')
    vers = etree.Element('Version')
    nowt = etree.Element('DateHandled')
    info.append(vers)
    info.append(nowt)
    root.append(info)
    vers.text = '1.0.0'
    nowt.text = str(datetime.now())
    
    resp = etree.Element('Response')
    
    for item in par:
        cur = par[item]
        date_set = set([date for date, dayfirst, yearfirst in cur['dates']])
        if len(date_set) > 1:
            date_set = set([])
            elem = etree.Element('AmbiguousDateCollection')
            for date, dayfirst, yearfirst in cur['dates']:
                if date in date_set:
                    continue
                node = etree.Element('AmbiguousDate')
                node.attrib["Date"] = str(date)
                node.attrib["DayFirst"] = str(dayfirst)
                node.attrib["YearFirst"] = str(yearfirst)
                node.text = str(date)
                elem.append(node)
                date_set.add(date)
        else:
            elem = etree.Element('Date')
            for date, dayfirst, yearfirst in cur['dates']:
                elem.attrib["Date"] = str(date)
        elem.attrib['Position'] = str(item)
        elem.attrib['OriginalText'] = cur['text']
        elem.attrib['ExceptionsDuringParsing'] = str(len(cur['exceptions']) > 0)
        elem.attrib['ParsedText'] = cur['prep']
        resp.append(elem)
        
    root.append(resp)
        
    
    re = Response(etree.tostring(root, pretty_print=True), status=200, mimetype='application/xml')
    return re
    

if __name__ == "__main__":
    app.debug = True
    app.run(use_debugger = True)