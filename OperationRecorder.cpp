#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <optional>

size_t next(size_t index, size_t size, size_t step = 1)
{
    return (index + step) % size;
}

size_t prev(size_t index, size_t size, size_t step = 1)
{
    return (index + size - step % size) % size;
}

class OperationRecorder
{
private:
    size_t buffer_size;
    std::vector<std::optional<std::string>> buffer;
    size_t tail;
    size_t count;
    size_t undocount;
    size_t total;

public:
    OperationRecorder(size_t size = 10000)
        : buffer_size(size), buffer(), tail(0), count(0), undocount(0), total(0) {}

    void record(const std::string &data)
    {
        if (undocount > 0)
        {
            count -= undocount;
            undocount = 0;
        }

        if (tail == total)
        {
            buffer.push_back(data);
            total++;
        }
        else
        {
            buffer[tail] = data;
        }

        tail = next(tail, buffer_size);
        if (count < buffer_size)
        {
            count++;
        }
    }

    std::optional<std::string> undo()
    {
        if (undocount >= count)
        {
            return std::nullopt;
        }

        tail = prev(tail, buffer_size);
        undocount++;
        return buffer[tail];
    }

    std::optional<std::string> redo()
    {
        if (undocount == 0)
        {
            return std::nullopt;
        }

        undocount--;
        std::string tmp = *buffer[tail];
        tail = next(tail, buffer_size);
        return tmp;
    }

    void clear()
    {
        tail = 0;
        count = 0;
        undocount = 0;
    }
};

class OperationRecorderLite
{
private:
    size_t buffer_size;
    std::vector<std::optional<std::string>> buffer;
    size_t head;
    size_t count;
public:
    bool can_undo;

    OperationRecorderLite(size_t size = 10000)
        : buffer_size(size), buffer(size), head(0), count(0), can_undo(false) {}
    
    void record(const std::string &data)
    {
        buffer[head] = data;
        head = next(head, buffer_size);
        can_undo = true;
        if (count < buffer_size) count++;
    }

    std::optional<std::string> undo()
    {
        switch (count)
        {
            case 0:
                return std::nullopt;
            case 1:
                can_undo = false;
        }
        head = prev(head, buffer_size);
        count--;
        return buffer[head];
    }

    std::optional<std::string> redo()
    {
        return std::nullopt;
    }

    void clear()
    {
        head = 0;
        count = 0;
        can_undo = false;
    }
};

int main()
{
    OperationRecorder recorder(5);
    recorder.record("Operation 1");
    recorder.record("Operation 2");
    recorder.record("Operation 3");

    auto op = recorder.undo();
    if (op)
        std::cout << "Undid: " << *op << std::endl;

    op = recorder.redo();
    if (op)
        std::cout << "Redid: " << *op << std::endl;

    recorder.clear();
    return 0;
}