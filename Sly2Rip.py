#By FroggestSpirit
version="0.1"
#Scans eeMemory.bin from savestates of Sly 2 NTSC for model information
#Make backups, this can overwrite files without confirmation. To write files, uncomment the 3 lines starting with "#outfile"
import sys
import math
				
sysargv=sys.argv
echo=True
mode=0
print("Sly2 Rip "+version+"\n")
infileArg=-1;
outfileArg=-1;
for i in range(len(sysargv)):
	if(i>0):
		if(sysargv[i].startswith("-")):
			if(sysargv[i]=="-d" or sysargv[i]=="--decode"):
				mode=1
			elif(sysargv[i]=="-h" or sysargv[i]=="--help"):
				mode=0
		else:
			if(infileArg==-1): infileArg=i
			elif(outfileArg==-1): outfileArg=i
			
if(infileArg==-1):
	mode=0
else:
	if(outfileArg==-1):
		if(sysargv[infileArg].find(".bin")!=-1):
			if(mode==0): mode=1
			outfileArg=len(sysargv)
			sysargv.append(sysargv[infileArg].replace(".bin",".txt"))
		elif(sysargv[infileArg].find(".txt")!=-1):
			if(mode==0): mode=2
			outfileArg=len(sysargv)
			sysargv.append(sysargv[infileArg].replace(".txt",".bin"))
		else:
			mode=0
	else:
		if(sysargv[infileArg]==sysargv[outfileArg]):
			print("Input and output files cannot be the same")
			sys.exit()
if(mode==0): #Help
	print("Usage: "+sysargv[0]+" eeMemory.bin [mode] [output file] [flags]\nMode:\n\t-d\tDump info\n\t-h\tShow this help message\n")
	sys.exit()
elif(mode==1): #dump
    infile=open(sysargv[infileArg], "rb")
    ramFile=infile.read()
    infile.close()
    fileSize=len(ramFile)
    #outfile=open(sysargv[outfileArg],"w")
    filePos=0x180BF50
    modelNum=0
    modelLoc=[]
    modelHeader=0
    tempRead=0
    UVHeader=0
    UVCount=0
    vertexHeader=0
    vertexCount=0
    while(filePos<fileSize-4):
        if(ramFile[filePos]==0x00 and ramFile[filePos+1]==0xC0 and ramFile[filePos+2]==0x04 and ramFile[filePos+3]==0x6C):
            if(ramFile[filePos-16]==0x06 and ramFile[filePos-15]==0x00 and ramFile[filePos-14]==0x00 and ramFile[filePos-13]==0x10):
                modelHeader=ramFile[filePos+0x67]
                modelHeader*=0x100
                modelHeader+=ramFile[filePos+0x66]
                modelHeader*=0x100
                modelHeader+=ramFile[filePos+0x65]
                modelHeader*=0x100
                modelHeader+=ramFile[filePos+0x64]
                if(modelHeader<0x2000000):
                    if(ramFile[modelHeader]==0x09 and ramFile[modelHeader+1]==0xC0 and ramFile[modelHeader+2]==0x01 and ramFile[modelHeader+3]==0x6C):#model header
                        if(ramFile[modelHeader+0x198]==0x04 and ramFile[modelHeader+0x199]==0x01 and ramFile[modelHeader+0x19A]==0x00 and ramFile[modelHeader+0x19B]==0x01):#UV Mapping Header
                            UVHeader=modelHeader+0x198
                            UVCount=ramFile[UVHeader+0x6]#number of UV Coords
                            vertexHeader=UVHeader+8+(UVCount*4)#skip the 8 byte header plus the 4 bytes per UV coord
                            if((vertexHeader%0x10)>0):
                                vertexHeader+=0x10-(vertexHeader%0x10)#align to the next 0x10 multiple
                            vertexCount=ramFile[vertexHeader+0x2]#number of vertices
                            tempRead=ramFile[vertexHeader]#get the vertex header
                            tempRead*=0x100
                            tempRead+=ramFile[vertexHeader+0x1]
                            tempRead*=0x100
                            tempRead+=ramFile[vertexHeader+0x2]
                            tempRead*=0x100
                            tempRead+=ramFile[vertexHeader+0x3]
                            print("Model at: "+hex(filePos-16)+", Mesh at: "+hex(modelHeader)+"\n"+str(UVCount)+" UV coords at: "+hex(UVHeader)+"\n"+str(vertexCount)+" Vertices at: "+hex(vertexHeader)+" (header is "+hex(tempRead)+")\n")
                            modelLoc.append(filePos-16)
                            #outfile.write("Model at: "+hex(filePos-16)+", Mesh at: "+hex(modelHeader)+"\n"+str(UVCount)+" UV coords at: "+hex(UVHeader)+"\n"+str(vertexCount)+" Vertices at: "+hex(vertexHeader)+" (header is "+hex(tempRead)+")\n\n")
                            modelNum+=1
        filePos+=4
    print("Models found:"+str(modelNum))
    #outfile.close()