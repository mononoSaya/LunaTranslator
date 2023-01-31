﻿#include <windows.h>
#include<string>
#include<thread> 
using std::string;
#define BUFSIZE 4096
#pragma comment( linker, "/subsystem:windows /entry:mainCRTStartup" )
 
static UINT64 getCurrentMilliSecTimestamp() {
	FILETIME file_time;
	GetSystemTimeAsFileTime(&file_time);
	UINT64 time = ((UINT64)file_time.dwLowDateTime) + ((UINT64)file_time.dwHighDateTime << 32);

	// This magic number is the number of 100 nanosecond intervals since January 1, 1601 (UTC)
	// until 00:00:00 January 1, 1970
	static const UINT64 EPOCH = ((UINT64)116444736000000000ULL);

	return (UINT64)((time - EPOCH) / 10000LL);
}
int pid_running(int pid) {
	HANDLE handle = OpenProcess(SYNCHRONIZE, FALSE, pid);
	int ret = WaitForSingleObject(handle, 0);
	CloseHandle(handle);
	return ret == WAIT_TIMEOUT;
} 
int main() { 
	 
	
	UINT64 tm = getCurrentMilliSecTimestamp();
	wchar_t buffw[32];
	swprintf_s(buffw, 32, L"%lld", tm);
	std::wstring starttimew= std::wstring(buffw);


	std::thread t1= std::thread([starttimew]() {
		
		while (true) { 
			HANDLE hPipe = CreateNamedPipe((std::wstring(L"\\\\.\\Pipe\\newsentence")+starttimew).c_str(), PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT
				, PIPE_UNLIMITED_INSTANCES, 0, 0, NMPWAIT_WAIT_FOREVER, 0);
			if (ConnectNamedPipe(hPipe, NULL) == NULL) {
				continue;
			} 
			BOOL fSuccess = false;
			DWORD len = 0;
			char buffer[BUFSIZE];
			string recvData = "";
			do
			{
				fSuccess = ReadFile(hPipe, buffer, BUFSIZE * sizeof(char), &len, NULL);
				char buffer2[BUFSIZE + 1] = { 0 };
				memcpy(buffer2, buffer, len);
				recvData.append(buffer2);
				if (!fSuccess || len < BUFSIZE)
					break;
			} while (true); 
			if (strcmp(recvData.c_str(), "end") == 0) {
				break;
			}
			//WinExec("taskkill /IM voice2.exe /F", SW_HIDE);
			//WinExec("./files/voiceroid2/voice2.exe C:/dataH/Yukari2 C:/tmp/LunaTranslator/files/voiceroid2/aitalked.dll yukari_emo_44 1 1.05 C:/tmp/LunaTranslator/ttscache/1.wav  86 111 105 99 101 82 111 105 100 50 32", SW_HIDE);
			WinExec(recvData.c_str(), SW_HIDE); 
		}

		});
	 

	STARTUPINFO si = {0}; 
	si.cb = sizeof(STARTUPINFO);
	si.dwFlags = STARTF_USESHOWWINDOW;
	si.wShowWindow = SW_SHOW;
	PROCESS_INFORMATION pi; 
	if (CreateProcessW(L".\\LunaTranslator\\LunaTranslator_main.exe", (LPWSTR)(std::wstring(L".\\LunaTranslator\\LunaTranslator_main.exe ") + starttimew).c_str(), NULL,
		NULL, FALSE, 0, NULL, NULL, &si, &pi)) { 
		while (true)
		{  
			if (pid_running(pi.dwProcessId) == 0) {
				break;
			} 
			Sleep(100);
		}
	}

}
 