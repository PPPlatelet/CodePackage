#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <optional>

class OperationRecorder {
private:
    static const size_t BUFFER_SIZE = 1024;
    std::vector<std::string> buffer;
    size_t head;           // 指向最早的操作
    size_t tail;           // 指向下一个要写入的位置
    size_t count;          // 当前存储的操作数量
    size_t undoPointer;    // 外部控制的回退指针
    bool full;             // 标记缓冲区是否已满
    
public:
    OperationRecorder() 
        : buffer(BUFFER_SIZE), head(0), tail(0), count(0), undoPointer(0), full(false) {}
    
    // 记录一个新的操作
    void recordOperation(const std::string& operation) {
        buffer[tail] = operation;
        
        if (full) {
            // 缓冲区已满，覆盖最早的操作
            head = (head + 1) % BUFFER_SIZE;
        } else {
            count++;
        }
        
        tail = (tail + 1) % BUFFER_SIZE;
        full = (tail == head);
        
        // 当有新操作时，重置重做指针到最新位置
        resetUndoPointerToLatest();
    }
    
    // 回退一次操作（外部通过指针控制）
    std::optional<std::string> undo() {
        if (isEmpty() || undoPointer == 0) {
            return std::nullopt;  // 没有可回退的操作
        }
        
        undoPointer--;
        size_t index = getIndexForUndoPointer();
        
        return buffer[index];
    }
    
    // 重做一次被回退的操作
    std::optional<std::string> redo() {
        if (isEmpty() || undoPointer >= getValidCount()) {
            return std::nullopt;  // 没有可重做的操作
        }
        
        size_t index = getIndexForUndoPointer();
        undoPointer++;
        
        return buffer[index];
    }
    
    // 获取当前可回退的操作数量
    size_t getUndoCount() const {
        return undoPointer;
    }
    
    // 获取当前可重做的操作数量
    size_t getRedoCount() const {
        return getValidCount() - undoPointer;
    }
    
    // 清空操作记录（只重置外部指针，不重置实际存储）
    void clearOperations() {
        undoPointer = 0;
    }
    
    // 获取当前有效操作数量
    size_t getValidCount() const {
        if (full) {
            return BUFFER_SIZE;
        }
        return count;
    }
    
    // 判断是否为空
    bool isEmpty() const {
        return (!full && (head == tail));
    }
    
    // 判断是否为满
    bool isFull() const {
        return full;
    }
    
    // 打印当前状态（用于调试）
    void printStatus() const {
        std::cout << "Buffer Status:" << std::endl;
        std::cout << "  Capacity: " << BUFFER_SIZE << std::endl;
        std::cout << "  Head: " << head << std::endl;
        std::cout << "  Tail: " << tail << std::endl;
        std::cout << "  Count: " << getValidCount() << std::endl;
        std::cout << "  Undo Pointer: " << undoPointer << std::endl;
        std::cout << "  Undo Available: " << getUndoCount() << std::endl;
        std::cout << "  Redo Available: " << getRedoCount() << std::endl;
        std::cout << "  Is Full: " << (isFull() ? "Yes" : "No") << std::endl;
    }
    
    // 打印所有存储的操作（按存储顺序）
    void printAllOperations() const {
        std::cout << "All stored operations:" << std::endl;
        if (isEmpty()) {
            std::cout << "  (empty)" << std::endl;
            return;
        }
        
        size_t idx = head;
        for (size_t i = 0; i < getValidCount(); i++) {
            std::cout << "  [" << i << "] " << buffer[idx] 
                     << (i == undoPointer ? " <-- undo pointer" : "") << std::endl;
            idx = (idx + 1) % BUFFER_SIZE;
        }
    }
    
private:
    // 根据undoPointer获取对应的缓冲区索引
    size_t getIndexForUndoPointer() const {
        if (isEmpty()) {
            return 0;
        }
        
        // undoPointer表示从最早的操作开始的偏移量
        // 0表示最早的操作，getValidCount()-1表示最新的操作
        size_t offset = undoPointer;
        
        if (full && undoPointer == getValidCount()) {
            offset = BUFFER_SIZE - 1;
        }
        
        return (head + offset) % BUFFER_SIZE;
    }
    
    // 重置undo指针到最新位置
    void resetUndoPointerToLatest() {
        undoPointer = getValidCount();
    }
};

// 使用示例
int main() {
    OperationRecorder recorder;
    
    std::cout << "=== Operation Recorder Demo ===" << std::endl;
    
    // 记录一些操作
    recorder.recordOperation("Create document");
    recorder.recordOperation("Edit paragraph 1");
    recorder.recordOperation("Insert image");
    recorder.recordOperation("Format text");
    
    recorder.printStatus();
    std::cout << std::endl;
    
    // 测试回退
    std::cout << "--- Undo Operations ---" << std::endl;
    auto undoResult = recorder.undo();
    if (undoResult) {
        std::cout << "Undo: " << *undoResult << std::endl;
    }
    
    recorder.printStatus();
    std::cout << std::endl;
    
    // 测试重做
    std::cout << "--- Redo Operation ---" << std::endl;
    auto redoResult = recorder.redo();
    if (redoResult) {
        std::cout << "Redo: " << *redoResult << std::endl;
    }
    
    recorder.printStatus();
    std::cout << std::endl;
    
    // 清空操作记录（只重置指针）
    std::cout << "--- Clear Operations ---" << std::endl;
    recorder.clearOperations();
    recorder.printStatus();
    std::cout << std::endl;
    
    // 演示循环覆盖
    std::cout << "--- Testing Circular Buffer (adding 1026 operations) ---" << std::endl;
    OperationRecorder recorder2;
    
    // 添加超过缓冲区容量的操作
    for (int i = 0; i < 1026; i++) {
        recorder2.recordOperation("Operation " + std::to_string(i + 1));
    }
    
    recorder2.printStatus();
    std::cout << std::endl;
    std::cout << "First stored operation: " << std::endl;
    
    // 查看当前存储的操作（应该是最新的1024个）
    recorder2.printAllOperations();
    
    // 多次回退
    std::cout << "\n--- Multiple Undo/Redo ---" << std::endl;
    for (int i = 0; i < 5; i++) {
        auto op = recorder2.undo();
        if (op) {
            std::cout << "Undo " << (i+1) << ": " << *op << std::endl;
        }
    }
    
    std::cout << "\nAfter 5 undos:" << std::endl;
    recorder2.printStatus();
    
    // 测试重做
    std::cout << "\nRedoing 3 operations:" << std::endl;
    for (int i = 0; i < 3; i++) {
        auto op = recorder2.redo();
        if (op) {
            std::cout << "Redo " << (i+1) << ": " << *op << std::endl;
        }
    }
    
    return 0;
}