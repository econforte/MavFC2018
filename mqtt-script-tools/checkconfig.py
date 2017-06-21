###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
Mosquitto config file checker
"""
infile="mosquitto.conf"
outfile=infile
lines=[]
inputs=dict()
def check_lines(lines):
    for x,line in enumerate(lines):
        #print(line)
        line=line.strip()
        if len(line)>0:
            if line[0]=="#":
                pass
            else:
                print(line,"   ######Line Number",x+1)
    
def write_lines(outfile): #not implemented yet

    with open(outfile,"w") as fo :      
            fo.writelines(lines)

def get_lines(infile):
    try:
        with open(infile) as fo :
            for line in fo:
                lines.append(line)

    except FileNotFoundError as e:
        print("file not found ",e)
        sys.exit(2)

def get_input(argv):
    inputs["filein"]=""
    try:
      opts, args = getopt.getopt(argv,"f:")
    except getopt.GetoptError:
        print (sys.argv[0]," -f<config file default mosquitto.conf>")
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print (sys.argv[0]," -f<config file default mosquitto.conf>")
            sys.exit()
        elif opt == "-f":
            inputs["filein"] = str(arg)

#main
if __name__ == "__main__":
    import sys, getopt
    if len(sys.argv)>=2:
        get_input(sys.argv[1:])
        if inputs["filein"]!="":
            infile=inputs["filein"]
        
get_lines(infile)
check_lines(lines)



             
         

