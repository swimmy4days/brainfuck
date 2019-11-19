#!/usr/bin/env python3

from signal import SIGINT, signal
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from reprint import output
from time import sleep
from sys import stdout, version_info
from os import path

if version_info.major != 3:
    raise(EnvironmentError("Error: Unsupported Python Version"))


class Parser(object):
    """
    The parser Class

    Args:
        file (string): What file should i execute?
        debug (flaot): Sould i debug?
        intify (bool): Print as an int or char
        no_warnings (bool): Should i print the warnings?
        size (int): What is the maximum size of each cell

    """

    def __init__(self, file=None, debug=False, intify=False, no_warnings=False, size=255):
        if not file:
            raise(EnvironmentError("Error: Must Provide A Source File"))
        bracket = 0
        self.debug = None
        self.program = None
        self.intify = intify
        self.no_warnings = no_warnings
        self.maxCellSize = size
        if debug == None:
            self.debug = 0.1
        elif debug < 0:
            self.debug = False
        try:
            with open(file) as f:
                extension = path.splitext(file)[1]
                self.program = f.read()
                if extension.lower() != ".bf" and not self.no_warnings:
                    print("Warning: Unsupported Extension, Supports Only *.bf Files")
        except Exception:
            raise(EnvironmentError("Error: Could Not Find The Source File!"))

        self.program = self.program.replace("\n", "")
        self.program += " "

        for char in self.program:
            if char == '[':
                bracket += 1
            elif char == ']':
                bracket -= 1

        if bracket and not self.no_warnings:
            print("Warning, Unmatching Number Of '[' To ']' (Invalid Loop)")

    def parse(self):
        try:
            signal(SIGINT, lambda s, f: (
                   stdout.flush(),
                   print('Error: The Process Was Closed By The User'),
                   exit(1)))

            prgPointer = 0
            pointer = 0
            tape = [0]
            prints = ""
            cells = ""

            with output(initial_len=5, interval=0) as output_lines:
                while prgPointer < len(self.program):

                    if self.debug:
                        sleep(self.debug)
                        cells = ""
                        for c in tape:
                            cells += f"{str(c).zfill(len(str(self.maxCellSize)))} "
                        output_lines[0] = f"Tape: {cells}"
                        output_lines[1] = "Ptr:  {}^".format((" " * (len(str(self.maxCellSize)) + 1)) * pointer)
                        output_lines[2] = f"self.Program: {self.program[prgPointer - 1:prgPointer + 71]}"
                        output_lines[3] = "          ^"
                        output_lines[4] = f"Output: {prints}"
                    else:
                        print(f"Output: {prints}", end="\r")
                    if self.program[prgPointer] == '>':
                        pointer += 1
                        if pointer >= len(tape):
                            tape.append(0)
                    elif self.program[prgPointer] == '<':
                        pointer -= 1
                        if pointer < 0:
                            raise(EnvironmentError("Error: Out Of Tape!"))
                    elif self.program[prgPointer] == '+':
                        tape[pointer] += 1
                        if tape[pointer] > self.maxCellSize + 1:
                            tape[pointer] = 0
                    elif self.program[prgPointer] == '-':
                        tape[pointer] -= 1
                        if tape[pointer] < 0:
                            tape[pointer] = self.maxCellSize
                    elif self.program[prgPointer] == '.':
                        if not self.intify:
                            prints += chr(tape[pointer])
                        else:
                            prints += str(int(tape[pointer]))
                    elif self.program[prgPointer] == ',':
                        inp = input("Input: ")
                        tape[pointer] = ord(inp[0])
                    elif self.program[prgPointer] == '[':
                        if tape[pointer] == 0:
                            bracket = 0
                            prgPointer += 1
                            while prgPointer < len(self.program):
                                if self.program[prgPointer] == ']' and bracket == 0:
                                    break
                                if self.program[prgPointer] == '[':
                                    bracket += 1
                                elif self.program[prgPointer] == ']':
                                    bracket -= 1
                                prgPointer += 1
                    elif self.program[prgPointer] == ']':
                        if tape[pointer] != 0:
                            bracket = 0
                            prgPointer -= 1
                            while prgPointer >= 0:
                                if self.program[prgPointer] == '[' and bracket == 0:
                                    break
                                if self.program[prgPointer] == ']':
                                    bracket += 1
                                elif self.program[prgPointer] == '[':
                                    bracket -= 1
                                prgPointer -= 1
                    prgPointer += 1

        except Exception:
            raise(EnvironmentError("Error: Unknown Error"))


if __name__ == '__main__':
    prs = ArgumentParser(prog="BrainFuck Parser",
                         formatter_class=RawDescriptionHelpFormatter,
                         description=('''Interperete And Runs A BrainFuck (*.bf) Program
--------------------------------
    An Easy To Use Simple BrainFuck Interpreter
    The Debugger Goes Through Each Commend And Shows The Tape And The Current Instruction
    Example: python ./parser.py HelloWorld.bf'''), epilog="Made By swimmy4days")
    prs.add_argument("file", help="The Path To The BrainFuck File",  type=str)
    prs.add_argument("-s", "--size", help="Set The Maximum Size Of Each Cell",
                     default=255, type=int, dest="size", metavar="Size")
    prs.add_argument("-i", "--intify", help="Prints The Numbers Inside The Cells As An Integer", action='store_true')
    prs.add_argument("-d", "--debug", dest="debug", metavar="Sec", type=float, nargs='?', default=-1, required=False,
                     help="Enables The Debugger, Sec - The Amount Of Time Between Each Operation In Seconds (default 0.1 Seconds)")
    prs.add_argument("--no_warnings", action='store_true', help="Disables The Parsers Warnings")
    args = prs.parse_args()

    a = Parser(args.file, args.debug, args.intify, args.no_warnings, args.size)
    a.parse()
