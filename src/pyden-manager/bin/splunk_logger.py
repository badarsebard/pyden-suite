import os
import logging
import logging.handlers


loggers = {}


# The following two functions are taken from the `splunk` module written into Splunk Enterprise
# These are necessary to set up logging in accordance with Splunk defined best practice but the module is
# lost when the process is re-executed under a different Python interpreter.
def getSplunkLoggingConfig(baseLogger, defaultConfigFile, localConfigFile, loggingStanzaName, verbose):
    loggingLevels = []

    # read in config file and set logging levels
    if os.access(localConfigFile, os.R_OK):
        if verbose:
            baseLogger.info('Using local logging config file: %s' % localConfigFile)
        logConfig = open(localConfigFile, 'r')
    else:
        if verbose:
            baseLogger.info('Using default logging config file: %s' % defaultConfigFile)
        logConfig = open(defaultConfigFile, 'r')

    try:
        inStanza = False
        for line in logConfig:

            # strip comments
            line = line.strip()
            if '#' in line:
                line = line[:(line.index('#'))]

            # skip blank lines
            line = line.strip()
            if not line:
                continue

            # # # skip malformatted lines: stanza, key=value, or WTF?
            if line.startswith('['):
                if not line.endswith(']') or line.index(']') != (len(line) - 1):
                    continue
            elif '=' in line:
                key_test, value_test = line.split('=')
                if not key_test or not value_test:
                    continue
            else:
                continue

            # # # validation done, now we finally have parsing logic proper
            if not inStanza and line.startswith('[%s]' % loggingStanzaName):
                inStanza = True
                continue
            elif inStanza:
                if line.startswith('['):
                    break
                else:
                    name, level = line.split('=', 1)
                    if verbose:
                        baseLogger.info('Setting logger=%s level=%s' % (name.strip(), level.strip()))
                    loggingLevels.append((name.strip(), level.strip().upper()))
    except Exception as e:
        baseLogger.exception(e)
    finally:
        if logConfig: logConfig.close()

    return loggingLevels


def setupSplunkLogger(baseLogger, defaultConfigFile, localConfigFile, loggingStanzaName, verbose=True):
    '''
    Takes the base logging.logger instance, and scaffolds the splunk logging namespace
    and sets up the logging levels as defined in the config files
    '''

    levels = getSplunkLoggingConfig(baseLogger, defaultConfigFile, localConfigFile, loggingStanzaName, verbose)

    for item in levels:
        loggerName = item[0]
        level = item[1]
        if hasattr(logging, level):
            logging.getLogger(loggerName).setLevel(getattr(logging, level))
        if verbose and (loggerName == "appender.python.maxFileSize" or loggerName == "appender.python.maxBackupIndex"):
            baseLogger.info('Python log rotation is not supported. Ignoring %s' % loggerName)


def setup_logging():
    global loggers

    if loggers.get('splunk.pyden'):
        return loggers.get('splunk.pyden')
    else:
        logger = logging.getLogger('splunk.pyden')
        splunk_home = os.environ['SPLUNK_HOME']
        logging_default_config_file = os.path.join(splunk_home, 'etc', 'log.cfg')
        logging_local_config_file = os.path.join(splunk_home, 'etc', 'log-local.cfg')
        logging_stanza_name = 'python'
        logging_file_name = "pyden.log"
        base_log_path = os.path.join('var', 'log', 'splunk')
        logging_format = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
        splunk_log_handler = logging.handlers.RotatingFileHandler(
            os.path.join(splunk_home, base_log_path, logging_file_name), mode='a')
        splunk_log_handler.setFormatter(logging.Formatter(logging_format))
        logger.addHandler(splunk_log_handler)
        setupSplunkLogger(logger, logging_default_config_file, logging_local_config_file, logging_stanza_name)
        loggers['splunk.pyden'] = logger
        return logger
