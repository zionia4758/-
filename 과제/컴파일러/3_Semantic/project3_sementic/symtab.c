/****************************************************/
/* File: symtab.c                                   */
/* Symbol table implementation for the TINY compiler*/
/* (allows only one symbol table)                   */
/* Symbol table is implemented as a chained         */
/* hash table                                       */
/* Compiler Construction: Principles and Practice   */
/* Kenneth C. Louden                                */
/****************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symtab.h"
#include "globals.h"
/* SIZE is the size of the hash table */
#define size 211

/* SHIFT is the power of two used as multiplier
   in hash function  */
#define SHIFT 4

/* the hash function */
static int hash ( char * key )
{ int temp = 0;
	int i = 0;
	while (key[i] != '\0')
	{ temp = ((temp << SHIFT) + key[i]) % SIZE;
		++i;
	}
	return temp;
}

/* the list of line numbers of the source 
 * code in which a variable is referenced
 */
/* The record in the bucket lists for
 * each variable, including name, 
 * assigned memory location, and
 * the list of line numbers in which
 * it appears in the source code
 */

/* the hash table */
static FuncList hashTable_Func[SIZE];
static ScopeList hashTable_scope[SIZE];
/* Procedure st_insert inserts line numbers and
 * memory locations into the symbol table
 * loc = memory location is inserted only the
 * first time, otherwise ignored
 */
void st_insert_func(char*name,ExpType type,int isFunc,char* scope)
{
	int h= hash(name);
	if(isFunc==1)
	{
		FuncList s=hashTable_Func[h];
		while(s!=NULL && (strcmp(s->name,name)!=0))
			s=s->next;
		if(s==NULL)
		{
			s=(FuncList)calloc(1,sizeof(struct FuncListRec));
			strncpy(s->name,name,19);
			s->type=type;
			hashTable_Func[h]=s;
		}
	}
	else if(isFunc==0)
	{
		h=hash(scope);
		FuncList s=hashTable_Func[h];
		if(s==NULL) return;
		while(s!=NULL&&(strcmp(s->name,scope)!=0))
		{
			s=s->next;
		}
		VarList l=s->arg;
		if(l==NULL)
		{
			l=(VarList)calloc(1,sizeof(struct VarListRec));
			strncpy(l->name,name,19);
			l->type=type;
			s->argCnt++;
			s->arg=l;
			return;
		}
		if(l->next!=NULL)
			l=l->next;
		l->next=(VarList)calloc(1,sizeof(struct VarListRec));
		strncpy(l->next->name,name,19);
		l->next->type=type;
		s->argCnt++;
	}
	return ;

}
void st_insert(char*parent_scope, char * scope,char*name, ExpType type,int nestLevel, int lineno, int loc )
{ 
	int h = hash(scope);

	ScopeList s=hashTable_scope[h];

	//scope table 탐색
	if(s==NULL)
	{

		s=(ScopeList)calloc(1,sizeof(struct ScopeListRec));
		strncpy(s->scope,scope,19);
		//	s->bucket=(BucketList)malloc(sizeof(struct BucketListRec)*SIZE);
		hashTable_scope[h]=s;
		if(parent_scope==NULL)
		{
			s->parent=NULL;
		}
		else
		{
			int ph=hash(parent_scope);
			s->parent=hashTable_scope[ph];

		}
	}

	int h_=hash(name);
	BucketList l =  s->bucket[h_];
	while ((l != NULL) && (strncmp(name,l->name,19) != 0))
	{
		l = l->next;
	}
	if (l == NULL) /* variable not yet in table */
	{ 	l = (BucketList) malloc(sizeof(struct BucketListRec));
		strncpy(l->name ,name,19);
		l->lines = (LineList) malloc(sizeof(struct LineListRec));
		l->lines->lineno = lineno;
		l->type=type;
		l->memloc = loc;
		l->lines->next = NULL;
		l->next = NULL;
		l->nested_level=nestLevel;
		strncpy(l->scope,scope,19);
		s->bucket[h_] = l;

	}
	else /* found in table, so just add line number */
	{	LineList t = l->lines;
		while (t->next != NULL){t = t->next;}
		t->next = (LineList) malloc(sizeof(struct LineListRec));
		t->next->lineno = lineno;
		t->next->next = NULL;
	}
}
BucketList st_lookup(char*scope, char*name)
{
	int h =hash(scope);
	ScopeList s=hashTable_scope[h];
	while(s!=NULL)
	{
		h=hash(name);
		BucketList l=s->bucket[h];
		while((l!=NULL)&&(strcmp(name,l->name)!=0))
			l=l->next;
		return l;
	}
	return NULL;

}
void st_lookup_including_parent(char*scope,char*name,BucketList b)
{
	int h=hash(scope);
	BucketList l;
	ScopeList s=hashTable_scope[h];
	if(s!=NULL)
	{
		h=hash(name);
		l=s->bucket[h];
		while((l!=NULL)&&(strcmp(name,l->name)!=0))
			l=l->next;
	}
	if(l==NULL)
	{
		h=hash("global");
		s=hashTable_scope[h];
		if(s==NULL) b=NULL;
		h=hash(name);
		l=s->bucket[h];
		while((l!=NULL)&&(strcmp(name,l->name)!=0))
			l=l->next;
		if(l==NULL) {b=NULL; return ;}
	}
	memcpy(b,l,sizeof(struct BucketListRec));
}

FuncList lookup_func(char*name,FuncList f)
{
	int h=hash(name);
	if(hashTable_Func[h]!=NULL)
		memcpy(f,hashTable_Func[h],sizeof(struct FuncListRec));
	return f;	

}


void printSymTab(FILE * listing)
{ 	int i;
	int j;
	fprintf(listing,"< Symbol Table>\n");
	fprintf(listing,"Variable Name  Variable Type  Scope name  Location   Line Numbers\n");
	fprintf(listing,"-------------  -------------  ----------  --------   ------------\n");

	for (i=0;i<SIZE;++i)
	{
		ScopeList s= hashTable_scope[i];
		if(s==NULL) continue;



			for(j=0;j<SIZE;++j)
			{
				BucketList l=s->bucket[j];
				if(l==NULL) continue;
			
				while(l!=NULL)
				{

				fprintf(listing,"%-14s ",l->name);
				fprintf(listing,"%-14s ",TypeList[l->type]);
				fprintf(listing,"%-11s ",s->scope);
				fprintf(listing,"%-9d  ",l->memloc);


				LineList t=l->lines;
				while(t!=NULL)
				{
					fprintf(listing,"%d ",t->lineno);
					t=t->next;
				}
				//	if(s->parent->scope!=NULL)
				//			fprintf(listing,"%-10s",s->parent->scope);
				fprintf(listing,"\n");
				l=l->next;
				}
			}
		}

	


	fprintf(listing,"\n< Function Table>\n");
	fprintf(listing,"Function Name  Return Type  Parameter Name  Parameter Type\n");
	fprintf(listing,"-------------  -----------  --------------  --------------\n");
	for(i=0;i<SIZE;++i)
	{
		FuncList s=hashTable_Func[i];
		if(s==NULL) continue;
		fprintf(listing,"%-14s ",s->name);
		fprintf(listing,"%-11s ",TypeList[s->type]);
		fprintf(listing,"\n");
		VarList l=s->arg;
		while(l!=NULL)
		{
			fprintf(listing,"                             ");
			fprintf(listing,"%-14s ",l->name);
			fprintf(listing,"%-14s ",TypeList[l->type]);		
			fprintf(listing,"\n");
			l=l->next;
		}
		
	}	
	fprintf(listing,"\n");		
}
/* printSymTab */

void reservedFunc()
{
	st_insert(NULL,"global","input",5,0,0,0);
	st_insert(NULL,"global","output",5,0,0,1);
	st_insert_func("input",Integer,1,NULL);
	st_insert_func("output",Void,1,NULL);
	st_insert_func("",Integer,0,"output");

}
