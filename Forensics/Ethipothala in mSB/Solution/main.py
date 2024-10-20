import os
import binascii
import sys
from PIL import Image

def help(func=None):
    if func is None:
        print("Usage:\n\tsbPy [OPTIONS] [FILE]")
        print("\nOptions:\n\t-t=<lsb or msb or mSB>, --type=<lsb or msb or mSB>:\n\t\tChoose between read LSB, MSB, or mSB (Default is LSB)\n\n\t-o=<Order sigle>, --order=<Order sigle>:\n\t\tRead the lsb or msb in the specify order (Default is RGB)\n\n\t-out=<Output name>, --output=<Output name>\n\t\tChoose the name of the output file (Default is outputSB)\n\n\t-e=<Row or Column>, --extract=<Row or Column>\n\t\tChoose between extracting by row or column (Default is Column)\n\n\t-b=<7 bits of your choice>, --bits=<7 bits of your choice>\n\t\tChoose the bits you want to extract info (Have higher priority than '--type or -t')")
    return

def extractBin(strInput, bits):
    strInput = strInput[2:]
    outputList = []

    while len(strInput) < 8:
        strInput = "0" + strInput

    for i in range(0, 8):
        if bits[i] == '1':
            outputList.append(strInput[i])
    return outputList

def writeResults(outputFile, dataBin):
    with open(outputFile + ".txt", "w") as resultFile:
        size = len(dataBin)
        for i in range(0, size, 8):
            value = int("".join(dataBin[i:i + 8]), 2)
            if 32 <= value <= 126:
                resultFile.write(chr(value))
        resultFile.write("\n")

def getSB(file, ord, outFile, ext, bits):
    dataBin = []
    with Image.open(file) as img:
        width, height = img.size
        xPattern = height
        yPattern = width
        if ext == "ROW":
            xPattern = width
            yPattern = height
        for x in range(0, xPattern):
            for y in range(0, yPattern):
                if ext == "ROW":
                    pixel = list(img.getpixel((x, y)))
                else:
                    pixel = list(img.getpixel((y, x)))

                R = extractBin(bin(pixel[0]), bits)
                G = extractBin(bin(pixel[1]), bits)
                B = extractBin(bin(pixel[2]), bits)
                if ord == "RGB":
                    dataBin.extend(R)
                    dataBin.extend(G)
                    dataBin.extend(B)
                elif ord == "RBG":
                    dataBin.extend(R)
                    dataBin.extend(B)
                    dataBin.extend(G)
                elif ord == "GRB":
                    dataBin.extend(G)
                    dataBin.extend(R)
                    dataBin.extend(B)
                elif ord == "GBR":
                    dataBin.extend(G)
                    dataBin.extend(B)
                    dataBin.extend(R)
                elif ord == "BRG":
                    dataBin.extend(B)
                    dataBin.extend(R)
                    dataBin.extend(G)
                else:
                    dataBin.extend(B)
                    dataBin.extend(G)
                    dataBin.extend(R)
    writeResults(outFile, dataBin)
    print("Done, check the output file!")

def checkParameters(file, parameters):
    order = 'RGB'  # Default
    sbType = 'LSB'  # Default
    outputFile = "outputSB"  # Default
    extract = "COLUMN"  # Default
    bitsSelection = None

    if file.find(".") == -1:
        print(f"INPUT ERROR: Unrecognized file type for '{file}'")
        exit()

    for param in parameters:
        if param in ("--help", "-h"):
            help()
            exit()
        elif param.startswith("-o="):
            order = param[3:].upper()
            if len(order) > 3 or any(c not in "RGB" for c in order):
                print(f"INPUT ERROR: Parameter '{order}' is invalid")
                exit()
        elif param.startswith("--order="):
            order = param[8:].upper()
            if len(order) > 3 or any(c not in "RGB" for c in order):
                print(f"INPUT ERROR: Parameter '{order}' is invalid")
                exit()
        elif param.startswith("-t="):
            sbType = param[3:].upper()
            if sbType not in ("LSB", "MSB", "mSB"):
                print(f"INPUT ERROR: Type '{sbType}' Not recognized")
                exit()
        elif param.startswith("--type="):
            sbType = param[7:].upper()
            if sbType not in ("LSB", "MSB", "mSB"):
                print(f"INPUT ERROR: Type '{sbType}' Not recognized")
                exit()
        elif param.startswith("-out="):
            outputFile = param[5:]
        elif param.startswith("--output="):
            outputFile = param[9:]
        elif param.startswith("-b="):
            bitsSelection = param[3:]
            if len(bitsSelection) != 8 or int(bitsSelection, 2) == 0:
                print(f"INPUT ERROR: Parameter 'bits' Expected 8 bits")
                exit()
        elif param.startswith("--bits="):
            bitsSelection = param[7:]
            if len(bitsSelection) != 8 or int(bitsSelection, 2) == 0:
                print(f"INPUT ERROR: Parameter 'bits' Expected 8 bits")
                exit()
        elif param.startswith("-e="):
            extract = param[3:].upper()
        elif param.startswith("--extract="):
            extract = param[10:].upper()
        else:
            print(f"INPUT ERROR: Parameter '{param}' Not recognized")
            exit()

    if bitsSelection is None:
        if sbType == "LSB":
            bitsSelection = "00000001"
        elif sbType == "MSB":
            bitsSelection = "10000000"
        elif sbType == "mSB":
            bitsSelection = "00001000"  # Middle significant bit

    getSB(file, ord=order, outFile=outputFile, ext=extract, bits=bitsSelection)

def main():
    if len(sys.argv) < 2:
        help()
        return
    elif len(sys.argv) == 2 and (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        help()
        return
    checkParameters(sys.argv[-1], sys.argv[1:-1])

if __name__ == "__main__":
    main()
