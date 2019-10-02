#pragma once
#include "tracking_malloc.hpp"
#include <map>
#include <list>
#include <thread>
#include <mutex>
#include <time.h>

struct tracking_malloc_alloc_info {
    size_t alloc_size;
    time_t alloc_time;
    int alloc_stacktrace_analysed;
    struct stacktrace* alloc_stacktrace;
};

struct tracking_malloc_alloc_opt {
    int opt_type;
    void* ptr;
    tracking_malloc_alloc_info* info;
};

typedef std::map<void*, tracking_malloc_alloc_info*, std::less<void*>, sys_allocator<std::pair<void*, tracking_malloc_alloc_info*> > > tracking_malloc_alloc_info_table;
typedef std::list<tracking_malloc_alloc_opt, sys_allocator<tracking_malloc_alloc_opt>> tracking_malloc_alloc_opt_list;

class tracking_malloc_record {
public:
    ~tracking_malloc_record();
    bool init();
    bool add_alloc(void* ptr, size_t size);
    bool add_free(void* ptr);

private:
    void apply_tracking_malloc_alloc_opt_list(tracking_malloc_alloc_opt_list& opt_list);
    void output(const char* suffix);
    int work_thread();

    tracking_malloc_alloc_info_table m_alloc_info_table;
    tracking_malloc_alloc_opt_list m_alloc_opt_list;
    std::recursive_mutex m_mutex;
    std::thread m_thread;
    int m_exit_flag;
    time_t next_save_time;
};
