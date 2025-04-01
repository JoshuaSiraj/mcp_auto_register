from mcp_auto_register.register import register_functions_from_package
from mcp.server.fastmcp import FastMCP

# Initialize MCP instance
mcp_instance = FastMCP()

register_functions_from_package('scipy.linalg', mcp_instance=mcp_instance, func_filter=['eigh', 'inv'])

if __name__ == "__main__":
    mcp_instance.run()


