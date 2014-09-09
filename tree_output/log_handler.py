from logging import Handler, NOTSET


class HierarchicalOutputHandler(Handler):

    def __init__(self, level=NOTSET, houtput=None):
        Handler.__init__(self, level)
        self.houtput = houtput

    def emit(self, record):
        try:
            msg = self.format(record)
            add_hlevel = record.__dict__.get('add_hlevel', False)
            remove_hlevel = record.__dict__.get('remove_hlevel', False)
            hclosed = record.__dict__.get('hclosed', False)
            # Do output with thread-safe locking.
            self.acquire()
            try:
                if add_hlevel:
                    self.houtput.add_level()
                self.houtput.emit(msg, closed=hclosed)
                if remove_hlevel:
                    self.houtput.remove_level()
            finally:
                self.release()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
