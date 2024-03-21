






var BarsChart = (function() {

	//
	// Variables
	//
	fetch(`/api/get_user_category_spend/${uid}`)
		.then(response => response.json())
		.then(data => {
			console.log(Object.keys(data))
			console.log(Object.values(data))
			var $chart = $('#chart-bars');

			function initChart($chart)
			{
				// Create chart
				var ordersChart = new Chart($chart, {
					type: 'pie',
					data: {
						labels: Object.keys(data),
						datasets: [{
							data: Object.values(data),
							backgroundColor: ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"],
						}]
					}
				});

				// Save to jQuery object
				$chart.data('chart', ordersChart);
			}
			// Init chart
			if ($chart.length) {
				initChart($chart);
			}
		});




	//
	// Methods
	//

	// Init chart


})();