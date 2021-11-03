import re
import html # Modification Importing HTML module

from core.colors import red, end, yellow


def dom(response):
    highlighted = []
    sources = r'''document\.(URL|documentURI|URLUnencoded|baseURI|cookie|referrer)|location\.(href|search|hash|pathname)|window\.name|history\.(pushState|replaceState)(local|session)Storage'''
    sinks = r'''eval|evaluate|execCommand|assign|navigate|getResponseHeaderopen|showModalDialog|Function|set(Timeout|Interval|Immediate)|execScript|crypto.generateCRMFRequest|ScriptElement\.(src|text|textContent|innerText)|.*?\.onEventName|document\.(write|writeln)|.*?\.innerHTML|Range\.createContextualFragment|(document|window)\.location'''
    scripts = re.findall(r'(?i)(?s)<script[^>]*>(.*?)</script>', response)
    sinkFound, sourceFound = False, False
    for script in scripts:
        script = script.split('\n')
        num = 1
        try:
            for newLine in script:
                line = newLine  # HTML escaping lines
                parts = line.split('var ')
                controlledVariables = set()
                allControlledVariables = set()
                if len(parts) > 1:
                    for part in parts:
                        for controlledVariable in allControlledVariables:
                            if controlledVariable in part:
                                controlledVariables.add(re.search(r'[a-zA-Z$_][a-zA-Z0-9$_]+', part).group().replace('$', '\$'))
                pattern = re.finditer(sources, newLine)
                for grp in pattern:
                    if grp:
                        source = newLine[grp.start():grp.end()].replace(' ', '')
                        if source:
                            if len(parts) > 1:
                               for part in parts:
                                    if source in part:
                                        controlledVariables.add(re.search(r'[a-zA-Z$_][a-zA-Z0-9$_]+', part).group().replace('$', '\$'))
                                        sourceFound = True
                            line = line.replace(source, '<span class="Purple">'+ html.escape(source) +'</span>') # Purple Modification 
                for controlledVariable in controlledVariables:
                    allControlledVariables.add(controlledVariable)
                for controlledVariable in allControlledVariables:
                    matches = list(filter(None, re.findall(r'\b%s\b' % controlledVariable, line))) #Modification
                    if matches:
                        line = re.sub(r'\b%s\b' % controlledVariable, '<span class="GreenDisplay">' + controlledVariable + '</span>' , line) # Green Modification 
                pattern = re.finditer(sinks, newLine)
                for grp in pattern:
                    if grp:
                        sink = newLine[grp.start():grp.end()].replace(' ', '')
#                        line = html.escape(line)
                        if sink:
                            line = line.replace(sink, '<span class="red">' + html.escape(sink) + '</span>')
                            sinkFound = True
                if line != newLine:
                    highlighted.append('%-3s %s' % (str(num), line.lstrip(' ')))
                num += 1
        except MemoryError:
            pass
    if sinkFound and sourceFound:
        return highlighted
    else:
        return []

