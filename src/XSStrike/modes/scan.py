import copy
import re
from urllib.parse import urlparse, quote, unquote

from core.arjun import arjun
from core.checker import checker
from core.colors import good, bad, end, info, green, red, que
import core.config
from core.config import xsschecker, minEfficiency
from core.dom import dom
from core.filterChecker import filterChecker
from core.generator import generator
from core.htmlParser import htmlParser
from core.requester import requester
from core.utils import getUrl, getParams, getVar
from core.wafDetector import wafDetector
from core.log import setup_logger

import html #Modification 13

logger = setup_logger(__name__)


def scan(target, paramData, encoding, headers, delay, timeout, skipDOM, find, skip):
    GET, POST = (False, True) if paramData else (True, False)
    # If the user hasn't supplied the root url with http(s), we will handle it
    if not target.startswith('http'):
        try:
            response = requester('https://' + target, {},
                                 headers, GET, delay, timeout)
            target = 'https://' + target
        except:
            target = 'http://' + target
    logger.debug('Scan target: {}'.format(target))
    response = requester(target, {}, headers, GET, delay, timeout).text

    if not skipDOM:
        print('<h2>Checking for DOM vulnerabilities<h2>')
        highlighted = dom(response)
        if highlighted:
            print('<h2><span class="GreenDisplay">[+]</span> Potentially vulnerable objects found!!</h2>') # Modification 30
            for line in highlighted:
                print('<h2>[+] Inline:%s</h2>' % line) # Modification 32
    host = urlparse(target).netloc  # Extracts host out of the url
    logger.debug('Host to scan: {}'.format(host))
    url = getUrl(target, GET)
    logger.debug('Url to scan: {}'.format(url))
    params = getParams(target, paramData, GET)
    logger.debug_json('Scan parameters:', params)
    if find:
        params = arjun(url, GET, headers, delay, timeout)
    if not params:
        print('<h2><span class="red">No parameters to test in URL, Use crawl option</span></h2>')
        quit()
    WAF = wafDetector(
        url, {list(params.keys())[0]: xsschecker}, headers, GET, delay, timeout)
    if WAF:
        print('<h2>WAF Detected: <span class="GreenDisplay">%s</span></h2>' % (WAF)) # Modification-4
    else:
        print('<h2> WAF Status: <span class="GreenDisplay">Offline</span></h2>')  # Modification-5

    for paramName in params.keys():
        paramsCopy = copy.deepcopy(params)
        print('<h2><span class="GreenDisplay">+</span> Testing parameter: <span class="RedDisplay">%s</span></h2>' % paramName) # Modification-6
        if encoding:
            paramsCopy[paramName] = encoding(xsschecker)
        else:
            paramsCopy[paramName] = xsschecker
        response = requester(url, paramsCopy, headers, GET, delay, timeout)
        occurences = htmlParser(response, encoding)
        positions = occurences.keys()
        logger.debug('Scan occurences: {}'.format(occurences))
        if not occurences:
            print('<h2><span class="RedDisplay">+</span> No reflection found</h2>') # Modification 8
            continue
        else:
            print('<h2>[<span class="Purple">+</span>] Reflections found: <span class="RedDisplay">%i</span></h2>' % len(occurences)) # Modification 7

        print('<h2>[~] Analysing reflections</h2>') # Modification 9
        efficiencies = filterChecker(
            url, paramsCopy, headers, GET, delay, occurences, timeout, encoding)
        logger.debug('Scan efficiencies: {}'.format(efficiencies))
        print('<h2>[~] Generating payloads</h2>') # Modification 20
        vectors = generator(occurences, response.text)
        total = 0
        for v in vectors.values():
            total += len(v)
        if total == 0:
            print('<h2><span class="RedDisplay">No vectors were crafted</span></h2>') #Modification 10
            continue
        print('<h2>[~] Payloads generated: <span class="RedDisplay">%i</span></h2>' % total) # Modification 11
        progress = 0
        for confidence, vects in vectors.items():
            for vect in vects:
                if core.config.globalVariables['path']:
                    vect = vect.replace('/', '%2F')
                loggerVector = vect
                progress += 1
                print('<h2>[<span class="purple">!</span>] Payload [<span class="Purple">%i</span>/%i]</h2>' % (progress, total), end='\r') # Modification 14
                if not GET:
                    vect = unquote(vect)
                efficiencies = checker(
                    url, paramsCopy, headers, GET, delay, vect, positions, timeout, encoding)
                if not efficiencies:
                    for i in range(len(occurences)):
                        efficiencies.append(0)
                bestEfficiency = max(efficiencies)
                if bestEfficiency == 100 or (vect[0] == '\\' and bestEfficiency >= 95):
                    print('<h2> <span class="red">%s?%s=%s</span></h2>' % (html.escape(url), html.escape(paramName), html.escape(vect))) # Modification 12
                    print('<h2>[<span class="GreenDisplay">+</span>] Payload Efficiency: <span class="red">%i</span></h2>' % bestEfficiency) #Modification 15
                    print('<h2>[<span class="GreenDisplay">+</span>] Confidence Level: <span class="red">%i</span>/10</h2>' % confidence) #Modification 16
                    if not skip:
                        # choice = input('%s Would you like to continue scanning? [y/N] ' % que).lower()
                        quit()			# Modification-2: Stopping after getting payload with 100% efficiency
                        if choice != 'y':
                            quit()
                elif progress == 10:		# Modification-1: Stopping after generating 10 payloads
                    quit()
                elif bestEfficiency > minEfficiency:
                    print('<h2><span class="red">%s?%s=%s</span></h2>' % (html.escape(url), html.escape(paramName), html.escape(loggerVector))) # Modification 17
                    print('<h2>[<span class="GreenDisplay">+</span>] Payload Efficiency: <span class="red">%i</span></h2>' % bestEfficiency) # Modification 18
                    print('<h2>[<span class="GreenDisplay">+</span>] Confidence Level: <span class="red">%i</span>/10</h2>' % confidence) # Modification 19

        logger.no_format('')
