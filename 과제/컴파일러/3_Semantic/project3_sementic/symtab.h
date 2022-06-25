/****************************************************/
/* File: symtab.h                                   */
/* Symbol table interface for the TINY compiler     */
/* (allows only one symbol table)                   */
/* Compiler Construction: Principles and Practice   */
/* Kenneth C. Louden                                */
/****************************************************/

#ifndef _SYMTAB_H_
#define _SYMTAB_H_
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symtab.h"
#include "globals.h"

#define SIZE 211
/* Procedure st_insert inserts line numbers and
 * memory locations into the symbol table
 * loc = memory location is inserted only the
 * first time, otherwise ignored
 */
//void st_insert( char * name, int lineno, int loc );


/* Function st_lookup returns the memory 
 * location of a variable or -1 if not found
 */
/* Procedure printSymTab prints a formatted 
 * listing of the symbol table contents 
 * to the listing file
 */
typedef struct LineListRec
{ int lineno;
	struct LineListRec * next;
} * LineList;


void printSymTab(FILE * listing);
typedef struct VarListRec
{
	char name[20];
	ExpType type;
	struct VarListRec* next;
}*VarList;

typedef struct FuncListRec
{ char  name[20];
	ExpType type;
	VarList arg;
	int argCnt;
	struct FuncListRec * next;
}*FuncList;
typedef struct BucketListRec
{ char  name[20];
	ExpType type;
	int nested_level;
	LineList lines;
	char scope[20];
	int memloc ; /* memory location for variable */
	struct BucketListRec * next;
}*BucketList;
typedef struct ScopeListRec
{
	char scope[20];
	BucketList bucket[SIZE];
	struct ScopeListRec *parent;
}*ScopeList;




#endif
