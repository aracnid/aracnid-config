"""Class module to interface with MongoDB.
"""
from dateutil import tz
import logging
import os

from bson.codec_options import CodecOptions
import pymongo

# initialize logging
logger = logging.getLogger(__name__)


class MongoDBInterface:
    """MongoDB interface class.

    Attributes:
        db: MongoDB database
        db_name: Name of the interfacing database.
        mongo_client: MongoDB client.
    """

    def __init__(self, db_name=None):
        """Initializes the interface with the database name.

        If no database name is supplied, the name is read from environment.

        Args:
            db_name: The name of the interfacing database.
        """
        # read environment variables
        mdb_user_token = os.environ.get('MONGODB_USER_TOKEN')
        mdb_hostname = os.environ.get('MONGODB_HOSTNAME')
        self.db_name = os.environ.get('MONGODB_DBNAME')

        # override database name, if provided
        if db_name:
            self.db_name = db_name

        # initialize mongodb client
        connection_string = (
            f'mongodb+srv://{mdb_user_token}@{mdb_hostname}'
            '/?retryWrites=true')
        self.mongo_client = pymongo.MongoClient(host=connection_string)

        # initialize mongodb database
        codec_options = CodecOptions(tz_aware=True, tzinfo=tz.tzlocal())
        self.db = pymongo.database.Database(
            client=self.mongo_client, 
            name=self.db_name, 
            codec_options=codec_options)

    def create_collection(self, name):
        """Creates and returns the specified collection.

        Args:
            name: The name of the database collection to create.

        Returns:
            The MongoDB collection object.
        """
        return self.db.create_collection(name=name)

    def read_collection(self, name):
        """Returns the specified collection.

        Args:
            name: The name of the database collection to return.

        Returns:
            The MongoDB collection object.
        """
        return self.db.get_collection(name=name)

    def delete_collection(self, name):
        """Deletes the specified collection.

        Args:
            name: The name of the database collection to delete.

        Returns:
            None
        """
        self.db.drop_collection(name_or_collection=name)
