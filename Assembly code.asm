#loading address
la R0,R0,0x00000001
#loading data
#Data is 32 bits in data image so 2 loads will give 4 Data
lw R0,R1,0x00000005
lw R0,R3,0x00000009
#Outer loop for 1024 bit encyption iteration
LOOP1:
	#Keys are loaded. data image is 32bits so 6keys loaded
	lw R0,R5,0x0000000D
	lw R0,R7,0x00000011
	lw R0,R9,0x00000015
	#Inner loop for 8 rounds in IDEA algorithm
	LOOP2:
		#R11 stores the count for rounds=8
		addi R0,R11,0X00000008
		#R12=(R1*R5)%65537
		modmul R1,R5,R12
		#R13=(R2+R6)%65536
		addmul R2,R6,R13
		#R14=(R3+R7)%65536
		addmul R3,R7,R14
		#R15=(R4*R8)%65537
		modmul R4,R8,R15
		#R16=R12^R14
		xor R12,R14,R16
		#R17=R13^R15
		xor R13,R15,R17
		#R18=(R16*R9)%65537
		modmul R16,R9,R18
		#R19=(R18*R17)%65536
		addmul R18,R17,R19
		#R20=(R19*R10)%65537
		modmul R19,R10,R20
		#R21=(R20*R18)%65536
		addmul R20,R18,R21
		#R22=R12^R20
		xor R12,R20,R22
		#R23=R13^R21
		xor R13,R21,R23
		#R24=R14^R20
		xor R14,R20,R24
		#R25=R21^R15
		xor R15,R21,R25
	#Loading next set of keys for round2
	lw R0,R5,0x00000019
	lw R0,R7,0x0000001D
	lw R0,R9,0x00000021
	#Subtracting the round counter by 1. R11=7 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #rOUND2
	#Loading next set of keys for round2
	lw R0,R5,0x00000025
	lw R0,R7,0x00000029
	lw R0,R9,0x0000002D
	#Subtracting the round counter by 1. R11=6 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #ROUND3
	#Loading next set of keys for round2
	lw R0,R5,0x00000031
	lw R0,R7,0x00000035
	lw R0,R9,0x00000039
	#Subtracting the round counter by 1. R11=5 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #ROUND4
	#Loading next set of keys for round2
	lw R0,R5,0x0000003D
	lw R0,R7,0x00000041
	lw R0,R9,0x00000045
	#Subtracting the round counter by 1. R11=4 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #ROUND5
	#Loading next set of keys for round2
	lw R0,R5,0x00000049
	lw R0,R7,0x0000004D
	lw R0,R9,0x00000051
	#Subtracting the round counter by 1. R11=3 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #ROUND6
	#Loading next set of keys for round2
	lw R0,R5,0x00000055
	lw R0,R7,0x00000059
	lw R0,R9,0x0000005D
	#Subtracting the round counter by 1. R11=2 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #ROUND7
	#Loading next set of keys for round2
	lw R0,R5,0x00000061
	lw R0,R7,0x00000065
	lw R0,R9,0x00000069
	#Subtracting the round counter by 1. R11=1 after sub
	subi R0,R11,0x00000001
	#Branching to Loop2 if Rounter count is not equal to R0
	bne R11,R0, LOOP2 #ROUND8
	#Loading next set of keys for round2
	lw R0,R5,0x0000006D
	lw R0,R7,0x00000071
	#Encrypted keys stored in R22,R23,R24,R25
	modmul R1,R5,R22
	addmul R3,R6,R23
	addmul R2,R7,R24
	modmul R4,R8,R25
#128bit encryption over
#Has to be repeated 15 more times to encrypt 1024bits
#So loading next set of data. Keys remain the same
lw R0,R1,0x00000075
lw R0,R3,0x00000079
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat2
#Loading data for next 128bit encryption
lw R0,R1,0x0000007D
lw R0,R3,0x00000081
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat3
#Loading data for next 128bit encryption
lw R0,R1,0x00000085
lw R0,R3,0x00000089
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat4
#Loading data for next 128bit encryption
lw R0,R1,0x0000008D
lw R0,R3,0x00000091
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat5
#Loading data for next 128bit encryption
lw R0,R1,0x00000095
lw R0,R3,0x00000099
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat6
#Loading data for next 128bit encryption
lw R0,R1,0x0000009D
lw R0,R3,0x000000A1
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat7
#Loading data for next 128bit encryption
lw R0,R1,0x000000A5
lw R0,R3,0x000000A9
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat8
#Loading data for next 128bit encryption
lw R0,R1,0x000000AD
lw R0,R3,0x000000B1
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1#Repeat9
#Loading data for next 128bit encryption
lw R0,R1,0x000000B5
lw R0,R3,0x000000B9
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1#Repeat10
#Loading data for next 128bit encryption
lw R0,R1,0x000000BD
lw R0,R3,0x000000C1
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1#Repeat11
#Loading data for next 128bit encryption
lw R0,R1,0x000000C5
lw R0,R3,0x000000C9
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1#Repeat12
#Loading data for next 128bit encryption
lw R0,R1,0x000000CD
lw R0,R3,0x000000D1
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1#Repeat13
#Loading data for next 128bit encryption
lw R0,R1,0x000000D5
lw R0,R3,0x000000D9
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1#Repeat14
#Loading data for next 128bit encryption
lw R0,R1,0x000000DD
lw R0,R3,0x000000E1
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat15
#Loading data for next 128bit encryption
lw R0,R1,0x000000E5
lw R0,R3,0x000000E9
#Branching to loop1 if R0 is positive
bp R11,R0,LOOP1 #Repeat16
#Program execution stops with halt
halt 
