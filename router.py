import inspect


class Router():
    def __init__(
            self, 
            var_keyword = '__var__',
            commands = {}
        ) -> None:

        self.var_keyword = var_keyword
        self.commands = commands
    
    def command(self, path):
        def add_func(command):
            path = path.split(' ')
            self.add_command(path, self.commands)
            return command
        
        return add_func  
    
    def add_command(self, path, command):
        try:
            if path[0] in command:
                self.add_command(path[:1], command[:1 ])
        except IndexError:
            pass

        

    def find(self, command):
        return self.find_function(command.split(' '), self.commands)

    def find_function(self, command, tree):
        args = ()
        try:
            if inspect.ismethod(tree):
                return tree, args
            elif type(tree[command[0]]) == dict:
                tree = tree[command[0]]
                tree, new_args = self.find_function(command[1:], tree)
                args += new_args
                return tree, args
        except KeyError as e:
            if self.var_keyword in tree:
                args += tuple([command[0]])
                tree, new_args = self.find_function(command[1:], tree[self.var_keyword])
                args += new_args
                return tree, args
            else:
                print(e)
            
               

