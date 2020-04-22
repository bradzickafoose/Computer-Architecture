"""CPU functionality."""

import sys

## ALU ops
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b01100101
DEC = 0b01100110
CMP = 0b10100111
AND = 0b10101000
NOT = 0b01101001
OR  = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

## PC mutators
CALL = 0b01010000
RET  = 0b00010001
INT  = 0b01010010
IRET = 0b00010011
JMP  = 0b01010100
JEQ  = 0b01010101
JNE  = 0b01010110
JGT  = 0b01010111
JLT  = 0b01011000
JLE  = 0b01011001
JGE  = 0b01011010

## Other
NOP  = 0b00000000
HLT  = 0b00000001
LDI  = 0b10000010
LD   = 0b10000011
ST   = 0b10000100
PUSH = 0b01000101
POP  = 0b01000110
PRN  = 0b01000111
PRA  = 0b01001000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory (RAM)
        self.registers = [0] * 8  # 8 general-purpose CPU registers
        self.registers[7] = 0xf4
        self.pc = 0 # Program Counter, address of the currently executing instruction
        self.running = True


    def ram_read(self, address):
      return self.ram[address]

    def ram_write(self, address, value):
      self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.split('#')[0].strip()
                if line.startswith(('0', '1')) and len(line) == 8:
                    instruction = int(line, 2)
                    self.ram_write(address, instruction)
                    address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
          ir = self.ram_read(self.pc) # Instruction Register, contains a copy of the currently executing instruction
          inst_len = (ir >> 6) + 0b1
          operand_a = self.ram_read(self.pc+1)
          operand_b = self.ram_read(self.pc+2)

          if ir == LDI:
            self.registers[operand_a] = operand_b

          elif ir == PRN: # Print
            print(self.registers[operand_a])

          elif ir == MUL: # Multiply
            self.registers[operand_a] *= self.registers[operand_b]

          elif ir == HLT: # Halt
            self.running = False

          else:
            print(f"Unknown command {ir}")
            break

          self.pc += inst_len

