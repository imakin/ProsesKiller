/**
 * @file common.h
 * @author Izzulmakin 2016-05-10
 * provide commonly used api
 */

#ifndef __COMMON_H__
#define __COMMON_H__

#include <Windows.h>
#include "../lib/AutoIt3.h"
#include <stdint.h>
#include <stdio.h>

typedef LPCWSTR lpcwstr;

/** allstop flag, if 1 then must go idle */
extern uint8_t all_stop;

typedef struct linkedlist_st linkedlist;
struct linkedlist_st {
	long data1;
	long data2;
	long data3;
	long data4;
	linkedlist *next;
	linkedlist **multinext;
	linkedlist *prev;
};


/** where the result saved */
extern uint32_t *pixelsearch_result;

/** flag valued 1 if a thread is currently updating pixelsearch_result */
extern uint8_t pixelsearch_result_lock;

/** how much has found / in what index the latest pixelsearch_result is saved */
extern uint8_t pixelsearch_result_num;

/** on each pixelsearch sweep, how many pixel skipped? 
 * 	for faster performance default 5 */
extern uint8_t pixelsearch_skip;

/** this variable specify the state of hdc: 
 * <ul>
 * 	<li> not ready: value 0 </li>
 * 	<li> currently initiated: value 1 </li>
 * 	<li> ready to use: value 2 </li>
 * </ul>
 */
extern uint8_t pixelsearch_hdc_ready;

extern FARPROC pGetPixel;
extern HINSTANCE hGDI;
extern HDC hdc;


/**
 * pixel search color for threading
 * @see pixelsearch_param
 * @param param is a pointer to a set of 5 datas, comprises:
 * 	- 	4 long* starts from index 0 to 3 is x1,y1,x2,y2 which represent 
 * 		the rectangle area to search.
 * 	-	index 4 is the function pointer to the test of the color 
 * 		will be called like test_color(color_value) and shall 
 * 		return 1 for true, 0 for false
 */ 
void pixelsearch(void *param);


/**
 * create a param named "name" to be used in pixelsearch
 * @see pixelsearch_result
 * @param name the name of the param variable
 * @param thread_id is the ID of the thread using this param 
 * @param x1 the area to search rectangle x1
 * @param y1 the area to search rectangle y1
 * @param x2 the area to search rectangle x2
 * @param y2 the area to search rectangle y2
 * @param test_color the pointer to method for the color test to search
 * 		this might be defined in uint8_t test_methodname(long color)
 * 		and must return 1 if color match desired color, or return 0 if not
 */
#define pixelsearch_param(name, thread_id, x1,y1, x2,y2, test_color) \
	uint32_t *name; \
	name = malloc(7*sizeof(uint32_t)); \
	name[0] = thread_id; \
	name[1] = x1; \
	name[2] = y1; \
	name[3] = x2; \
	name[4] = y2; \
	name[6] = test_color;

/**
 * call pixelsearch_param then _beginthread with pixelsearch method
 * @see pixelsearch_param
 * @see pixelsearch
 * @param name unique name of this thread
 * @param thread_id is the unique ID of this thread
 * @param x1 the area to search rectangle x1
 * @param y1 the area to search rectangle y1
 * @param x2 the area to search rectangle x2
 * @param y2 the area to search rectangle y2
 * @param test_color the pointer to method for the color test to search
 * 		this might be defined in uint8_t test_methodname(long color)
 * 		and must return 1 if color match desired color, or return 0 if not
 */
#define pixelsearch_thread(name, thread_id, x1,y1, x2,y2, test_color) \
	pixelsearch_param(name, thread_id, x1,y1, x2,y2, test_color); \
	_beginthread(pixelsearch, 0, (void*)name);


/**
 * call pixelsearch_param then execute pixelsearch w/o threading
 * @see pixelsearch_param
 * @see pixelsearch
 * @param x1 the area to search rectangle x1
 * @param y1 the area to search rectangle y1
 * @param x2 the area to search rectangle x2
 * @param y2 the area to search rectangle y2
 * @param test_color the pointer to method for the color test to search
 * 		this might be defined in uint8_t test_methodname(long color)
 * 		and must return 1 if color match desired color, or return 0 if not
 */
#define pixelsearch_nothread(x1,y1, x2,y2, test_color) \
	pixelsearch_param(myparam, 0, x1,y1, x2,y2, test_color); \
	pixelsearch((void*)myparam);

#endif
