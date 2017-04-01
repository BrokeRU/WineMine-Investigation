# WineMine Investigation
My investigation about some logical WineMine error.

One day I played ReactOS' WinMine and noticed some strange behavior. I was not able to finish game successfully because of few numbers showed incorrect values.

# Stage 1: Data Collection
I decided to explore this issue. After reading sources about 2 hours I modified WinMine so it got solved in just one click to game board. Then I wrote AutoHotKey script to automatically open WinMine, start new game, click in random cell on the game board, press Alt+PrtScr to make screenshot of current windows, save screenshot to directory. Result: about 5000 WinMine solution screens.

# Stage 2: Data Processing
I wrote Python script to cut out game board, parse cells and check that all numbers show correct values. Result: 4025 valid games, 47 anomalies. You can see anomalies here: https://drive.google.com/open?id=0B_kxhWQBawvjYkZXb2E5X3NGR00

# Stage 3: Code Analysis
Thus bug evidently exists. Have found place in code where game board gets generated.

    col = (int) (p_board->cols * (float) rand() / RAND_MAX + 1);
    row = (int) (p_board->rows * (float) rand() / RAND_MAX + 1);

Wrote some little program to test this piece of code 1 000 000 times (assuming `p_board->cols = p_board->rows = 9`).
Result: Algorithm returns almost uniform distribution. But... ~30 times of 1 000 000 it returned 10.

    0: 0
    1: 110972
    2: 111621
    3: 110342
    4: 111289
    5: 111040
    6: 111535
    7: 110949
    8: 110681
    9: 111541
    10: 30 <--- ???

Thus numbers showed correct values. Just mines were out of the game board.

# Stage 4: Fix
    col = rand() % p_board->cols + 1;
    row = rand() % p_board->rows + 1;

Result:

    0: 0
    1: 110615
    2: 111038
    3: 111140
    4: 111170
    5: 111481
    6: 110881
    7: 110785
    8: 111723
    9: 111167
    10: 0

# Conclusion
For now patch is send and accepted in Wine. Waiting while ReactOS sync WinMine with Wine.
