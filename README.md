# Plentify Python for hardware work product

The goal of this work product is to evaluate a candidate's ability to implement a basic hardware driver for a chip using Python.

## Goal
Using *only* the [native microPython I2C APIs](https://docs.micropython.org/en/latest/library/machine.I2C.html), implement a driver for the  [DS1307](https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf) RTCC.
A basic skeleton API has been provided in the RTC.py file, feel free to update and change this interface as you see fit.

The desired minimum output is a program that reads the current time from the RTC every second, starting from 11:57:23 03/02/2024

## Rules/Guidance
* Create a public git repo on the platform of your choice so others can use your driver in Wokwi, use this repo as a means of demonstrating your understanding of git and source control management
* Use the [Wokwi VSCode plugin](https://docs.wokwi.com/vscode/getting-started) to develop and test locally. See [the example project](https://github.com/wokwi/wokwi-vscode-micropython)
* Implement this yourself - don't use AI or other online resourses. You will be asked to explain your code later
* Feel free to update the RTC library template to make it more maintainable and extensible
* Write the RTC driver as if it could be shared standalone
* Feel free to edit this README.md file to document your work
* Once complete, share the repo link with your contact at Plentify

### Limitations!
In order to allow the use of an online simulator, programming must be done on a simulated [Raspberry Pi Pico (RP2040)](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html) using the [microPython](https://micropython.org/) framework.
microPython is a port of Python that is intended to be used on resourse constrained devices like microcontrollers, because of this there are limitations and differences relative to full Python 3. 

Plentify does not use microPython, however for the purposes of this project, it is a good analog