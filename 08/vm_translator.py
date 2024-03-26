import argparse
import pathlib
import os

from typing import Dict

heap_pointer: int = 2048


def code_to_push_to_stack(value:str) -> str:
    #TODO add push code here
    pass

def remove_comments(line: str) -> str:
    n_line = line.split("//")[0]
    return n_line.strip()

def write_call(return_adr: str, args: str, f_name: str) -> str:
        #push return adress
        asm_code = ""
        asm_code += f"@{return_adr}\nD=A\n"
        asm_code += f"@SP\nA=M\nM=D\n"
        asm_code += f"@SP\nM=M+1\n"

        # push LCL
        asm_code += f"@LCL\nD=M\n"
        asm_code += f"@SP\nA=M\nM=D\n"
        asm_code += f"@SP\nM=M+1\n"

        #push ARG
        asm_code += f"@ARG\nD=M\n"
        asm_code += f"@SP\nA=M\nM=D\n"
        asm_code += f"@SP\nM=M+1\n"

        #push THIS
        asm_code += f"@THIS\nD=M\n"
        asm_code += f"@SP\nA=M\nM=D\n"
        asm_code += f"@SP\nM=M+1\n"

        #push THAT
        asm_code += f"@THAT\nD=M\n"
        asm_code += f"@SP\nA=M\nM=D\n"
        asm_code += f"@SP\nM=M+1\n"

        # arg = sp -n-5
        tmp =  int(args) + 5
        asm_code +=f"@{tmp}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n"
        
        #LCL = sp
        asm_code +=f"@SP\nD=M\n@LCL\nM=D\n"

        # goto f
        asm_code += f"@{f_name}\n0;JMP\n"

        asm_code += f"({return_adr})\n"

        return asm_code

def translate_vm_line_to_assembly(line: str, line_no: int, file_name: str) -> str:
    assembly_code = f"//{line}\n"
    line = remove_comments(line)
    # assembly_code: str = ""
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

    elif line.startswith("label"):
        label: str = line.split()[1] 
        assembly_code += f"({label})\n"
    elif line.startswith("goto"):
        label: str = line.split()[1]
        assembly_code += f"@{label}\n0;JMP\n"
    elif line.startswith("if-goto"):
        label: str = line.split()[1]
        assembly_code += f"@SP\nA=M-1\n"
        assembly_code += f"D=M\n"
        assembly_code += f"@SP\nM=M-1\n"
        assembly_code += f"@{label}\nD;JNE\n"
    
    elif line.startswith("function"):
        _, f_name, n_of_local_vars = line.split()
        assembly_code += f"({f_name})\n"
        for _ in range(int(n_of_local_vars)):
            assembly_code += f"@SP\nA=M\nM=0\n"
            assembly_code += f"@SP\nM=M+1\n"
    
    elif line.startswith("call"):
        _, f_name, args = line.split()
        return_adr: str = f_name + f".ret.{line_no}"
        assembly_code += write_call(return_adr, args, f_name)
        

    elif line.startswith("return"):
        assembly_code += f"@LCL\nD=M\n@R13\nM=D\n"
        # RET = Frame -5
        assembly_code += f"@5\nD=A\n@R13\nA=M-D\nD=M\n@R14\nM=D\n"
        # ARG = POP
        assembly_code += f"@SP\nA=M-1\n"
        assembly_code += f"D=M\n"
        assembly_code += f"@SP\nM=M-1\n"
        assembly_code += f"@ARG\nA=M\nM=D\n"
        # assembly_code += f"@ARG\nM=D\n"

        #sp= arg+1 
        assembly_code +=  f"@ARG\nD=M+1\n@SP\nM=D\n"
        #THAT = FRAME-1
        assembly_code +=  f"@R13\nA=M-1\nD=M\n@THAT\nM=D\n"
        #THIS = FRAME-2
        assembly_code +=  f"@2\nD=A\n@R13\nA=M-D\nD=M\n@THIS\nM=D\n"
        #ARG = FRAME-3
        assembly_code +=  f"@3\nD=A\n@R13\nA=M-D\nD=M\n@ARG\nM=D\n"
        #LCL = FRAME-4
        assembly_code +=  f"@4\nD=A\n@R13\nA=M-D\nD=M\n@LCL\nM=D\n"
        assembly_code +=  f"@R14\nA=M\n0;JMP\n"


    return assembly_code


def translate_vm_file_to_assembly(vm_file: pathlib.Path) -> str:
    """
    params:
        vm_file -> file to be translated
    return:
        A string of the translated content
    """
    asm_code = ""
    with open(vm_file, "r") as vm:
        vm_code = vm.readlines()
        for line_no, line in enumerate(vm_code):
            asm_code += translate_vm_line_to_assembly(
                line=line.strip(), line_no=line_no, file_name=vm_file.stem
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
    asm_code = "@256\nD=A\n@SP\nM=D\n"
    asm_code += write_call(f_name="Sys.init", args="0", return_adr=f"Sys.init.ret..")
    # if file is path check it has a .vm file
    if source_path.is_dir():
        for f in os.listdir(source):
            if f.endswith(".vm"):
                n_source = os.path.join(source, f)
                n_source_path: pathlib.Path = pathlib.Path(n_source)
                asm_code += translate_vm_file_to_assembly(n_source_path)
        out_name = os.path.join(source_path, source_path.stem)
        with open(f"{out_name}.asm", "w") as out_f:
            out_f.write(asm_code)

    elif source.endswith(".vm"):
        asm_code += translate_vm_file_to_assembly(source_path)
    
        out_name = source_path.stem
        out_name = os.path.join(source_path.parent, out_name)
        with open(f"{out_name}.asm", "w") as out_f:
            out_f.write(asm_code)

    else:
        print(
            "The source should be a .vm file or a folder containing at least one .vm file"
        )
