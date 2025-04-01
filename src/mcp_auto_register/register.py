import importlib
import inspect
import pkgutil
from mcp.server.fastmcp import FastMCP
from typing import Optional, Callable, List

def register_functions_from_package(
        package_name: str, 
        mcp_instance: FastMCP | None = None, 
        func_filter: List[str] | None = None
    ):
    """
    Registers all functions from a package as MCP functions.

    Parameters
    ----------
    package_name : str
        The name of the package to scan for functions.
    mcp_instance : FastMCP, optional
        The instance of FastMCP to register the functions with. If None, a new instance is created.
    func_filter : list, optional
        A list of function names to filter which functions to register. If None, registers all functions.
    """
    if mcp_instance is None:
        mcp_instance = FastMCP()

    package = importlib.import_module(package_name)

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if is_pkg:
            continue 

        try:
            importlib.import_module(module_name)
        except ImportError:
            continue  # Skip modules that cannot be imported
        module = importlib.import_module(module_name)

        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("_"):
                continue

            if func.__module__ != module_name:
                continue  # Ensure the function belongs to the module

            if func_filter and name not in func_filter:
                continue  # Skip if the function is not in the filter
                
            print(f"Registering function: {name}")
            mcp_instance.tool(name=name)(func)  # Register function with its name

    return mcp_instance


def register_classes_from_package(
        package_name: str, 
        class_wrapper: Callable, 
        mcp_instance: FastMCP | None = None, 
        class_filter: List[str] | None = None
    ):
    """
    Registers classes from a given package as MCP tools. The provided `class_wrapper` callable is applied to each 
    class, and the result is registered as an MCP tool.

    Parameters
    ----------
    package_name : str
        The name of the package to scan for classes and methods.
    class_wrapper : Callable
        A callable that takes a class as an argument and returns a callable function.
    mcp_instance : FastMCP, optional
        The instance of FastMCP to register the methods with. If None, a new instance is created.
    class_filter : list, optional
        A list of class names to filter which classes to register. If None, registers all classes.
    """
    if mcp_instance is None:
        mcp_instance = FastMCP()

    package = importlib.import_module(package_name)

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if is_pkg:
            continue  # Skip sub-packages

        module = importlib.import_module(module_name)

        for name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != module_name:
                continue  # Ensure the class belongs to the module

            if class_filter and name not in class_filter:
                continue  # Skip if the class is not in the filter
            
            mcp_instance.tool(name=name)(class_wrapper(cls))
            

    return mcp_instance
