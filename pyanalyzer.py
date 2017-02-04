# Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS
#
# This file is part of PyAnalyzer.
#
# PyAnalyzer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, see <http://www.gnu.org/licenses/>.
# or see <http://www.opensource.org/licenses/gpl-3.0.html>
#
# Contact:
#         Junior FLEURIAL MONFILS <frederic dot fleurialmonfils at cetic dot be>

"""PyAnalyzer is an extensible analyzer for Python source files.
It can computes metrics or check rules written as extension classes.
It relies entirely on the 'compiler' package.
This means that it only analyzes python projects of
the same language version as the actual 'python' interpreter.

Please use the following command for help
$ python pyanalyzer.py -h
"""

__author__ = "Frederic F. MONFILS"
__version__ = "$Revision: $".split()[1]
__revision__ = __version__
# $Source: $
__date__ = "$Date: 10/12/2009 $".split()[1]
__copyright__ = "Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS"
__license__ = "GPLv3"
__contact__ = "ffm at cetic.be"
__release__ = "0.1"

import os
import sys
import compiler
import logging
import time
import optparse

from inspect import getmembers, isclass
from ConfigParser import ConfigParser

from core.assigner.endlineassigner import EndlineAssigner
from core.assigner.linesofcommentsassigner import LinesOfCommentsAssigner
from core.assigner.intervalassigner import IntervalAssigner
from core.ast.project import Project
from core.visitor import Visitor
from core.ast.nameresolver import NameResolver
from core.computer.metricscomputer import MetricsComputer
from core.reporter.metricsreporter import MetricsReporter
from core.reporter.rulesreporter import RulesReporter


def get_options(args):
    """Get the options from the arguments
    """
    parser = optparse.OptionParser(
            formatter=optparse.IndentedHelpFormatter(
                    indent_increment=0,
                    max_help_position=30,
                    width=None,
                    short_first=1),
            version="%%prog %s (%s)" % (__release__, __date__),
            usage="""python %%prog [options | --help]

            release: v%s (%s)""" % (__release__, __date__)
    )
    parser.set_defaults(
            fast=False,
            verbose=False,
            debug=False,
            recursive=False,
            resolve=False,
            metrics_format="csv",
            rules_format="txt",
            metrics_to_file=False,
            rules_to_file=False,
            output="output",
            name="project",
            log="log",
            profile=False,
            python_version="%s%s" % sys.version_info[:2]
    )
    parser.add_option("-d", "--dir",
        help="Directory to analyze")
    parser.add_option("-s", "--recursive",
        help="Analyze recursively DIR [%default]",
        action="store_true")
    parser.add_option("-f", "--file",
        help="File containing filenames to analyze")
    parser.add_option("-n", "--name",
        help="Name of the project")
    parser.add_option("-p", "--python-version",
        help="Python version [%default]")
    parser.add_option("--resolve",
        help="BETA, Best effort name resolving [%default]",
        action="store_true")
    parser.add_option("--metrics",
        help="Comma separated list of metrics, '*' for all")
    parser.add_option("--rules",
        help="Comma separated list of rules, '*' for all")
    parser.add_option("-o", "--output",
        help="Output directory for -r and -m [%default]")
    parser.add_option("-M", "--metrics-format",
        help="Format of metrics ouput (csv|sql) [%default]",
        choices=("csv", "sql"))
    parser.add_option("-R", "--rules-format",
        help="Format of rules output (txt|csv|sql) [%default]",
        choices=("txt", "csv", "sql"))
    parser.add_option("-m", "--metrics-to-file",
        help="Output metrics to 'NAME_metrics.METRICS_FORMAT'",
        action="store_true")
    parser.add_option("-r", "--rules-to-file",
        help="Output rules to 'NAME_rules.RULES_FORMAT'",
        action="store_true")
    parser.add_option("--doc",
        help="Print documentation for the given metric/rule")
    parser.add_option("--list-metrics",
        help="List available metrics for (Project|Class|Module|Function|*)")
    parser.add_option("--list-rules",
        help="List available rules for (compiler.ast.Node|*) [%default]")
    parser.add_option("--generate-config",
        help="Generate a config file based on options provided at command line",
        action="store_true")
    parser.add_option("--config",
        help="Get options from .ini configuration file")
    parser.add_option("--fast",
        help="Speed up execution [%default]",
        action="store_true")
    parser.add_option("--verbose",
        help="Print execution trace [%default]",
        action="store_true")
    parser.add_option("--quiet",
        help="Don't print anything [True]",
        action="store_false",
        dest="verbose")
    parser.add_option("--debug",
        help="Print debug informations [%default]",
        action="store_true")
    parser.add_option("--profile",
        help="Perform profiling of the run [%default]",
        action="store_true")
    parser.add_option("--log",
        help="Log execution trace in directory [%default]")
    options, args = parser.parse_args(args)
    return parser, options, args


def set_trace_options(options):
    """Set tracing options
    """
    if options.log:  # record logging of the execution
        if not os.path.isdir(options.log):
            os.makedirs(options.log)
        logging.basicConfig(
            level=options.debug and logging.DEBUG or logging.INFO,
            format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=os.path.join(
                options.log,
                "%s_log.txt" % time.strftime("%Y%m%d")
            ),
            filemod="w"
        )
    else:  # do not trace anything
        # report only critical errors
        logging.getLogger('').setLevel(logging.CRITICAL)
    if options.verbose:  # show trace of execution
        if options.log:  # trace logging to stdout and file
            console = logging.StreamHandler()
            console.setLevel(options.debug and logging.DEBUG or logging.INFO)
            console.setFormatter(
                    logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
            )
            logging.getLogger('').addHandler(console)
        else:  # trace logging to stdout
            logging.basicConfig(
                    level=options.debug and logging.DEBUG or logging.INFO,
                    format='%(name)-8s: %(levelname)-8s %(message)s',
            )
    options.log = logging
    if options.fast:  # speed up execution
        try:
            import psyco
            psyco.full()
        except ImportError:
            logging.warning("psyco not installed")


def set_options(parser, options, args=None):
    """Perform immediate actions from @options,
    Check basic options and set trace options
    """
    if options.generate_config:
        sys.exit(generate_config(parser, options))
    if options.list_metrics:
        sys.exit(list_metrics(options))
    if options.list_rules:
        sys.exit(list_rules(options))
    if options.doc:
        sys.exit(doc(options.doc))
    if options.config:
        cfg = ConfigParser()
        cfg.optionxform = lambda name: name.replace("-", "_")
        cfg.read(options.config)
        boolean = dict(
            true=True,
            false=False,
            yes=True,
            no=False,
            y=True,
            n=False
        )
        for section in cfg.sections():
            for (key, value) in cfg.items(section):
                if value:
                    setattr(options, key, boolean.get(value.lower(), value))
    if not (options.file or options.dir or options.metrics or options.rules):
        parser.print_help()
        sys.exit("\nMissing input and action "
                 "please specify --file/--dir and --metrics/--rules)")
    if not (options.file or options.dir):
        parser.print_help()
        sys.exit("\nMissing input (please specify --file/--dir)")
    if not (options.metrics or options.rules):
        parser.print_help()
        sys.exit("\nMissing action (please specify --rules/--metrics)")                        
    set_trace_options(options)
    
    return options


def get_source_files(options):
    """Return the list of python filenames (.py) to analyze
    """
    if options.file:
        # the file contains one filename per line
        return [
            filename
            for filename in (line.split() for line in open(options.file))
                if os.path.splitext(filename)[1] == ".py"  # only python files
        ]
    elif options.dir:
        # the directory contains the filenames
        if options.recursive:
            # if recursive, traverse the path
            return [
                os.path.join(path, filename)
                for (path, _, filenames) in os.walk(options.dir)
                    for filename in filenames 
                        # only python files
                        if os.path.splitext(filename)[1] == ".py"
            ]
        else:
            # if not recursive, get the list from the directory
            return [
                os.path.join(options.dir, filename)
                for filename in os.listdir(options.dir)
                    # only python files
                    if os.path.splitext(filename)[1] == ".py"
            ]


def get_basenames_from(directory):
    """Get a comma separated list of the python filenames from @directory
    """
    return ",".join([
        os.path.splitext(filename)[0]
        for filename in os.listdir(directory)
            if os.path.splitext(filename)[1] == ".py" 
                and not filename.startswith("__init__")
    ])


def show_progress(progress, prompt=""):
    stars   = '*' * int(progress*50)
    percent = int(progress*100)
    show = (percent >= 100) and 'done.' or '%d%%' % percent
    sys.stdout.write("\r%s[%-50s] %s" % (prompt, stars, show))
    sys.stdout.flush()


def run(options):
    """Run the analyzer with the provided @options
    
    0. Create metrics computer, and metrics/rules reporters
    1. Parse files
    2. Create project
    3. Compute the metrics (if necessary)
    4. Check the rules (if necessary)
    """
    # 0. Create metrics computer, and metrics/rules reporters
    if options.metrics:
        if options.metrics == "*":
            options.metrics = get_basenames_from("metrics")
        metrics_computer = MetricsComputer(options)
        metrics_reporter = MetricsReporter(options)
    if options.rules:
        if options.rules == "*":
            options.rules = get_basenames_from("rules")
        rules_reporter = RulesReporter(options)
    Visitor.log = options.log
    # 1. Parse files
    modules = []
    filenames = get_source_files(options)
    if options.resolve:
        # builtin_path = os.path.join("core", "builtins", options.python_version)
        # filenames.extend([
            # os.path.join(builtin_path, "__functions__.py"),
            # os.path.join(builtin_path, "__types__.py"),
            # os.path.join(builtin_path, "__variables__.py")
        # ])
        pass
    numfiles = len(filenames)
    common_path = os.path.commonprefix(filenames)
    common_path_length = len(common_path)
    for (i, filename) in enumerate(filenames):
        options.log.info("Parsing %s..." % filename)
        if not options.verbose: show_progress(float(i)/numfiles, "Parsing... ")
        # 1.1 parse source file
        module = compiler.parseFile(filename)
        module.name = os.path.splitext(os.path.basename(filename))[0]
        module.filename = filename
        # module.relname = filename[common_path_length:]
        # 1.2 apply basic helpers
        options.log.debug("    Assigning endline to classes, functions and modules")
        compiler.walk(module, EndlineAssigner(filename, common_path_length))
        options.log.debug("    Assigning lines of comments to classes, functions and modules")
        compiler.walk(module, LinesOfCommentsAssigner(filename))
        # 1.3 record parsed file
        modules.append(module)
    if not options.verbose: show_progress(1, "Parsing... ")
    # 2. Create project
    options.log.info("Creating the project %s" % options.name)
    project = Project(common_path, options.name, modules)
    project.endline = sum(module.endline for module in modules)
    options.log.debug("    Assigning id and bounds to classes, functions and modules")
    compiler.walk(project, IntervalAssigner())
    
    # 2.1 Resolve the names
    if options.resolve:
        options.log.info("Resolving names...")
        compiler.walk(project, NameResolver(options))
        options.log.info("Name resolving done.")
    
    # 3. Compute the metrics
    if options.metrics:
        options.log.info("Computing metrics...")
        compiler.walk(project, metrics_computer)
        # 3.1 Report the metrics
        compiler.walk(project, metrics_reporter)
        options.log.info("Metrics computing done.")
    # 4. Check the rules
    if options.rules:
        options.log.info("Checking rules...")
        # 4.1 Report the rules
        rules_reporter.report(project)
        options.log.info("Rules checking done.")
    options.log.info("Done.")


def doc(metric_or_rule):
    """Print the documentation for the given @metric_or_rule
    """
    found = showall = False        
    if metric_or_rule == "*":
        showall = True
    for directory in ("metrics", "rules"):
        for filename in os.listdir(directory):
            basename, ext = os.path.splitext(os.path.basename(filename))
            if ((ext == ".py")
                    and (not basename.startswith("__"))
                    and (showall or (basename == metric_or_rule))):
                module = __import__(
                    '%s.%s' % (directory, basename),
                    globals(),
                    locals(),
                    [basename]
                )
                title = "%s: %s" % (directory.title()[:-1], basename)
                print
                print title
                print "-"*len(title)
                found = True
                instance = getattr(module, basename)
                if directory == "metrics":
                    print instance.__doc__
                else:
                    print instance.__doc__ % instance.info.message
                if not showall:
                    break
    if (not found) and (not showall) :
        print "Metric/Rule '%s' does not exist" % metric_or_rule


def generate_config(parser, options):
    """Generate the configuration file based on the provided @options
    """
    trace = ("fast", "log", "debug", "verbose", "quiet")
    exclude = ("generate_config", "doc", "list_metrics", "list_rules", "config")
    
    class ConfigHelpParser(ConfigParser):
        """Modified ConfigParser that creates a .ini-format config file with
        the options from an OptionParser and with the help messages enabled
        """
        __option_parser = parser
        __help_section = dict(
                main="Main configuration of the analysis",
                trace="Trace the execution"
        )
        def write(self, fileobject):
            """Write an .ini-format representation of the configuration state.
            """
            for section in self._sections:
                fileobject.write(
                    "\n[%s]\n#\n# %s\n#\n\n"
                    % (section, self.__help_section[section]))
                for (key, value) in sorted(self._sections[section].items()):
                    if key != "__name__":
                        key = key.replace("_", "-")
                        text = self.__option_parser.get_option(
                                                (len(key)>1)
                                                and ("--%s"%key)
                                                or ("-%s"%key)
                                        ).help
                        text = (
                                ("%default" in text)
                                and (text.replace("%default", "%s") % value)
                                or text
                        )
                        fileobject.write("# %s\n" % text)
                        fileobject.write(
                            "%s = %s\n\n" % 
                            (key, str(value or "").replace('\n', '\n\t'))
                        )
                fileobject.write("\n")
    
    config = ConfigHelpParser()
    config.add_section("trace")
    config.add_section("main")
    for option in parser.option_list:
        if (not option.dest) or (option.dest in exclude):
            continue
        elif option.dest in trace:
            section = "trace"
        else:
            section = "main"
        config.set(section, option.dest, getattr(options, option.dest))
    config.write(sys.stdout)


def list_metrics_or_rules(options, kind):
    """List all available metrics or rules for the given @options
    """
    count = 0
    listall = (getattr(options, "list_%s" % kind) == "*")
    print kind.title()
    print ("-" * len(kind))
    directory = kind
    for filename in os.listdir(directory):
        basename, ext = os.path.splitext(os.path.basename(filename))
        provides_metric = False
        if ext == ".py" and basename != "__init__":                        
            module = __import__(
                '%s.%s' % (directory, basename),
                globals(),
                locals(),
                [basename]
            )
            classes = [
                member
                for (name, member) in getmembers(module)
                    if isclass(member) and name.endswith(basename)
            ]
            if not classes:
                print "Warning: File %s should contain a class named %s" % (
                        filename,
                        basename
                )
            if not listall:
                provides_metric = sum(
                    1 
                        for (name, member) in getmembers(classes[0])
                            if name.endswith(getattr(options, "list_%s" % kind))
                )
            if listall or provides_metric:
                print "\t%s" % basename
                count += 1
    print
    print "\t%d %s found" % (count, kind)


def list_metrics(options):
    """List all metrics for the given options"""
    return list_metrics_or_rules(options, "metrics")


def list_rules(options):
    """List all rules for the given options"""
    return list_metrics_or_rules(options, "rules")

if __name__ == "__main__":
    PARSER, OPTIONS, ARGS = get_options(sys.argv)
    OPTIONS = set_options(PARSER, OPTIONS, ARGS)

    def main():
        run(OPTIONS)

    if OPTIONS.profile:
        # This is the main function for profiling
        import profile
        import pstats
        import StringIO
        profile.Profile.dispatch['c_exception'] = profile.Profile.trace_dispatch_return
        # profile.runctx("run(OPTIONS)", globals(), locals(), "profiling.prof")
        profile.run("main()", "profiling.prof")
        # stream = StringIO.StringIO()
        stats = pstats.Stats("profiling.prof")
        stats.sort_stats("time")  # Or cumulative
        stats.print_stats(80)  # 80 = how many to print
        # The rest is optional.
        # stats.print_callees()
        # stats.print_callers()
        # logging.info("Profile data:\n%s", stream.getvalue())
        stats.dump_stats("profiling.stats")
    else:
        run(OPTIONS)
