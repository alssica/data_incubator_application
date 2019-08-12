queue()
	.defer(d3.json, "/corp_miscon/projects")
	.defer(d3.json, "static/geojson/us-states.json")
	.await(makeGraphs);

function makeGraphs(error, projectsJson, statesJson) {

	//Clean projectsJson data
	var corpmisconProjects = projectsJson;
	var dateFormat = d3.time.format("%Y%m%d");
	corpmisconProjects.forEach(function (d) {
		// d["Penalty Date"] = d["Penalty Date"].toString();
		d["Penalty Date"] = dateFormat.parse(d["Penalty Date"]);
		d["Penalty Date"].setDate(1);
		d["Penalty Amount"] = +d["Penalty Amount"];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(corpmisconProjects);

	//Define Dimensions
	var dateDim = ndx.dimension(function (d) { return d["Penalty Date"]; });
	var industryTypeDim = ndx.dimension(function (d) { return d["Major Industry of Parent"]; });
	var agencyDim = ndx.dimension(function (d) { return d["Agency"]; });
	var stateDim = ndx.dimension(function (d) { return d["Facility State"]; });
	var penaltyDim = ndx.dimension(function (d) { return d["Penalty Amount"]; });


	//Calculate metrics
	var numCompaniesByDate = dateDim.group();
	var numCompaniesByIndustryType = industryTypeDim.group();
	var numCompaniesByAgency = agencyDim.group();
	var totalPenaltyByState = stateDim.group().reduceSum(function (d) {
		return d["Penalty Amount"];
	});

	var all = ndx.groupAll();
	var totalPenalties = ndx.groupAll().reduceSum(function (d) { return d["Penalty Amount"]; });

	var max_state = totalPenaltyByState.top(1)[0].value;

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["Penalty Date"];
	var maxDate = dateDim.top(1)[0]["Penalty Date"];

	//Charts
	var timeChart = dc.barChart("#time-chart");
	var industryTypeChart = dc.rowChart("#industry-type-row-chart");
	var agencyChart = dc.rowChart("#agency-row-chart");
	var usChart = dc.geoChoroplethChart("#us-chart");
	var numberCompaniesND = dc.numberDisplay("#number-companies-nd");
	var totalPenaltiesND = dc.numberDisplay("#total-penalties-nd");

	numberCompaniesND
		.formatNumber(d3.format("d"))
		.valueAccessor(function (d) { return d; })
		.group(all);

	totalPenaltiesND
		.formatNumber(d3.format("d"))
		.valueAccessor(function (d) { return d; })
		.group(totalPenalties)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(160)
		.margins({ top: 10, right: 50, bottom: 30, left: 50 })
		.dimension(dateDim)
		.group(numCompaniesByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);

	industryTypeChart
		.width(300)
		.height(250)
		.dimension(industryTypeDim)
		.group(numCompaniesByIndustryType)
		.xAxis().ticks(4);

	agencyChart
		.width(300)
		.height(250)
		.dimension(agencyDim)
		.group(numCompaniesByAgency)
		.xAxis().ticks(4);


	usChart.width(1000)
		.height(330)
		.dimension(stateDim)
		.group(totalPenaltyByState)
		.colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
		.colorDomain([0, max_state])
		.overlayGeoJson(statesJson["features"], "state", function (d) {
			return d.properties.name;
		})
		.projection(d3.geo.albersUsa()
			.scale(600)
			.translate([340, 150]))
		.title(function (p) {
			return "State: " + p["key"]
				+ "\n"
				+ "Total Penalties: " + Math.round(p["value"]) + " $";
		})

	dc.renderAll();

};