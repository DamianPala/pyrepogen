
import argparse

from . import logger 

logger = logger.get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Python Repository Assistant",
                                     epilog="""Available commands: ...""")
    parser.add_argument('command', action='store', default=None, help="Repo name or path to the directory when repository will be generated. If directory does not exist then will be created.")
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help="Disable output")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help="Enable debug output")
    args = parser.parse_args()
        
    
if __name__ == '__main__':
    main()