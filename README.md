# BrainFuck interpreter
![](https://img.shields.io/pypi/v/brainfuck-swimmy4days) ![](https://img.shields.io/pypi/l/brainfuck-swimmy4days) ![](https://img.shields.io/codacy/grade/54cf04f725fd4d06a26f0c1a3aa02e13)
- A simple to use, open source brainfuck interpreter
- Easy to run
- Optional debugger
- Changeable  cell size
- Print as an integer insted of ASCII 
- And mush more features

# What is BrainFuck?
brainfuck is an esoteric programming language with only 8 oparetions

|operation  | Explanation|
|- | -|
|`>` |  increment the data pointer.|
|`<` | decrement the data pointer.|
|`+` | increment the byte at the data pointer.|
|`-`  | decrement the byte at the data pointer.|
|`.` | output the byte at the data pointer.|
|`,` | accept one byte of input, storing its value in the byte at the data pointer.|
|`[` |if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching `]` command.|
|`]` |if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching `[` command.|

[More Information](https://en.wikipedia.org/wiki/Brainfuck)

[Even More Information](https://esolangs.org/wiki/Brainfuck)

#### To download the required packages in order to run the source type in the shell 
`$ python -m pip install -r requirements.txt`

Made by [@swimmy4days](https://github.com/swimmy4days).
