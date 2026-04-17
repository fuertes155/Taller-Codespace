grammar WhileLang;

program : statement* EOF;

statement : varDecl ';'
          | assignment ';'
          | ifStmt
          | whileStmt
          ;

varDecl : type ID '=' expr # VarDeclWithInit
        | type ID         # VarDecl
        ;

assignment : ID '=' expr;

ifStmt : 'if' '(' expr ')' '{' statement* '}' ('else' '{' statement* '}')?;

whileStmt : 'while' '(' expr ')' '{' statement* '}';

expr : expr op=('+'|'-'|'*'|'/') expr # BinaryOp
     | expr op=('<'|'>'|'=='|'!=') expr # Comparison
     | '(' expr ')'                   # ParenExpr
     | ID                             # VarRef
     | INT                            # IntLiteral
     | STRING                         # StringLiteral
     | BOOL                           # BoolLiteral
     ;

type : 'int' | 'string' | 'bool';

ID : [a-zA-Z_][a-zA-Z0-9_]*;
INT : [0-9]+;
STRING : '"' (~["\\] | '\\' .)* '"';
BOOL : 'true' | 'false';

WS : [ \t\r\n]+ -> skip;