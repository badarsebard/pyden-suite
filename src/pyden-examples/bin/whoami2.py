import activate
import sys
import os
from itertools import chain
import json

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration
from splunklib import six


@Configuration()
class WhoAmI(StreamingCommand):
    def stream(self, records):
        for record in records:
            record['executable'] = sys.executable
            record['version'] = sys.version
            record['cwd'] = os.getcwd()
            try:
                import splunklib
            except ImportError:
                record["foundSDK"] = "false"
            else:
                record["foundSDK"] = "true"
            record['stdin'] = self._metadata
            metadata = chain(six.iteritems(self._configuration), (('inspector', self._record_writer._inspector if self._record_writer._inspector else None),))
            metadata = str(''.join(self._record_writer._iterencode_json(dict([(n, v) for n, v in metadata if v is not None]), 0)))
            record['metadata'] = json.dumps(metadata, indent=2)
            record['file'] = str(__file__)
            record['argv'] = sys.argv
            yield record


if __name__ == "__main__":
    dispatch(WhoAmI, sys.argv, sys.stdin, sys.stdout, __name__)
