def assemble(instruction):
    parts = instruction.split()
    opcode = parts[0]
    
    if opcode == 'ADD':
        func7 = '0000000'
        regDest = format(int(parts[1][1:]), '05b')  
        reg2 = format(int(parts[3][1:]), '05b')
        reg1 = format(int(parts[2][1:]), '05b')     
        func3 = '000'
        opcode_bin = '0110011'
        return f'{func7}{reg2}{reg1}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'SUB':
        func7 = '0100000'
        regDest = format(int(parts[1][1:]), '05b')
        reg2 = format(int(parts[3][1:]), '05b')
        reg1 = format(int(parts[2][1:]), '05b')
        func3 = '000'
        opcode_bin = '0110011'
        return f'{func7}{reg2}{reg1}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'ADDi':
        func7 = '00'
        imediato = format(int(parts[2]), '010b')  
        reg = format(int(parts[1][1:]), '05b')
        func3 = '000'
        regDest = format(int(parts[3][1:]), '05b')
        opcode_bin = '0010011'
        return f'{func7}{imediato}{reg}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'SUBi':
        func7 = '01'
        imediato = format(int(parts[2]), '010b')  
        reg = format(int(parts[1][1:]), '05b')
        func3 = '000'
        regDest = format(int(parts[3][1:]), '05b')
        opcode_bin = '0010011'
        return f'{func7}{imediato}{reg}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'STORE':
        reg2 = format(int(parts[2][1:]), '05b')
        reg1 = format(int(parts[1][1:]), '05b')
        func3 = '000'
        opcode_bin = '0100011'
        endreg = '00000'
        complemento = '0000000'
        return f'{complemento}{reg2}{endreg}{func3}{reg1}{opcode_bin}'
    
    elif opcode == 'JMP':
        offset = format(int(parts[1]), '06b') # 6-bit offset
        opcode_bin = '1101111' 
        zeros = '0' * 19  
        return f'{offset}{zeros}{opcode_bin}'

    elif opcode == 'LOAD':
        reg2 = format(int(parts[2][1:]), '05b')
        reg1 = format(int(parts[1][1:]), '05b')
        func3 = '000'
        opcode_bin = '0000011'
        endreg = '00000'
        complemento = '0000000'
        return f'{complemento}{reg2}{endreg}{func3}{reg1}{opcode_bin}'
    
    elif opcode == 'DIV2':
        reg2 = format(int(parts[3][1:]), '05b')
        reg1 = format(int(parts[2][1:]), '05b')
        func3 = '001'
        opcode_bin = '0110011'
        endreg = format(int(parts[1][1:]), '05b')
        complemento = '0000000'
        return f'{complemento}{reg2}{reg1}{func3}{endreg}{opcode_bin}'
    
    elif opcode == 'MUL2':
        reg2 = format(int(parts[3][1:]), '05b')
        reg1 = format(int(parts[2][1:]), '05b')
        func3 = '101'
        opcode_bin = '0110011'
        endreg = format(int(parts[1][1:]), '05b')
        complemento = '0100000'
        return f'{complemento}{reg2}{reg1}{func3}{endreg}{opcode_bin}'
    
    elif opcode == 'RESET':
        zeros = 25*'0'
        opcode_bin = '1010101'
        return f'{zeros}{opcode_bin}'
    else:
        raise ValueError("Instrução desconhecida!")

instructions = [
    "ADDi R1 5 R1",
    "ADDi R1 5 R1",
    "ADDi R2 4 R0",
    "SUB R4 R5 R6",
    "ADDi R7 3 R8",
    "SUBi R9 5 R10",
    "STORE R11 R12 13",
    "JMP 10"
]

# Monta as instruções e escreve no arquivo txt
with open('output_instructions.txt', 'w') as f:
    for inst in instructions:
        binary_instruction = assemble(inst)
        f.write(binary_instruction + '\n')

    # Preenche as linhas restantes com zeros, se necessário
    remaining_lines = 64 - len(instructions)
    for _ in range(remaining_lines):
        f.write('0' * 32 + '\n')
        
print("Instruções montadas e salvas em 'output_instructions.txt'")
