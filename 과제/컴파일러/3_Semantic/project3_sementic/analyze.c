/****************************************************/
/* File: analyze.c                                  */
/* Semantic analyzer implementation                 */
/* for the TINY compiler                            */
/* Compiler Construction: Principles and Practice   */
/* Kenneth C. Louden                                */
/****************************************************/

#include "globals.h"
#include "symtab.h"
#include "analyze.h"

/* counter for variable memory locations */
static int location = 2;
static int localLoc=2;
static char* cur_scope="global";
static char* parent_scope="root";
static int nested_level=1;
static int travCnt=0;
/* Procedure traverse is a generic recursive 
 * syntax tree traversal routine:
 * it applies preProc in preorder and postProc 
 * in postorder to tree pointed to by t
 */
static void traverse( TreeNode * t,
		void (* preProc) (TreeNode *),
		void (* postProc) (TreeNode *) )
{ 
	if (t != NULL)
	{
		if(t->nodekind==ExpK && t->kind.exp==FuncK)
			cur_scope=t->attr.name;
	       	preProc(t);
		{
		       	int i;
			for (i=0; i < MAXCHILDREN; i++)
				traverse(t->child[i],preProc,postProc);
		}
		postProc(t);
		traverse(t->sibling,preProc,postProc);
	}
}

/* nullProc is a do-nothing procedure to 
 * generate preorder-only or postorder-only
 * traversals from traverse
 */
static void semantic_error(TreeNode*t, char*message)
{
	fprintf(listing,"Semantic Error: %s '%s' at line %d\n",message,t->attr.name,t->lineno);
	Error=TRUE;
}
static void nullProc(TreeNode * t)
{ 
	if (t==NULL) return;
	else return;
}
static void nullProc2(TreeNode*t)
{
	if(t==NULL) return;
	else
	{
		if(t->nodekind==ExpK)
			if(t->kind.exp== FuncK)
				cur_scope=t->attr.name;
		
	}
	return;


}
/* Procedure insertNode inserts 
 * identifiers stored in t into 
 * the symbol table 
 */
static void insertNode( TreeNode * t)
{
	//printf("%p,%d\n",t,t->nodekind);
	//printNode(t);
	char s[20];
	switch (t->nodekind)
	{ 
		case StmtK:
			switch (t->kind.stmt)
			{ 
				case WhileK:

				case IfElseK:
				case IfK:
					break;
				case CompoundK:
					localLoc=0;
					nested_level++;
					break;
				case ReturnK:
				case ReturnNonK:
				case StmtListK:
				case EmptyK:
					/*
				case ReadK:
				if (st_lookup(t->attr.name) == -1)
					// not yet in table, so treat as new definition 
					st_insert(t->attr.name,t->lineno,location++);
				else
					 already in table, so ignore location, 
					   //add line number of use only 
					st_insert(t->attr.name,t->lineno,0);
				break;
				*/
				default:
				break;
			}
			break;
		case ExpK:

			switch (t->kind.exp)
			{ 

				case ParamK:
					if(travCnt==0)
					{
						st_insert("global",cur_scope,t->attr.name,t->type,nested_level,t->lineno,localLoc++);
						st_insert_func(t->attr.name,t->type,0,cur_scope);
					}
					break;
				case ParamArrK:
					if(travCnt==0)
					{
						st_insert("global",cur_scope,t->attr.name,t->type,nested_level,t->lineno,localLoc++);
						st_insert_func(t->attr.name,t->type,0,cur_scope);
					}
					break;


				case VoidK:
					break;
				case VarDeK:
					if(travCnt==0){
					if(st_lookup(cur_scope,t->attr.name)!=NULL)
						semantic_error(t,"redefined variable");
					else 
						st_insert(parent_scope,cur_scope,t->attr.name,t->type,nested_level,t->lineno,localLoc++);
					}
					break;
				case VarK:
					if(travCnt==0)
						if(st_lookup(cur_scope,t->attr.name)!=NULL)
							st_insert(parent_scope,cur_scope,t->attr.name,t->type,nested_level,t->lineno,0);
						else
							semantic_error(t,"undefined variable");
					break;
				case VarArrK:
					if(travCnt==0)
						if(st_lookup(cur_scope,t->attr.name)!=NULL)
							st_insert(parent_scope,cur_scope,t->attr.name,t->type,nested_level,t->lineno,0);
						else
							semantic_error(t,"undefined variable");
					break;
	case OpK:
					break;				
				case AssignK:
					break;
				case FuncK:
					if(travCnt==0)
					{
					if(st_lookup("global",t->attr.name)==NULL)
					{
						nested_level=0;
						parent_scope="global";
						cur_scope=t->attr.name;
						localLoc=0;
						st_insert(NULL,"global",t->attr.name,5,0, t->lineno,location++);
						st_insert_func(t->attr.name,t->type,1,NULL);	
					}
					else
						semantic_error(t,"redefined function");
					}
					break;
				case CallK:
					if(travCnt==1)
					{
						if(st_lookup("global",t->attr.name)==NULL)
							semantic_error(t,"undefined function");
						st_insert(NULL,"global",t->attr.name,t->type,0,t->lineno,location++);
					}						
					break;
				case TypeK:
					break;
				case ConstantK:
					break;
				case IdK:
					/* not yet in table, so treat as new definition */
					/* already in table, so ignore location, 
					   add line number of use only */ 
					printf("IdK\n");
					break;
				default:
					break;
			}
			break;
		default:
			printf("none type\n");
			break;
	}
}

/* Function buildSymtab constructs the symbol 
 * table by preorder traversal of the syntax tree
 */
void buildSymtab(TreeNode * syntaxTree)
{ 
	reservedFunc();
	traverse(syntaxTree,insertNode,nullProc);

	travCnt++;
	traverse(syntaxTree,insertNode,nullProc);
	if (TraceAnalyze)
	{ fprintf(listing,"\nSymbol table:\n\n");
		printSymTab(listing);
	}
}

static void typeError(TreeNode * t, char * message)
{
	fprintf(listing,"Type error at line %d: %s\n",t->lineno,message);
	Error = TRUE;
}

/* Procedure checkNode performs
 * type checking at a single tree node
 */
static void checkNode(TreeNode * t)
{

	ExpType ch1;
	ExpType ch2;	
	TreeNode *ch;
	VarList v;
	BucketList l=(BucketList)malloc(sizeof(struct BucketListRec));
	FuncList f=(FuncList)malloc(sizeof(struct BucketListRec));

/*
	if(t->nodekind==ExpK)
		printf("Tkind : %s\n",ExpList[t->kind.exp]);
	else
		printf("Tkind : %s\n",StmtList[t->kind.stmt]);
*/

	switch (t->nodekind)
	{
		case ExpK:
		switch (t->kind.exp)
		{
		       	case OpK:
			ch1=t->child[0]->type;
			ch2=t->child[1]->type;
			///////////////////////
			if ((ch1!= Integer&&ch1!=IntegerArr) ||(ch2!= Integer&& ch2!=IntegerArr))
				typeError(t,"Op applied to non-integer");
			if ((t->attr.op == EQ) || (t->attr.op == LT)|| (t->attr.op==LE) || (t->attr.op==NE)||(t->attr.op==GT)||(t->attr.op==GE))
				t->type = Boolean;
			else
				t->type = Integer;
			break;
			case AssignK:
				ch1=t->child[0]->type;
				if(ch1==IntegerArr && t->child[0]->child[0]!=NULL)
					ch1=Integer;
				ch2=t->child[1]->type;
				if(ch2=IntegerArr && t->child[1]->child[0]!=NULL)
					ch2=Integer;
				if(t->child[1]->nodekind==ExpK && t->child[1]->kind.exp==ConstantK)
					ch2=Integer;
				if( ( ch1!=ch2)|| !(ch1==Integer || ch1==IntegerArr) )
					typeError(t,"assign should be integer");
			break;
			case IdK:
			t->type = Integer;
			break;
			case FuncK:
				if(t->type==VoidArr)
					typeError(t,"Void[] can't available for function");
				cur_scope=t->attr.name;
				
			break;
			case VarDeK:
				if(t->type==Void||t->type==VoidArr)
					typeError(t,"Variable type cannot be Void");

			break;
			case VarArrK:

				st_lookup_including_parent(cur_scope,t->attr.name,l);
				if(l==NULL)
					semantic_error(t,"undefined variable");
				else
				{
					t->type=l->type;
				}
				if(l->type==IntegerArr)
				{
					if(t->child[0]->nodekind==ExpK && t->child[0]->kind.exp==CallK)
						semantic_error(t,"invalid array indexing. indices should be int");

				}
				break;
			case VarK:
				st_lookup_including_parent(cur_scope,t->attr.name,l);
				if(l==NULL)
					semantic_error(t,"undefined variable");
				else
				{
					t->type=l->type;
				}
			break;
			case ParamArrK:
			case ParamK:
				t->type=l->type;
				break;
			case CallK:
				ch=t->child[0];
				lookup_func(t->attr.name,f);
				if(f==NULL)      
					break;
				v=f->arg;
				t->type=f->type;
				if(v==NULL&&ch->nodekind==StmtK&&ch->kind.stmt==EmptyK)
				{
					break;	
				}
			
				while(v!=NULL||ch!=NULL)
				{
					ch1=ch->type;
					if(ch->child[0]!=NULL&& ch1==IntegerArr)
						ch1=Integer;
					if(v==NULL || ch==NULL||(v->type!=ch1))
					{
						typeError(t,"invalid function call");
						break;
					}

					v=v->next;
					ch=ch->sibling;
					
				}
				break;
			case ConstantK:
				t->type=Integer;
				break;
			default:
			break;
		}
		break;
		case StmtK:
		switch (t->kind.stmt)
		{
		       	case IfK:
			if (t->child[0]->type != Boolean)
				typeError(t->child[0],"if test is not Boolean");
			break;
			case ReturnK:
				lookup_func(cur_scope,f);
				if(f->type!=t->child[0]->type)
					typeError(t,"invalid return type");
			break;
		
		
			case ReturnNonK:
				lookup_func(cur_scope,f);
				if(f->type!=t->type)
					typeError(t,"invalid return type");
		
			break;
			default:
			break;
		
		}
		break;
		default:
		break;

	}
	free(l);
	free(f);
}

/* Procedure typeCheck performs type checking 
 * by a postorder syntax tree traversal
 */
void typeCheck(TreeNode * syntaxTree)
{ 
	cur_scope="global";
	traverse(syntaxTree,nullProc2,checkNode);
}
