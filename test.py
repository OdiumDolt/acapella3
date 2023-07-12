from router import Router

routes = Router()

@routes.command("!p __var__")
def new_command(var):
    


func, args = routes.find("!p this_is_a_url This_is_url_2")
# print(type(args))
func(args)