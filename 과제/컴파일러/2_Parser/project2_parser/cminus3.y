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
static int savedVal;
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
	{savedTree=$1;}	
	;
declaration_list	:declaration_list declaration			
	    		{YYSTYPE t=$1;
			if(t!=NULL)
			{	while(t->sibling!=NULL) t=t->sibling;
				t->sibling=$2;
				$$=$1;}
			else $$=$2;
			}
			|declaration
			{$$=$1;}
			;
declaration		:var_declaration
	     		{$$=$1;}
			|fun_declaration
			{$$=$1;}
			;
var_declaration		:type_specifier id SEMI
		 	{$$=$1;
			$$->kind.exp=VarDeK;
			$$->attr.name=$2->attr.name;
			}
			|type_specifier id LBRACE NUM{savedVal=atoi(tokenString);}
			 RBRACE SEMI
			{$$=$1;
			$$->type=IntegerArr;
			$$->kind.exp=VarDeK;
			$$->attr.name=$2->attr.name;

			$4=newExpNode(ConstantK);
			$4->attr.val=savedVal;
			$$->child[0]=$4;
			}
			;
id			:ID
     			{$$=newExpNode(IdK);
			$$->attr.name=copyString(tokenString);
			};
type_specifier		:INT
			{$$=newExpNode(TypeK);
			$$->type=Integer;}
			|VOID
			{$$=newExpNode(TypeK);
			$$->type=Void;}
			|INT LBRACE RBRACE
			{$$=newExpNode(TypeK);
			$$->type=IntegerArr;}
			|VOID LBRACE RBRACE
			{$$=newExpNode(TypeK);
			$$->type=VoidArr;}
			;
fun_declaration		:type_specifier id LPAREN params RPAREN compound_stmt
		 	{
			$$=$1;
			$$->kind.exp=FuncK;
			$$->attr.name=$2->attr.name;
			$$->child[0]=$4;
			$$->child[1]=$6;
			}
			;
params			:param_list
	 		{$$=$1;}
	 		|VOID
			{$$=newExpNode(VoidK);}
			;
param_list		:param_list COMMA param
	    		{YYSTYPE t=$1;
			if(t!=NULL)
			{	while(t->sibling!=NULL) t=t->sibling;
				t->sibling=$3;
				$$=$1;}
			else $$=$3;
			}	
	    		|param
			{$$=$1;}
			;
param			:type_specifier id
			{$$=$1;
			$$->kind.exp=ParamK;
			$$->attr.name=$2->attr.name;
			}
			|type_specifier id LBRACE RBRACE
			{$$=$1;
			$$->kind.exp=ParamK;
			$$->attr.name=$2->attr.name;
			}
			;
compound_stmt		:LCURLY local_declarations statement_list RCURLY
	      		{$$=newStmtNode(CompoundK);
			if($2!=NULL){
				$$->child[0]=$2;
				$$->child[1]=$3;
			}
			else
				$$->child[0]=$3;
			}
			;
local_declarations	:local_declarations var_declaration
			{YYSTYPE t=$1;
			if(t!=NULL)
			{	while(t->sibling!=NULL) t=t->sibling;
				t->sibling=$2;
				$$=$1;}
			else $$=$2;
			}
		   	|{$$=NULL;}
			
			;
statement_list		:statement_list statement
	    		{YYSTYPE t=$1;
			if(t!=NULL)
			{	while(t->sibling!=NULL) t=t->sibling;
				t->sibling=$2;
				$$=$1;}
			else $$=$2;
			}
			|
			{$$=newStmtNode(StmtListK);
			}
			;
statement		:expression_stmt	{$$=$1;}
	   		|compound_stmt		{$$=$1;}
			|selection_stmt		{$$=$1;}
			|iteration_stmt		{$$=$1;}
			|return_stmt		{$$=$1;}
			;
expression_stmt		:expression SEMI
		 	|SEMI
			;
selection_stmt		:IF LPAREN expression RPAREN statement %prec IFX
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
iteration_stmt		:WHILE LPAREN expression RPAREN statement
			{$$=newStmtNode(WhileK);
			$$->child[0]=$3;
			$$->child[1]=$5;
			}
			;
return_stmt		:RETURN SEMI
	     		{$$=newStmtNode(ReturnNonK);}
	     		|RETURN expression SEMI
			{$$=newStmtNode(ReturnK);
			$$->child[0]=$2;
			}
			;
expression		:var ASSIGN expression
	    		{$$=newExpNode(AssignK);
			$$->child[0]=$1;
			$$->child[1]=$3;
			}
	    		|simple_expression
			{$$=$1;}

			;
var			:id
      			{$$=newExpNode(VarK);
			$$->attr.name=$1->attr.name;
			}
      			|id LBRACE expression RBRACE
			{$$=newExpNode(VarK);
			$$->attr.name=$1->attr.name;
			$$->child[0]=$3;
			}
			;
simple_expression	:additive_expression relop additive_expression
		  	{$$=$2;
			$$->child[0]=$1;
			$$->child[1]=$3;
			}
		  	|additive_expression
			{$$=$1;
			}
			;
relop			:LE	{$$=newExpNode(OpK);$$->attr.op=LE;}
			|LT	{$$=newExpNode(OpK);$$->attr.op=LT;}
			|GE	{$$=newExpNode(OpK);$$->attr.op=GE;}
			|GT	{$$=newExpNode(OpK);$$->attr.op=GT;}
			|EQ	{$$=newExpNode(OpK);$$->attr.op=EQ;}
			|NE	{$$=newExpNode(OpK);$$->attr.op=NE;}
			;
additive_expression	:additive_expression addop term
		    	{$$=$2;
			$$->child[0]=$1;
			$$->child[1]=$3;
			}
		    	|term
			{$$=$1;}
			;
addop			:PLUS	{$$=newExpNode(OpK);$$->attr.op=PLUS;}
			|MINUS	{$$=newExpNode(OpK);$$->attr.op=MINUS;}
			;
term			:term mulop factor
       			{$$=$2;
			$$->child[0]=$1;
			$$->child[1]=$3;
			}
       			|factor{$$=$1;}
			;
mulop			:TIMES	{$$=newExpNode(OpK);$$->attr.op=TIMES;}
			|OVER	{$$=newExpNode(OpK);$$->attr.op=OVER;}
			;
factor			:LPAREN expression RPAREN
	 		{$$=$2;}
	 		|var	{$$=$1;}
			|call	{$$=$1;}
			|NUM	
			{$$=newExpNode(ConstantK);
			$$->attr.val=atoi(tokenString);
			}
			;
call			:id LPAREN args RPAREN
       			{$$=newExpNode(CallK);
			$$->attr.name=$1->attr.name;
			$$->lineno=savedLineNo;
			$$->child[0]=$3;
			}
       			;
args			:arg_list
       			{$$=$1;}
       			|/*empty*/
			{$$=newStmtNode(EmptyK);
			}
			;
arg_list		:arg_list COMMA expression	
	    		{YYSTYPE t=$1;
			if(t!=NULL)
			{	while(t->sibling!=NULL) t=t->sibling;
				t->sibling=$3;
				$$=$1;}
			else $$=$3;
			}
	  		|expression
			{$$=$1;}
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

