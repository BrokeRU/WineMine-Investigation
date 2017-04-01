#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode, 2
Run, PaintDotNet
Sleep, 30000
Run, winmine.exe
Sleep, 2000

Random, , %A_TickCount%

Loop, 1000
{
	WinActivate, WineMine
	Sleep, 300
	Send, {F2}
	Sleep, 400
	Random, x, 0, 29
	Random, y, 0, 23
	MouseMove, 16 + 16 * x, 85 + 16 * y
	;MouseMove, 362 + 16 * x, 165 + 16 * y
	Sleep, 200
	Click
	; MsgBox, %x%, %y%
	Send, {Alt Down}{PrintScreen}{Alt Up}
	Sleep, 500
	WinActivate, paint.net
	Sleep, 1000
	Send, {Ctrl Down}v{Ctrl Up}
	Sleep, 800
	Send, {Ctrl Down}{Shift Down}x{Shift Up}{Ctrl Up}
	Sleep, 800
	Send, {Ctrl Down}{Shift Down}s{Shift Up}{Ctrl Up}
	Sleep, 900
	Send, %A_Index%_%x%_%y%
	Send, {Enter}
	Sleep, 700
	Send, {Enter}
	Sleep, 600
}
