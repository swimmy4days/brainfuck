#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from signal import SIGINT, signal
from readchar import readchar
from sys import version_info, stdout
from time import sleep
from os import path, system, name
import constants

if version_info.major != 3:
    raise(EnvironmentError(constants.UNSUPPORTED_VERSION))


class Parser(object):
    """
    The parser Class

    Args:
        file (string): What file should i execute?
        debug (float): Should i debug?
        intify (bool): Print as an int or char
        no_warnings (bool): Should i print the warnings?
        size (int): What is the maximum size of each cell

    """

    def __init__(self, file=None, debug=False, intify=False, no_warnings=False, size=255):
        """Summary

        Args:
            file (string, required)
            debug (bool, optional)
            intify (bool, optional)
            no_warnings (bool, optional)
            size (int, optional
        """
        super(Parser, self).__init__()
        if not file:
            raise(EnvironmentError(constants.NO_FILE))
        bracket = 0
        self.debug = None
        self.program = str()
        self.intify = intify
        self.no_warnings = no_warnings
        self.maxCellSize = size
        if debug == None:
            self.debug = 0.1
        elif debug < 0:
            self.debug = False
        elif debug > 0:
            self.debug = debug
        try:
            with open(file) as f:
                extension = path.splitext(file)[1]
                program = f.read()
                if extension.lower() != ".bf" and not self.no_warnings:
                    print(constants.BF_FILES)
        except Exception:
            raise(EnvironmentError(constants.NO_FILE))

        letters = ['[', ']', '+', '-', ',', '.', '<', '>']
        for char in program:
            if char in letters:
                self.program += char
            if char == '[':
                bracket += 1
            elif char == ']':
                bracket -= 1
        self.program += ' '

        if bracket and not self.no_warnings:
            print(constants.LOOP_WARNING)

    def parse(self):
        try:
            signal(SIGINT, lambda s, f: (
                   stdout.flush(constants.CTRL_C),
                   exit(1)))

            prgPointer = 0
            pointer = 0
            tape = [0]
            prints = ""
            cells = ""

            # with output(initial_len=6, interval=0) as output_lines:
            while prgPointer < len(self.program):

                if self.debug:
                    sleep(self.debug)
                    cells = ""
                    for c in tape:
                        cells += f"{str(c).zfill(len(str(self.maxCellSize)))} "

                    self.clear_screen()
                    print(f"       ")
                    print(f"Output: {prints}")
                    print(f"Tape: {cells}")
                    print("Ptr:  {}^".format(
                        (" " * (len(str(self.maxCellSize)) + 1)) * pointer))
                    print(
                        f"Program: {self.program[prgPointer - 1:prgPointer + 71]}")
                    print("          ^")
                else:
                    print(f"Output: {prints}", end="\r")
                if self.program[prgPointer] == '>':
                    pointer += 1
                    if pointer >= len(tape):
                        tape.append(0)
                elif self.program[prgPointer] == '<':
                    pointer -= 1
                    if pointer < 0:
                        raise(EnvironmentError(constants.TAPE_ERROR))
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
                    print("Input: ", end='\r')
                    inp = readchar()
                    tape[pointer] = ord(inp.decode())
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

        except Exception as e:
            print(e)
            raise(EnvironmentError(constants.UNKNOWN_ERROR))

    @staticmethod
    def clear_screen():
        """
        Clear the terminal screen, OS aware.
        """

        # Windows
        if name == 'nt':
            _ = system('cls')

        # Mac/Linux
        else:
            _ = system('clear')


if __name__ == '__main__':
    prs = ArgumentParser(prog=constants.PROGRAM_NAME, formatter_class=RawDescriptionHelpFormatter,
                         description=(constants.PARSER_MSG), epilog=constants.EPILOG)
    prs.add_argument("file", help=constants.FILE_HELP,  type=str)
    prs.add_argument("-s", "--size", help=constants.SIZE_HELP,
                     default=255, type=int, dest="size", metavar="Size")
    prs.add_argument("-i", "--intify",
                     help=constants.INTIFY_HELP, action='store_true')
    prs.add_argument("-d", "--debug", dest="debug", metavar="Sec", type=float,
                     nargs='?', default=-1, required=False, help=constants.DEBUG_HELP)
    prs.add_argument("--no_warnings", action='store_true',
                     help=constants.NO_WARNINGS_HELP)
    args = prs.parse_args()

    Parser(args.file, args.debug, args.intify,
           args.no_warnings, args.size).parse()
