#include <chrono>
#include <thread>
#include <iostream>

#include "types.h"

class Timer {
private:
    f64 limit;
    u32 count;
    f64 _current;
    u32 _reach_count;

public:
    Timer(f64 _limit, u32 _count = 0)
        : limit(_limit), count(_count), _current(0), _reach_count(_count) {}

    Timer(const Timer&) = delete;
    Timer& operator=(const Timer&) = delete;
    Timer(Timer&&) = delete;
    Timer& operator=(Timer&&) = delete;
    ~Timer() = default;

    Timer& start() {
        if (!started()) {
            _current = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
            _reach_count = 0;
        }
        return *this;
    }

    bool started() const {
        return _current != 0;
    }

    f64 current() const {
        if (started()) {
            return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count() - _current;
        }
        else {
            return 0;
        }
    }

    bool reached() {
        _reach_count++;
        return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count() - _current > limit && _reach_count > count;
    }

    Timer& reset() {
        _current = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
        _reach_count = 0;
        return *this;
    }

    Timer& clear() {
        _current = 0;
        _reach_count = count;
        return *this;
    }

    bool reached_and_reset() {
        if (reached()) {
            reset();
            return true;
        }
        else {
            return false;
        }
    }

    void wait() {
        f64 diff = _current + limit - std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
        if (diff > 0) {
            std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<u32>(diff)));
        }
    }

    void show() {
        std::cout << *this << std::endl;
    }

    friend std::ostream& operator<<(std::ostream& os, const Timer& timer) {
        return os << "Timer(limit=" << timer.current() << "/" << timer.limit << ", count=" << timer._reach_count << "/" << timer.count << ")";
    }
};