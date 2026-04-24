#include <iostream>
#include <iomanip>
#include <random>
#include <vector>
#include <string>
#include <stdexcept>
#include <optional>
#include <mutex>

inline size_t next(const size_t &index, const size_t &size, const size_t &step = 1)
{
    return (index + step) % size;
}

inline size_t prev(const size_t &index, const size_t &size, const size_t &step = 1)
{
    return (index - step + size) % size;
}

inline void divmod(const size_t &x, const size_t &y, size_t &d, size_t &m)
{
    d = x / y;
    m = x % y;
}

class OperationRecorder
{
private:
    size_t buffer_size;
    std::vector<std::optional<std::string>> buffer;
    size_t head;
    size_t tail;
    size_t count;
    size_t undocount;

    mutable std::mutex mtx;

public:
    OperationRecorder(size_t size = 10000)
        : buffer_size(size), buffer(size), head(0), tail(0), count(0), undocount(0) {}

    void record(std::string &&data)
    {
        std::lock_guard<std::mutex> lock(mtx);

        if (undocount > 0)
        {
            count -= undocount;
            undocount = 0;
        }
        buffer[tail] = std::forward<std::string>(data);

        tail = next(tail, buffer_size);
        if (count < buffer_size)
            count++;
        else
            head = next(head, buffer_size);
    }

    std::optional<std::string> undo(size_t step = 1)
    {
        std::lock_guard<std::mutex> lock(mtx);

        if (undocount >= count)
        {
            return std::nullopt;
        }

        size_t actual = std::min(step, count - undocount);

        tail = prev(tail, buffer_size, actual);
        undocount += actual;
        return buffer[tail];
    }

    std::optional<std::string> redo(size_t step = 1)
    {
        std::lock_guard<std::mutex> lock(mtx);

        if (undocount == 0)
        {
            return std::nullopt;
        }

        size_t actual = std::min(step, undocount);

        undocount -= actual;

        std::string res = buffer[next(tail, buffer_size, actual - 1)].value();

        tail = next(tail, buffer_size, actual);

        return res;
    }

    void clear()
    {
        std::lock_guard<std::mutex> lock(mtx);

        head = 0;
        tail = 0;
        count = 0;
        undocount = 0;
    }
};

struct Block;
class Player;

int main()
{
}

struct Block
{
    int status;
    bool is_black;
    Player *source;
    int count;
};

class Player
{
private:
    size_t size;
    std::vector<std::optional<Block>> buffer;
    size_t tail;
    size_t count;
    size_t undocount;

public:
    Player(size_t size = 10000)
        : size(size), buffer(size), tail(0), count(0), undocount(0) {}

    void record(Block &&block) noexcept
    {
        if (undocount > 0)
        {
            count -= undocount;
            undocount = 0;
        }

        buffer[tail] = std::forward<Block>(block);

        // if (block.source == nullptr)
        // {
        //     buffer[tail]->source = this;
        //     buffer[tail]->count = 1;
        // }
        // else
        if (buffer[tail]->source == this)
        {
            buffer[tail]->count++;
        }
        else
        {
            buffer[tail]->source = this;
            buffer[tail]->count = 1;
        }

        tail = next(tail, size);
        count = std::min(count + 1, size);
    }

    std::optional<Block> undo() noexcept
    {
        if (undocount >= count)
        {
            return std::nullopt;
        }

        tail = prev(tail, size);
        undocount++;

        // if (buffer[tail]->source == nullptr)
        // {
        //     return std::nullopt;
        // }
        // else
        if (buffer[tail]->source == this)
        {

            buffer[tail]->count--;
            if (buffer[tail]->count == 0)
            {
                buffer[tail]->source = nullptr;
            }
            return buffer[tail];
        }
        else
        {
            return std::nullopt;
        }
    }

    std::optional<Block> redo() noexcept
    {
        if (undocount == 0)
        {
            return std::nullopt;
        }

        undocount--;
        std::optional<Block> res = std::nullopt;

        if (buffer[tail]->source == nullptr)
        {
            buffer[tail]->source = this;
            buffer[tail]->count = 1;
            res = *buffer[tail];
        }
        else if (buffer[tail]->source == this)
        {
            buffer[tail]->count++;
            res = *buffer[tail];
        }
        // else do nothing, return nullopt
        tail = next(tail, size);
        return res;
    }

    void clear() noexcept
    {
        tail = 0;
        count = 0;
        undocount = 0;
    }
};

struct Vector3
{
    float x, y, z;
};

class Frame
{
private:
    Vector3 float3;   // X, Y, Angle
    Vector3 velocity; // Vx, Vy, 0
public:
    Frame(float x = 0, float y = 0, float angle = 0, float vx = 0, float vy = 0)
        : float3{x, y, angle}, velocity{vx, vy, 0} {}

    friend std::ostream &operator<<(std::ostream &os, const Frame &frame)
    {
        os << std::fixed << std::setprecision(2)
           << "Position: (" << frame.float3.x << ", " << frame.float3.y << "), "
           << "Angle: " << frame.float3.z << " degrees, "
           << "Velocity: (" << frame.velocity.x << ", " << frame.velocity.y << ")";
        return os;
    }
};

class Client
{
private:
    size_t capacity;
    size_t size;

    std::vector<std::vector<Frame>> segments;
    size_t head;
    size_t tail;
    size_t count;

    std::vector<Frame> seg;
    size_t seg_idx;
    size_t seg_snap;

    size_t timeline_end;
    size_t timeline_cursor;

    bool replay_mode;
    size_t direction;

    bool paused;

public:
    Client(size_t capacity = 10000, size_t size = 16)
        : capacity(capacity), size(size),
          segments(capacity, std::vector<Frame>(size)), seg(size)
    {
        head = tail = count = 0;
        seg_idx = seg_snap = 0;
        timeline_end = timeline_cursor = 0;
        replay_mode = false;
        direction = 0;
        paused = false;
    }

    void execute(const Frame &frame)
    {
        std::cout << "Execute frame:" << frame << std::endl;
        signal_resume();
    }

    void record(const Frame &frame)
    {
        seg[seg_idx++] = frame;
        if (seg_idx == size)
        {
            segments[tail] = seg;
            tail = next(tail, capacity);
            if (count < capacity)
                count++;
            else
                head = next(head, capacity);
            seg_idx = 0;
        }
    }

    void replay()
    {
        if (!replay_mode)
        {
            seg_snap = seg_idx;

            timeline_end = timeline_cursor = count * size;

            replay_mode = true;
            direction = -1;
        }
        else
        {
            size_t seg_pos, frame_pos;
            divmod(timeline_cursor, size, seg_pos, frame_pos);

            if (seg_pos < count)
            {
                count = seg_pos;
                tail = next(head, capacity, count);
                if (frame_pos > 0)
                {
                    seg = segments[next(head, capacity, seg_pos)];
                    seg_idx = frame_pos;
                }
            }

            replay_mode = false;
            direction = 0;
        }
    }

    void rewind()
    {
        switch (direction)
        {
        case 0:
            break;
        case -1:
            if (seg_idx > 0)
            {
                execute(seg[--seg_idx]);
                return;
            }

            if (timeline_cursor > 0)
            {
                size_t seg_pos, frame_pos;
                divmod(--timeline_cursor, size, seg_pos, frame_pos);
                execute(segments[next(head, capacity, seg_pos)][frame_pos]);
                return;
            }
            break;
        case 1:
            if (timeline_cursor < timeline_end)
            {
                size_t seg_pos, frame_pos;
                divmod(timeline_cursor++, size, seg_pos, frame_pos);
                execute(segments[next(head, capacity, seg_pos)][frame_pos]);
                return;
            }

            if (seg_idx < seg_snap)
            {
                execute(seg[seg_idx++]);
                return;
            }
            break;
        }
        signal_stop();
    }

    void backward()
    {
        switch (direction)
        {
        case 0:
            direction = -1;
            signal_resume();
            break;
        case 1:
            direction = 0;
            signal_stop();
            break;
        default:
            break;
        }
    }

    void forward()
    {
        switch (direction)
        {
        case -1:
            direction = 0;
            signal_stop();
            break;
        case 0:
            direction = 1;
            signal_resume();
            break;
        default:
            break;
        }
    }

    void signal_resume()
    {
        if (paused)
        {
            paused = false;
            std::cout << "Signal resume" << std::endl;
        }
    }

    void signal_stop()
    {
        if (!paused)
        {
            paused = true;
            std::cout << "Signal stop" << std::endl;
        }
    }
};
