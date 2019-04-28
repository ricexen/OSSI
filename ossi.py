import pprint
from definitions import define_directories, terminal, user_request_exit
from src.navegation import navegation_menu
from src.models import FBPerson as Person

define_directories()

pp = pprint.PrettyPrinter()
me = Person('me')
me.load_knowns(depth=0)
me.save_connections()

pp.pprint(me.__dict__)


# while (not user_request_exit):
#   terminal.run_command(navegation_menu)
