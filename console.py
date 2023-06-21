#!/usr/bin/python3
"""Console Module"""
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    # Determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline converted to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '').replace('_', ' ')

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' \
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """Method to print the help message for the quit command"""
        print('Quit command to exit the program')

    def do_EOF(self, command):
        """Method to handle EOF"""
        exit()

    def help_EOF(self):
        """Method to print the help message for the EOF command"""
        print('EOF command to exit the program')

    def do_create(self, arg):
        """Method to create a new instance of BaseModel"""
        if not arg:
            print('** class name missing **')
        elif arg not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            new_dict = HBNBCommand.classes[arg]()
            new_dict.save()
            print(new_dict.id)

    def help_create(self):
        """Method to print the help message for the create command"""
        print('Create a new instance of BaseModel and save it to JSON file')
        print('Usage: create <class_name>')

    def do_show(self, arg):
        """Method to retrieve a BaseModel object from JSON storage"""
        args = arg.split()
        if not arg:
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        elif len(args) < 2:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            objects = storage.all()
            if key in objects:
                print(objects[key])
            else:
                print('** no instance found **')

    def help_show(self):
        """Method to print the help message for the show command"""
        print('Prints the string representation of a BaseModel instance')
        print('Usage: show <class_name> <id>')

    def do_destroy(self, arg):
        """Method to delete a BaseModel object from JSON storage"""
        args = arg.split()
        if not arg:
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        elif len(args) < 2:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            objects = storage.all()
            if key in objects:
                objects.pop(key)
                storage.save()
            else:
                print('** no instance found **')

    def help_destroy(self):
        """Method to print the help message for the destroy command"""
        print('Deletes a BaseModel instance based on the class name and id')
        print('Usage: destroy <class_name> <id>')

    def do_all(self, arg):
        """Method to retrieve all instances or all instances of a class"""
        objects = storage.all()
        args = arg.split()

        if not arg:
            print([str(objects[k]) for k in objects])
        elif args[0] in HBNBCommand.classes:
            print([str(objects[k]) for k in objects if
                   args[0] == k.split('.')[0]])
        else:
            print('** class doesn\'t exist **')

    def help_all(self):
        """Method to print the help message for the all command"""
        print('Prints all string representations of all instances')
        print('Usage: all [class_name]')

    def do_update(self, arg):
        """Method to update an instance of BaseModel"""
        args = arg.split()

        if not arg:
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        elif len(args) < 2:
            print('** instance id missing **')
        elif len(args) < 3:
            print('** attribute name missing **')
        elif len(args) < 4:
            print('** value missing **')
        else:
            key = args[0] + '.' + args[1]
            objects = storage.all()
            if key in objects:
                obj = objects[key]
                attr_type = type(getattr(obj, args[2], None))
                if attr_type is None:
                    setattr(obj, args[2], args[3])
                else:
                    setattr(obj, args[2], attr_type(args[3]))
                obj.save()
            else:
                print('** no instance found **')

    def help_update(self):
        """Method to print the help message for the update command"""
        print('Updates a BaseModel instance based on the class name and id')
        print('Usage: update <class_name> <id> <attribute_name> <value>')

    def emptyline(self):
        """Method to handle empty line"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()

