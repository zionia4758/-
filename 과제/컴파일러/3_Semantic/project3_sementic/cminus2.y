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

%token WHILE RETURN INT VOID IF
%nonassoc IFX
%nonassoc ELSE
%token ID NUM
%token EQ NE LT LE GT GE
%left PLUS MINUS
%right ASSIGN TIMES OVER
%token SEMI COMMA RCURLY LCURLY
%token LBRACE RBRACE
%token LPAREN RPAREN
%token ENDFILE ERROR


%% /* Grammar for TINY */

program	:declaration_list
	
	;
declaration_list	:declaration_list declaration
			{}
			|declaration
			{}
			;
declaration		:var_declaration
	     		
			|fun_declaration
			;
var_declaration		:type_specifier id SEMI

			|type_specifier id LBRACE NUM RBRACE SEMI
			;
id			:ID
     			;
type_specifier		:INT
			|VOID
fun_declaration		:type_specifier id LPAREN params RPAREN compound_stmt
		 	;
params			:param_list
	 		|VOID
			;
param_list		:param_list COMMA param
	    		|param
param			:type_specifier ID 
			|type_specifier id LBRACE RBRACE
			;
compound_stmt		:LCURLY local_declarations statement_list RCURLY
	      		;
local_declarations	:local_declarations var_declaration
		   	|ENDFILE
			;
statement_list		:statement_list statement
			|ENDFILE
			;
statement		:expression_stmt
	   		|compound_stmt
			|selection_stmt
			|iteration_stmt
			|return_stmt
			;
expression_stmt		:expression SEMI
		 	|SEMI
			;
selection_stmt		:IF LPAREN expression RPAREN statement %prec IFX
			|IF LPAREN expression RPAREN statement ELSE statement
			;
iteration_stmt		:WHILE LPAREN expression RPAREN statement
			;
return_stmt		:RETURN SEMI
	     		|RETURN expression SEMI
			;
expression		:var ASSIGN expression
	    		|simple_expression
			;
var			:ID
      			|id LBRACE expression RBRACE
			;
simple_expression	:additive_expression relop additive_expression
		  	|additive_expression
			;
relop			:LE
			|LT
			|GE
			|GT
			|EQ
			|NE
			;
additive_expression	:additive_expression addop term
		    	|term
			;
addop			:PLUS
			|MINUS
			;
term			:term mulop factor
       			|factor
			;
mulop			:TIMES
			|OVER
			;
factor			:LPAREN expression RPAREN
	 		|var
			|call
			|NUM
			;
call			:id LPAREN args RPAREN
       			;
args			:arg_list
       			|ENDFILE
			;
arg_list		:arg_list COMMA expression
	  		|expression
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

