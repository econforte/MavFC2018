###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
import paho.mqtt.client as mqtt  #import the client
import time
QOS0=0
QOS1=0
QOS2=0
RETAIN=True
CLEAN_SESSION=True
#List and optionally delete retained messages

inputs={}
retained_topics=[]
def on_message(client, userdata, message):
    time.sleep(1)
    if verbose:
        msg=str(message.payload.decode("utf-8"))
        topic=message.topic
        print("message received  ",msg,"topic",topic,"retained ",message.retain)
    if message.retain==1:
        retained_topics.append((topic,msg))
    
    
def on_publish(client, userdata, mid):
    print("message published "  )

def clear_retained(retained): #accepts single topic or list
    msg=""
    if isinstance(retained[0],str):
        client.publish(retained[0],msg,qos=QOS0,retain=RETAIN)
    else:
        try:
            for t in retained:
                client.publish(t[0],msg,qos=QOS0,retain=RETAIN)
                print ("Clearing retaind on ",msg,"topic -",t[0]," qos=",QOS0," retain=",RETAIN)
        except:
            Print("problems with topic")
            return -1
    
##############
def get_input(argv):
    _topics=[]

    try:
      opts, args = getopt.getopt(argv,"hb:p:t:c:v:u:p:")
    except getopt.GetoptError:
        print (sys.argv[0]," -b <broker> -p <port> -t <topic> -v \
<verbose True or False>, -c <clear retained True or False>," )
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print (sys.argv[0]," -b <broker> -p <port> -t <topic> -v \
<verbose True or False>, -c <clear retained True or False>," )
            sys.exit()
        elif opt == "-b":
            inputs["broker"] = str(arg)
        elif opt == "-u":
            inputs["USERNAME"] = str(arg)
        elif opt == "-p":
            inputs["PASSWORD"] = str(arg)
        elif opt =="-t":
            _topics.append(str(arg))
            
        elif opt =="-p":
         inputs["port"] = int(arg)
        elif opt == "-v":
            verbose=(str(arg)).lower()
            if verbose=="true" or verbose=="t":
                inputs["verbose"] =True
            else:
                inputs["verbose"] =False
                
        elif opt == "-c":
            clear_retained=(str(arg)).lower()
            if clear_retained=="true" or clear_retained=="t":
                inputs["clear_retained"] =True
            else:
                inputs["clear_retained"] =False
    inputs["topic"] = _topics
    return(inputs)


USERNAME=""
PASSWORD=""
port=1883
broker="192.168.1.184"
#broker="iot.eclipse.org"
topic_list=["#"]

port=1883
inputs={}
inputs["USERNAME"]=USERNAME
inputs["PASSWORD"]=PASSWORD
inputs["clear_retained"]=False
inputs["verbose"] =True
inputs["port"]=port
inputs["broker"]=broker
inputs["topic"]=""


if __name__ == "__main__":
    import sys, getopt
    if len(sys.argv)>=2:
        inputs=get_input(sys.argv[1:])

verbose=inputs["verbose"]
print("verbose is ",verbose)
print("Clear retained messages  is ",inputs["clear_retained"])

print("Creating client  with clean session set to ",CLEAN_SESSION)
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION) #create new instance
client.on_message=on_message        #attach function to callback
if inputs["PASSWORD"]:
    client.username_pw_set(username=inputs["USERNAME"],password=inputs["PASSWORD"])
client.connect(inputs["broker"])      #connect to broker
time.sleep(2)
client.loop_start()
time.sleep(2)

tlist=[]
if inputs["topic"]:
    if isinstance(inputs["topic"],str):
        topic=(inputs["topic"],0)
        tlist.append(topic)
    else:
        for t in inputs["topic"]:
            topic=(t,0)
            tlist.append(topic)
else:
    for t in topic_list:
        topic=(t,0)
        tlist.append(topic)

print("subscribing to topic ", tlist)    


client.subscribe(tlist)

time.sleep(10)#wait
if len(retained_topics)>0:
    print("Found these topics with possible retained messages")
    for t in retained_topics:
        print("topic =",t[0],"  Mesagge= ",t[1])
else:
    print("No topics with retained messages found")
    
if inputs["clear_retained"]:
    if len(retained_topics)>0:
        verbose=False
        clear_retained(retained_topics)
time.sleep(2)
client.loop_stop()
client.disconnect()
print("disconnecting")
print("Ending")


