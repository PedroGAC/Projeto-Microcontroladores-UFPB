import tkinter as tk
from tkinter import filedialog, messagebox

def assemble(instruction):

    def to_twos_complement(value, bits):
        if value < 0:
            value = (1 << bits) + value
        return format(value, f'0{bits}b')

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
        reg = format(int(parts[3][1:]), '05b')
        func3 = '000'
        regDest = format(int(parts[1][1:]), '05b')
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
        reg1 = format(int(parts[2][1:]), '05b')
        regDest = format(int(parts[1][1:]), '05b')
        func3 = '000'
        opcode_bin = '0100011'
        endreg = '00000'
        zeros = '0000000'
        return f'{zeros}{reg1}{endreg}{func3}{regDest}{opcode_bin}'
    
    elif opcode == 'JMP':
        offset = to_twos_complement(int(parts[1]), 6)  # 6-bit offset
        opcode_bin = '1101111' 
        zeros = '0' * 19  
        return f'{offset}{zeros}{opcode_bin}'

    elif opcode == 'LOAD':
        reg1 = format(int(parts[2][1:]), '05b')
        regDest = format(int(parts[1][1:]), '05b')
        func3 = '000'
        opcode_bin = '0000011'
        endreg = '00000'
        complemento = '0000000'
        return f'{complemento}{reg1}{endreg}{func3}{regDest}{opcode_bin}'
    
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

    elif opcode == 'OUT':
        opcode_bin = '1110001'
        endreg = format(int(parts[1][1:]), '05b')
        complemento = 20 * '0'
        return f'{complemento}{endreg}{opcode_bin}'
    
    elif opcode == 'RESET':
        zeros = 25*'0'
        opcode_bin = '1010101'
        return f'{zeros}{opcode_bin}'

    elif opcode == 'MOV':
        func7 = '0000000'
        regDest = format(int(parts[1][1:]), '05b')  
        reg2 = '00000'
        reg1 = format(int(parts[2][1:]), '05b')     
        func3 = '000'
        opcode_bin = '0110011'
        return f'{func7}{reg2}{reg1}{func3}{regDest}{opcode_bin}'
    else:
        raise ValueError("Instrução desconhecida!")

def generate_code():
    assembly_code = assembly_input.get("1.0", tk.END).strip().splitlines()
    machine_code = []

    try:
        for instruction in assembly_code:
            machine_code.append(assemble(instruction))
        
        # Preencher com linhas de zeros até 64 linhas, se necessário
        while len(machine_code) < 64:
            machine_code.append('0' * 32)
        
        machine_code_output.config(state=tk.NORMAL)
        machine_code_output.delete("1.0", tk.END)
        machine_code_output.insert(tk.END, "\n".join(machine_code))
        machine_code_output.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Erro", str(e))

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(machine_code_output.get("1.0", tk.END).strip())
        messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")

root = tk.Tk()
root.title("Assembler Interface")

assembly_label = tk.Label(root, text="Código Assembly:")
assembly_label.grid(row=0, column=0, padx=10, pady=10)

assembly_input = tk.Text(root, height=20, width=50)
assembly_input.grid(row=1, column=0, padx=10, pady=10)

machine_code_label = tk.Label(root, text="Código de Máquina:")
machine_code_label.grid(row=0, column=1, padx=10, pady=10)

machine_code_output = tk.Text(root, height=20, width=50)
machine_code_output.grid(row=1, column=1, padx=10, pady=10)
machine_code_output.config(state=tk.DISABLED)

generate_button = tk.Button(root, text="Gerar Código", command=generate_code)
generate_button.grid(row=2, column=0, padx=10, pady=10)

save_button = tk.Button(root, text="Salvar Código", command=save_file)
save_button.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()