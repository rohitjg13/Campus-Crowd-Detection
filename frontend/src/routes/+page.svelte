<script>
	import { onMount } from 'svelte';

	// Locations with their names
	const locations = [
		{ id: 'DH-1', name: 'Dining Hall 1' },
		{ id: 'DH-2', name: 'Dining Hall 2' },
		{ id: 'DH-3', name: 'Dining Hall 3' },
		{ id: 'LIB', name: 'Library' },
		{ id: 'CAFE', name: 'Cafe' },
		{ id: 'GYM', name: 'Gym' },
		{ id: 'SARC', name: 'SARC' },
		{ id: 'CD', name: 'C & D' },
		{ id: 'AB', name: 'A & B' }
	];

	// Generate data points with 5-minute granularity
	const generateDetailedLocationData = (locationId) => {
		const minuteData = [];
		const now = new Date();
		
		// Start 1 hour ago, in 5-minute increments
		for (let i = -60; i <= 60; i += 5) {
			const timePoint = new Date(now.getTime() + i * 60 * 1000);
			const hour = timePoint.getHours();
			const minute = timePoint.getMinutes();
			const timeLabel = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
			
			// Flag for time relative to current
			const isPast = i < 0;
			const isFuture = i > 0;
			const isCurrent = i === 0;
			
			// Base density value based on time of day (similar to original logic)
			let baseDensity;
			
			// Generate specific density patterns for each location
			switch (locationId) {
				case 'DH-1': // Dining Hall 1 - peaks at meal times
					baseDensity =
						hour === 8
							? 0.7 // Breakfast
							: hour === 12
								? 0.9 // Lunch
								: hour === 18
									? 0.85 // Dinner
									: hour > 20 || hour < 6
										? 0.1 // Late night/early morning
										: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'DH-2': // Dining Hall 2 - similar but less crowded
					baseDensity =
						hour === 8
							? 0.6 // Breakfast
							: hour === 12
								? 0.75 // Lunch
								: hour === 18
									? 0.7 // Dinner
									: hour > 20 || hour < 6
										? 0.05 // Late night/early morning
										: 0.2 + Math.random() * 0.2; // Base level
					break;
				case 'DH-3': // Dining Hall 3 - different pattern
					baseDensity =
						hour === 8
							? 0.5 // Breakfast
							: hour === 12
								? 0.8 // Lunch
								: hour === 18
									? 0.65 // Dinner
									: hour > 21 || hour < 7
										? 0.05 // Late night/early morning
										: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'LIB': // Library - busier in afternoons and evenings
					baseDensity =
						hour >= 10 && hour <= 16
							? 0.6 + Math.random() * 0.2 // Daytime
							: hour >= 19 && hour <= 22
								? 0.7 + Math.random() * 0.2 // Evening
								: hour > 22 || hour < 8
									? 0.1 + Math.random() * 0.1 // Late night
									: 0.4 + Math.random() * 0.2; // Base level
					break;
				case 'GYM': // Gym - morning and evening peaks
					baseDensity =
						hour >= 6 && hour <= 9
							? 0.7 + Math.random() * 0.2 // Morning
							: hour >= 16 && hour <= 20
								? 0.8 + Math.random() * 0.2 // Evening
								: hour > 22 || hour < 5
									? 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'CAFE': // Cafe - morning peak
					baseDensity =
						hour >= 7 && hour <= 10
							? 0.8 + Math.random() * 0.2 // Morning
							: hour >= 15 && hour <= 17
								? 0.5 + Math.random() * 0.2 // Afternoon
								: hour > 20 || hour < 6
									? 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'SARC': // SARC - technical area with steady daytime use
					baseDensity =
						hour >= 9 && hour <= 17
							? 0.65 + Math.random() * 0.2 // Daytime
							: hour >= 18 && hour <= 20
								? 0.5 + Math.random() * 0.2 // Evening
								: hour > 21 || hour < 8
									? 0.1 + Math.random() * 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'CD': // C & D - evening peak study area
					baseDensity =
						hour >= 15 && hour <= 20
							? 0.75 + Math.random() * 0.2 // Evening
							: hour >= 9 && hour <= 14
								? 0.4 + Math.random() * 0.2 // Daytime
								: hour > 22 || hour < 8
									? 0.1 + Math.random() * 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'AB': // A & B - steady traffic
					baseDensity =
						hour >= 10 && hour <= 16
							? 0.5 + Math.random() * 0.2 // Day
							: hour >= 17 && hour <= 20
								? 0.6 + Math.random() * 0.2 // Evening
								: hour > 21 || hour < 8
									? 0.2 + Math.random() * 0.1 // Late night/early morning
									: 0.4 + Math.random() * 0.2; // Base level
					break;
				default:
					baseDensity = Math.random() * 0.5;
			}
			
			// Add small fluctuations for more realistic minute-by-minute data
			let density = baseDensity;
			
			// Add some small random variations for each 5-minute interval
			density += (Math.random() * 0.1 - 0.05);
			
			// Add small trends for future prediction (gradually increasing or decreasing)
			if (isFuture) {
				// Future predictions have slight trends based on time of day
				const trend = (hour >= 11 && hour < 14) || (hour >= 17 && hour < 20)
					? 0.005 * (i / 5) // Increasing trend during meal times
					: (hour >= 21 || hour < 7)
						? -0.003 * (i / 5) // Decreasing trend late night
						: (Math.random() > 0.5 ? 1 : -1) * 0.002 * (i / 5); // Random slight trend otherwise
				
				density += trend;
			}
			
			// Clamp density between 0 and 1
			density = Math.min(1, Math.max(0, density));
			
			minuteData.push({
				time: timeLabel,
				density: parseFloat(density.toFixed(2)),
				isPast,
				isFuture,
				isCurrent
			});
		}
		
		return minuteData;
	};

	let selectedLocation = locations[0];
	let chartData = [];
	let chart;
	let currentStatus = '';

	// Get descriptive text for density value
	const getDensityLabel = (value) => {
		if (value >= 0.8) return 'Highly Crowded';
		if (value >= 0.6) return 'Crowded';
		if (value >= 0.4) return 'Moderate';
		if (value >= 0.2) return 'Low';
		return 'Free';
	};

	// Update chart data when location changes
	const updateChartData = () => {
		chartData = generateDetailedLocationData(selectedLocation.id);
		
		// Set current status based on the current time's density value
		const currentTimeData = chartData.find(d => d.isCurrent);
		if (currentTimeData) {
			const density = currentTimeData.density;
			currentStatus = getDensityLabel(density);
		}
		
		if (browser) {
			setTimeout(() => {
				renderChart();
			}, 0);
		}
	};

	let browser = false;

	onMount(() => {
		browser = true;
		updateChartData();
		
		// Update chart every minute to keep "current time" accurate
		const interval = setInterval(() => {
			updateChartData();
		}, 60000);
		
		return () => clearInterval(interval);
	});

	// Handle location change
	const handleLocationChange = (event) => {
		selectedLocation = locations.find((loc) => loc.id === event.target.value);
		updateChartData();
	};

	// Format timestamp for display
	const formatTime = (date) => {
		return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
	}

	// Function to render Chart.js chart
	const renderChart = () => {
		if (!browser) return;

		const ctx = document.getElementById('densityChart');
		if (!ctx) return;

		// Destroy existing chart if it exists
		if (chart) {
			chart.destroy();
		}

		// Get current time for reference
		const now = new Date();
		const currentTimeLabel = formatTime(now);

		// Create datasets for past and future data
		const pastData = chartData
			.filter(d => d.isPast)
			.map(d => ({ x: d.time, y: d.density }));
			
		const futureData = chartData
			.filter(d => d.isFuture)
			.map(d => ({ x: d.time, y: d.density }));
			
		const currentPoint = chartData
			.filter(d => d.isCurrent)
			.map(d => ({ x: d.time, y: d.density }))[0];

		// Create new chart
		chart = new Chart(ctx, {
			type: 'line',
			data: {
				datasets: [
					{
						label: 'Past Data',
						data: pastData,
						borderColor: '#4ade80', // Green
						backgroundColor: 'rgba(74, 222, 128, 0.1)',
						borderWidth: 2,
						fill: true,
						tension: 0.2,
						pointRadius: 0, // Hide points except on hover
						pointHoverRadius: 4,
						pointBackgroundColor: '#4ade80',
						pointBorderColor: '#4ade80'
					},
					{
						label: 'Current Time',
						data: [currentPoint],
						borderColor: '#ef4444', // Red
						backgroundColor: '#ef4444',
						borderWidth: 0,
						pointRadius: 6,
						pointHoverRadius: 8,
						pointBackgroundColor: '#ef4444',
						pointBorderColor: '#ffffff',
						pointBorderWidth: 2,
						showLine: false
					},
					{
						label: 'Future Prediction',
						data: futureData,
						borderColor: '#facc15', // Yellow
						backgroundColor: 'rgba(250, 204, 21, 0.1)',
						borderWidth: 2,
						borderDash: [5, 5], // Dashed line for future prediction
						fill: true,
						tension: 0.2,
						pointRadius: 0, // Hide points except on hover
						pointHoverRadius: 4,
						pointBackgroundColor: '#facc15',
						pointBorderColor: '#facc15'
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				scales: {
					y: {
						min: 0,
						max: 1,
						title: {
							display: true,
							text: 'Crowd Density'
						},
						ticks: {
							callback: function (value) {
								if (value === 1) return 'Very Crowded';
								if (value === 0.75) return 'Crowded';
								if (value === 0.5) return 'Average';
								if (value === 0.25) return 'Low';
								if (value === 0) return 'Free';
								return '';
							}
						}
					},
					x: {
						type: 'category',
						title: {
							display: true,
							text: 'Time'
						},
						grid: {
							color: (context) => {
								// Highlight current time vertical line
								const index = context.tick.label === currentTimeLabel;
								return index ? 'rgba(239, 68, 68, 0.7)' : 'rgba(0, 0, 0, 0.1)';
							},
							lineWidth: (context) => {
								// Make current time grid line thicker
								const index = context.tick.label === currentTimeLabel;
								return index ? 2 : 1;
							}
						},
						ticks: {
							maxTicksLimit: 13, // Show fewer ticks for better readability
							maxRotation: 45,
							minRotation: 45,
							color: (context) => {
								// Highlight current time label
								const label = context.tick && context.tick.label;
								return label === currentTimeLabel ? '#ef4444' : '#666';
							},
							font: (context) => {
								// Make current time text bold
								const label = context.tick && context.tick.label;
								return {
									weight: label === currentTimeLabel ? 'bold' : 'normal'
								};
							}
						},
						// CENTER THE CURRENT TIME - set center point to current time
						afterFit: function(scale) {
							const currentTimeIndex = scale.ticks.findIndex(tick => tick.label === currentTimeLabel);
							if (currentTimeIndex >= 0) {
								const centerPosition = scale.width / 2;
								const tickWidth = scale.width / scale.ticks.length;
								const currentTickPosition = (currentTimeIndex + 0.5) * tickWidth;
								const offset = centerPosition - currentTickPosition;
								
								// Apply the offset to center the current time
								scale.paddingLeft = Math.max(0, scale.paddingLeft + offset);
								scale.paddingRight = Math.max(0, scale.paddingRight - offset);
							}
						}
					}
				},
				plugins: {
					annotation: {
						annotations: {
							currentTimeLine: {
								type: 'line',
								xMin: currentTimeLabel,
								xMax: currentTimeLabel,
								borderColor: 'rgba(239, 68, 68, 0.7)',
								borderWidth: 2,
								borderDash: [0, 0],
								label: {
									backgroundColor: 'rgba(239, 68, 68, 0.7)',
									content: 'Current Time',
									display: true,
									position: 'top'
								}
							}
						}
					},
					tooltip: {
						callbacks: {
							label: function (context) {
								const density = context.parsed.y;
								const datasetLabel = context.dataset.label;
								const statusLabel = getDensityLabel(density);
								return `${datasetLabel}: ${statusLabel} (${(density * 100).toFixed(0)}%)`;
							},
							title: function(tooltipItems) {
								return `Time: ${tooltipItems[0].label}`;
							}
						}
					},
					legend: {
						display: true,
						position: 'top',
						labels: {
							usePointStyle: true,
							boxWidth: 10
						}
					}
				}
			}
		});
	};

	// Helper to get status color
	const getStatusColor = (status) => {
		switch (status) {
			case 'Free':
				return 'text-green-700';
			case 'Low':
				return 'text-green-500';
			case 'Moderate':
				return 'text-yellow-500';
			case 'Crowded':
				return 'text-orange-500';
			case 'Highly Crowded':
				return 'text-red-500';
			default:
				return 'text-gray-500';
		}
	};

	// Format the current datetime for display
	const getCurrentTimeFormatted = () => {
		const now = new Date();
		return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
	}
	
	let currentTime = getCurrentTimeFormatted();
	
	// Update time display
	const updateCurrentTime = () => {
		currentTime = getCurrentTimeFormatted();
	}
	
	onMount(() => {
		// Update time display every second
		const timeInterval = setInterval(updateCurrentTime, 1000);
		return () => clearInterval(timeInterval);
	});
</script>

<svelte:head>
	<title>Campus Crowd Tracker</title>
	<script src="https://cdn.tailwindcss.com"></script>
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
	<style>
		.legend-item {
			display: flex;
			align-items: center;
			margin-right: 16px;
		}
		.legend-color {
			width: 12px;
			height: 12px;
			border-radius: 50%;
			margin-right: 4px;
		}
	</style>
</svelte:head>

<div class="max-w-4xl mx-auto p-6">
	<h1 class="text-2xl font-bold mb-6">Campus Crowd Tracker</h1>

	<div class="flex flex-wrap items-center mb-6">
		<div class="mr-4 mb-2">
			<label for="location" class="block text-sm font-medium text-gray-700 mb-1"
				>Location</label
			>
			<select
				id="location"
				class="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
				value={selectedLocation.id}
				on:change={handleLocationChange}
			>
				{#each locations as location}
					<option value={location.id}>{location.name}</option>
				{/each}
			</select>
		</div>

		<div class="mb-2 ml-4">
			<span class="block text-sm font-medium text-gray-700 mb-1">Current Status</span>
			<span class="font-semibold {getStatusColor(currentStatus)} text-lg">
				{currentStatus}
			</span>
		</div>
	</div>

	<div class="border rounded-lg p-4 bg-white shadow-sm">
		<div class="flex justify-between items-center mb-4">
			<h2 class="text-lg font-medium">Crowd Density - {selectedLocation.name}</h2>
			<div class="flex flex-wrap">
				<div class="legend-item">
					<div class="legend-color" style="background-color: #4ade80;"></div>
					<span class="text-xs">Past Data</span>
				</div>
				<div class="legend-item">
					<div class="legend-color" style="background-color: #ef4444;"></div>
					<span class="text-xs">Current Time</span>
				</div>
				<div class="legend-item">
					<div class="legend-color" style="background-color: #facc15;"></div>
					<span class="text-xs">Future Predicted</span>
				</div>
			</div>
		</div>
		<div class="h-72">
			<canvas id="densityChart"></canvas>
		</div>
		<div class="text-xs text-right mt-2 text-gray-500">
			<p>Time window: 1 hour past to 1 hour future (5-minute intervals)</p>
		</div>
	</div>

	<div class="mt-6 text-sm text-gray-600 flex justify-between">
		<p>Last updated: {currentTime}</p>
		<p class="text-blue-600 hover:underline cursor-pointer" on:click={updateChartData}>
			Refresh Data
		</p>
	</div>
</div>