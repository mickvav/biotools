#!/usr/bin/python

class FullGenome:
    files=[]
    contexts={}
    filename=""
    def __init__(self,filename):
        counter=-1
        self.filename=filename
        with open(filename,"r") as f:
            buff=""
            for line in f:
                if(line[0] == '>'):
                    if(len(buff) > 0):
                        self.files[counter].write(buff)
                    counter+=1
                    self.files.append(open(filename + "." + str(counter),"rw+"))
                    self.pushcontexts(counter,buff)
                else:
                    line=line.strip()
                    buff=buff+line
            if(len(buff) > 0):
                self.files[counter].write(buff)
                self.pushcontexts(counter,buff)
        for i in self.contexts:
            self.contexts[i].close()

    def pushcontexts(self,nchr,buff):
        for i in range(0,len(buff)-2):
            context=buff[i:i+3]
            if not(context in self.contexts):
                self.contexts[context]=open(self.filename+"_"+context,"w")
            self.contexts[context].write(str(nchr)+"\t"+str(i+2)+"\n")


    def getcontext(self,nchr,npos):
        self.files[nchr].seek(npos-2)
        return self.files[nchr].read(3)


