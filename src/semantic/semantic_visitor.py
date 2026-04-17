from src.grammar.generated.WhileLangVisitor import WhileLangVisitor
from src.grammar.generated.WhileLangParser import WhileLangParser
from src.semantic.symbol_table import SymbolTable, SemanticError

class SemanticVisitor(WhileLangVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def visitProgram(self, ctx: WhileLangParser.ProgramContext):
        self.symbol_table.enter_scope()  # Scope global
        self.visitChildren(ctx)
        self.symbol_table.exit_scope()
        if self.errors:
            raise Exception("Errores semánticos encontrados:\n" + "\n".join(str(e) for e in self.errors))

    def visitVarDeclWithInit(self, ctx: WhileLangParser.VarDeclWithInitContext):
        var_type = ctx.type_().getText()
        name = ctx.ID().getText()
        expr_type = self.visit(ctx.expr())
        if var_type != expr_type:
            self.errors.append(SemanticError(f"No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'. Tipos incompatibles.", ctx.start.line))
        try:
            self.symbol_table.declare(name, var_type, ctx.start.line)
        except SemanticError as e:
            self.errors.append(e)

    def visitVarDecl(self, ctx: WhileLangParser.VarDeclContext):
        var_type = ctx.type_().getText()
        name = ctx.ID().getText()
        try:
            self.symbol_table.declare(name, var_type, ctx.start.line)
        except SemanticError as e:
            self.errors.append(e)

    def visitAssignment(self, ctx: WhileLangParser.AssignmentContext):
        name = ctx.ID().getText()
        expr_type = self.visit(ctx.expr())
        try:
            var_type = self.symbol_table.get_type(name, ctx.start.line)
            if var_type != expr_type:
                self.errors.append(SemanticError(f"No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'. Tipos incompatibles.", ctx.start.line))
        except SemanticError as e:
            self.errors.append(e)

    def visitIfStmt(self, ctx: WhileLangParser.IfStmtContext):
        cond_type = self.visit(ctx.expr())
        if cond_type != 'bool':
            self.errors.append(SemanticError(f"La condición del 'if' debe ser de tipo 'bool', pero se encontró '{cond_type}'.", ctx.start.line))
        self.symbol_table.enter_scope()
        self.visitChildren(ctx)
        self.symbol_table.exit_scope()

    def visitWhileStmt(self, ctx: WhileLangParser.WhileStmtContext):
        cond_type = self.visit(ctx.expr())
        if cond_type != 'bool':
            self.errors.append(SemanticError(f"La condición del 'while' debe ser de tipo 'bool', pero se encontró '{cond_type}'.", ctx.start.line))
        self.symbol_table.enter_scope()
        self.visitChildren(ctx)
        self.symbol_table.exit_scope()

    def visitBinaryOp(self, ctx: WhileLangParser.BinaryOpContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        op = ctx.op.text
        if op in ['+', '-', '*', '/']:
            if left_type != 'int' or right_type != 'int':
                self.errors.append(SemanticError(f"Operador '{op}' no definido para operandos de tipo '{left_type}' y '{right_type}'. Se esperaba tipos numéricos.", ctx.start.line))
            return 'int'
        elif op in ['<', '>', '==', '!=']:
            if left_type != right_type:
                self.errors.append(SemanticError(f"Operador '{op}' requiere operandos del mismo tipo, pero se encontró '{left_type}' y '{right_type}'.", ctx.start.line))
            if left_type == 'string' and op in ['<', '>']:
                self.errors.append(SemanticError(f"Operador '{op}' no definido para operandos de tipo 'string'. Se esperaba tipos numéricos.", ctx.start.line))
            return 'bool'

    def visitComparison(self, ctx: WhileLangParser.ComparisonContext):
        return self.visitBinaryOp(ctx)  # Reutilizar lógica

    def visitVarRef(self, ctx: WhileLangParser.VarRefContext):
        name = ctx.ID().getText()
        try:
            return self.symbol_table.get_type(name, ctx.start.line)
        except SemanticError as e:
            self.errors.append(e)
            return 'unknown'

    def visitIntLiteral(self, ctx: WhileLangParser.IntLiteralContext):
        return 'int'

    def visitStringLiteral(self, ctx: WhileLangParser.StringLiteralContext):
        return 'string'

    def visitBoolLiteral(self, ctx: WhileLangParser.BoolLiteralContext):
        return 'bool'