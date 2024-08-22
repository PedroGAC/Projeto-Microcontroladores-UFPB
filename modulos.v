module ALU( A, B, ALUcontrol_In, ALUResult, zero);

input [31:0] A,B;
input [3:0] ALUcontrol_In;
output reg zero;
output reg [31:0] ALUResult;

always @ (ALUcontrol_In or A or B)
begin
    case (ALUcontrol_In)
        4'b0000: begin zero<=0; ALUResult<=A&B; end
        4'b0001: begin zero<=0; ALUResult<=A|B; end
        4'b0010: begin zero<=0; ALUResult<=A+B; end
        4'b0110: begin if(A==B) zero<=1; else zero<=0; ALUResult<=A-B; end
        default: begin zero<=0; ALUResult<=A; end
    endcase
end

endmodule

module ALU_Control(ALUOp, funct7, funct3, ALUControl_out);

    input [1:0] ALUOp;
    input funct7;
    input [2:0] funct3;
    output reg [3:0] ALUControl_out;

    always @(*) begin
        case ({ALUOp, funct7, funct3})
            6'b00_0_000 : ALUControl_out <= 4'b0010; // ADD
            6'b01_0_000 : ALUControl_out <= 4'b0110; // SUB
            6'b10_0_000 : ALUControl_out <= 4'b0010; // ADD aritmetica
            6'b10_1_000 : ALUControl_out <= 4'b0110; // SUB aritmetica
            6'b10_0_111 : ALUControl_out <= 4'b0000; // AND aritmetica
            6'b10_0_110 : ALUControl_out <= 4'b0001; // OR  aritmetica
            default: ALUControl_out <= 4'b0000; // Handle invalid inputs
        endcase
    end

endmodule 

module And(branch, zero, andout);

    input branch, zero;
    output andout;
    
    assign andout = branch & zero;

endmodule 

module Control_Unit ( Opcode,Branch,MemRead,MemtoReg,MemWrite,ALUSrc,RegWrite, ALUOp);

    input [6:0] Opcode;
    output reg Branch,MemRead,MemtoReg,MemWrite,ALUSrc,RegWrite;
    output reg [1:0] ALUOp;

    always @(*)
    begin
        case (Opcode)
            7'b0110011: // R-type instruction
            begin 
                ALUSrc <= 0;
                MemtoReg <= 0;
                RegWrite <= 1;
                MemRead <= 0;
                MemWrite <= 0;
                Branch <= 0;
                ALUOp <= 2'b10;
            end

            7'b0000011: // Load instruction
            begin 
                ALUSrc <= 1;
                MemtoReg <= 1;
                RegWrite <= 1;
                MemRead <= 1;
                MemWrite <= 0;
                Branch <= 0;
                ALUOp <= 2'b00;
            end

            7'b0100011: // Store instruction
            begin 
                ALUSrc <= 1;
                MemtoReg <= 0;
                RegWrite <= 0;
                MemRead <= 0;
                MemWrite <= 1;
                Branch <= 0;
                ALUOp <= 2'b00;
            end

            7'b1100011: // Branch-equal instruction
            begin 
                ALUSrc <= 0;
                MemtoReg <= 0;
                RegWrite <= 0;
                MemRead <= 0;
                MemWrite <= 0;
                Branch <= 1;
                ALUOp <= 2'b01;
            end

				7'b0010011: // ADDi (soma com imediato)
            begin 
                ALUSrc <= 1;
                MemtoReg <= 0;
                RegWrite <= 1;
                MemRead <= 0;
                MemWrite <= 0;
                Branch <= 0;
                ALUOp <= 2'b10;
            end
				
            default: // same as R-type
            begin 
                ALUSrc <= 0;
                MemtoReg <= 0;
                RegWrite <= 1;
                MemRead <= 0;
                MemWrite <= 0;
                Branch <= 0;
                ALUOp <= 2'b10;
            end
        endcase
    end

endmodule 

module Data_Memory(clk, reset, MemWrite, MemRead, address, Writedata, Data_out);

    input clk, reset, MemWrite, MemRead;
    input [31:0] address, Writedata;
    output [31:0] Data_out;

    reg [31:0] DataMemory [63:0];
    assign Data_out = (MemRead) ? DataMemory[address] : 32'b0;

    integer k;
    always @(posedge clk)
    begin
        if (reset == 1'b1) begin
            for (k = 0; k < 64; k = k + 1)
                DataMemory[k] = 32'b0;
        end
        else if (MemWrite) begin
            DataMemory[address] = Writedata;
        end
    end

endmodule 

module immediate_Generator (
    input [6:0] Opcode,
    input [31:0] instruction,
    output reg [31:0] ImmExt
);

always @* begin
    case (Opcode)
        7'b0010011: ImmExt = {{20{instruction[31]}}, instruction[31:20]};  // I instruction
        7'b0100011: ImmExt = {{20{instruction[31]}}, instruction[31:25], instruction[11:7]};  // S instruction
		  7'b1100011: ImmExt = {{19{instruction[31]}}, instruction[31], instruction[7], instruction[30:25], instruction[11:8], 1'b0};  // B instruction
        default: ImmExt = {{22{instruction[29]}}, instruction[29:20]};  // Default case for other instructions
    endcase
end

endmodule 

module Instruction_Memory(clk, reset, read_address, Instructions_out);

	input clk, reset;
	input [31:0] read_address;
	output [31:0] Instructions_out;
	reg [31:0] Imemory [63:0];
	integer k;
	
	initial begin
		$readmemb("teste.txt", Imemory);
	end
	
	assign Instructions_out = Imemory[read_address];
	/*always @(posedge clk)
	begin
		 if (reset == 1'b1) begin
			  for (k=0; k<64; k=k+1)
			Imemory[k] = 32'b0;end
	end*/
endmodule 

module Mux1(Sel, A1, B1, Mux1_out);

    input Sel;
    input [31:0] A1, B1;
    output [31:0] Mux1_out;
    
    assign Mux1_out = (Sel == 1'b0) ? A1 : B1;

endmodule 

module Mux2(Sel, A2, B2, Mux2_out);

    input Sel;
    input [31:0] A2, B2;
    output [31:0] Mux2_out;
    
    assign Mux2_out = (Sel == 1'b0) ? A2 : B2;

endmodule 

module Mux3(Sel, A3, B3, Mux3_out);

    input Sel;
    input [31:0] A3, B3;
    output [31:0] Mux3_out;
    
    assign Mux3_out = (Sel == 1'b0) ? A3 : B3;

endmodule 

module PCplus4(fromPC, NexttoPC);

	input  [31:0] fromPC;
	output [31:0] NexttoPC;

	// No livro, é somado + 4. Para o que esperávamos, precisa somar 1
	assign NexttoPC = fromPC + 32'h00000001;

endmodule 

// Módulo do Program_Counter
module Program_Counter (clk, reset, PC_in, PC_out);

input clk, reset;
input [31:0] PC_in;
output reg [31:0] PC_out;
always @ (posedge clk)
begin
    if(reset==1'b1)
        PC_out <= 32'h0;
    else
        PC_out <= PC_in;
end
endmodule

module Register_File(clk, reset, RegWrite, Rs1, Rs2, Rd, Write_data, Read_data1, Read_data2);

input clk, reset, RegWrite;
input [4:0] Rs1, Rs2, Rd;
input [31:0] Write_data;
output [31:0] Read_data1, Read_data2;

reg [31:0] Registers [31:0];
integer k;

always @(posedge clk) begin
    if (reset == 1'b1) begin
        for (k = 0; k < 32; k = k + 1) begin
            Registers[k] = 32'h0;
        end
    end
    else if (RegWrite == 1'b1) begin
        Registers[Rd] = Write_data;
    end
end

assign Read_data1 = Registers[Rs1];
assign Read_data2 = Registers[Rs2];

endmodule 

module seletor_bits (
    input [31:0] data_in,
    output [6:0] instruction_control,
	 output [4:0] intruction_r_register1,
	 output [4:0] intruction_r_register2,
	 output [4:0] instruction_w_register
);

assign instruction_control = data_in[6:0];
assign intruction_r_register1 = data_in[19:15];
assign intruction_r_register2 = data_in[24:20];
assign instruction_w_register = data_in[11:7];

endmodule 

module seletor_bits_2 (
    input [31:0] data_in,
	 output func7,
	 output [2:0] func3
);

assign func7 = data_in[30];
assign func3 = data_in[14:12];

endmodule 

module PC_Next(
    input [31:0] fromPC,
    input [31:0] Imediato,
    input jump,
    output [31:0] NexttoPC
);

    assign NexttoPC = jump ? (fromPC + Imediato) : (fromPC + 32'd1);

endmodule