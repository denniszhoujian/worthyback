/*
  returns the min_ratio of the values in a distribution
  input parameters:
  data (real)
  number of decimals in result (int, optional)
  output:
  min_ratio value of the distribution (real)
  registering the function:
  CREATE AGGREGATE FUNCTION min_ratio RETURNS REAL SONAME 'udf_min_ratio.so';
  getting rid of the function:
  DROP FUNCTION min_ratio;
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
#define MIN_DOUBLE 0.00001


extern "C" {
    my_bool min_ratio_init( UDF_INIT* initid, UDF_ARGS* args, char* message );
    void min_ratio_deinit( UDF_INIT* initid );
    void min_ratio_clear(UDF_INIT *initid, char *is_null, char *is_error);
    void min_ratio_reset( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char *error );
    void min_ratio_add( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char *error );
    double min_ratio( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char *error );
}


struct min_ratio_data
{
  unsigned long count;
  unsigned long abscount;
  unsigned long pages;
  double *values;
};


my_bool min_ratio_init( UDF_INIT* initid, UDF_ARGS* args, char* message )
{
  if (args->arg_count < 1 || args->arg_count>2)
  {
    strcpy(message,"wrong number of arguments: min_ratio() requires one or two arguments");
    return 1;
  }

  if (args->arg_type[0]!=REAL_RESULT)
  {
    args->arg_type[0] = REAL_RESULT;
  }

  if (args->arg_count>1 && (args->arg_type[1]!=INT_RESULT))
  {
    strcpy(message,"min_ratio() requires an int as parameter 2");
    return 1;
  }

  initid->decimals=2;
  if (args->arg_count==2 && (*((ulong*)args->args[1])<=16))
  {
    initid->decimals=*((ulong*)args->args[1]);
  }

  min_ratio_data *buffer = new min_ratio_data;
  buffer->count = 0;
  buffer->abscount=0;
  buffer->pages = 1;
  buffer->values = NULL;

  initid->maybe_null  = 1;
  initid->max_length  = 32;
  initid->ptr = (char*)buffer;

  return 0;
}


void min_ratio_deinit( UDF_INIT* initid )
{
  min_ratio_data *buffer = (min_ratio_data*)initid->ptr;

  if (buffer->values != NULL)
  {
    free(buffer->values);
    buffer->values=NULL;
  }
  delete initid->ptr;
}


void min_ratio_clear(UDF_INIT *initid, char *is_null, char *is_error)
{
  min_ratio_data *buffer = (min_ratio_data*)initid->ptr;
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

void min_ratio_reset( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char* is_error )
{
  min_ratio_clear(initid, is_null, is_error);
  min_ratio_add( initid, args, is_null, is_error );
}


void min_ratio_add( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char* is_error )
{
  if (args->args[0]!=NULL)
  {
    min_ratio_data *buffer = (min_ratio_data*)initid->ptr;
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



int compare_doubles (const void *a, const void *b)
{
  const double *da = (const double *) a;
  const double *db = (const double *) b;

  return (*da < *db) - (*da > *db);
}

int is_double_equal (const double a, const double b) {
    double diff = a - b;
    if (diff < 0) diff = 0.0 - diff;
    if (diff < MIN_DOUBLE)
        return 1;
    else return 0;
}

double get_min_val(const void* a, int size) {
    const double *da = (const double *) a;
    double min_val = da[0];
    for (int i=0;i<size;i++) if (da[i] < min_val) min_val = da[i];
    return min_val;
}


double min_ratio( UDF_INIT* initid, UDF_ARGS* args, char* is_null, char* is_error )
{
  min_ratio_data* buffer = (min_ratio_data*)initid->ptr;

  if (buffer->abscount==0 || *is_error!=0)
  {
    *is_null = 1;
    return 0.0;
  }

  *is_null=0;
  if (buffer->abscount==1)
  {
    return 1.0;
  }

  //qsort(buffer->values,buffer->abscount,sizeof(double),compare_doubles);


    //double min_val = buffer->values[0]
    double min_val = get_min_val(buffer->values,buffer->abscount);
    int min_count = 0;
    for (int i=0;i<buffer->abscount;i++)
        if (is_double_equal(min_val, buffer->values[i])) min_count ++;

  return (1.0f*min_count)/(1.0f*buffer->abscount);
}

#endif


