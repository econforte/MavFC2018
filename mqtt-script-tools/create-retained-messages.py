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

inputs={}
def on_message(client, userdata, message):
    time.sleep(1)
    if verbose:
        print("message received  ",str(message.payload.decode("utf-8")),\
          "topic",message.topic,"retained ",message.retain)
    if message.retain==1:
        retained_topics.append(message.topic)
    
    
def on_publish(client, userdata, mid):
    print("message published "  )


    
##############
def get_input(argv):
    _topics=[]

    try:
      opts, args = getopt.getopt(argv,"hb:p:t:c:v:u:p:")
    except getopt.GetoptError:
        print (sys.argv[0]," -b <broker> -p <port> -t <topic> -v \
<verbose True or False>,-m <Message>," )
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print (sys.argv[0]," -b <broker> -p <port> -t <topic> -v \
<verbose True or False>, -m <Message>," )
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
                
        elif opt == "-m":
            inputs["message"] = arg

    inputs["topic"] = _topics
    return(inputs)

#def main(argv):
    #get_input(argv)
#main start
USERNAME=""
PASSWORD=""
broker="192.168.1.184"
#broker="iot.eclipse.org"
##edit Topic list
topic_list=["house/room1/lights/bulb1",\
            "house/room1/lights/bulb2",\
            "house1/room1/temp","house1/room2/temp"]
port=1883
######
inputs={}
inputs["USERNAME"]=USERNAME
inputs["PASSWORD"]=PASSWORD
inputs["clear_retained"]=False
inputs["verbose"] =True
inputs["port"]=port
inputs["broker"]=broker
inputs["topic"]=""
inputs["message"]="retained message"

if __name__ == "__main__":
    import sys, getopt
    if len(sys.argv)>=2:
        inputs=get_input(sys.argv[1:])

verbose=inputs["verbose"]
print("verbose is ",verbose)

print("Creating client  with clean session set to ",CLEAN_SESSION)
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION) #create new instance
client.on_message=on_message        #attach function to callback
if inputs["PASSWORD"]:
    client.username_pw_set(username=inputs["USERNAME"],password=inputs["PASSWORD"])
client.connect(inputs["broker"])      #connect to broker
time.sleep(2)
client.loop_start()

tlist=[]
if inputs["topic"]:
    topic_list=[]
    if isinstance(inputs["topic"],str):
        topic_list.append(inputs["topic"])
    else:
        topic_list=inputs["topic"]

for t in topic_list:
    print("creating retained message on topic =",t)
    client.publish(t,inputs["message"],0,True) 


time.sleep(2)
client.loop_stop()
client.disconnect()
print("disconnecting")
print("Ending")


