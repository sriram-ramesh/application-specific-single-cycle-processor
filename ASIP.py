#***************************************************************
# Single Cycle Application Specific Processor for Cryptographic
# Block Cipher algorithms
# Author:   SRIRAM RAMESH
# Date:     02/28/2016
# Time:     12.30AM
# Status:   In-Progress
#***************************************************************

#Importing necessary modules

import binascii
import os
import sys
import re
import linecache
from array import array

#***************************************************************
# Global Variables Initialization so that they can be accessed
# everywhere in program as processor is split into 
# functions such as ALU, ControlUnit, DataMemory, RegisterFile,
# PC, InstMem etc., based on their operation.
#***************************************************************

ClockCounter=0                          #counter for clock cycles
WriteData3=0                            #WriteBack into Register File
ReadData2=0                             #Read Data in port2 of Register File
SignImm=0                               #Output of SignExtension
PCSrc=0                                 #PC+4 or PCBranch selection signal
Destination=0                           #Destination Address for WriteBack
ControlSignals=[1,0,0,0,0,0,1,0,1,0]    #Control Signals from Control Unit
Result=0                                #Output of Instruction Executed
Registers=['0']*22                     #Contains all the registers
line=0                                  #Indicates Line of instruction/data in memoryimage
NextInstruction='0000000000000000'      #Indicates NextInstruction to be executed PC'
CurrentInstruction=''                   #Indicates Current Instruction
FlagFunct=0                             #Flag to indicate Funct field in R-Type instruction needs to be looked at to decide ALU Operation
PCBranch=0                              #PC of Branched Instruction
BranchInstruction=''                    #Instruction from which Branch happens. Used to return to this Instruction+4 after branch completes
BranchFlag=0                            #Indicates Branching
BranchEnd=0                             #Indicates end of branch and to return to instruction from where it branched from+4
BranchBack=0                            #Indicates program has to go to the PC from where it branched 
Round=0                                 #Round count for IDEA
ClockCount=0                            #Global Clock
Temp=0                                  #Non-Archtectural 32bit Register
PCSrc=0
OpCode=0
BranchEnd1=0
BranchInstruction1=''
Branched1=0
lines=0
BranchBack1=0

#file= open("trace1.txt",'w')
#sys.stdout = file
#*************************************************************
#Function to Convert Hexadecimal Instruction or Data to Binary
#*************************************************************

def BinaryConverter(HexInput,length):
    BinOutput=array('i')
    for i in range(length):
        BinOutput.append((int(HexInput[i],16)))
    #Instruction is 8bits Hex 
    if(length==8):
        BinOutput=bin(BinOutput[0])[2:].zfill(4)+bin(BinOutput[1])[2:].zfill(4)+bin(BinOutput[2])[2:].zfill(4)+bin(BinOutput[3])[2:].zfill(4)+bin(BinOutput[4])[2:].zfill(4)+bin(BinOutput[5])[2:].zfill(4)+bin(BinOutput[6])[2:].zfill(4)+bin(BinOutput[7])[2:].zfill(4)
    return(BinOutput)

#**************************************************************
#Function that Fetches Instruction or Data from Image File
#'Instruction.txt' contains all the Instructions in Hex Format
#'Data.txt' contains all the Data in Hex Format
#**************************************************************

def Fetch(Instr):
    global Line
    global Registers
    global FlagFunct
    global IoD
    #IoD determines Instruction or Data to be Fetched
    if(IoD==1):
        #Fetches Instruction from the address indicated by Line
        Instr= linecache.getline('trial.txt', Line)
        Instr=Instr.rstrip('\n')
        print("Instruction Fetched",Instr)
    #If it is not Instruction Fetch it can be DataFetch from
    #Data Image or Register Access
    else:
        #Register Access
        if(FlagFunct==1):
            return(Registers[Line])
        elif(IoD==0):
            #Fetches Data from the address indicated by Line
            Instr=linecache.getline('data.txt', Line)
            Instr=Instr.rstrip('\n')
            print("Data Fetched",Instr)
    length=len(Instr)
    #Hex to Binary Conversion done by BinaryConverter()
    Instr=BinaryConverter(Instr,length)
    #Setting Recursion limit of Python to avoid Recursion Error
    sys.setrecursionlimit(1000000)
    return (Instr)


#**************************************************************
#ProgramCounter-16bit Register. Its output,'PC', points to the
#Current Instruction. Its Input,'NextInstruction', indicates the
#address if the next instruction. It is a Synchronous Sequential
#circuit which operates only on rising clock edge.
#**************************************************************

def ProgramCounter(NextInstruction):
    orig_stdout = sys.stdout
##    f=open('exrace.txt', 'w')
##    sys.stdout=f
    global ClockCounter
    ClockCounter=ClockCounter+1
    print("ClockCount",ClockCounter)
    print("At PositiveEdge Clock")
    #Current Instruction=Next Instruction
    PC=NextInstruction
    print ("ProgramCounter",PC)
    #Function call with PC as an argument
    #to Instruction Memory
##    sys.stdout=orig_stdout
##    f.close()
    InstructionMemory(PC)

#***************************************************************
#InstructionMemory-Has Single Read Port. Takes 16bit instruction
#address input,'Instruction', and reads the 16bit instruction 
#from address onto read data output 'Instr'
#***************************************************************

def InstructionMemory(PC):
    global IoD
    global Line
    global CurrentInstruction
    global FlagFunct
    global BranchEnd
    global BranchFlag
    global BranchBack
    global Registers
    global OpCode
    global Branched1
    global BranchEnd1
    global BranchBack1
    global lines
    #IoD=1 indicates Instruciton Fetch from Instruction.txt
    IoD=1
    #Determining Instruction to be fetched using PC as line indicator in instruction image
    Line=int(PC,2)+1
    lines=Line
    #Handles Branch
    #BranchFlag Indicates Branch operation
    if((BranchFlag!=1)&(Branched1==1)):
        if(Line==249):
            BranchEnd1=1
            Nextinstruction()
        else:
            BranchEnd1=0
    elif((BranchFlag==1)):
        #Loop is from Instruction 8 till Instrcution 21. So after Instruction 21 is executed
        #it has to go back to Instruction from where it branch from.Therefore Line=22*4+1=89
        if(Line==85):
            #Indicates loop has ended 
            BranchEnd=1
            #So goes to next instruction which will be instruction from it branched+4
            Nextinstruction()
        else:
            BranchEnd=0

    #If branch condition met it fetches the new PC
    #Appropriate branch flags are reset
    if((BranchBack==1)):
        BranchEnd=0
        BranchBack=0
        Instr=Fetch(PC)
    elif(BranchBack1==1):
        #Function Call for Instruction Fetch using PC
        Instr=Fetch(PC)
        BranchEnd1=0
        BranchBack1=0
    else:
        Instr=Fetch(PC)
    #Saving Current Instruction    
    CurrentInstruction=Instr

    #Determines OpCode which indicates Instruction operation.
    OpCode=int(CurrentInstruction[0:4],2)

    #If Halt Instruction is fetched, Exit execution
    if(OpCode==8):
        print("Halt Encountered, Program Execution Stopped!!")
        #Built-In function to stop program execution
        sys.exit(0)
    else:
        #Register Access if FlagFunct=1
        #Except load, store, halt and load address all operations are register access
        #Opcode 1,2,8,9 indicates load, store, halt and load address respectively
        if((OpCode==1)|(OpCode==2)|(OpCode==8)|(OpCode==9)):
            FlagFunct=0
        else:
            FlagFunct=1
        #Function Call with 'Instr' as argument to Control Unit
        ControlUnit(Instr[0:4],Instr[24:32])
        #Function Call with 'Instr' as argument for calculating
        #SignExtension and Destination Address
        SEandD(Instr)
        #Function Call with 'Instr' as argument to Register File
        RegisterFile(Instr)

#****************************************************************************
#Computes Control Signals from Instruction
#Format: |MemReg|MemWrite|Branch|ALUControl[2:0]|ALUSrc|RegDst|RegWrite|Jump|
#Index:     0       1        2   3     4     5      6      7      8      9 
#****************************************************************************

def ControlUnit(Op,Funct):
    
    global ControlSignals
    #Control Signal for ADD,SUB,MUL,OR,AND,XOR,MULMOD,ADDMOD respectively
    #Control Signal '2' is assigned instead of "Dont-Care"
    if(Op=='0000'):
        if(Funct=='10000000'):
            ControlSignals=[0,0,0,0,0,0,0,1,1,0]
        elif(Funct=='10000010'):
            ControlSignals=[0,0,0,0,0,1,0,1,1,0]
        elif(Funct=='10000011'):
            ControlSignals=[0,0,0,0,1,0,0,1,1,0]
        elif(Funct=='10000100'):
            ControlSignals=[0,0,0,0,1,1,0,1,1,0]
        elif(Funct=='10000101'):
            ControlSignals=[0,0,0,1,0,0,0,1,1,0]
        elif(Funct=='10000110'):
            ControlSignals=[0,0,0,1,0,1,0,1,1,0]
        elif(Funct=='10000111'):
            ControlSignals=[0,0,0,1,1,0,0,1,1,0]
        elif(Funct=='10001000'):
            ControlSignals=[0,0,0,1,1,1,0,1,1,0]
    #Control Signal for LOAD and LA
    elif((Op=='0001')|(Op=='1001')):
        ControlSignals=[1,0,0,0,0,0,1,0,1,0]
    #Control Signal for STORE
    elif(Op=='0010'):
        ControlSignals=[2,1,0,0,0,0,1,2,0,0]
    #Control Signal for BZ, BEQ, BP, BN, BNE
    elif((Op=='0011')|(Op=='0100')|(Op=='0101')|(Op=='0110')|(Op=='1100')):
        ControlSignals=[2,0,1,0,0,1,0,2,0,0]
    #Control Signal for JUMP
    elif(Op=='0111'):
       ControlSignals=[2,0,2,2,2,2,2,2,0,1]
    #Control Signal for HALT
    elif(Op=='1000'):
       ControlSignals=[2,2,2,2,2,2,2,2,2,2]
    #Control Signal for ADDIU
    elif((Op=='1011')):
        ControlSignals=[0,0,0,0,0,0,1,0,1,0]
    #Control Signal for SUBIU
    elif((Op=='1010')):
        ControlSignals=[0,0,0,0,0,1,1,0,1,0]
    print ("Control Signal",ControlSignals)
        
#***************************************************************
#SignExtend and Destination Register
#***************************************************************
def SEandD(Instr):
    global SignImm
    global Destination
    global ControlSignals
    #Sign Immediate
    SignImm=Instr[16:32]
    print ("SignImmediate",SignImm)
    #Sign Extend to 32bits. SignImm[0]denotes MSB
    SignExtend=(SignImm[0]*16)+SignImm

    #Determining Destination Register
    if(ControlSignals[7]==1):
        #For R-Type Instruction Destination denoted by Instruction[14:18] 
        Destination=Instr[14:19]
    else:
        #For I-Type Instruction Destination denoted by Instruction[9:13]
        Destination=Instr[9:14]
    print("Destination Register",Destination)
    if(ControlSignals[9]==1):
        Nextinstruction()

#**************************************************************
#RegisterFile- 2Readports and 1Writeport. 5bit input address
#given to readports. They read register values on output ports
#respectively
#**************************************************************
def RegisterFile(Instr):
    global ReadData2
    global CurrentInstruction
    global FlagFunct
    global IoD
    global Line
    global flag
    global Temp1
    global Temp2
    global ClockCounter
    global ControlSignals
    #ReadPort1 of Register File. Address Input1
    A1=Instr[4:9]
    #ReadPort2 of Register File. Address Input2
    A2=Instr[9:14]
    IoD=0
    #Indicates Register Access
    if(FlagFunct==1):
        #CurrentInstruction[4:9] is Source1
        Line=int(CurrentInstruction[4:9],2)
        ReadData1=Fetch(Line)
        print("ReadData",ReadData1)
        #CurrentInstruction[9:14] is Source2
        Line=int(CurrentInstruction[9:14],2)
        ReadData2=Fetch(Line)
    else:    
        Line=int(A1,2)+1
        IoD=0
        #Fetching Data from Address given by A1 and A2
        Temp1=Fetch(int(A1,2))
        Temp2=Fetch(int(A2,2))
        ReadData1=Temp1[0:16]
        ReadData2=Temp2[0:16]
    #Readport3 of Register File
    #Indicates Address at which Result must be written
    #Denoted by Destination calculated from SEandD()
    A3=Destination
    #At positive edge clock
    #Data at Address A1 in Register File
    print("At positive edge clock")
    ClockCounter=ClockCounter
    SrcA=ReadData1
    print ("SrcA",SrcA)
    #Unless if instruction is load store or immediate SrcB equals readdata
    if(ControlSignals[6]==0):
        SrcB=ReadData2
    #If load store or immediate operation SrcB is SignImmediate value
    elif(ControlSignals[6]==1):
        SrcB=SignImm
    else:
        SrcB=ReadData2
    print ("SrcB",SrcB)
    #Determining if Instruction is Load
    #If so 32bits are fetched and written 16bits at a time
    lw=int(CurrentInstruction[0:4],2)
    #lw=1,9 indicates load word and load address respectively
    #flag indicates it is load instruction
    if(((lw==1)|(lw==9))):
        flag=1
    #Function Call to ALU with SrcA and SrcB as arguments
    ALU(SrcA,SrcB)

#**************************************************************************
#Write operation in Register File. Address to be written at is denoted by
#Destination calculated at SEandD() and Data to be written is 'Result' or
#'upperload'(incase of load instruction alone).
#**************************************************************************
def WriteBack():
    global Destination
    global ClockCounter
    global Registers
    global ControlSignals
    global upperload
    global flag
    global Line
    global lines
    #ControlSignals[8] indicates RegWrite. If asserted then write into Register
    if(ControlSignals[8]==1):
        D=int(Destination,2)
        Registers[D]=Result
        print("Register File:")
        for i in Registers:
            print(hex(int(i,2))[2:].zfill(4),end=',')
        print("\n")
        #flag=1 indicates load operation where data[16:32] has to be written
        if(flag==1):
            ClockCounter=ClockCounter+1
            print("ClockCount",ClockCounter)
            print("Processor State remains same")
            print("Loading Data[16:32] fetched from same instruction")
            print("At positive edge of Clock")
            #Loading data[16:32] at next clock edge
            Registers[D+1]=upperload
            flag=0
            print("Register File:")
            for i in Registers:
                print(hex(int(i,2))[2:].zfill(4),end=',')
            print("\n")
        if(lines==245):
             with open("data.txt", "a") as myfile:
                myfile.write("\n\n\n\n")
                myfile.write(hex(int(Registers[12],2))[2:])
                myfile.write(hex(int(Registers[13],2))[2:])
                myfile.write(hex(int(Registers[14],2))[2:])
                myfile.write(hex(int(Registers[15],2))[2:])
    Nextinstruction()
#******************************************************************************
#Function to determine next instruction. It can be next instruciton in file and
#branch instruction or jump instruction which needs to be handled differenty
#******************************************************************************
def Nextinstruction():
    global PCBranch
    global SignImm
    global NextInstruction
    global BranchEnd
    global BranchInstruction
    global BranchBack
    global BranchFlag
    global PCSrc
    global CurrentInstruction
    global Branched1
    global BranchInstruction1
    global BranchEnd1
    global BranchBack1
    global PCJump
    #Calculating PCBranch
    #Relative Addressing by left shifting SignImm by 2 bits(or multiply by 4 and modulus)
    PCJump=bin((int(SignImm,2)*4))[2:].zfill(16)
    PCBranch=bin((int(SignImm,2)*4)%(32568))[2:].zfill(16)
    if(CurrentInstruction[0:4]=='0101'):
         Branched1=1
         BranchInstruction1=NextInstruction
    elif(CurrentInstruction[0:4]=='1100'):
        BranchFlag=1
    if(BranchEnd1==1):
         NextInstruction=bin(int(BranchInstruction1,2)+int('0000000000000100',2))[2:].zfill(16)
         Branched1=0
         BranchEnd1=0
         BranchBack1=1
    #If Branch loop has ended next instruction is Instruction from where it branched+4
    #'0000000000000100' indicates integer value of 4
    elif(BranchEnd==1):
        print(int(BranchInstruction,2))
        NextInstruction=bin(int(BranchInstruction,2)+int('0000000000000100',2))[2:].zfill(16)
        BranchBack=1
        BranchFlag=0
        InstructionMemory(NextInstruction)
    #Branch if PCSrc=1
    elif(PCSrc==1):
        global Round
        global i
        global Line
        print("PCBranch",PCBranch)
        #Saving Instruction from which Branch Occurs in 'BranchInstruction'
        BranchInstruction=NextInstruction
        #NextInstruction will be equal to the PCBranch calculated
        NextInstruction=PCBranch
    #Else NextInstruction=NextInstruction+4
    else:
        NextInstruction=bin(int(NextInstruction,2)+int('0000000000000100',2))[2:].zfill(16)
    print("********************************************************************************")
    if(ControlSignals[9]==1):
        print("PCJump",PCJump)
        NextInstruction=PCJump
    else:
        NextInstruction=NextInstruction
    #Function Call to Program Counter with Next Instruction
    ProgramCounter(NextInstruction)

#*******************************************************************************************
#Arithmetic and Logic Unit. Takes two arguments SrcA,SrcB and based on Control Signals[3:6]
#which denotes ALUOP does 1 of 8 operations in ADD,SUB,MUL,OR,AND,XOR,MODMUL,ADDMUL
#*******************************************************************************************

def ALU(SrcA,SrcB):
    global BranchFlag
    global ClockCounter
    global PCSrc
    global OpCode
    global Result
    global CurrentInstruction
    #ADDITION
    if(ControlSignals[3:6]==[0,0,0]):
        print("ADDITION OPERATION")
        ALUResult=bin(int(SrcA,2)+int(SrcB,2))[2:].zfill(16)
    #SUBTRACTION
    elif(ControlSignals[3:6]==[0,0,1]):
        print("SUBTRACTION OPERATION")
        ALUResult=bin(int(SrcA,2)-int(SrcB,2))[2:].zfill(16)
    #MULTIPLICATION
    elif(ControlSignals[3:6]==[0,1,0]):
        print("MULTIPLICATION OPERATION")
        ALUResult= bin(int(SrcA,2)*int(SrcB,2))[2:].zfill(16)
    #LOGICAL OR
    elif(ControlSignals[3:6]==[0,1,1]):
        print("LOGICAL OR OPERATION")
        ALUResult= bin(int(SrcA,2)|int(SrcB,2))[2:].zfill(16)
    #LOGICAL AND
    elif(ControlSignals[3:6]==[1,0,0]):
        print("LOGICAL AND OPERATION")
        ALUResult=bin(int(SrcA,2)&int(SrcB,2))[2:].zfill(16)
    #LOGICAL XOR
    elif(ControlSignals[3:6]==[1,0,1]):
        print("LOGICAL XOR OPERATION")
        ALUResult=bin(int(SrcA,2)^int(SrcB,2))[2:].zfill(16)
    #MULTIPLICATION MODULUS
    elif(ControlSignals[3:6]==[1,1,0]):
        ClockCounter=ClockCounter+3
        print("MULTIPLICATION MODULUS OPERATION")
        #All-Zero condition on inputs. If input zero it is considered as 2^16
        if(int(SrcA,2)==0):
            SrcA='1111111111111111'
        elif(int(SrcB,2)==0):
            SrcB='1111111111111111'
        R32bit=(bin(int(SrcA,2)*int(SrcB,2))[2:].zfill(32))
        Hi=int(((R32bit[16:32])),2)
        Lo=int(R32bit[0:16],2)
        if(Hi>Lo):
            ALUResult=bin(Hi-Lo)[2:].zfill(16)
        else:
            ALUResult=bin(Hi-Lo+65537)[2:].zfill(16)
        #All-one condition on outputs. If output is all 1 then it is considered as all zero
        if(int(ALUResult,2)=='1111111111111111'):
            ALUResult='0000000000000000'
    #ALUResult=bin((int(SrcA,2)*int(SrcB,2))%65537)[2:].zfill(16)
    #ADDITION MODULUS
    elif(ControlSignals[3:6]==[1,1,1]):
        print("ADDITION MODULUS OPERATION")
        ALUResult=bin((int(SrcA,2)+int(SrcB,2))%65536)[2:].zfill(16)
    print ("ALUResult",ALUResult)
    #ZERO FLAG
    if(int(ALUResult,2)==0):
        Zero=1
    else:
        Zero=0
    print("ZeroFlag",Zero)
    #Select Signal 'PCSrc' for multiplexer to choose between PC+4 and PCBranch
    if(int(ALUResult,2)>0):
        Positive=1
        Negative=0
    else:
        Negative=1
        Positive=0
    #If Instruction is for BEQ or BZ
    if((CurrentInstruction[0:4]=='0011')|(CurrentInstruction[0:4]=='0100')):
        PCSrc=(ControlSignals[2]&((Zero)))
    #If Instruction is for BP
    elif((CurrentInstruction[0:4])=='0101'):
        PCSrc=(ControlSignals[2]&((Positive)))
    #If Instruction is for BN
    elif((CurrentInstruction[0:4])=='0110'):
        PCSrc=(ControlSignals[2]&((Negative)))
     #If Instruction is for BNE
    else:
        PCSrc=(ControlSignals[2]&(not(Zero)))
    print("PCSrc",PCSrc)
    #If MemtoReg is '0' Result is ALUResult
    if(ControlSignals[0]==0):
        Result=ALUResult
        WriteBack()
    #If MemtoReg is '1' Result is Data Read from memory
    elif(ControlSignals[0]==1):
        DataMemory(ALUResult)
    #If MemWrite is '1' the it is store instruction
    elif(ControlSignals[1]==1):
        DataMemory(ALUResult)
    #Else denotes Branch Instruction or Jump
    else:
        WriteBack()

#********************************************************************************
#Has Single read/write port. If WriteEnable is 1 then it writes Data into address
#indicated by ALUResult on rising edge of clock. If WriteEnable is 0 then reads
#data in address ALUResult onto output ReadData.
#********************************************************************************
def DataMemory(ALUResult):
    global IoD
    global Line
    global flag
    global upperload
    global Result
    global ControlSignals
    global ReadData2
    global Registers
    
    #Indicates Fetch from Data.txt
    IoD=0
    #Indicates position of register in RegisterFile
    Line=int(ALUResult,2)
    #Load Word Operation or R-Type I-Type or Immediate Instruction
    if(ControlSignals[1]==0):
        #Value fetched from RegisterFile
        ReadData3=Fetch(int(ALUResult,2))
        ReadData=ReadData3[0:16]
        #Data[16:32] stored in upperload in case of load instruction
        upperload=ReadData3[16:32]
        print ("ReadData",ReadData)
    #Store Word Operation
    elif(ControlSignals[1]==1):
       Write=Registers[Line]
       print("At Positive edge Clock")
       print("Storing word in memory")
       with open("data.txt", "a") as my:
            my.write("\n\n\n\n")
            my.write(str(hex(int(Write,2)))[2:].zfill(4))        
    #Multiplexer which selects between ReadData and ALUResult
    #based on Control Signal MemtoReg
    if(ControlSignals[1]==1):
        WriteData=Registers[Line]
        Nextinstruction()
    elif(ControlSignals[0]=='0'):
        Result=ALUResult
    else:
        Result=ReadData
    print ("Result",Result)
    if(ControlSignals[1]==0):
        #Calling writeback function to update Result onto Register File
        WriteBack()
    #If Store Instruction was executed no need to go to write back stage
    #Goes to NextInstruction()
    else:
        NextInstruction()
#KickStarting the Program by Calling ProgramCounter()
ProgramCounter('0000000000000000')
#file.close()

