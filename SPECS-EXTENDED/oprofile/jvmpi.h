#include "jni.h"

#define JVMPI_VERSION_1 (jint)0x10000001
struct _jobjectID;
typedef struct _jobjectID *jobjectID;
struct _JVMPI_RawMonitor;
typedef struct _JVMPI_RawMonitor *JVMPI_RawMonitor;
typedef struct
{
  jint lineno;
  jmethodID method_id;
} JVMPI_CallFrame;
typedef struct
{
  JNIEnv *env_id;
  jint num_frames;
  JVMPI_CallFrame *frames;
} JVMPI_CallTrace;
typedef struct
{
  char *method_name;
  char *method_signature;
  jint start_lineno;
  jint end_lineno;
  jmethodID method_id;
} JVMPI_Method;
typedef struct
{
  char *field_name;
  char *field_signature;
} JVMPI_Field;
typedef struct
{
  jint offset;
  jint lineno;
} JVMPI_Lineno;
typedef struct
{
  jint event_type;
  JNIEnv *env_id;
  union
  {
    struct
    {
      const char *class_name;
      char *source_name;
      jint num_interfaces;
      jint num_methods;
      JVMPI_Method *methods;
      jint num_static_fields;
      JVMPI_Field *statics;
      jint num_instance_fields;
      JVMPI_Field *instances;
      jobjectID class_id;
    } class_load;
    struct
    {
      jmethodID method_id;
      void *code_addr;
      jint code_size;
      jint lineno_table_size;
      JVMPI_Lineno *lineno_table;
    } compiled_method_load;
  } u;
} JVMPI_Event;
typedef struct
{
  jint version;
  void (*NotifyEvent) (JVMPI_Event *);
  jint (*EnableEvent) (jint, void *);
  jint (*DisableEvent) (jint, void *);
  jint (*RequestEvent) (jint, void *);
  void (*GetCallTrace) (JVMPI_CallTrace *, jint);
  void (*ProfilerExit) (jint);
  JVMPI_RawMonitor (*RawMonitorCreate) (char *);
  void (*RawMonitorEnter) (JVMPI_RawMonitor);
  void (*RawMonitorExit) (JVMPI_RawMonitor);
  void (*RawMonitorWait) (JVMPI_RawMonitor, jlong);
  void (*RawMonitorNotifyAll) (JVMPI_RawMonitor);
  void (*RawMonitorDestroy) (JVMPI_RawMonitor);
  jlong (*GetCurrentThreadCpuTime) (void);
  void (*SuspendThread) (JNIEnv *);
  void (*ResumeThread) (JNIEnv *);
  jint (*GetThreadStatus) (JNIEnv *);
  jboolean (*ThreadHasRun) (JNIEnv *);
  jint (*CreateSystemThread) (char *, jint, void (*)(void *));
  void (*SetThreadLocalStorage) (JNIEnv *, void *);
  void *(*GetThreadLocalStorage) (JNIEnv *);
  void (*DisableGC) (void);
  void (*EnableGC) (void);
  void (*RunGC) (void);
  jobjectID (*GetThreadObject) (JNIEnv *);
  jobjectID (*GetMethodClass) (jmethodID);
  jobject (*jobjectID2jobject) (jobjectID);
  jobjectID (*jobject2jobjectID) (jobject);
  void (*SuspendThreadList) (jint, JNIEnv **, jint *);
  void (*ResumeThreadList) (jint, JNIEnv **, jint *);
} JVMPI_Interface;

#define JVMPI_EVENT_COMPILED_METHOD_LOAD 7
#define JVMPI_EVENT_COMPILED_METHOD_UNLOAD 8
#define JVMPI_EVENT_CLASS_LOAD 42
#define JVMPI_EVENT_CLASS_UNLOAD 43
#define JVMPI_EVENT_JVM_SHUT_DOWN 47
