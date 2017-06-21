###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
mqtt pinger
"""
import paho.mqtt.client as mqtt
import time
import json
##user can edit thhis data

mqttclient_log=True
max_connection_time=6 # if not connected after this time assume failure
cname="pinger"
msg="ping test:" +cname
topic="pingtest"
broker="loopback"
port=1883
inputs={"broker":broker,"port":port,"topic":"pingtest","loops":\
        4,"loop_delay":1,"silent_flag":False}
username=""
password=""
mqttclient_log=False
##end user editable data
responses=[]
sent=[]
###
#username="toyerbnp"
#password="JUlkU47AEy8o"
#broker="m21.cloudmqtt.com"
#port=17363
####



def on_connect(client, userdata, flags, rc):
    client.connected_flag=True
    print("connected sending ",inputs["loops"]," messages ",\
          inputs["loop_delay"]," second Intervals")

def on_disconnect(client, userdata, rc):
    m="disconnecting reason  "  ,str(rc)
    client.connect_flag=False
    client.disconnect_flag=True
    
def on_subscribe(client, userdata, mid, granted_qos):
    client.suback_flag=True
def on_publish(client, userdata, mid):
    client.puback_flag=True

    

def on_message(client, userdata, message):
    topic=message.topic
    msgr=str(message.payload.decode("utf-8"))
    responses.append(json.loads(msgr))
    client.rmsg_count+=1
    client.rmsg_flagset=True

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def Initialise_client_object():  
    mqtt.Client.bad_connection_flag=False
    mqtt.Client.connected_flag=False
    mqtt.Client.disconnect_flag=False
    mqtt.Client.disconnect_time=0.0
    mqtt.Client.disconnect_flagset=False
    mqtt.Client.rmsg_flagset=False
    mqtt.Client.rmsg_count=0
    mqtt.Client.display_msg_count=0

def Initialise_clients(cname):
    #flags set
    client= mqtt.Client(cname)
    if mqttclient_log: #enable mqqt client logging
        client.on_log=on_log
    client.on_connect= on_connect        #attach function to callback
    client.on_message=on_message        #attach function to callback
    client.on_disconnect=on_disconnect
    client.on_subscribe=on_subscribe
    client.on_publish=on_publish
    return client 



def get_input(argv):
    broker_in=""
    port_in=0
    topics_in=""
    try:
      opts, args = getopt.getopt(argv,"hb:p:t:c:d:s:")
    except getopt.GetoptError:
        print (sys.argv[0]," -b <broker> -p <port> -t <topic> -c <count> \
-d <delay>-s <silent> True/False" )
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print (sys.argv[0]," -b <broker> -p <port> -t <topic> -c <count> \
-d <delay>-s <silent> True/False" )
            sys.exit()
        elif opt == "-b":
         inputs["broker"] = str(arg)
        elif opt =="-t":
         inputs["topic"] = str(arg)
        elif opt =="-p":
         inputs["port"] = int(arg)
        elif opt =="-c":
         inputs["loops"] = int(arg)
        elif opt =="-d":
         inputs["loop_delay"] =int(arg)
        elif opt == "-s":
         silent=(str(arg)).lower()
         if silent=="true":
             inputs["silent_flag"] =True

    return((broker_in,port_in,topics_in))

#def main(argv):
    #get_input(argv)
#main start
if __name__ == "__main__":
    import sys, getopt
    if len(sys.argv)>=2:
        get_input(sys.argv[1:])
###
Initialise_client_object()
#client= mqtt.Client(cname)       #create client object
client=Initialise_clients(cname)
if username!="":
    client.username_pw_set(username=username,password=password)
print("connecting to broker ",inputs["broker"],"on port ",inputs["port"],\
      " topic",inputs["topic"])
try:
    res=client.connect(inputs["broker"],inputs["port"])           #establish connection
except:
    print("can't connect to broker",inputs["broker"])
    sys.exit()
if res !=0:
    print("connection failure ",res," to broker",inputs["broker"])
    sys.exit()
#print("connection result",res)
#client.on_connect= on_connect 
client.loop_start()
tstart=time.time()
while not client.connected_flag:
    time.sleep(.5)


        
if inputs["silent_flag"]:
    print ("Silent Mode is on")    
client.subscribe(inputs["topic"])
count=0
tbegin=time.time()

try:
    while count<inputs["loops"]:
        wait_response_flag=True
        client.rmsg_flagset=False 
        count+=1
        m_out=json.dumps((msg,count))
        sent.append(m_out)
        if not inputs["silent_flag"]:
            print("sending:",m_out)
        client.publish(inputs["topic"],m_out)    #publish
        tstart=time.time()
        #print("flags " ,wait_response_flag,client.rmsg_flagset)
        while wait_response_flag:
            if responses and client.rmsg_flagset:
                ttrip=time.time()-tstart
                if not inputs["silent_flag"]:
                    print("received:",responses.pop(0),"time= %2.3f"%ttrip)
                wait_response_flag=False


        time.sleep(inputs["loop_delay"]-ttrip)
except KeyboardInterrupt:
    print("interrrupted by keyboard")



print("Total time= %2.3f"%(tbegin-time.time()))
print("Total sent=",count)
print("Total received=",client.rmsg_count)
time.sleep(2)
client.disconnect()
client.loop_stop()
time.sleep(2)
