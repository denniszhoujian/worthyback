/*
  returns the LPDR of the values in a distribution
  input parameters:
  data (real)
  number of decimals in result (int, optional)
  output:
  LPDR value of the distribution (real)
  registering the function:
  CREATE AGGREGATE FUNCTION LPDR RETURNS REAL SONAME 'udf_LPDR.so';
  getting rid of the function:
  DROP FUNCTION LPDR;
*/


#ifdef STANDARD
#include <stdio.h>
#include <string.h>
#ifdef __WIN__
typedef unsigned __int64 ulonglong;
typedef __int64 longlong;
#else
typedef unsigned long long ulonglong;
typedef long long longlong;
#endif /*__WIN__*/
#else
#include <my_global.h>
#include <my_sys.h>
#endif
#include <mysql.h>
#include <m_ctype.h>
#include <m_string.h>

#ifdef HAVE_DLOPEN


#define BUFFERSIZE 1024



extern "C" {
my_bool LPDR_init( UDF_INIT* initid, UDF_ARGS* args, char* message );
void LPDR_deinit( UDF_INIT* initid );
void LPDR_clear(UDF_INIT *initid, char *is_null, char *is_error);
void LPDR_reset( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char *error );
void LPDR_add( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char *error );
double LPDR( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char *error );
}


struct LPDR_data
{
  unsigned long count;
  unsigned long abscount;
  unsigned long pages;
  double *values;
};


my_bool LPDR_init( UDF_INIT* initid, UDF_ARGS* args, char* message )
{
  if (args->arg_count < 1 || args->arg_count>2)
  {
    strcpy(message,"wrong number of arguments: LPDR() requires one or two arguments");
    return 1;
  }

  if (args->arg_type[0]!=REAL_RESULT)
  {
    args->arg_type[0] = REAL_RESULT;
  }

  if (args->arg_count>1 && (args->arg_type[1]!=INT_RESULT))
  {
    strcpy(message,"LPDR() requires an int as parameter 2");
    return 1;
  }

  initid->decimals=2;
  if (args->arg_count==2 && (*((ulong*)args->args[1])<=16))
  {
    initid->decimals=*((ulong*)args->args[1]);
  }

  LPDR_data *buffer = new LPDR_data;
  buffer->count = 0;
  buffer->abscount=0;
  buffer->pages = 1;
  buffer->values = NULL;

  initid->maybe_null  = 1;
  initid->max_length  = 32;
  initid->ptr = (char*)buffer;

  return 0;
}


void LPDR_deinit( UDF_INIT* initid )
{
  LPDR_data *buffer = (LPDR_data*)initid->ptr;

  if (buffer->values != NULL)
  {
    free(buffer->values);
    buffer->values=NULL;
  }
  delete initid->ptr;
}


void LPDR_clear(UDF_INIT *initid, char *is_null, char *is_error)
{
  LPDR_data *buffer = (LPDR_data*)initid->ptr;
  buffer->count = 0;
  buffer->abscount=0;
  buffer->pages = 1;
  *is_null = 0;
  *is_error = 0;

  if (buffer->values != NULL)
  {
    free(buffer->values);
    buffer->values=NULL;
  }

  buffer->values=(double *) malloc(BUFFERSIZE*sizeof(double));
}

void LPDR_reset( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char* is_error )
{
  LPDR_clear(initid, is_null, is_error);
  LPDR_add( initid, args, is_null, is_error );
}


void LPDR_add( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char* is_error )
{
  if (args->args[0]!=NULL)
  {
    LPDR_data *buffer = (LPDR_data*)initid->ptr;
    if (buffer->count>=BUFFERSIZE)
    {
      buffer->pages++;
      buffer->count=0;
      buffer->values=(double *) realloc(buffer->values,BUFFERSIZE*buffer->pages*sizeof(double));
    }
    buffer->values[buffer->abscount++] = *((double*)args->args[0]);
    buffer->count++;
  }
}



int
compare_doubles (const void *a, const void *b)
{
  const double *da = (const double *) a;
  const double *db = (const double *) b;
  return (*da > *db) - (*da < *db);
}


double LPDR( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char* is_error )
{
  LPDR_data* buffer = (LPDR_data*)initid->ptr;

  if (buffer->abscount==0 || *is_error!=0)
  {
    *is_null = 1;
    return 0.0;
  }

  *is_null=0;
  if (buffer->abscount==1)
  {
    return buffer->values[0];
  }

  qsort(buffer->values,buffer->abscount,sizeof(double),compare_doubles);

  double min_val = buffer->values[0];
  double low_10percentile_price = buffer->values[buffer->abscount/10];
  double diff = low_10percentile_price - min_val;
  double ratio = diff / min_val;
  return ratio;
}

#endif


