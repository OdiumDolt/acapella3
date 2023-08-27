class CMDRouter():
    def __init__(
            self, 
            var_keyword = '__var__',
            commands = {}
        ) -> None:

        self.var_keyword = var_keyword
        self.commands = commands
    
    def __add_command(self, path, commands, final_func):
        print(path)
        if path[0] in commands:
            self.__add_command(path[:1], commands[path[0]], final_func)
        
        elif path[0] not in commands:
            if len(path) == 1:
                commands[path[0]] = final_func
                return commands
            else:
                commands[path[0]] = {}
                return self.__add_command(path[1:], commands[path[0]], final_func)
            

    def command(self, path):
        path = path.split(' ')
        def add_func(func):
            self.__add_command(path, self.commands, func)
            return func
        
        return add_func

    def find(self, command):
        return self.__find_function(command.split(' '), self.commands)

    def __find_function(self, command, tree):
        args = ()
        try:
            if callable(tree):
                if len(command) > 0:
                    args += tuple([' '.join(command)])
                return tree, args
            
            elif type(tree) == dict:
                tree = tree[command[0]]
                tree, new_args = self.__find_function(command[1:], tree)
                args += new_args
                return tree, args
        
        except KeyError or IndexError as e:
            if self.var_keyword in tree:
                args += tuple([command[0]])
                tree, new_args = self.__find_function(command[1:], tree[self.var_keyword])
                args += new_args
                return tree, args
            else:
                print(e)
            
               

router = CMDRouter()