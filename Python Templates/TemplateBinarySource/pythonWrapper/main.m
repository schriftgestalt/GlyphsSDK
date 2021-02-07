//
//  main.m
//  apptemplate
//
//  Created by Bob Ippolito on Mon September 20 2004.
//  Copyright (c) 2004 Bob Ippolito. All rights reserved.
//

#import <Foundation/Foundation.h>
#include <crt_externs.h>
#include <langinfo.h>
#include <locale.h>
#include <mach-o/dyld.h>
#include <mach-o/loader.h>
#include <sys/stat.h>
#include <sys/syslimits.h>
#include <sys/types.h>
#include <wchar.h>

#include <objc/objc-class.h>
#include <Python/Python.h>
#import "dlfcn.h"
//
// Constants
//
NSString *ERR_CANNOT_SAVE_LOCALE = @"Cannot save locale information";
NSString *ERR_REALLYBADTITLE = @"The bundle could not be launched.";
NSString *ERR_TITLEFORMAT = @"%@ has encountered a fatal error, and will now terminate.";
NSString *ERR_PYRUNTIME = @"Couldn’t find python runtime";
//NSString *ERR_PYRUNTIMELOCATIONS = @"The Info.plist file must have a PyRuntimeLocations array containing string values for preferred Python runtime locations.  These strings should be \"otool -L\" style mach ids; \"@executable_stub\" and \"~\" prefixes will be translated accordingly.";
//NSString *ERR_NOPYTHONRUNTIME = @"A Python runtime could be located.  You may need to install a framework build of Python, or edit the PyRuntimeLocations array in this bundle's Info.plist file.\rThese runtime locations were attempted:\r\r";
NSString *ERR_NOPYTHONSCRIPT = @"A main script could not be located in the Resources folder.\rThese files were tried:\r\r";
NSString *ERR_LINKERRFMT = @"An internal error occurred while attempting to link with:\r\r%s\r\rSee the Console for a detailed dyld error message";
NSString *ERR_PYTHONEXCEPTION = @"An uncaught exception was raised during execution of the main script:\n\n%@: %@"; // \r\rThis may mean that an unexpected error has occurred, or that you do not have all of the dependencies for this bundle.";

//
// Typedefs
//

@interface NSObject (Python)
- (PyObject *)pyObject;
@end

PyGILState_STATE (*PyGILState_EnsurePtr)(void);
void (*PyGILState_ReleasePtr)(PyGILState_STATE);

#ifdef DEBUG
int (*gsPyObject_Print)(PyObject *o, FILE *fp, int flags);
PyObject* (*gsPyObject_Type)(PyObject *o);

int _pyo(PyObject *object);
int _pyo(PyObject *object) {
	if (gsPyObject_Print) {
		PyGILState_STATE gilState = (*PyGILState_EnsurePtr)();
		int result = (*gsPyObject_Print)(object, stdout, 0);
		(*PyGILState_ReleasePtr)(gilState);
		return result;
	}
	else {
		NSLog(@"lib not loaded yet");
	}
	return -2;
}

int _pyType(PyObject *object);
int _pyType(PyObject *object) {
	if (gsPyObject_Type) {
		PyObject *typeObject = (*gsPyObject_Type)(object);
		_pyo(typeObject);
		return 0;
	}
	NSLog(@"lib not loaded yet");
	return -1;
}
#endif

#define Py_file_input 257

PyThreadState *(*PyThreadState_SwapPtr)(PyThreadState *);
void (*PyEval_ReleaseLockPtr)(void);
void (*PyErr_ClearPtr)(void);
void (*PyErr_PrintPtr)(void);
int (*PyErr_OccurredPtr)(void);

PyObject *(*PyBytes_FromStringPtr)(const char *);
PyObject *(*PyString_FromStringPtr)(const char *);
const char *(*PyBytes_AsStringPtr)(PyObject *);
const char *(*PyString_AsStringPtr)(PyObject *);

PyObject *(*PyString_JoinPtr)(PyObject *separator, PyObject *seq);
int (*PyList_InsertPtr)(PyObject *, int, PyObject *);
void (*Py_DecRefPtr)(PyObject *);
int (*Py_IsInitializedPtr)(void);
void (*Py_InitializePtr)(void);
void (*PyEval_InitThreadsPtr)(void);
PyObject *(*PyRun_FilePtr)(FILE *, const char *, int, PyObject *, PyObject *);
PyObject *(*PySys_GetObjectPtr)(const char *);
int *(*PySys_SetArgvPtr)(int argc, char **argv);
PyObject *(*PyObject_StrPtr)(PyObject *);

PyObject *(*PyObject_GetAttrStringPtr)(PyObject *, const char *);
PyObject *(*PyObject_CallMethodPtr)(PyObject *, const char *, const char *, ...);
PyObject *(*PyImport_ImportModulePtr)(char *);
PyObject *(*PyImport_AddModulePtr)(char *);
PyObject *(*PyModule_AddStringConstantPtr)(PyObject *, char *, char *);
PyObject *(*PyModule_AddObjectPtr)(PyObject *, char *, PyObject *);
PyObject *(*PyModule_GetDictPtr)(PyObject *);
void (*PyObject_SetItemPtr)(PyObject *, PyObject *, PyObject *);
void (*PyErr_NormalizeExceptionPtr)(PyObject**exc, PyObject**val, PyObject**tb);
int (*depythonify_c_valuePtr)(const char* type, PyObject* arg, void* datum);


void (*PyErr_FetchPtr)(PyObject **ptype, PyObject **pvalue, PyObject **ptraceback);

PyObject* (*gsPyObject_Repr)(PyObject *o);

//typedef wchar_t *(*_Py_DecodeUTF8_surrogateescapePtr)(const char *s, ssize_t size);

//
// Signatures
//

//static void DefaultDecRef(PyObject *op);

static int report_error(NSString *err, NSString *errName);

static int report_linkEdit_error(const char *name);
static NSString *getBundleName(void);
static NSString *getErrorTitle(NSString *bundleName);
static const char *bundlePath(void);
static NSBundle *bundleBundle(void);
static int pyobjc_main(int argc, char *const *argv, char *const *envp);

//
// Mach-O Constructor
//

static void __attribute__((constructor)) _py2app_bundle_load(void);

@interface OC_PythonObject : NSObject
- (instancetype)initWithPyObject:(PyObject *)pyObject;
@end

//
// Implementation
//

static const char *bundlePath(void) {
	int i;
	const struct mach_header *myHeader = _dyld_get_image_header_containing_address(&bundlePath);
	int count = _dyld_image_count();
	for (i = 0; i < count; i++) {
		if (_dyld_get_image_header(i) == myHeader) {
			return _dyld_get_image_name(i);
		}
	}
	abort();
	return NULL;
}

static NSBundle *bundleBundle(void) {
	static NSBundle *myBundle = NULL;
	if (!myBundle) {
		int i;
		NSString *path = [NSString stringWithUTF8String:bundlePath()];
		// strip Contents/MacOS/App
		for (i = 0; i < 3; i++) {
			path = [path stringByDeletingLastPathComponent];
		}
		myBundle = [[NSBundle alloc] initWithPath:path];
	}
	return myBundle;
}

static int report_error(NSString *err, NSString *errName) {
	NSLog(@"%@", getErrorTitle(getBundleName()));
	NSLog(@"%@", err);
	[[NSNotificationCenter defaultCenter] postNotificationName:@"RemotePythonError" object:nil userInfo:@{@"errorMessage": err, @"exceptionName": errName}];
	return -1;
}

static int report_linkEdit_error(const char *name) {
//	NSLog(@"Couldn’t find python library: %s", name);
//	NSLinkEditErrors errorClass;
//	int errorNumber;
//	const char *fileName;
//	const char *errorString;
//	NSLinkEditError(&errorClass, &errorNumber, &fileName, &errorString);
//	NSLog(@"%s: %s", name, errorString);
//	printf("<<<py2app>>>> %s: %s\n", name, errorString);
	return report_error([NSString stringWithFormat:ERR_LINKERRFMT, name], @"LinkError");
}

static NSString *getBundleName(void) {
	NSDictionary *infoDictionary = [bundleBundle() infoDictionary];
	NSString *bundleName = [infoDictionary objectForKey:@"CFBundleName"];
	if (!bundleName) {
		bundleName = [infoDictionary objectForKey:@"CFBundleExecutable"];
	}
	return bundleName;
}

static NSString *getErrorTitle(NSString *bundleName) {
	if (!bundleName) {
		return ERR_REALLYBADTITLE;
	}
	return [NSString stringWithFormat:ERR_TITLEFORMAT, bundleName];
}

static NSArray *getPythonPathArray(NSDictionary *infoDictionary, NSString *resourcePath) {
	NSMutableArray *pythonPathArray = [NSMutableArray arrayWithObject:resourcePath];
	NSArray *pyResourcePackages = [infoDictionary objectForKey:@"PyResourcePackages"];
	if (pyResourcePackages != nil) {
		NSString *pkg;
		NSEnumerator *pyResourcePackageEnumerator = [pyResourcePackages objectEnumerator];
		while ((pkg = [pyResourcePackageEnumerator nextObject])) {
			pkg = [pkg stringByExpandingTildeInPath];
			if (![@"/" isEqualToString:[pkg substringToIndex:1]]) {
				pkg = [resourcePath stringByAppendingPathComponent:pkg];
			}
			[pythonPathArray addObject:pkg];
		}
	}
	return pythonPathArray;
}

static NSString *getMainPyPath(NSDictionary *infoDictionary) {
	NSArray *possibleMains = [infoDictionary objectForKey:@"PyMainFileNames"];

	if (!possibleMains) {
		// find main python file.  __main__.py seems to be a standard, so we'll go ahead and add defaults.
		possibleMains = [NSArray arrayWithObjects:
									 @"plugin.py",
									 @"plugin.pyc",
									 //			@"__main__",
									 //			@"__realmain__",
									 //			@"Main",
									 nil];
	}
	NSEnumerator *possibleMainsEnumerator = [possibleMains objectEnumerator];
	NSString *mainPyPath = nil;
	NSString *nextFileName = nil;
	NSBundle *bundle = bundleBundle();
	while ((nextFileName = [possibleMainsEnumerator nextObject]) && !mainPyPath) {
		mainPyPath = [bundle pathForResource:nextFileName ofType:nil];
	}
	if (!mainPyPath) {
		NSString *components = [possibleMains componentsJoinedByString:@"\r"];
		if (components.length == 0) {
			components = [NSString stringWithFormat:@"!mainPyPath (%@)", bundle.bundlePath];
		}
		report_error([ERR_NOPYTHONSCRIPT stringByAppendingString:components], @"NoPythonScriptError");
	}
	return mainPyPath;
}

bool getErrorValueAndTraceback(PyObject **exc_type, PyObject **exc_value, PyObject **exc_traceback);

int loadSymbols(void *py_dylib, bool *isPy3k, char **curlocale, char **curenv);
int loadSymbols(void *py_dylib, bool *isPy3k, char **curlocale, char **curenv) {
	// Load the symbols we need from Python.
	Py_DecRefPtr = dlsym(py_dylib, "Py_DecRef");
	Py_IsInitializedPtr = dlsym(py_dylib, "Py_IsInitialized");
	Py_InitializePtr = dlsym(py_dylib, "Py_Initialize");
	PyErr_ClearPtr = dlsym(py_dylib, "PyErr_Clear");
	PyErr_PrintPtr = dlsym(py_dylib, "PyErr_Print");
	PyErr_OccurredPtr = dlsym(py_dylib, "PyErr_Occurred");
	PyEval_ReleaseLockPtr = dlsym(py_dylib, "PyEval_ReleaseLock");
	PyGILState_EnsurePtr = dlsym(py_dylib, "PyGILState_Ensure");
	PyGILState_ReleasePtr = dlsym(py_dylib, "PyGILState_Release");
	PyEval_InitThreadsPtr = dlsym(py_dylib, "PyEval_InitThreads");
	PyRun_FilePtr = dlsym(py_dylib, "PyRun_File");
	PySys_GetObjectPtr = dlsym(py_dylib, "PySys_GetObject");
	PySys_SetArgvPtr = dlsym(py_dylib, "PySys_SetArgv");
	PyObject_StrPtr = dlsym(py_dylib, "PyObject_Str");
	PyList_InsertPtr = dlsym(py_dylib, "PyList_Insert");
	PyObject_GetAttrStringPtr = dlsym(py_dylib, "PyObject_GetAttrString");
	PyObject_CallMethodPtr = dlsym(py_dylib, "PyObject_CallMethod");
	PyImport_ImportModulePtr = dlsym(py_dylib, "PyImport_ImportModule");
	PyImport_AddModulePtr = dlsym(py_dylib, "PyImport_AddModule");
	PyObject_SetItemPtr = dlsym(py_dylib, "PyObject_SetItem");
	PyModule_AddStringConstantPtr = dlsym(py_dylib, "PyModule_AddStringConstant");
	PyModule_AddObjectPtr = dlsym(py_dylib, "PyModule_AddObject");
	PyModule_GetDictPtr = dlsym(py_dylib, "PyModule_GetDict");
	PyThreadState_SwapPtr = dlsym(py_dylib, "PyThreadState_Swap");
	PyErr_NormalizeExceptionPtr = dlsym(py_dylib, "PyErr_NormalizeException");
	PyErr_FetchPtr = dlsym(py_dylib, "PyErr_Fetch");

	depythonify_c_valuePtr = dlsym(py_dylib, "depythonify_c_value");
	
	/* PyBytes / PyString lookups depend of if we're on py3k or not */
	PyBytes_AsStringPtr = dlsym(py_dylib, "PyBytes_AsString");
	PyBytes_FromStringPtr = dlsym(py_dylib, "PyBytes_FromString");
	*isPy3k = PyBytes_AsStringPtr != NULL;
	if (!*isPy3k) {
		PyBytes_AsStringPtr = dlsym(py_dylib, "PyString_AsString");
		PyBytes_FromStringPtr = dlsym(py_dylib, "PyString_FromString");
	}
	PyString_FromStringPtr = dlsym(py_dylib, "PyUnicode_FromString");
	if (!PyString_FromStringPtr) {
		PyString_FromStringPtr = dlsym(py_dylib, "PyString_FromString");
	}
	PyString_AsStringPtr = dlsym(py_dylib, "PyString_AsString");
	if (!PyString_AsStringPtr) {
		PyString_AsStringPtr = dlsym(py_dylib, "PyUnicode_AsUTF8");
	}
	
	PyString_JoinPtr = dlsym(py_dylib, "PyUnicode_Join");
	if (!PyString_JoinPtr) {
		PyString_JoinPtr = dlsym(py_dylib, "PyUnicodeUCS2_Join");
	}
	
	gsPyObject_Repr = dlsym(py_dylib, "PyObject_Repr");
	
#ifdef DEBUG
	gsPyObject_Print = dlsym(py_dylib, "PyObject_Print");
	gsPyObject_Type = dlsym(py_dylib, "PyObject_Type");
#endif
	
	/*
	 * When apps are started from the Finder (or anywhere
	 * except from the terminal), the LANG and LC_* variables
	 * aren't set in the environment. This confuses Py_Initialize
	 * when it tries to import the codec for UTF-8,
	 * therefore explicitly set the locale.
	 *
	 * Also set the LC_CTYPE environment variable because Py_Initialize
	 * reset the locale information using the environment :-(
	 */
	if (*isPy3k) {
		*curlocale = setlocale(LC_ALL, NULL);
		if (*curlocale != NULL) {
			*curlocale = strdup(*curlocale);
			if (*curlocale == NULL) {
				report_error(ERR_CANNOT_SAVE_LOCALE, @"CannotSaveLocaleError");
				return -1;
			}
		}
		setlocale(LC_ALL, "en_US.UTF-8");

		*curenv = getenv("LC_CTYPE");
		if (!*curenv) {
			setenv("LC_CTYPE", "en_US.UTF-8", 1);
		}
	}
	return 0;
}

int pyobjc_main(int argc, char *const *argv, char *const *envp) {
	
	
	if (getenv("PYTHONOPTIMIZE") != NULL) {
		unsetenv("PYTHONOPTIMIZE");
	}
	if (getenv("PYTHONDEBUG") != NULL) {
		unsetenv("PYTHONDEBUG");
	}
	if (getenv("PYTHONDONTWRITEBYTECODE") != NULL) {
		unsetenv("PYTHONDONTWRITEBYTECODE");
	}
	if (getenv("PYTHONIOENCODING") != NULL) {
		unsetenv("PYTHONIOENCODING");
	}
	setenv("PYTHONIOENCODING", "UTF-8", 1);
	if (getenv("PYTHONDUMPREFS") != NULL) {
		unsetenv("PYTHONDUMPREFS");
	}
	if (getenv("PYTHONMALLOCSTATS") != NULL) {
		unsetenv("PYTHONMALLOCSTATS");
	}

	/* Disable writing of bytecode files */
	setenv("PYTHONDONTWRITEBYTECODE", "1", 1);
	NSDictionary *infoDictionary = [bundleBundle() infoDictionary];

	NSString *pyLocation = nil;
	while (NSIsSymbolNameDefined("_Py_Initialize")) {
		// Python is already in-process
		NSSymbol sym = NSLookupAndBindSymbol("_Py_Initialize");
		if (!sym) {
			break;
		}
		NSModule mod = NSModuleForSymbol(sym);
		if (!mod) {
			break;
		}
		const char *python_dylib_path = NSLibraryNameForModule(mod);
		if (python_dylib_path) {
			pyLocation = [NSString stringWithUTF8String:python_dylib_path];
		}
		break;
	}

	if (!pyLocation) {
		return report_error(ERR_PYRUNTIME, @"ERR_PYRUNTIME");
	}
	// Find our resource path and possible PYTHONPATH
	NSString *resourcePath = [bundleBundle() resourcePath];
	NSArray *pythonPathArray = getPythonPathArray(infoDictionary, resourcePath);

	// find the main script
	NSString *mainPyPath = getMainPyPath(infoDictionary);
	if (!mainPyPath) {
		// error already reported
		return -1;
	}

	// Load the Python dylib (may have already been loaded, that is OK)
	void *py_dylib = dlopen([pyLocation fileSystemRepresentation], RTLD_LAZY);
	if (!py_dylib) {
		return report_linkEdit_error([pyLocation fileSystemRepresentation]);
	}
	bool isPy3k = false;
	char *curlocale = nil;
	char *curenv = nil;

	loadSymbols(py_dylib, &isPy3k, &curlocale, &curenv);
	
	int was_initialized = (*Py_IsInitializedPtr)();

	int rval = 0;
	FILE *mainPyFile = NULL;
	(*Py_InitializePtr)();
	//(*PyEval_InitThreadsPtr)();

	if (isPy3k) {
		/*
		 * Reset the environment and locale information
		 */
		setlocale(LC_CTYPE, curlocale);
		free(curlocale);

		if (!curenv) {
			unsetenv("LC_CTYPE");
		}
	}

	PyGILState_STATE gilState = (*PyGILState_EnsurePtr)();

	if (was_initialized) {
		// transfer path into existing Python process
		PyObject *path = (*PySys_GetObjectPtr)("path");
		NSEnumerator *pathEnumerator = [pythonPathArray reverseObjectEnumerator];
		NSString *curPath;
		while ((curPath = [pathEnumerator nextObject])) {
			PyObject *b = (*PyBytes_FromStringPtr)([curPath UTF8String]);
			PyObject *s = (*PyObject_CallMethodPtr)(b, "decode", "s", "utf-8");
			(*PyList_InsertPtr)(path, 0, s);
			(*Py_DecRefPtr)(b);
			(*Py_DecRefPtr)(s);
		}
	}

	char *c_mainPyPath = (char *)[mainPyPath fileSystemRepresentation];
	mainPyFile = fopen(c_mainPyPath, "r");
	PyObject *module = NULL;
	if (!mainPyFile) {
		rval = report_error([NSString stringWithFormat:@"Could not open main script %@", mainPyPath], @"NoMainPyFile");
		goto cleanup;
	}
	if (!was_initialized) {
		rval = report_error([NSString stringWithFormat:@"!was_initialized"], @"PythonNotInitialized");
		goto cleanup;
	}
	// create a unique moduleName by CFBundleIdentifier replacing . with _ and prepending __main__
	NSString *moduleName = [NSString stringWithFormat:@"__main__%@", [[[infoDictionary objectForKey:@"CFBundleIdentifier"] componentsSeparatedByString:@"."] componentsJoinedByString:@"_"]];
	module = (*PyImport_AddModulePtr)((char *)[moduleName UTF8String]);
	if (!module) {
		rval = report_error([NSString stringWithFormat:@"Could not create module '%@'", moduleName], @"CouldNotCreateModule");
		goto cleanup;
	}
	(*PyModule_AddStringConstantPtr)(module, "__file__", c_mainPyPath);
	char *builtinsName = isPy3k ? "builtins" : "__builtin__";
	PyObject *builtins = (*PyImport_ImportModulePtr)(builtinsName);
	(*PyModule_AddObjectPtr)(module, "__builtins__", builtins);
	PyObject *module_dict = (*PyModule_GetDictPtr)(module);
	if ((*PyErr_OccurredPtr)()) {
		goto cleanup;
	}
	PyObject *res = (*PyRun_FilePtr)(mainPyFile, c_mainPyPath, Py_file_input, module_dict, module_dict);
	if (res) {
		(*Py_DecRefPtr)(res);
	}
cleanup:
	if (mainPyFile) {
		fclose(mainPyFile);
	}
	if ((*PyErr_OccurredPtr)()) {
		rval = -1;
		//(*PyErr_PrintPtr)();
	}
	while (rval) {
#ifdef DEBUG
		//printError();
#endif
		PyObject *type = NULL;
		PyObject *value = NULL;
		PyObject *traceback = NULL;
		if (!getErrorValueAndTraceback(&type, &value, &traceback)) {
			return NO;
		}

		PyObject *mod = (*PyImport_ImportModulePtr)("traceback");
		if (!mod) {
			/* print some error */
			return YES;
		}
		PyObject *list = nil;
		if (traceback) {
			list = (*PyObject_CallMethodPtr)(mod, "format_exception", "OOO", type, value, traceback);
		}
		else {
			list = (*PyObject_CallMethodPtr)(mod, "format_exception_only", "OO", type, value);
		}
		PyObject *string = (*PyString_FromStringPtr)("\n");
		PyObject *ret = (*PyString_JoinPtr)(string, list);
		if (!ret) {
#ifdef DEBUG_
			//printError();
			id _obj = [[_OC_PythonObject alloc] initWithPyObject:list];
			NSString *_string = [_obj description];
			[_obj release];
			_string = [_string stringByReplacingOccurrencesOfString:@"\\n', " withString:@"\n"];
			_string = [_string stringByReplacingOccurrencesOfString:@"\\n" withString:@"\n"];
			NSLog(@"!!%@", _string);
#endif
		}
		else {
			NSString *errorName = @"UnknownError";
			if (value) {
				PyObject *reprObject = (*gsPyObject_Repr)(value);
				if (reprObject) {
					const char *s = (*PyString_AsStringPtr)(reprObject);
					errorName = [NSString stringWithCString:s encoding:NSUTF8StringEncoding];
				}
			}
			const char *s = (*PyString_AsStringPtr)(ret);
			NSString *reason = [NSString stringWithCString:s encoding:NSUTF8StringEncoding];
			report_error(reason, errorName);
		}
		if (list) {
			Py_DECREF(list);
		}
		if (string) {
			Py_DECREF(string);
		}
		if (type) {
			Py_DECREF(type);
		}
		if (value) {
			Py_DECREF(value);
		}
		if (traceback) {
			Py_DECREF(traceback);
		}
		break;
	}
	(*PyErr_ClearPtr)();
	(*PyGILState_ReleasePtr)(gilState);
//	if (gilState == PyGILState_LOCKED) {
//		(*PyThreadState_SwapPtr)(NULL);
//		(*PyEval_ReleaseLockPtr)();
//	}
	return rval;
}

bool getErrorValueAndTraceback(PyObject **exc_type, PyObject **exc_value, PyObject **exc_traceback) {

	(*PyErr_FetchPtr)(exc_type, exc_value, exc_traceback);
	if (exc_type == NULL) {
		return NO;
	}
	(*PyErr_NormalizeExceptionPtr)(exc_type, exc_value, exc_traceback);
	(*PyErr_ClearPtr)();
	
	return true;
}

static void _py2app_bundle_load(void) {
	NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
	int argc = 1;
	char *const argv[] = {(char *)bundlePath(), NULL};
	char *const *envp = *_NSGetEnviron();
	(void)pyobjc_main(argc, argv, envp);
	[pool release];
}
