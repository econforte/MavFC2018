

// CREATING NECESSARY DATA PARSING METHOD
// add parseDate

function getColorList(colorlist){
	switch(colorlist) {
		case 1:
			return [d3.rgb("#C0392B"), 
			        d3.rgb("#884EA0"), 
			        d3.rgb("#2471A3"),
			        d3.rgb("#138D75"),
			        d3.rgb("#28B463"),
			        d3.rgb("#D68910"),
			        d3.rgb("#273746"),
			        d3.rgb("#CC99FF"),
			        d3.rgb("#CC3333"),
			        d3.rgb("#6666FF"),
			        d3.rgb("#669999"),
			        d3.rgb("#999900"),
			        d3.rgb("#00CC66"),
			        d3.rgb("#3333CC"),
			        d3.rgb("#330066"),
			        d3.rgb("#330000"),
			        d3.rgb("#42F4EB"),
			        d3.rgb("#81C42F"),
			        d3.rgb("#C4592F"),
			        d3.rgb("#59240F"),
			        d3.rgb("#4E3F59"),
			        d3.rgb("#4C1272"),
			        d3.rgb("#C1016E"),
			        d3.rgb("#824F6C"),
			        d3.rgb("#8C313E"),
			        d3.rgb("#330000"),
			        ];
			break;
		default:
			return getColorList(1);
	}
}

// GETTING THE DATA / PROCESSING THE DATA
var data = d3.json("{% url "data_list" %}" );

var columns = Object.keys(data[0]);
var colnum = columns.length;
var actuators = Object.values(data[0])
var isActuator = new Object();
var numActuators = 0;
for (c = 0; c < columns.length; c++){
	isActuator[columns[c]] = actuators[c];
	numActuators = (actuators[c] == 1) ? numActuators + 1 : numActuators;
};

data.forEach(function (d) {
	Object.getOwnPropertyNames(d).forEach(function(val){
		if(isActuator[val]==1){
			d[val] = (d[val] == 0) ? null : +d[val];
		} else if (val=="date") {
			d[val] = parseDate(d[val]);
		} else {
			d[val] = +d[val];
		}
	})
});
data.shift();

// CREATING THE GRAPH
var dimX = 700;
var dimY = 300;
var margin = {top: (30+10*data.numActuators), right: (2+45*(data.colnum-data.numActuators-1)), bottom: 30, left: 50}
var width = dimX - margin.left - margin.right;
var height = dimY - margin.top - margin.bottom;

var acceptableColors = getColorList(1);

// initializing axes size
var x = d3.time.scale().range([0, width]);
var ys = Object();
var as = Object();
var aspot = 1;
for (i=0;i<columns.length;i++){
	if(isActuator[columns[i]] == 1){
		as[columns[i]] = d3.scale.linear().range([height, 10+10*aspot]);
		aspot++;
	} else if (columns[i].localeCompare("date") == 0){
		continue;
	} else {
		ys[columns[i]] = d3.scale.linear().range([height, 0]);
	}
}



// initializing axes attributes
var xAxis = d3.svg.axis().scale(x)
	.orient("bottom").ticks(10);
var yAxes = Object();
var firstflag = true;
for (i=0;i<columns.length;i++){
	if(data.isActuator[columns[i]] == 1){
		continue;
	} else if (columns[i] == "date"){
		continue;
	} else {
		if (firstflag) {
			yAxes[columns[i]] = d3.svg.axis().scale(ys[columns[i]])
				.orient("left").ticks(8);
			firstflag = false;
		} else {
			yAxes[columns[i]] = d3.svg.axis().scale(ys[columns[i]])
				.orient("right").ticks(8);
		}
	}
}

// creating data series
var yines = Object();
var aines = Object();

columns.forEach(function(column){
	console.log(column);
  if(isActuator[column] == 1){
  	console.log("is actuator");
    aines[column] = d3.svg.line()
    	.defined(function(d) { return d[column]; })
    	.x(function (d) { return x(d["date"]); })
    	.y(function (d) { return as[column](d[column]); });
  } else if (column.localeCompare("date") == 0){
  	console.log("is date");
  } else {
  	yines[column] = d3.svg.line()
    	.x(function (d) { return x(d["date"]); })
    	.y(function (d) { return ys[column](d[column]); });
  	console.log("is sensor");
  }
});

// initializing graph size
var svg = d3.select("body")
	.append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// aligning series to axes
columns.forEach(function(column){
	if(isActuator[column] == 1){
		as[column].domain([0, d3.max(data, function (d) {
				return d.light;
				})]);
  } else if (column.localeCompare("date") == 0){
  	x.domain(d3.extent(data, function (d) {
    		return d.date;
    		}));
  } else {
  	ys[column].domain([0, d3.max(data, function (d) {
    return d[column];
    })]);
  }
});

// assigning colors
var colors = Object();
columns.forEach(function(column){
	colors[column] = acceptableColors.shift();
});

// adding data series (lines) to the graph
columns.forEach(function(column){
	if(isActuator[column] == 1){
  	svg.append("path")
			.style("stroke", colors[column])
    	.style("stroke-width", 10)
    	.attr("d", aines[column](data));
  } else if (column.localeCompare("date") == 0){
		console.log("ignoring date series")
  } else {
		svg.append("path")
    		.style("stroke", colors[column])
    		.attr("d", yines[column](data));
  }
});

// adding the axes to the graph AND adding actuator text to the graph
firstflag = true;
var acount = 1;
var scount = 0;
columns.forEach(function(column){
	if(isActuator[column] == 1){
    svg.append("text") // actuator 2
      .style("fill", colors[column])
      .attr("x", -45)
      .attr("y", -6-(10*acount))
      .text(column);
    acount++;
  } else if (column.localeCompare("date") == 0){
		svg.append("g")
				.attr("class", "x axis")
    		.attr("transform", "translate(0," + height + ")")
    		.call(xAxis);
  } else {
		if (firstflag){
      svg.append("g") 
          .style("fill", colors[column])
          .attr("class", "y axis")
          .attr("transform", "translate(-15,0)")
          .call(yAxes[column])
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 3)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text(column);
    	firstflag = false;
    } else {
      svg.append("g") // y1 open
        .style("fill", colors[column])
        .attr("class", "y axis")
        .attr("transform", "translate(" + (width+2+(45*scount)) + " ,0)")
        .call(yAxes[column])
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -14)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(column);
      scount++;
    }
  }
});





















