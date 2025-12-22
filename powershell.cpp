#include <Python.h>
#include <Windows.h>
#include <stdio.h>
#include <string.h>

static HANDLE hStdIn, hStdOut, hStdErr;
static PROCESS_INFORMATION piProcInfo;
static STARTUPINFO siStartInfo;

static int start_powershell_session() {
    // 创建管道用于进程间通信
    SECURITY_ATTRIBUTES saAttr = { sizeof(SECURITY_ATTRIBUTES), NULL, TRUE };
    if (!CreatePipe(&hStdOut, &hStdIn, &saAttr, 0)) {
        return -1;
    }
    if (!CreatePipe(&hStdErr, &hStdOut, &saAttr, 0)) {
        return -1;
    }

    // 配置启动信息
    ZeroMemory(&siStartInfo, sizeof(STARTUPINFO));
    siStartInfo.cb = sizeof(STARTUPINFO);
    siStartInfo.hStdOutput = hStdOut;
    siStartInfo.hStdError = hStdErr;
    siStartInfo.hStdInput = hStdIn;
    siStartInfo.dwFlags |= STARTF_USESTDHANDLES;

    // 启动 PowerShell 进程
    ZeroMemory(&piProcInfo, sizeof(PROCESS_INFORMATION));
    if (!CreateProcess(
            L"powershell.exe",    // 可执行程序
            (LPWSTR)L"powershell.exe",    // 命令行参数
            NULL,                // 进程安全属性
            NULL,                // 线程安全属性
            TRUE,                // 继承句柄
            CREATE_NO_WINDOW,    // 不显示窗口
            NULL,                // 环境变量
            NULL,                // 当前目录
            &siStartInfo,        // 启动信息
            &piProcInfo)) {      // 进程信息
        return -1;
    }

    return 0;
}

static void send_command_to_powershell(const char* command) {
    DWORD bytesWritten;
    WriteFile(hStdIn, command, strlen(command), &bytesWritten, NULL);
    WriteFile(hStdIn, "\n", 1, &bytesWritten, NULL);
}

static void read_output_from_powershell() {
    char buffer[4096];
    DWORD bytesRead;
    while (ReadFile(hStdOut, buffer, sizeof(buffer) - 1, &bytesRead, NULL) && bytesRead > 0) {
        buffer[bytesRead] = '\0';  // null-terminate the string
        printf("%s", buffer);      // 输出到标准输出（或做进一步处理）
    }
}

static PyObject* execute_powershell_command(PyObject* self, PyObject* args) {
    const char* command;

    // 解析参数
    if (!PyArg_ParseTuple(args, "s", &command)) {
        return NULL;
    }

    // 启动 PowerShell 会话
    if (start_powershell_session() != 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to start PowerShell session.");
        return NULL;
    }

    // 发送命令到 PowerShell
    send_command_to_powershell(command);

    // 读取输出
    read_output_from_powershell();

    return Py_None;
}

static PyMethodDef methods[] = {
    {"execute_powershell_command", execute_powershell_command, METH_VARARGS, "Execute a PowerShell command."},
    {NULL, NULL, 0, NULL}  // 终止标志
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "powershell",  // 模块名称
    "A module to interact with PowerShell.",  // 模块描述
    -1,
    methods
};

PyMODINIT_FUNC PyInit_powershell(void) {
    return PyModule_Create(&module);
}
