/****************************************************/
/* File: tiny.y                                     */
/* The TINY Yacc/Bison specification file           */
/* Compiler Construction: Principles and Practice   */
/* Kenneth C. Louden                                */
/****************************************************/
%{
#define YYPARSER /* distinguishes Yacc output from other code files */

#include "globals.h"
#include "util.h"
#include "scan.h"
#include "parse.h"

#define YYSTYPE TreeNode *
static char * savedName; /* for use in assignments */
static int savedLineNo;  /* ditto */
static TreeNode * savedTree; /* stores syntax tree for later return */
static int yylex(void); // added 11/2/11 to ensure no conflict with lex

%}

%token ENDFILE ERROR
%token IF WHILE RETURN INT VOID
%token ID NUM ELSE
%token ASSIGN EQ NE LT LE GT GE PLUS MINUS TIMES OVER LPAREN RPAREN LBRACE RBRACE LCURLY RCURLY SEMI COMMA

%% /* Grammar for TINY */

program     : declaration_list
                 { savedTree = $1;} 
            ;
declaration_list	:declaration_list declaration
			{YYSTYPE t=$1;
			if(t!=NULL)
				{while(t->sibling!=NULL)
					t=t->sibling;
				t->sibling=$2;
				$$=$1;}
			else $$=$2;
			}
			|declaration{$$=$1;}
	    		;
declaration	:var_declaration{$$=$1;}
	    	|fun_declaration{$$=$1;}
var_declaration	:type_specifier ID{savedName=copyString(tokenString);
	       			savedLineNo=lineno;}
		SEMI
		{$$=newExpNode(ConstK);
		$$->child[0]=$2;
		$$->type=$1;
		$$->attr.name=savedName;
		$$->lineno=savedLineNo;
		}
		|type_specifier ID{savedName=copyString(tokenString);
				savedLineNo=lineno;}
		 LBRACE NUM RBRACE SEMI
		{$$=newExpNode(ConstK);
		$$->child[0]=$2;
		$$->child[1]=$3;
		$$->type=$1;
		$$->attr.name=savedName;
		$$->lineno=savedLineNo;
		}
		;
type_specifier	: INT
	       	{$$=$1;}
		| VOID
		{$$->$1;}
	       ;
fun_declaration	:type_specifier ID{savedName=copyString(tokenString);
	       			savedLineNo=lineno;}
		LCURLY params RCURLY compound_stmt
		{$$=newExpNode(FuncK);
		$$->child[0]=$2;
		$$->child[1]=$3;
		$$->child[2]=$4;
		$$->type=$1;
		$$->attr.name=savedName;
		$$->lineno=savedLineNo;
		}
		;
params		:param_list
		{$$=$1;}
		|VOID
		{$$=$1;}
	   	;
param_list	:param_list COMMA param
		{YYSTYPE t=$1;
		if(t!=NULL)
			{while(t->sibling!=NULL) t=t->sibling;
			t->sibling=$2;
			$$=$1;}
		else $$=$2;
		}
		|param
		{$$=$1;}
       		;
param		: type_specifier ID
      		{
		$$->type=$1;
		$$->attr.name=copyString(tokenString);
		$$->attr.lineeno=lineno;
		}
		|type_specifier ID{savedName=copyString(tokenString);
				savedLineNo=lineno;}
		 LBRACE RBRACE
		{
		$$->type=$1;
		$$->attr.name=savedName;
		$$->lineno=lineno;
		}
      ;
compound_stmt	:LCURLY local_declarations statement_list RCURLY
	      	{$$=newStmtNode(CompoundK);
		$$->child[0]=$2;
		$$->child[1]=$3;
		}
	      ;
local_declarations	:local_declarations var_declaration
		   	{$$=newStmtNode(StmtK);
			$$->child[0]=$1;
			$$->child[1]=$2;
			}
			|ENDFILE{}
		  	;
statement_list	:statement_list statement
		{YYSTYPE t=$1;
		if(t!=NULL)
			{while(t->sibling!=NULL) t=t->sibling;
			t->sibling=$2;
			$$=$1;}
		else $$=$2;
		}
		|ENDFILE{}	
		;
statement	:expression_stmt{$$=$1;}
	       	|compound_stmt{$$=$1;}
		|selection_stmt{$$=$1;}
		|iteration_stmt{$$=$1;}
		|return_stmt{$$=$1;}
	       ;
expression_stmt	:expression SEMI
		{$$=$1;}
		|SEMI{$$=$1}
		;
selection_stmt	:IF LPAREN expression RPAREN statement
	       	{$$=newStmtNode(IfK);
		$$->child[0]=$3;
		$$->child[1]=$5;
		}
		|IF LPAREN expression RPAREN statement ELSE statement
		{$$=newStmtNode(IfElseK);
		$$->child[0]=$3;
		$$->child[1]=$5;
		$$->child[2]=$7;
		}
	       ;
iteration_stmt	:WHILE LPAREN expression RPAREN statement
	       	{$$=newStmtNode(WhileK);
		$$->child[0]=$3;
		$$->child[1]=$5;
		}
	       ;
return_stmt	:RETURN SEMI
	    	{$$=$1;}
		|RETURN expression
		{$$=newStmtNode(ReturnK);
		$$->child[0]=$2;
		}
	    ;
expression	:var ASSIGN expression
	  	{$$=newExpNode(ConstK);
		$$->child[0]=$1;
		$$->child[1]=$3;
		}
		|simple_expression
	   	{$$=$1;		
		}
		;
var		:ID
    		{$$->name=copyString(tokenString);}
		|ID{savedName=copyString(tokenString);
		savedLineNo=lineno;}
		LBRACE expression RBRACE
		{$$=newStmtNode(StmtK); 
		$$->name=savedName;
		$$->lineno=savedLineNo;
		$$->child[0]=$3;
		}
   	 	;
simple_expression	:additive_expression relop additive_expression
		{$$=newExpNode(OpK);
		$$->child[0]=$1;
		$$->child[1]=$3;
		$$->attr.op=$2;		
		}
		|additive_expression
		{$$=$1;}
		 ;
relop		:LE{$$=$1;}
       		|LT{$$=$1;}
		|GE{$$=$1;}
		|GT{$$=$1;}
		|EQ{$$=$1;}
		|NE{$$=$1;}
		;
additive_expression	:additive_expression addop term
			{$$=newExpNode(OpK);
			$$->child[0]=$1;
			$$->child[1]=$3;
			$$->attr.op=$2;
			}
			|term
			{$$=$1;
			}
		    	;
addop		:PLUS{$$=$1;}
       		|MINUS{$$=$1;}
      		;
term		:term mulop factor
      		{$$=newExpNode(OpK);
		$$->child[0]=$1;
		$$->child[1]=$3;
		$$->attr.op=$2;
		}
		|factor{$$=$1;}
     		;
mulop		:TIMES{$$=$1;}
       		|OVER{$$=$1;}
     		;
factor		:LPAREN expression RPAREN
		{$$=$2;}
		|var{$$=$1;}
		|call{$$=$1;}
		|NUM{$$=$1;}
       		;
call		:ID{savedName=copyString(tokenString);
     		savedLineNo=lineno;}
		LPAREN args RPAREN
      		{$$=newExpNode(IdK);
		$$->child[0]=$3;
		$$->attr.name=savedName;
		$$->lineno=savedLineNo;
		}
     		;
args		:arg_list{$$=$1;}
      		|ENDFILE{}
     		;
arg_list	:arg_list COMMA expression
	 	{$$=newStmtNode(StmtK);
		$$->child[0]=$1;
		$$->child[1]=$3;
		}
		|expression{$$=$1;}
		;






%%

int yyerror(char * message)
{ fprintf(listing,"Syntax error at line %d: %s\n",lineno,message);
  fprintf(listing,"Current token: ");
  printToken(yychar,tokenString);
  Error = TRUE;
  return 0;
}

/* yylex calls getToken to make Yacc/Bison output
 * compatible with ealier versions of the TINY scanner
 */
static int yylex(void)
{ return getToken(); }

TreeNode * parse(void)
{ yyparse();
  return savedTree;
}

