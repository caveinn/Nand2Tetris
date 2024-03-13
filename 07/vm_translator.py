import argparse
import pathlib
import os

from typing import Dict

heap_pointer: int = 2048


def code_to_push_to_stack(value:str) -> str:
    #TODO add push code here
    pass

def translate_vm_line_to_assembly(line: str, line_no: int, file_name: str) -> str:
    # assembly_code = f"//{line}\n"
    assembly_code: str = ""
    # handle memory access
    if line.startswith("push") or line.startswith("pop"):
        command, segment, index = line.split()

        if segment == "constant":
            if command == "push":
                assembly_code += f"@{index}\nD=A\n@SP\nA=M\nM=D\n"
                assembly_code += f"@SP\nM=M+1\n"
            else:
                # handle pop constants
                pass
        elif segment in (
            "argument",
            "local",
            "this",
            "that",
        ):
            mem_location = {
                "argument": "ARG",
                "local": "LCL",
                "this": "THIS",
                "that": "THAT",
            }
            
            if command == "push":
                assembly_code += f"@{index}\nD=A\n"
                assembly_code += f"@{mem_location[segment]}\nA=M+D\nD=M\n"
                assembly_code += f"@SP\nA=M\nM=D\n"
                assembly_code += f"@SP\nM=M+1\n"
            else:
                assembly_code += f"@{index}\nD=A\n"
                assembly_code += f"@R13\nM=D\n"
                assembly_code += f"@{mem_location[segment]}\nD=M\n"
                assembly_code += f"@R13\nM=M+D\n"
                assembly_code += f"@SP\nA=M-1\nD=M\n"
                assembly_code += f"@R13\nA=M\nM=D\n"
                assembly_code += f"@SP\nM=M-1\n"
        elif segment in ("pointer", "temp"):
            seg_command: str = ""
            if segment == "pointer":
                seg_command = "THIS" if index == "0" else "THAT"
            else:
                seg_command = f"R{5+int(index)}"
            if command == "push":
                assembly_code += f"@{seg_command}\nD=M\n"
                assembly_code += f"@SP\nA=M\nM=D\n"
                assembly_code += f"@SP\nM=M+1\n"
            else:
                assembly_code += f"@SP\nA=M-1\nD=M\n"
                assembly_code += f"@{seg_command}\nM=D\n"
                assembly_code += f"@SP\nM=M-1\n"
        elif segment == "static":
            if command == "push":
                assembly_code += f"@{file_name}.{index}\nD=M\n"
                assembly_code += f"@SP\nA=M\nM=D\n"
                assembly_code += f"@SP\nM=M+1\n"
            else:
                assembly_code += f"@SP\nA=M-1\nD=M\n"
                assembly_code += f"@{file_name}.{index}\nM=D\n"
                assembly_code += f"@SP\nM=M-1\n"

    elif line in ("add", "sub", "and", "or", "lt", "eq", "gt"):
        operator: Dict[str, str] = {
            "add": "+",
            "sub": "-",
            "and": "&",
            "or": "|",
            "eq": "JEQ",
            "lt": "JLT",
            "gt": "JGT",
        }
        # pop x
        assembly_code += f"@SP\nA=M-1\n"
        assembly_code += f"D=M\n"
        assembly_code += f"@SP\nM=M-1\n"
        # pop y
        assembly_code += f"@SP\nA=M-1\n"
      

        # add/subtract
        if line in ("add", "sub", "and", "or"):
            assembly_code += f"D=M{operator[line]}D\n"
            # push solution
            assembly_code += f"@SP\nA=M-1\nM=D\n"
        # handle comparisons
        else:
            line_label = line + str(line_no)
            assembly_code += f"D=M-D\n"
            assembly_code += f"@{line_label}.true\n"
            assembly_code += f"D;{operator[line]}\n"
            # push solution
            assembly_code += f"@SP\nA=M-1\nM=0\n"
            assembly_code += f"@{line_label}.false\n"
            assembly_code += f"0;JMP\n"
            # jump if true
            assembly_code += f"({line_label}.true)\n"
            assembly_code += f"@SP\nA=M-1\nM=-1\n"
            assembly_code += f"({line_label}.false)\n"

    elif line in ("neg", "not"):
        operator: Dict[str] = {"neg": "-", "not": "!"}
        # pop y
        assembly_code += f"@SP\nA=M-1\n"
        assembly_code += f"D=M\n"
        assembly_code += f"@SP\nM=M-1\n"
        # push solution
        assembly_code += f"@SP\nA=M\nM={operator[line]}D\n"
        assembly_code += f"@SP\nM=M+1\n"

    return assembly_code


def translate_vm_file_to_assembly(vm_file: str, base_name:str) -> str:
    """
    params:
        vm_file -> file to be translated
    return:
        A string of the translated content
    """
    asm_code = "@256\nD=A\n@SP\nM=D\n"
    with open(vm_file, "r") as vm:
        vm_code = vm.readlines()
        for line_no, line in enumerate(vm_code):
            asm_code += translate_vm_line_to_assembly(
                line=line.strip(), line_no=line_no, file_name=base_name
            )
    return asm_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Jack VM",
        description="converts virtual machine code to hack assembly language",
    )

    parser.add_argument("source")

    source: str = parser.parse_args().source
    source_path: pathlib.Path = pathlib.Path(source)

    # if file is path check it has a .vm file
    if source_path.is_dir():
        for f in os.listdir(source):
            if f.endswith(".vm"):
                # TODO: Handle all files that are vms.
                break

    elif source.endswith(".vm"):
        out_name = source_path.stem
        parent = source_path.parent
        asm_code = translate_vm_file_to_assembly(source, out_name)
        out_name = os.path.join(parent, out_name)
        with open(f"{out_name}.asm", "w") as out_f:
            out_f.write(asm_code)

    else:
        print(
            "The source should be a .vm file or a folder containing at least one .vm file"
        )
