# Invaders-Clone

This was a project completed in the Fall of 2019 in Cornell's Intro to CS class and is a rendition of the famous Space Invaders game.
The program uses Python 3.6 Anaconda, Kivy, and Cornell's introcs package. More info on prerequistes [here](https://www.cs.cornell.edu/courses/cs1110/2019fa/materials/python/)

To run the game, download and install pre-requisites. Then, type ```python invaders``` in your terminal just outside the invaders directory.

This version of the game has an infinite number of waves and ends when you run out of lives or if the aliens reach your defensive line.

The score is tallied: the farther aliens are worth more points.
Aliens in 1st and 2nd row closest to ship worth 10 each
Aliens in 3rd and 4th row closest to ship worth 20 each
Aliens in 5th and 6th row closest to ship worth 30 each

Dyanmic aliens: Aliens move faster with each successive alien you kill. The wavespeed is multiplied by INCREMENT in consts.py.
The factor is currently set at 0.985.

