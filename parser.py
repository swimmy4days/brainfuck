#!/usr/bin/env python3

from signal import SIGINT, signal
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from reprint import output
from time import sleep
from sys import exit, stdout, version_info
from os import path

if version_info.major != 3:
    print("Error: Unsupported Python Version")
    exit(1)


def parser():
    try:
        signal(SIGINT, lambda s, f: (
               stdout.flush(),
               print('Error: The Process Was Closed By The User'),
               exit(1)))
        parser = ArgumentParser(prog="BrainFuck Parser",
                                formatter_class=RawDescriptionHelpFormatter,
                                description=('''Interperete And Runs A BrainFuck (*.bf) Program
--------------------------------
    An Easy To Use Simple BrainFuck Interpreter
    The Debugger Goes Through Each Commend And Shows The Tape And The Current Instruction
    Example: python ./parser.py HelloWorld.bf'''), epilog="Made By swimmy4days")
        parser.add_argument("file", help="The Path To The BrainFuck File",  type=str)
        parser.add_argument("-s", "--size", help="Set The Maximum Size Of Each Cell",
                            default=255, type=int, dest="size", metavar="Size")
        parser.add_argument("-i", "--intify", help="Prints The Numbers Inside The Cells As An Integer", action='store_true')
        parser.add_argument("-d", "--debug", dest="debug", metavar="Sec", type=float, nargs='?', default=-1, required=False,
                            help="Enables The Debugger, Sec - The Amount Of Time Between Each Operation In Seconds (default 0.1 Seconds)")
        parser.add_argument("--no_warnings", action='store_true', help="Disables The Parsers Warnings")
        args = parser.parse_args()
        if args.debug == None:
            args.debug = 0.1
        elif args.debug < 0:
            args.debug = False

        try:
            with open(args.file) as f:
                extension = path.splitext(args.file)[1]
                program = f.read()
                if extension.lower() != ".bf" and not args.no_warnings:
                    print("Warning: Unsupported Extension, Supports Only *.bf Files")
        except Exception as e:
            print("Error: Could Not Find The Source File!")
            exit(1)

        maxCellSize = args.size
        prgPointer = 0
        pointer = 0
        bracket = 0
        tape = [0]
        prints = ""
        cells = ""

        for char in program:
            if char == '[':
                bracket += 1
            elif char == ']':
                bracket -= 1

        if bracket and not args.no_warnings:
            print("Warning, Unmatching Number Of '[' To ']' (Invalid Loop)")

        program = program.replace("\n", "")
        program += " "

        with output(initial_len=5, interval=0) as output_lines:
            while prgPointer < len(program):

                if args.debug:
                    sleep(args.debug)
                    cells = ""
                    for c in tape:
                        cells += f"{str(c).zfill(len(str(maxCellSize)))} "
                    output_lines[0] = f"Tape: {cells}"
                    output_lines[1] = "Ptr:  {}^".format((" " * (len(str(maxCellSize)) + 1)) * pointer)
                    output_lines[2] = f"Program: {program[prgPointer - 1:prgPointer + 71]}"
                    output_lines[3] = "          ^"
                    output_lines[4] = f"Output: {prints}"
                else:
                    print(f"Output: {prints}", end="\r")
                if program[prgPointer] == '>':
                    pointer += 1
                    if pointer >= len(tape):
                        tape.append(0)
                elif program[prgPointer] == '<':
                    pointer -= 1
                    if pointer < 0:
                        print("Error: Out Of Tape!")
                        exit(1)
                elif program[prgPointer] == '+':
                    tape[pointer] += 1
                    if tape[pointer] > maxCellSize + 1:
                        tape[pointer] = 0
                elif program[prgPointer] == '-':
                    tape[pointer] -= 1
                    if tape[pointer] < 0:
                        tape[pointer] = maxCellSize
                elif program[prgPointer] == '.':
                    if not args.intify:
                        prints += chr(tape[pointer])
                    else:
                        prints += str(int(tape[pointer]))
                elif program[prgPointer] == ',':
                    inp = input("Input: ")
                    tape[pointer] = ord(inp[0])
                elif program[prgPointer] == '[':
                    if tape[pointer] == 0:
                        bracket = 0
                        prgPointer += 1
                        while prgPointer < len(program):
                            if program[prgPointer] == ']' and bracket == 0:
                                break
                            if program[prgPointer] == '[':
                                bracket += 1
                            elif program[prgPointer] == ']':
                                bracket -= 1
                            prgPointer += 1
                elif program[prgPointer] == ']':
                    if tape[pointer] != 0:
                        bracket = 0
                        prgPointer -= 1
                        while prgPointer >= 0:
                            if program[prgPointer] == '[' and bracket == 0:
                                break
                            if program[prgPointer] == ']':
                                bracket += 1
                            elif program[prgPointer] == '[':
                                bracket -= 1
                            prgPointer -= 1
                prgPointer += 1

    except Exception as e:
        print("Error: Unknown Error")
        exit(1)


if __name__ == '__main__':
    parser()
