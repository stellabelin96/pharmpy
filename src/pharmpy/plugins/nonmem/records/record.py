class Record:
    """
    Top level class for records.

    Create objects only by using the factory function create_record.
    """

    name = None

    def __init__(self, content, parser_class):
        self._content = content
        self._parser_class = parser_class
        self._root = None

    @property
    def root(self):
        """Root of the parse tree
           only parse on demand
        """
        if self._root is None:
            parser = self._parser_class(self._content)
            self._root = parser.root
            del self._parser_class
            del self._content
        return self._root

    def __str__(self):
        return self.raw_name + str(self.root)
