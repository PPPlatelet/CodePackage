#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <optional>
#include <mutex>

#define BUFFER_SIZE 10000

size_t next(size_t index, size_t size, size_t step = 1)
{
    return (index + step) % size;
}

size_t prev(size_t index, size_t size, size_t step = 1)
{
    return (index - step + size) % size;
}

class OperationRecorder
{
private:
    size_t buffer_size;
    std::vector<std::optional<std::string>> buffer;
    size_t tail;
    size_t count;
    size_t undocount;

    mutable std::mutex mtx;

public:
    OperationRecorder(size_t size = BUFFER_SIZE)
        : buffer_size(size), buffer(size), tail(0), count(0), undocount(0) {}

    template <typename T>
    void record(T &&data)
    {
        std::lock_guard<std::mutex> lock(mtx);

        if (undocount > 0)
        {
            count -= undocount;
            undocount = 0;
        }
        buffer[tail] = std::forward<T>(data);

        tail = next(tail, buffer_size);
        count = std::min(count + 1, buffer_size);
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

        std::string tmp = buffer[next(tail, buffer_size, actual - 1)].value();

        tail = next(tail, buffer_size, actual);

        return tmp;
    }

    void clear()
    {
        std::lock_guard<std::mutex> lock(mtx);

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
    std::vector<std::optional<Block>> buffer;
    size_t tail;
    size_t count;
    size_t undocount;

public:
    Player()
        : buffer(BUFFER_SIZE), tail(0), count(0), undocount(0) {}

    template <typename T>
    void record(T &&block)
    {
        if (undocount > 0)
        {
            count -= undocount;
            undocount = 0;
        }

        buffer[tail] = std::forward<T>(block);

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

        tail = next(tail, BUFFER_SIZE);
        if (count < BUFFER_SIZE)
        {
            count++;
        }
    }

    std::optional<Block> undo()
    {
        if (undocount >= count)
        {
            return std::nullopt;
        }

        tail = prev(tail, BUFFER_SIZE);
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

    std::optional<Block> redo()
    {
        if (undocount == 0)
        {
            return std::nullopt;
        }

        undocount--;
        std::optional<Block> tmp = std::nullopt;

        if (buffer[tail]->source == nullptr)
        {
            buffer[tail]->source = this;
            buffer[tail]->count = 1;
            tmp = *buffer[tail];
        }
        else if (buffer[tail]->source == this)
        {
            buffer[tail]->count++;
            tmp = *buffer[tail];
        }
        // else do nothing, return nullopt
        tail = next(tail, BUFFER_SIZE);
        return tmp;
    }

    void clear()
    {
        tail = 0;
        count = 0;
        undocount = 0;
    }
};