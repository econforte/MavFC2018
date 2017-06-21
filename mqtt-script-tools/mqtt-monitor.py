###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
Simple mqtt monitor
"""
import paho.mqtt.client as mqtt
import os
import time
import sys, getopt
import logging
import queue
import random
##### User configurable data section
time_stop=0 #set to 0 for infinite loop
username=""
password=""
display=True #set to show received messages on screen
verbose=True #True to display all messages, False to display ony changed messages
debug_log=False
brokers=["192.168.1.184","192.168.1.186","192.168.1.204","broker.hivemq.com",\
         "test.mosquitto.org"]
topics=[]
broker=brokers[0]
port=1883
####
topic_ack=[] #used to check for all subscriptions
sub_flag=""
keepalive=60
message_count=0
message_count2=0
message_q=queue.Queue()
messages=dict()
last_message=dict()
r=random.randrange(1,10000)
cname="monitor-"+str(r)

def has_changed(topic,m_rxd):
    global last_message
    if topic not in last_message:
        last_message[topic]=m_rxd
        return(0)
    else:
        if last_message[topic]==m_rxd: #no change
            return 1
        else:
            last_message[topic]=m_rxd #set last message
            return 0 # return 0 to output
               


########################

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id  "+str(client)
    logging.info(m)
    client.connected_flag=True

def on_disconnect(client, userdata, rc):

    logging.info("disconnecting reason  "+str(rc))
    client.connect_flag=False
    client.disconnect_flag=True
   

def on_subscribe(client,userdata,mid,granted_qos):
    logging.info("in on subscribe callback result "+str(mid))
    for t in topic_ack:
        if t[1]==mid:
            t[2]=1 #acknowledged
            logging.info("subscription acknowledged  "+t[0])
            client.suback_flag=True
def on_publish(client, userdata, mid):
    logging.info("pub ack "+ str(mid))
    client.puback_flag=True
    

def on_message(client, userdata, msg):
    global message_count,message_count2,verbose,log_data_flag
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    process_message(m_decode,topic)
    
def process_message(msg,topic):
    global message_count,message_count2,verbose,log_data_flag
    data=dict()
    tnow=time.localtime(time.time())
    message_count+=1
    m=time.asctime(tnow)+" "+topic+" "+msg
    if display:
        if verbose: #display all messages
            message_q.put(m)
            message_count2+=1
        else: # only display changed messages
             if has_changed(topic,msg)==0: #changed so print
                message_q.put(m)
                message_count2+=1


def check_subs():
    #returns flase if have an unacknowledged subsription
    for t in topic_ack:
        if t[2]==0:
            logging.info("subscription to "+t[0] +" not acknowledged")
            return(False)
    return True 
def subscribe_topics(client,topics):
    for t in topics:
        try:
            logging.info("subscribing  " + str(topics))
            r=client1.subscribe(t)
            if r[0]!=0:
                logging.info("error on subscribing "+str(r))
                return -1
            logging.info("subscribed to topics return code" +str(r))
        except Exception as e:
            logging.info("error on subscribe"+str(e))
            return -1
        topic_ack.append([t[0],r[1],0]) #keep track of subscription
    return 0


def wait_for(client,msgType,period=0.25):
    if msgType=="CONNACK":
        if client.on_connect:
            while not client.connected_flag:
                logging.info("waiting connack")
                client.loop()  #check for messages
                time.sleep(period)

    if msgType=="DISCONNECT":
        if client.on_disconnect:
            while client.connected_flag:
                logging.info("waiting disconnect")
                client.loop()  #check for messages
                time.sleep(period)
    if msgType=="SUBACK":
        if client.on_subscribe:
            while not client.suback_flag:
                logging.info("waiting suback")
                client.loop()  #check for messages
                time.sleep(period)
    if msgType=="PUBACK":
        if client.on_publish:
            print("will wait")
            while not client.puback_flag:
                client.loop()  #check for messages
                logging.info("waiting puback")
                time.sleep(period)
    if msgType=="CHECKSUBS":
        if check_subs:
            print("will wait for all subs")
            while not check_subs():
                client.loop()  #check for messages
                logging.info("waiting for all subscriptions")
                time.sleep(period)
##############helper functions
def convert(t):
    d=""
    for c in t:  # replace all chars outside BMP with a !
            d =d+(c if ord(c) < 0x10000 else '!')
    return(d)
def print_out(m):
    if display:
        print("\n",m)
######
def print_options():
    print ('broker is ', broker)
    print ('port is ', port)
    print ('topic and qos is ', topics)
    exit(0)
    
########################main program
topics_in=[]
if __name__ == "__main__" and len(sys.argv)>=2:

    valid_options=" -b <broker> -p <port>-t <topic> -q QOS -v <verbose yes/no> -h <help>\
-c <loop Time secs -d logging debug yes/no> >"
    print_options_flag=False
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hb:p:t:q:l:d:c:v:")
    except getopt.GetoptError:
      print (sys.argv[0],valid_options)
      sys.exit(2)
    tpc=""
    qos=0

    for opt, arg in opts:
      if opt == '-h':
            print (sys.argv[0],valid_options)
            sys.exit()
      elif opt == "-b":
             broker = str(arg)
      elif opt =="-c":
            time_stop = int(arg)
      elif opt =="-p":
            port = int(arg)
      elif opt =="-t":
            topics_in.append(arg)
      elif opt =="-q":
            qos= int(arg)
      elif opt =="-d":
        if arg[0].lower()=="y":
            print("here",arg[0])
            logging.basicConfig(level=logging.DEBUG)
            debug_log=True
        if arg[0].lower()=="n":
            pass 
      elif opt =="-v":
        if arg[0].lower()=="y":
             verbose=True
        if arg[0].lower()=="n":
             verbose=False         
    if tpc !="":
        topics=tpc
    if print_options_flag:
        print_options()
    
    print ('broker is ', broker)
    print ('port is ', port)
    print ('topic is ', topics_in)


#main start
#message logging
if not debug_log: #have we set it?
    logging.basicConfig(level=logging.WARNING)
#use DEBUG,INFO,WARNING
####
    
for i in range(len(topics_in)):
    topics.append((topics_in[i],qos))
    if not verbose:
        print("only dispalying changes")

#############
if username !="":
    client1.username_pw_set(username, password)

################ set flags
mqtt.Client.bad_connection_flag=False
mqtt.Client.connected_flag=False
mqtt.Client.disconnect_flag=False
#flags set
client1= mqtt.Client(cname)
client1.on_connect= on_connect        #attach function to callback
client1.on_message=on_message        #attach function to callback
client1.on_disconnect=on_disconnect
client1.on_subscribe=on_subscribe
client1.on_publish=on_publish
### end basic initialise
loopflag=True #
##start connection process
badcount=0 # counter for bad connection attempts
print("waiting to connect")
connflag=False
while not connflag:
    print("connecting to broker",broker,"retry= ",badcount)
    logging.info("connecting to broker "+str(broker))
    try:
        client1.connect(broker,port)      #connect to broker
        connflag=True

    except:
        client1.badconnection_flag=True
        logging.info("connection failed")
        badcount +=1
        if badcount==3:
            raise SystemExit #give up
    
wait_for(client1,"CONNACK") #now wait for connection to complete
print("connected")
#####end connecting
if client1.connected_flag:
    if(subscribe_topics(client1,topics)==-1): #subscribe to topics
        print("Can't subscribe quitting ")
        client1.bad_connection_flag=True
        loopflag=False #quit
    else:
        wait_for(client1,"CHECKSUBS") #wait for all subscriptions

print("starting ")
if time_stop!=0:
    print("running for ",time_stop," seconds ")
else:
    print("Use CTRL+C to stop")


end_time=time.time()+time_stop # set up timer for loop

try:
    while loopflag:
        now=time.time()
        try:
            client1.loop(.25)
        except Exception as e:
            break

        while not message_q.empty():
            m=message_q.get()
            m=convert(m)# replace all chars outside BMP with a !
            if len(str(m))>500:
                print_out("large message  ")
            else:
                print_out(m)

        #time.sleep(.2)
        if client1.disconnect_flag==True:
                print("got disconnect so breaking loop")
                loopflag=False

        if time_stop !=0 and now >end_time: #stop loop?
            loopflag=False
except KeyboardInterrupt:
    print("interrrupted by keyboard")
time.sleep(2)
client1.loop()  #final check for messages before exiting

print("total number of messages analysed=",message_count," displayed ",message_count2)
