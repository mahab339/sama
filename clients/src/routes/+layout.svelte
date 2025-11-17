<script>
    import favicon from '../../static/favicon.svg';
    export let children;

</script>

<svelte:head>
    <link rel="icon" href={favicon} />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
</svelte:head>

<div class="wrapper d-flex flex-column min-vh-100" style="font-family: 'Inter', sans-serif;">
    <!-- Header -->
    <header class="bg-white shadow-sm">
        <div class="container py-3">
            <div class="d-flex align-items-center">
                <a href="/" class="text-decoration-none text-dark d-flex align-items-center">
                    <span class="display-5 fw-bold me-2" style="color: #00b4d8; font-family: 'Poppins', sans-serif; font-weight: 700;">S</span>
					<span class="h5 mb-0 emblembody">ama calculator</span>                </a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow-1 py-4">
        <div class="container">
            {@render children?.()}
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-top bg-white mt-auto">
        <div class="container py-3">
            <div class="row g-3 text-center text-md-start">
                <div class="col-12 col-md-4 order-md-2">
                    <div class="d-flex flex-column flex-md-row justify-content-center gap-2">
                        <a href="https://play.google.com/store/apps/details?id=org.autostream.sama&pcampaignid=web_share" class="text-decoration-none text-muted">Mobile apps</a>
                    </div>
                </div>
                <div class="col-12 col-md-4 order-md-1">
                    <a href="https://github.com/mahab339/sama" class="text-decoration-none text-muted">Programs source</a>
                </div>
                <div class="col-12 col-md-4 order-md-3 text-md-end">
                    <a href="/privacy" class="text-decoration-none text-muted">Privacy policy</a>
                </div>
            </div>
        </div>
    </footer>
</div>

<style>
    :global(html), :global(body) {
        height: 100%;
        margin: 0;
        padding: 0;
    }

    :global(body) {
        background-color: #f8f9fa;
    }

    .wrapper {
        min-height: 100vh;
    }

    main {
        flex: 1;
    }

    .emblembody {
        margin-left: -8px;
					margin-top: 14px;
					font-family: 'Poppins', sans-serif;
					font-weight: 600;
    }

    @media (max-width: 767.98px) {
        .emblembody {
            margin-top: 6px;
        }
    }

</style>
