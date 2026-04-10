#include <windows.h>
#include <iostream>
#include <string>
#include <cstring>

// global variables
int g_current_value = 0;
HHOOK g_hKeyboardHook = NULL;

bool IsRunAsAdmin() {
    BOOL isElevated = FALSE;
    HANDLE hToken = NULL;

	if (OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken)) {
        TOKEN_ELEVATION elevation;
        DWORD dwSize = sizeof(TOKEN_ELEVATION);
        if (GetTokenInformation(hToken, TokenElevation, &elevation, dwSize, &dwSize)) {
			isElevated = elevation.TokenIsElevated;
        }
		CloseHandle(hToken);
    }
    return isElevated == TRUE;
}

// int -> string -> char* -> clipboard
void UpdateClipboard(int value) {
    std::string text = std::to_string(value);
    const char* str = text.c_str();
    int len = static_cast<int>(text.length()) + 1; // include '\0'

    if (!OpenClipboard(NULL)) {
        std::cerr << "Failed to open clipboard." << std::endl;
        return;
    }
    EmptyClipboard();

    HGLOBAL hMem = GlobalAlloc(GMEM_MOVEABLE | GMEM_DDESHARE, len);
    if (hMem) {
        char* pMem = static_cast<char*>(GlobalLock(hMem));
        if (pMem) {
            memcpy(pMem, str, len);
            GlobalUnlock(hMem);
            SetClipboardData(CF_TEXT, hMem);
        }
        else {
            GlobalFree(hMem);
        }
    }
    CloseClipboard();
}

// Callback function
LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        if (wParam == WM_KEYDOWN) {
            KBDLLHOOKSTRUCT* p = reinterpret_cast<KBDLLHOOKSTRUCT*>(lParam);
            if (p->vkCode == 'V' && (GetAsyncKeyState(VK_CONTROL) & 0x8000)) {
                UpdateClipboard(g_current_value);
                int pasted = g_current_value;
                g_current_value++;
                std::cout << "Pasted: " << pasted << " -> next: " << g_current_value << std::endl;
            }
            if (p->vkCode == VK_ESCAPE) {
                std::cout << "Exiting..." << std::endl;
                PostQuitMessage(0);
            }
        }
    }
    return CallNextHookEx(g_hKeyboardHook, nCode, wParam, lParam);
}

int main() {
	if (!IsRunAsAdmin()) {
        MessageBox(NULL,
            L"This program requires administrator privileges to run properly.\n"
            L"Please run as administrator.",
            L"Elevation Required",
            MB_OK | MB_ICONERROR);
        return 1;
    }

    std::cout << "Enter an initial integer(): ";
    std::cin >> g_current_value;
    if (std::cin.fail()) {
        std::cerr << "Invalid input." << std::endl;
        return 1;
    }

    // install keyboard hook
    g_hKeyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, GetModuleHandle(NULL), 0);
    if (g_hKeyboardHook == NULL) {
        std::cerr << "Failed to install keyboard hook. Error: " << GetLastError() << std::endl;
        return 1;
    }

    std::cout << "Hook installed. Press Esc to exit." << std::endl;

    // message loop
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // uninstall hook
    UnhookWindowsHookEx(g_hKeyboardHook);
    Sleep(2000);
    return 0;
}