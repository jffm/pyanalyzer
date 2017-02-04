# pyanalyzer

The Expandable Python Analyzer

PYANALYZER v0.1
===============

PyAnalyzer is a highly extensible python analyzer written entirely in python.
It relies on the standard python 'compiler' package.
It follows the idea of TheMetrics for Python (http://pythonmetric.sourceforge.net) 
but does not share any line of code. Unlike TheMetrics for Python, it supports
code written in Python > 2.2

The standard 'compiler' package is used to parse the source files and 
return the python ASTs. Metrics and Rules are computed on these ASTs, 
by using the compiler.visitor paradigm.

DOWNLOAD
========

PyAnalyzer can be downloaded here: 
    https://github.com/jffm/pyanalyzer
    
INSTALL
=======

Simply extract the archive.
Soon a python egg will be provided. As well as a publication on PyPI

REQUIREMENTS
------------
Python 2.4

RUN
===

Type the following command at prompt for help

    $ python pyanalyzer.py -h
    
    usage: python pyanalyzer.py [options | --help]
    
            release: v0.1 (10/12/2009)
    
    options:
    --version                     show program's version number and exit
    -h, --help                    show this help message and exit
    -d DIR, --dir=DIR             Directory to analyze
    -s, --recursive               Analyze recursively DIR [False]
    -f FILE, --file=FILE          File containing filenames to analyze
    -n NAME, --name=NAME          Name of the project
    --metrics=METRICS             Comma separated list of metrics, '*' for all
    --rules=RULES                 Comma separated list of rules, '*' for all
    -o OUTPUT, --output=OUTPUT    Output directory for -r and -m [output]
    -M METRICS_FORMAT, --metrics-format=METRICS_FORMAT
                                  Format of metrics ouput (csv|sql) [csv]
    -R RULES_FORMAT, --rules-format=RULES_FORMAT
                                  Format of rules output (txt|csv|sql) [txt]
    -m, --metrics-to-file         Output metrics to 'NAME_metrics.METRICS_FORMAT'
    -r, --rules-to-file           Output rules to 'NAME_rules.RULES_FORMAT'
    --doc=DOC                     Print documentation for the given metric/rule
    --list-metrics=LIST_METRICS   List available metrics for
                                  (Project|Class|Module|Function|*)
    --list-rules=LIST_RULES       List available rules for (compiler.ast.Node|*)
                                  [none]
    --generate-config             Generate a config file based on options provided
                                  at command line
    --config=CONFIG               Get options from .ini configuration file
    --fast                        Speed up execution [False]
    --verbose                     Print execution trace [False]
    --quiet                       Don't print anything [True]
    --debug                       Print debug informations [False]
    --log                         Log execution trace in log directory
    
    
PyAnalyzer is shipped with a default configuration file (config.ini) 
that has been generated with the following command line.

    $ python pyanalyzer.py --generate-config --dir=. --rules=* --metrics=* -m -Mcsv -r -Rcsv > config.ini

You can then analyse all the pyanalyzer itself by issuing

    $ python pyanalyzer.py --config=config.ini

PyAnalyzer has been tested on Windows platform. It should run as is on Linux/Unix platforms.

PROJECT
=======

Information and resources about the project can be found here:
    https://github.com/jffm/pyanalyzer/wiki
    
SUPPORT
-------
Support for PyAnalyzer is provided via the 'Issues' of the project
    https://github.com/jffm/pyanalyzer/issues

CREDITS
-------
PyAnalyzer has been started at CETIC during EU Funded FP6 QualOSS Project.

More Information
----------------
QUALOSS:
    http://www.qualoss.eu
    
CETIC:
    http://www.cetic.be

Main Author:
------------
Junior (Frederic) FLEURIAL MONFILS 
* github: jffm
* twitter: @fredericmonfils