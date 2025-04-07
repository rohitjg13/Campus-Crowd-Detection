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
		{ id: 'SARC', name: 'SARC C & D' },
		{ id: 'AB', name: 'A & B' }
	];

	// Generate realistic crowd density data for each location
	const generateLocationData = (locationId) => {
		const hourlyData = [];
		const now = new Date();
		const currentHour = now.getHours();

		// Create data for the full 24 hours
		for (let i = 0; i < 24; i++) {
			const hour = (currentHour - 23 + i + 24) % 24;
			const hourLabel = `${hour}:00`;
			const isCurrentHour = i === 23; // Last item is current hour

			let density;

			// Generate specific density patterns for each location
			switch (locationId) {
				case 'DH-1': // Dining Hall 1 - peaks at meal times
					density =
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
					density =
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
					density =
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
					density =
						hour >= 10 && hour <= 16
							? 0.6 + Math.random() * 0.2 // Daytime
							: hour >= 19 && hour <= 22
								? 0.7 + Math.random() * 0.2 // Evening
								: hour > 22 || hour < 8
									? 0.1 + Math.random() * 0.1 // Late night
									: 0.4 + Math.random() * 0.2; // Base level
					break;
				case 'GYM': // Gym - morning and evening peaks
					density =
						hour >= 6 && hour <= 9
							? 0.7 + Math.random() * 0.2 // Morning
							: hour >= 16 && hour <= 20
								? 0.8 + Math.random() * 0.2 // Evening
								: hour > 22 || hour < 5
									? 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'CAFE': // Cafe - morning peak
					density =
						hour >= 7 && hour <= 10
							? 0.8 + Math.random() * 0.2 // Morning
							: hour >= 15 && hour <= 17
								? 0.5 + Math.random() * 0.2 // Afternoon
								: hour > 20 || hour < 6
									? 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'SARC': // SARC C & D - evening peak
					density =
						hour >= 15 && hour <= 20
							? 0.75 + Math.random() * 0.2 // Evening
							: hour >= 9 && hour <= 14
								? 0.4 + Math.random() * 0.2 // Daytime
								: hour > 22 || hour < 8
									? 0.1 + Math.random() * 0.1 // Late night
									: 0.3 + Math.random() * 0.2; // Base level
					break;
				case 'AB': // A & B - steady traffic
					density =
						hour >= 10 && hour <= 16
							? 0.5 + Math.random() * 0.2 // Day
							: hour >= 17 && hour <= 20
								? 0.6 + Math.random() * 0.2 // Evening
								: hour > 21 || hour < 8
									? 0.2 + Math.random() * 0.1 // Late night/early morning
									: 0.4 + Math.random() * 0.2; // Base level
					break;
				default:
					density = Math.random() * 0.5;
			}

			// Add small random variation
			density = Math.min(1, Math.max(0, density + (Math.random() * 0.1 - 0.05)));

			hourlyData.push({
				time: hourLabel,
				density: parseFloat(density.toFixed(2)),
				isCurrentHour
			});
		}

		return hourlyData;
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
		chartData = generateLocationData(selectedLocation.id);

		// Set current status based on the current hour's density value
		const currentHourData = chartData.find((d) => d.isCurrentHour);
		if (currentHourData) {
			const density = currentHourData.density;
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
	});

	// Handle location change
	const handleLocationChange = (event) => {
		selectedLocation = locations.find((loc) => loc.id === event.target.value);
		updateChartData();
	};

	// Function to render Chart.js chart
	const renderChart = () => {
		if (!browser) return;

		const ctx = document.getElementById('densityChart');
		if (!ctx) return;

		// Destroy existing chart if it exists
		if (chart) {
			chart.destroy();
		}

		// Get current hour for highlighting
		const now = new Date();
		const currentHour = now.getHours();
		const currentTimeLabel = `${currentHour}:00`;

		// Create new chart
		chart = new Chart(ctx, {
			type: 'line',
			data: {
				labels: chartData.map((d) => d.time),
				datasets: [
					{
						label: 'Crowd Density',
						data: chartData.map((d) => d.density),
						borderColor: '#3B82F6',
						backgroundColor: 'rgba(59, 130, 246, 0.1)',
						borderWidth: 2,
						fill: true,
						tension: 0.1,
						pointRadius: (context) => {
							// Make current hour point larger
							const index = context.dataIndex;
							return chartData[index].isCurrentHour ? 6 : 3;
						},
						pointBackgroundColor: (context) => {
							// Highlight current hour point
							const index = context.dataIndex;
							return chartData[index].isCurrentHour ? '#FF6B6B' : '#3B82F6';
						},
						pointBorderColor: (context) => {
							// Highlight current hour point
							const index = context.dataIndex;
							return chartData[index].isCurrentHour ? '#FF6B6B' : '#3B82F6';
						},
						pointHoverRadius: 5
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
						ticks: {
							// Replace number values with text descriptions
							callback: function (value) {
								if (value === 1) return 'Highly Crowded';
								if (value === 0.75) return 'Crowded';
								if (value === 0.5) return 'Moderate';
								if (value === 0.25) return 'Low';
								if (value === 0) return 'Free';
								return '';
							}
						}
					},
					x: {
						grid: {
							color: (context) => {
								// Highlight current hour vertical line
								const label = context.tick.label;
								return label === currentTimeLabel
									? 'rgba(255, 107, 107, 0.5)'
									: 'rgba(0, 0, 0, 0.1)';
							},
							lineWidth: (context) => {
								// Make current hour grid line thicker
								const label = context.tick.label;
								return label === currentTimeLabel ? 2 : 1;
							}
						},
						ticks: {
							color: (context) => {
								// Highlight current hour label
								const label = context.tick.label;
								return label === currentTimeLabel ? '#FF6B6B' : '#666';
							},
							font: (context) => {
								// Make current hour text bold
								const label = context.tick.label;
								return {
									weight: label === currentTimeLabel ? 'bold' : 'normal'
								};
							},
							maxRotation: 45,
							minRotation: 45
						}
					}
				},
				plugins: {
					tooltip: {
						callbacks: {
							label: function (context) {
								const density = context.raw;
								return getDensityLabel(density);
							}
						}
					},
					legend: {
						display: false
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
</script>

<svelte:head>
	<title>Campus Crowd Tracker</title>
	<script src="https://cdn.tailwindcss.com"></script>
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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

		<div class="mb-2">
			<span class="block text-sm font-medium text-gray-700 mb-1">Current Status</span>
			<span class="font-semibold {getStatusColor(currentStatus)}">
				{currentStatus}
			</span>
		</div>
	</div>

	<div class="border rounded-lg p-4 bg-white shadow-sm">
		<h2 class="text-lg font-medium mb-4">24-Hour Crowd Density</h2>
		<div class="h-72">
			<canvas id="densityChart"></canvas>
		</div>
		<div class="text-xs text-center mt-2 text-gray-500">
			<span class="inline-block w-3 h-3 rounded-full bg-red-500 align-middle mr-1"></span> Current
			time
		</div>
	</div>

	<div class="mt-6 text-sm text-gray-600">
		<p>Last updated: {new Date().toLocaleTimeString()}</p>
	</div>
</div>
