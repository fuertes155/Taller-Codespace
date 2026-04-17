class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Pila de scopes, el último es el scope actual

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name, var_type, line):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise SemanticError(f"Variable '{name}' ya declarada en el ámbito actual.", line)
        current_scope[name] = {'type': var_type, 'line': line}

    def lookup(self, name, line):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SemanticError(f"Variable '{name}' no declarada en el ámbito actual.", line)

    def get_type(self, name, line):
        symbol = self.lookup(name, line)
        return symbol['type']

class SemanticError(Exception):
    def __init__(self, message, line):
        super().__init__(f"Error semántico en línea {line}: {message}")
        self.line = line