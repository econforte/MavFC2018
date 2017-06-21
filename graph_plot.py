import paho.mqtt.client as mqtt # mosquitto.py is deprecated
import time
from bokeh.plotting import figure, output_file, show

x=[0,1,2,3,4,5,6,7,8,9]
y=[0,1,2,3,4,5,6,7,8,9]


mqttc = mqtt.Client("ioana")
mqttc.connect("192.168.2.5", 1883, 60)
#mqttc.subscribe("test/", 2) # <- pointless unless you include a subscribe callback
mqttc.loop_start()
number +=1
while True:
    p=mqttc.publish("test","number")
time.sleep(10)# sleep for 10 seconds before next call

#output to a static HTML
output_file("plt.html")

# create a new plot with a title and axis labels
p = figure(title="simple line plot", x_axis_label='x', y_axis_label='y')

# add a line renderer with legend and line thickness
p.line(p, legend="Temp.", line_width=2)

# show the results
show(p)
