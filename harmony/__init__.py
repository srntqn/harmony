import pkg_resources


__distribution_name__ = "harmony"
__module_name__ = "harmony"
__project_name__ = pkg_resources.get_distribution(__distribution_name__).project_name
__version__ = pkg_resources.get_distribution(__distribution_name__).version
