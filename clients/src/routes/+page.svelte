<script>
	import { onMount } from 'svelte';
	import { Post, Isonline } from './mixin.js';
	import store from 'store';

	let expression = $state('');
	let result = $state('');
	let expressionsModal = null;
	let errorMessage = $state('');
	let showCopiedFeedback = $state(false);
	/** @type {ReturnType<typeof setTimeout> | null} */
	let copyFeedbackTimeout = null;

	onMount(() => {
		// Check if Bootstrap is loaded
		if (typeof bootstrap !== 'undefined') {
			const modalElement = document.getElementById('expressionsModal');
			if (modalElement) {
				expressionsModal = new bootstrap.Modal(modalElement);
			}
		}

		return () => {
			if (expressionsModal) {
				expressionsModal.dispose();
			}
		};
	});

	function showExpressionsModal() {
		if (expressionsModal) {
			expressionsModal.show();
		}
	}
	const Examples = [
		{
			expression: '100000(P|A, 5.25%, 5) + 50000(P|A, 4.75%, 3)+ 30000(P|A1, .09, 5.25%, 5)',
			result: '719816.5225995606',
			timestamp: '2025-08-18 06:34:25',
			user: 'mahab339'
		}
	];
	let history = $state(store.get('history') || Examples);

	const supportedExpressions = [
		'Future worth: (F|P, i, N)',
		'Present worth: (P|F, i, N)',
		'Future worth (Series): (F|A, i, N)',
		'Sinking fund (Series): (A|F, i, N)',
		'Present worth (Series): (P|A, i, N)',
		'Capital recovery (Series): (A|P, i, N)',
		'Present worth (Gradient): (P|G, i, N)',
		'Equal payments (Gradient): (A|G, i, N)',
		'Present worth (Geometric Gradient): (P|A1, g, i, N)'
	];
	
	// Import calculator function
	import { calcexpression } from '../calculator.js';
	
	async function handleCalculate() {
		errorMessage = ''; // Clear previous errors
		if (!expression.trim()) {
			errorMessage = 'Empty expression!';
			result = '';
			return;
		}

		if (history.some((item) => item.expression === expression)) {

			let result2 = history.find((item) => item.expression === expression).result
			if (result2 == result){
				
			}
			result = result2;
			return
		}
		try {
			// Use the imported calculator function
			result = calcexpression(expression);
            if (result === undefined || result === null || Number.isNaN(result)) {
				errorMessage = 'Unknown result..';
				result = '';
			} else {
				// Add to history if not already there
				if (!history.some((item) => item.expression === expression)) {
					history = [
						{
							expression,
							result,
							timestamp: new Date().toISOString(),
							user: 'current_user'
						},
						...history
					];
					store.set('history', history);
				}
			}
		} catch (error) {
			errorMessage = 'Unknown result..';
				result = '';
		}
	}

	function handleClear() {
		history = Examples;
		store.set('history', history);
	}

	function handleEdit(index) {
		const item = history[index];
		expression = item.expression;
		result = item.result;
	}

	async function handleCopy(text) {
		try {
			await navigator.clipboard.writeText(text);
			showCopiedFeedback = true;

			// Clear any existing timeout
			if (copyFeedbackTimeout) {
				clearTimeout(copyFeedbackTimeout);
			}

			// Hide the feedback after 2 seconds
			copyFeedbackTimeout = setTimeout(() => {
				showCopiedFeedback = false;
			}, 1000);
		} catch (err) {
			console.error('Failed to copy text: ', err);
		}
	}
</script>

<div class="row g-4">
	<!-- Calculator Section -->
	<div class="col-12">
		<div class="bg-white p-4 rounded shadow-sm">
			<!-- <h2 class="h5 mb-3" style="font-family: 'Poppins', sans-serif; font-weight: 600;">Expression Calculator</h2> -->
			<!-- Error Message -->
			{#if errorMessage}
				<div class="alert alert-danger p-2 mb-3" style="font-size: 0.9rem;">
					<i class="bi bi-exclamation-triangle-fill me-1"></i>
					{errorMessage}
				</div>
			{/if}

			<textarea
				class="bg-light form-control mb-0 expressioninput"
				rows="4"
				placeholder="Enter your expression here"
				bind:value={expression}
				style="font-family: 'Roboto Mono', monospace; font-size: 0.95rem;"
				on:keydown={() => (errorMessage = '')}
			></textarea>

			<!-- Result Display -->
			<div
				class="result-display mb-3 p-3 bg-light rounded position-relative"
				style="min-height: 60px;"
				role="button"
				tabindex="0"
				on:click={() => handleCopy(result)}
				on:keydown={(e) => e.key === 'Enter' && handleCopy(result)}
				aria-label="Click to copy result to clipboard"
			>
				{#if showCopiedFeedback}
					<div
						class="position-absolute top-0 start-50 translate-middle-x mt-1 bg-dark text-white px-2 py-1 rounded"
						style="font-size: 0.75rem; z-index: 10; white-space: nowrap;"
					>
						Copied!
					</div>
				{/if}
				<div class="d-flex align-items-center">
					<span class="me-2" style="font-family: 'Roboto Mono', monospace; font-size: 1.2rem;"
					></span>
					<div class="w-100 position-relative">
						<div
							class="result-value"
							
						>
							<div
								style="
                      position: absolute;
                      top: 0;
                      left: 0;
                      right: 0;
                      height: 2px;
                      background-image: linear-gradient(to right, #198754 50%, transparent 50%);
                      background-size: 10px 2px;
                      background-repeat: repeat-x;
                    "
							></div>
							{result || ''}
						</div>
					</div>
				</div>
			</div>

			<div class="d-flex justify-content-between align-items-center">
				<div class="text-muted small" style="font-family: 'Inter', sans-serif;"></div>
				<button
					class="btn btn-primary"
					on:click={handleCalculate}
					style="font-family: 'Poppins', sans-serif; font-weight: 500;"
				>
					<i class="bi bi-calculator me-1"></i> Calculate
				</button>
			</div>
		</div>
	</div>

	<div class="col-12 col-md-6 order-md-1">
		<div class="bg-white p-3 rounded shadow-sm">
			<div class="d-flex justify-content-between align-items-center mb-3">
				<h2 class="h6 mb-0">History</h2>
				<button 
					class="btn btn-sm btn-link text-decoration-none" 
					on:click={handleClear}
					aria-label="Clear history"
					title="Clear history"
				>
					<i class="bi bi-trash" aria-hidden="true"></i>
				</button>
			</div>
			<div class="history-list">
				{#each history as item, index}
					<div class="history-item">
						<div>
							<span class="history-expression">
								{item.expression + ' ='}
							</span>
							<span class="history-result">
								{item.result}
							</span>
						</div>
						<div class="history-actions">
							<button
								class="btn btn-sm btn-link text-decoration-none"
								on:click={() => handleEdit(index)}
								aria-label="Edit expression"
								title="Edit expression"
							>
								<i class="bi bi-pencil" aria-hidden="true"></i>
							</button>
							<button
								class="btn btn-sm btn-link text-decoration-none"
								on:click={() => handleCopy(`${item.expression} = ${item.result}`)}
								aria-label="Copy to clipboard"
								title="Copy to clipboard"
							>
								<i class="bi bi-clipboard" aria-hidden="true"></i>
							</button>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>

	<!-- Examples and History Sections -->
	<div class="col-12 col-md-6 order-md-2">
		<div class="bg-white p-3 rounded shadow-sm">
			<div class="d-flex align-items-center mb-3">
				<h2 class="h6 mb-0 me-2">Supported expressions</h2>
				<button
					type="button"
					class="btn btn-link p-0 border-0 bg-transparent"
					style="font-size: 0.9rem;"
					on:click={showExpressionsModal}
					title="View expressions reference"
					aria-label="View expressions reference"
				>
					<i class="bi bi-info-circle text-muted"></i>
				</button>
			</div>
			<ul class="list-unstyled mb-0 expression-list">
				{#each supportedExpressions as expression}
					<li class="supportexpression">{expression}</li>
				{/each}
			</ul>
		</div>
	</div>
</div>

<!-- Expressions Reference Modal -->
<div
	class="modal fade"
	id="expressionsModal"
	tabindex="-1"
	aria-labelledby="expressionsModalLabel"
	aria-hidden="true"
>
	<div class="modal-dialog modal-lg">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="expressionsModalLabel">Expressions Reference</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body text-center">
				<a href="/cache/expressions.webp" target="_blank" rel="noopener noreferrer">
					<img
						src="/cache/expressions.webp"
						alt="Financial Expressions Reference"
						class="img-fluid mb-3"
						style="max-height: 70vh; cursor: pointer;"
						title="Click to view full size"
					/>
				</a>
				<p class="text-muted small">
					Source: Park, Chan S., Fundamentals of Engineering Economics, 3rdEd., Prentice Hall (2013)
				</p>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
			</div>
		</div>
	</div>
</div>

<style>
	:global(html),
	:global(body) {
		height: 100%;
		margin: 0;
		padding: 0;
	}

	:global(body) {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background-color: #f8f9fa;
	}

	.expression-list li {
		padding: 0.5rem;
		border-radius: 0.25rem;
		transition: background-color 0.2s;
	}

	.expression-list li:hover {
		background-color: #f8f9fa;
	}

	.expression-list li {
		padding: 0.5rem;
		border-radius: 0.25rem;
		background-color: #f8f9fa;
		margin-bottom: 0.5rem;
		font-family: monospace;
		color: #0a58ca; /* Darker blue for better contrast */
	}

	.history-item {
		display: flex;
		justify-content: space-between;
		align-items: start;
		padding: 0.75rem;
		background-color: #f1f3f5; /* Slightly darker background */
		border-radius: 0.25rem;
		margin-bottom: 0.5rem;
	}

	.history-expression {
		font-family: monospace;
		color: #212529; /* Darker gray for better contrast */
		margin-right: 1rem;
		word-break: break-all;
	}

	.history-result {
		color: #0f5132; /* Darker green for better contrast */
		font-weight: 600; /* Slightly bolder for better readability */
	}

	.history-actions {
		flex-shrink: 0;
		margin-left: 0.5rem;
	}

	.expressioninput {
		border: none;
		border-bottom-right-radius: 0px;
		border-bottom-left-radius: 0px;
	}
	.expressioninput:focus {
		box-shadow: none;
	}
	.result-value {
		font-family: 'Roboto Mono', monospace;
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #198754;
                    min-height: 1.5em;
                    position: relative;
                    padding-top: 1rem;
                    user-select: none;
				}
</style>
