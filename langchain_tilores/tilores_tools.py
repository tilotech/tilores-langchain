from tilores import TiloresAPI
from tilores.helpers import PydanticFactory
from functools import cached_property
from langchain.tools import StructuredTool

class TiloresTools:
    """
    This class builds structured tools to be used in Langchain out of an instance of the Tilores API.

    The Tilores API and its objects (Record, SearchParams, RecordInput) are different from instance
    to instance. This class helps build structured tools at runtime, allowing them to be used
    against any Tilores instance.
    """

    def __init__(self, tilores_api: TiloresAPI):
        self.tilores_api = tilores_api

    @cached_property
    def references(self):
        return PydanticFactory(self.tilores_api.schema).generate()

    def all(self):
        return [
            self.search_tool
        ]

    def search_tool(self):
        return StructuredTool.from_function(**{
            'name': 'tilores_search',
            'description': 'useful for when you need to search entities on variable parameters',
            'args_schema': self.references['SearchParams'],
            'return_direct': True,
            'func': self.tilores_api.search
        })
