<script>
	import { onMount } from 'svelte';
	import {
		LineChart,
		Line,
		XAxis,
		YAxis,
		CartesianGrid,
		Tooltip,
		ResponsiveContainer
	} from 'recharts';

	// Locations with their current status
	const locations = [
		{ id: 'DH-1', name: 'Dining Hall 1', currentStatus: 'Crowded' },
		{ id: 'DH-2', name: 'Dining Hall 2', currentStatus: 'Moderate' },
		{ id: 'LIB-1', name: 'Main Library', currentStatus: 'Low' },
		{ id: 'GYM-1', name: 'Fitness Center', currentStatus: 'High' },
		{ id: 'STU-C', name: 'Student Center', currentStatus: 'Moderate' },
		{ id: 'CAFE', name: 'Campus Cafe', currentStatus: 'Low' },
		{ id: 'STUDY', name: 'Study Lounge', currentStatus: 'Crowded' }
	];

	// Generate realistic crowd density data for each location
	const generateLocationData = (locationId) => {
		const hourlyData = [];
		const now = new Date();
		const currentHour = now.getHours();

		// Create data for the past 12 hours
		for (let i = 0; i < 12; i++) {
			const hour = (currentHour - 11 + i + 24) % 24;
			const hourLabel = `${hour}:00`;

			let density;

			switch (locationId) {
				case 'DH-1': // Dining Hall 1 - peaks at meal times
					density = mealTimeDensity(hour);
					break;
				case 'DH-2': // Dining Hall 2 - similar but less crowded
					density = mealTimeDensity(hour) * 0.8;
					break;
				case 'LIB-1': // Library - busier in afternoons and evenings
					density = libraryDensity(hour);
					break;
				case 'GYM-1': // Gym - morning and evening peaks
					density = gymDensity(hour);
					break;
				case 'STU-C': // Student Center - steady throughout the day
					density = studentCenterDensity(hour);
					break;
				case 'CAFE': // Cafe - morning peak, afternoon moderate
					density = cafeDensity(hour);
					break;
				case 'STUDY': // Study Lounge - evening peak
					density = studyLoungeDensity(hour);
					break;
				default:
					density = Math.random() * 0.5;
			}

			// Add small random variation
			density = Math.min(1, Math.max(0, density + (Math.random() * 0.1 - 0.05)));

			hourlyData.push({
				time: hourLabel,
				density: parseFloat(density.toFixed(2))
			});
		}

		return hourlyData;
	};

	// Density patterns for different locations
	const mealTimeDensity = (hour) => {
		if (hour === 8) return 0.7; // Breakfast
		if (hour === 12) return 0.9; // Lunch
		if (hour === 18) return 0.85; // Dinner
		if (hour > 20 || hour < 6) return 0.1; // Late night/early morning
		return 0.3 + Math.random() * 0.2; // Base level
	};

	const libraryDensity = (hour) => {
		if (hour >= 10 && hour <= 16) return 0.6 + Math.random() * 0.2; // Busy during the day
		if (hour >= 19 && hour <= 22) return 0.7 + Math.random() * 0.2; // Evening study time
		if (hour > 22 || hour < 8) return 0.1 + Math.random() * 0.1; // Late night/early morning
		return 0.4 + Math.random() * 0.2; // Base level
	};

	const gymDensity = (hour) => {
		if (hour >= 6 && hour <= 9) return 0.7 + Math.random() * 0.2; // Morning workout
		if (hour >= 16 && hour <= 20) return 0.8 + Math.random() * 0.2; // After work/classes
		if (hour > 22 || hour < 5) return 0.1; // Late night
		return 0.3 + Math.random() * 0.2; // Base level
	};

	const studentCenterDensity = (hour) => {
		if (hour >= 11 && hour <= 14) return 0.7 + Math.random() * 0.2; // Lunch time
		if (hour >= 15 && hour <= 19) return 0.6 + Math.random() * 0.2; // Afternoon hangout
		if (hour > 22 || hour < 7) return 0.1 + Math.random() * 0.1; // Late night/early morning
		return 0.4 + Math.random() * 0.1; // Base level
	};

	const cafeDensity = (hour) => {
		if (hour >= 7 && hour <= 10) return 0.8 + Math.random() * 0.2; // Morning coffee
		if (hour >= 12 && hour <= 14) return 0.6 + Math.random() * 0.2; // Lunch
		if (hour >= 15 && hour <= 17) return 0.5 + Math.random() * 0.2; // Afternoon coffee
		if (hour > 20 || hour < 6) return 0.1; // Late night/early morning
		return 0.3 + Math.random() * 0.2; // Base level
	};

	const studyLoungeDensity = (hour) => {
		if (hour >= 19 && hour <= 23) return 0.8 + Math.random() * 0.2; // Evening study
		if (hour >= 9 && hour <= 16) return 0.5 + Math.random() * 0.2; // Daytime
		if (hour > 23 || hour < 7) return 0.2 + Math.random() * 0.1; // Late night/early morning
		return 0.3 + Math.random() * 0.2; // Base level
	};

	let selectedLocation = locations[0];
	let chartData = [];

	// Update chart data when location changes
	const updateChartData = () => {
		chartData = generateLocationData(selectedLocation.id);
	};

	onMount(() => {
		updateChartData();
	});

	// Handle location change
	const handleLocationChange = (event) => {
		selectedLocation = locations.find((loc) => loc.id === event.target.value);
		updateChartData();
	};

	// Helper to get status color
	const getStatusColor = (status) => {
		switch (status) {
			case 'Low':
				return 'text-green-600';
			case 'Moderate':
				return 'text-yellow-600';
			case 'High':
				return 'text-orange-600';
			case 'Crowded':
				return 'text-red-600';
			default:
				return 'text-gray-600';
		}
	};
</script>

<div class="max-w-4xl mx-auto p-6">
	<h1 class="text-2xl font-bold mb-6">Campus Crowd Tracker</h1>

	<div class="flex items-center mb-6">
		<div class="mr-4">
			<label for="location" class="block text-sm font-medium text-gray-700 mb-1"
				>Location</label
			>
			<select
				id="location"
				class="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
				bind:value={selectedLocation.id}
				on:change={handleLocationChange}
			>
				{#each locations as location}
					<option value={location.id}>{location.name}</option>
				{/each}
			</select>
		</div>

		<div>
			<span class="block text-sm font-medium text-gray-700 mb-1">Current Status</span>
			<span class={`font-semibold ${getStatusColor(selectedLocation.currentStatus)}`}>
				{selectedLocation.currentStatus}
			</span>
		</div>
	</div>

	<div class="border rounded-lg p-4 bg-white shadow-sm">
		<h2 class="text-lg font-medium mb-4">Crowd Density Over Time</h2>
		<div class="h-64">
			<ResponsiveContainer width="100%" height="100%">
				<LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
					<CartesianGrid strokeDasharray="3 3" />
					<XAxis dataKey="time" />
					<YAxis domain={[0, 1]} tickFormatter={(tick) => `${tick * 100}%`} />
					<Tooltip formatter={(value) => `${(value * 100).toFixed(0)}%`} />
					<Line
						type="monotone"
						dataKey="density"
						stroke="#3B82F6"
						strokeWidth={2}
						dot={{ r: 3 }}
						activeDot={{ r: 5 }}
						name="Crowd Density"
					/>
				</LineChart>
			</ResponsiveContainer>
		</div>
	</div>

	<div class="mt-6 text-sm text-gray-600">
		<p>Last updated: {new Date().toLocaleTimeString()}</p>
	</div>
</div>
