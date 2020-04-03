from csv_handler import CSVFileHandler

class StorageHandler(object):
    """Factory class for storage handlers.
    It reads `storage_type` from args and then create its own storage handler.
    It exposes the method `store()` and every storage handlers created
    must implement a `store()` method tooself.

    Attributes:
    -----------
    - `storage_wrapper`: a storage object which implements the `store()` method
    """

    def __init__(self, args, tweets):
        """Initializes StorageHandler

        Parameters
        ----------
        - `args`: argparse data structure; it must contains:
            - `storage_type`: string, specifies the type of storge handler
                              (CSV, Elasticsearch, ...)
            - `tweets`: list of `Status` object from `python-twitter` module
        """
        if args.storage_type == "CSV":
            self.storage_wrapper = CSVFileHandler(args, tweets)
        elif args.storage_type == "ES":
            self.storage_wrapper = ElasticsearchHandler(args, tweets)
        else:
            raise ValueError(args.storage_type)

    def store(self):
        """Wrapper method to the `store()` method of the concrete storage handler"""
        self.storage_wrapper.store()
