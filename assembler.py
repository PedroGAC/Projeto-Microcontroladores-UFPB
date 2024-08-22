def assemble(instruction):
    # Split instruction into its components
    parts = instruction.split()
    opcode = parts[0]
    
    if opcode == 'ADD':
        func7 = '0000000'
        regDest = format(int(parts[1][1:]), '05b')  # R1 -> regDest
        reg2 = format(int(parts[2][1:]), '05b')     # R2 -> reg2
        reg1 = format(int(parts[3][1:]), '05b')     # R3 -> reg1
        func3 = '000'
        opcode_bin = '0110011'
        return f'{func7}{reg1}{reg2}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'SUB':
        func7 = '0100000'
        regDest = format(int(parts[1][1:]), '05b')  # R1 -> regDest
        reg2 = format(int(parts[2][1:]), '05b')     # R2 -> reg2
        reg1 = format(int(parts[3][1:]), '05b')     # R3 -> reg1
        func3 = '000'
        opcode_bin = '0110011'
        return f'{func7}{reg1}{reg2}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'ADDi':
        imediato = format(int(parts[2]), '012b')  # 12-bit immediate value
        reg = format(int(parts[1][1:]), '05b')
        func3 = '000'
        regDest = format(int(parts[3][1:]), '05b')
        opcode_bin = '0010011'
        return f'{imediato}{reg}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'SUBi':
        imediato = format(int(parts[2]), '012b')  # 12-bit immediate value
        reg = format(int(parts[1][1:]), '05b')
        func3 = '000'
        regDest = format(int(parts[3][1:]), '05b')
        opcode_bin = '0010011'
        return f'{imediato}{reg}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'STORE':
        imm_part1 = format(int(parts[3]), '07b')
        reg2 = format(int(parts[2][1:]), '05b')
        reg1 = format(int(parts[1][1:]), '05b')
        func3 = '000'
        imm_part2 = format(int(parts[3]), '05b')
        opcode_bin = '0100011'
        return f'{imm_part1}{reg1}{reg2}{func3}{imm_part2}{opcode_bin}'
    
    elif opcode == 'JMP':
        # Extrai o deslocamento e converte para binário com 6 bits
        offset = format(int(parts[1]), '06b')  # 6-bit offset
        opcode_bin = '1101111'  # Opcode de 7 bits
        zeros = '0' * 19  # 19 bits de zeros
        
        # Combina tudo em uma instrução de 32 bits
        return f'{offset}{zeros}{opcode_bin}'

    else:
        raise ValueError("Instrução desconhecida!")

# Lista de instruções para serem convertidas
instructions = [
    "ADDi R1 5 R1"
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
        f.write('0' * 32 + '\n')  # Preenche com 32 zeros

print("Instruções montadas e salvas em 'output_instructions.txt'")
