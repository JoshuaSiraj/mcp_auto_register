import inspect

from mcp_auto_register.register import register_classes_from_package
from mcp.server.fastmcp import FastMCP

from nba_api.stats.endpoints._base import Endpoint

# Create MCP instance
mcp = FastMCP()

def nba_endpoint_wrapper(endpoint: Endpoint):
    init_params = inspect.signature(endpoint.__init__).parameters
    required_args = {
        p: param.annotation if param.annotation != inspect.Parameter.empty else "Any"
        for p, param in init_params.items()
        if p != "self" and param.default == inspect.Parameter.empty
    }
    def wrapper(**kwargs):
        return endpoint(**kwargs).get_dict()
    
    wrapper.__signature__ = inspect.Signature(
        parameters=[
            inspect.Parameter(arg, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            for arg, _ in required_args.items()
        ]
    )
    return wrapper

register_classes_from_package("nba_api.stats.endpoints", nba_endpoint_wrapper, mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
