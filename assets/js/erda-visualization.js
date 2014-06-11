!function(){

	Handlebars.registerHelper('isArray', function(item, options){
		if(_.isArray(item))
			return options.fn(item);
		else
			return options.inverse(item);
	});

	var ErdaData = Backbone.Model.extend({
		url : function(){
			return 'data/1000events.json';
		},

		responseSecondsBins : 20,

		parse : function(rawEvents){
			var events = crossfilter(rawEvents);
			var latLongDim = events.dimension(this._parseLatLong);
			var dateDim = events.dimension(this._parseDate);
			var typeDim = events.dimension(this._parseType);
			var responseMinutesExtents = d3.extent(rawEvents, this._parseResponseMinutes);
			var responseMinutesDim = events.dimension(this._parseResponseMinutes);
			return {
				// Dimensions
				latLongDim : latLongDim,
				responseMinutesDim : responseMinutesDim,
				dateDim : dateDim,
				typeDim : typeDim,
				// Groups
				latLongGroup : latLongDim.group().reduce(this._generateLongitude, function(){return 0;}, function(){return 0;}),
				typeTotalGroup : typeDim.group().reduceCount(),
				responseMinutesGroup : responseMinutesDim.group().reduceCount(),
				responseMinutesExtents : responseMinutesExtents
			};
		},

		_parseLatLong: function(d){
			return d.longitude;
		},

		_generateLongitude : function(p, d){
			return d.latitude;
		},

		_parseResponseMinutes : function(d){
			return d.response_seconds / 60;
		},

		_parseDate : function(d){
			return Date.parse(d.date+' '+d.dispatch_time);
		},

		_parseType : function(d){
			switch(d.unit){
				case 'ENG':
				case 'TRUCK':
					return 'Fire';
				case 'AMB':
					return 'Ambulance';
				default:
					return 'Other';
			}
		}

	});

	var Breadcrumbs = Backbone.View.extend({
		template : Handlebars.compile($('#breadcrumbs_template').html()),

		events : {
			
		},

		titles : {
			'start-time' : 'Start Response Time',
			'end-time' : 'End Response Time',
			'type' : 'Incident Type'
		},

		update : function(params){
			var processedParams = {};
			if(!_.isEmpty(params)){
				_(params).forOwn(function(value, key){
					if(key === 'start-time' || key === 'end-time')
						value = Math.floor(value) + ' Minutes';
					processedParams[key] = {
						title : this.titles[key],
						type : key,
						value : value
					};
				}, this);
				this.$el.html(this.template(processedParams));
			}
			else
				this.$el.empty();
		}
	});

	var TypeBarChart = Backbone.View.extend({
		id : 'type_bar_chart',

		initialize : function(){
			this.listenTo(this.model, 'change', this.render);
		},

		render : function(){
			this.chart = dc.rowChart('#'+this.id)
				.dimension(this.model.get('typeDim'))
				.group(this.model.get('typeTotalGroup'))
				.elasticX(true)
				.height(this.$el.height())
				.width(this.$el.width())
				.filterHandler(_.bindKey(this, 'filterHandler'))
				.render();
			this.trigger('render');
		},

		filterHandler : function(dimension, filter){
			this.trigger('filter', {
				type : 'incidentType',
				filter : filter
			});
		}
	});

	var ResponseTimeHistogram = Backbone.View.extend({
		id : 'response_time_histogram',

		initialize : function(){
			this.listenTo(this.model, 'change', this.render);
		},

		render : function(){
			var extents = this.model.get('responseMinutesExtents');
			this.chart = dc.barChart('#'+this.id)
				.dimension(this.model.get('responseMinutesDim'))
				.group(this.model.get('responseMinutesGroup'))
				.height(this.$el.height())
				.width(this.$el.width())
				.filterHandler(_.bindKey(this, 'filterHandler'))
				.xUnits(function(){return 30;})
				.x(d3.scale.linear().domain(extents))
				.render();
			this.trigger('render');
		},

		filterHandler : function(dimension, filter){
			this.trigger('filter', {
				type : 'responseMinutes',
				filter : filter[0]
			});
		}
	});

	var IncidentsMap = Backbone.View.extend({
		className : 'incidents_map',
		mapOptions : {
			center: new google.maps.LatLng(38.903725,-77.016202),
			zoom: 12
		},

		initialize : function(){
			this.listenTo(this.model, 'change', this.render);
		},

		render : function(){
			this.renderMap();
		},

		renderMap : function(){
			var renderPlot = _.bindKey(this, 'renderPlot');
			this.map = new google.maps.Map(this.$el.get(0), this.mapOptions);
			this.overlay = new google.maps.OverlayView();
			this.overlay.onAdd = _.bind(function(){
				this.overlay.draw = renderPlot;
			}, this);
			this.map.addListener('center_changed', renderPlot);
			this.map.addListener('drag', renderPlot);
			this.overlay.setMap(this.map);
		},

		renderPlot : function(){
			if(!this.chart)
				this.generatePlot();
			else
				this.updatePlot();
		},

		generatePlot : function(){
			var scales = this.generatePlotScales();
			$('<div></div>')
				.appendTo(this.getOverlayEl())
				.attr('id', 'incidents_map_plot');
			this.chart = dc.bubbleChart('#incidents_map_plot')
				.dimension(this.model.get('latLongDim'))
				.group(this.model.get('latLongGroup'))
				.margins({top : 0, left : 0, bottom : 0, right : 0})
				.height(this.$el.height())
				.width(this.$el.width())
				.x(scales.x)
				.y(scales.y)
				.r(d3.scale.linear().domain([0, 19]))
				.colors(['#ff0000'])
				.radiusValueAccessor(_.bind(function(d){
					return d.value > 0 ? 0.1 : 0;
				}, this))
				.maxBubbleRelativeSize(0.01)
				.renderLabel(false)
				.transitionDuration(0)
				.render();
			this.trigger('render');
		},

		updatePlot : function(){
			var scales = this.generatePlotScales();
			this.resizePlot();
			this.chart.x(scales.x)
				.y(scales.y)
				.redraw();
		},

		resizePlot : function(){
			var projection = this.overlay.getProjection();
			var corners = this.getCorners();
			var nePoint = projection.fromLatLngToDivPixel(corners.ne);
			var swPoint = projection.fromLatLngToDivPixel(corners.sw);
			var chartRootEl = this.getChartRootEl();

			chartRootEl.css({
				top : nePoint.y,
				left : swPoint.x,
				height : swPoint.y - nePoint.y,
				width : nePoint.x - swPoint.x
			});
		},

		getOverlayEl : function(){
			return $(this.overlay.getPanes().overlayLayer);
		},

		getChartRootEl : function(){
			return $(this.chart.root()[0][0]);
		},
		
		getCorners : function(){
			var bounds = this.map.getBounds();
			return {
				sw : bounds.getSouthWest(),
				ne : bounds.getNorthEast()
			};
		},

		generatePlotScales : function(){
			var corners = this.getCorners();
			return {
				y : d3.scale.linear().domain([corners.sw.lat(), corners.ne.lat()]),
				x : d3.scale.linear().domain([corners.sw.lng(), corners.ne.lng()])
			};
		}
	});

	var Router = Backbone.Router.extend({
		routes : {
			'(:query)' : 'filter'
		},
	 
		initialize : function(){
			this.erdaData = new ErdaData();
			this.incidentsMap = new IncidentsMap({
				el : $('#incidents_map'),
				model : this.erdaData
			});
			this.responseTimeHistogram = new ResponseTimeHistogram({
				el : $('#response_time_histogram'),
				model : this.erdaData
			});
			this.listenTo(this.responseTimeHistogram, 'filter', this.filterHandler);
			this.typeBarChart = new TypeBarChart({
				el : $('#type_bar_chart'),
				model : this.erdaData
			});
			this.listenTo(this.typeBarChart, 'filter', this.filterHandler);
			this.breadcrumbs = new Breadcrumbs({
				el : $('#breadcrumbs')
			});
			this.erdaData.fetch();
		},

		filterHandler : function(info){
			if(info.filter !== undefined){
				switch(info.type){
					case 'responseMinutes':
						this.updateParams({
							'start-time' : info.filter[0],
							'end-time' : info.filter[1]
						});
						break;
					case 'incidentType':
						this.updateParams({
							'type' : info.filter
						});
						break;
					default:
						return;
				}
			}
		},

		updateParams : function(params){
			window.location.hash = $.param(_.defaults(params, this.params), true);
		},

		filter : function(query){
			this.params = {};
			if(query){
				var rawParams = _(query.split('&'))
					.map(function(param){
						return param.split('=');
					})
					.unzip()
					.value();
					_(rawParams[0]).forEach(function(key, index){
						var val = rawParams[1][index];
						if(!this.params[key])
							this.params[key] = val;
						else if(!_.isArray(this.params[key]))
							this.params[key] = [this.params[key], val];
						else
							this.params[key].push(val);
					}, this);
					this.breadcrumbs.update(this.params);
					if(!this.updateFromControl){
						var startTime, endTime;
						_(this.params).forOwn(function(val, key){
							switch(key){
								case 'type':
									if(this.responseTimeHistogram.chart)
										this.typeBarChart.chart.filter(val);
									else
										this.listenToOnce(this.typeBarChart, 'render', function(){
											this.typeBarChart.chart.filter(val);
										});
									break;
								case 'start-time':
								case 'end-time':
									if(key === 'start-time')
										startTime = parseFloat(val);
									else
										endTime = parseFloat(val);
									if(startTime !== undefined && endTime !== undefined){
										if(this.responseTimeHistogram.chart)
											this.responseTimeHistogram.chart.filter([startTime, endTime]);
										else
											this.listenToOnce(this.responseTimeHistogram, 'render', function(){
												this.responseTimeHistogram.chart.filter([startTime, endTime]);
											});
									}
									break;
								}
							}, this);
						}
				}
		}
	});

	window.Router = Router;

}();
