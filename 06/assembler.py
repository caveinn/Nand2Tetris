import argparse

from typing import List, Dict
from pprint import pprint


dest_map: Dict[str, str] = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
    "ADM": "111",
}

jump_map: Dict[str, str] = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

comp_map: Dict[str, str] = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "Z": "110000",
    "!D": "001101",
    "!Z": "110001",
    "-D": "001111",
    "-Z": "110011",
    "D+1": "011111",
    "Z+1": "110111",
    "D-1": "001110",
    "Z-1": "110010",
    "D+Z": "000010",
    "D-Z": "010011",
    "Z-D": "000111",
    "D&Z": "000000",
    "D|Z": "010101",
}

labels: Dict[str, int] = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}

symbols_map: Dict[str, str] = {}


def build_symbol_map(lines: List[str]) -> None:
    lines_count: int = 0
    for line in lines:
        line = line.strip()

        # handle comments
        comment_loc: int = line.find("//")
        line = line[:comment_loc] if comment_loc > -1 else line
        if not line:
            continue

        # handles 'A' commands
        if line[0] == '@':
            lines_count += 1

        # handles symbols
        elif line[0] == "(":
            symbol_name: str = line[1:-1]
            if symbols_map.get(symbol_name, None):
                print("ERROR")
            else:
                symbols_map[symbol_name] = bin(lines_count)[2:]
            continue
        # handles "C" commands
        else:
            lines_count += 1


def assemble(lines: List[str]) -> str:
    bin_lines: str = ''
    build_symbol_map(lines)
    ram_lines: int = 16
    for line in lines:

        digits: List[str] = [str(x) for x in range(10)]
        RS: List[str] = [f"R{x}" for x in range(16)]

        # handle comments
        comment_loc: int = line.find("//")
        line = line[:comment_loc] if comment_loc > -1 else line
        line = line.strip()
        if not line:
            continue

        # handles 'A' commands
        if line[0] == '@':
            bin_code = "0"
            val: str = line[1:].strip()
            if val[0] in digits:
                bin_code += bin(int(val))[2:]
            else:
                label: int = labels.get(val, None)
                if type(label) == int:
                    bin_code += bin(label)[2:]
                elif val in RS:
                    label = int(val[1:])
                    bin_code += bin(label)[2:]
                else:
                    if symbols_map.get(val, None):
                        bin_code += symbols_map[val]
                    else:
                        symbols_map[val] = bin(ram_lines)[2:]
                        bin_code += bin(ram_lines)[2:]
                        ram_lines += 1

        # handles symbols
        elif line[0] == "(":
            continue

        # handles "C" commands
        else:
            bin_code = "111"
            dest: str = ""
            comp: str = ""
            jump: str = ""
            if "=" in line:
                dest, comp = line.split("=")
            elif ";" in line:
                comp, jump = line.split(";")
            a: str = "1" if "M" in comp else "0"
            comp = comp.replace("A", "Z")
            comp = comp.replace("M", "Z")
            bin_code += a
            bin_code += comp_map[comp]
            bin_code += dest_map[dest]
            bin_code += jump_map[jump]
        bin_code = bin_code.rjust(16, "0")
        bin_lines += f"{bin_code}\n"
    return bin_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Assembler for Hack Programming Language")
    parser.add_argument("filename")
    filename = parser.parse_args().filename
    hack_code = ""
    with open(filename) as asm:
        lines = asm.readlines()
        hack_code = assemble(lines)
    with open("out.hack", "w") as hbin:
        hbin.write(hack_code)
