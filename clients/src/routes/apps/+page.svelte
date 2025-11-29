<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
</script>

<svelte:head>
  <title>Sama Calculator Apps</title>
  <meta name="description" content="Download Sama Calculator Android App" />
</svelte:head>

<div class="container">
  <div class="header">
    <h1>Sama Calculator Apps</h1>
    <p>Android apps on Play Store</p>
  </div>

 
  <div class="requirements">
    <h3>Sama Calculator Android App</h3>
    <p><a href="https://play.google.com/store/apps/details?id=org.autostream.sama" target="_blank" class="download-link">Download Now</a></p>
  </div>
   <div class="requirements mt-4">
    <h3>Sama Calculator Android App (Offline Mode)</h3>
    <p><a href="https://play.google.com/store/apps/details?id=org.autostream.samaoffline" target="_blank" class="download-link">Download Now</a></p>
  </div>
</div>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  .header {
    text-align: center;
    margin-bottom: 3rem;
  }

  .header h1 {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 0.5rem;
  }

  .header p {
    font-size: 1.2rem;
    color: #666;
  }

  .apps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
  }

  .app-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .app-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .app-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .app-icon.offline {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  }

  .app-card h3 {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 1rem;
  }

  .app-card p {
    color: #666;
    margin-bottom: 1.5rem;
    line-height: 1.6;
  }

  .features {
    margin-bottom: 2rem;
  }

  .features ul {
    list-style: none;
    padding: 0;
  }

  .features li {
    padding: 0.25rem 0;
    color: #555;
    font-size: 0.9rem;
  }

  .download-btn {
    display: inline-block;
    padding: 0.75rem 2rem;
    border-radius: 25px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 1rem;
  }

  .download-btn.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .download-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }

  .download-btn.secondary {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
  }

  .download-btn.secondary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(240, 147, 251, 0.4);
  }

  .info-section {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
  }

  .info-section h2 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .comparison {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
  }

  .comparison-item {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
  }

  .comparison-item h4 {
    color: #333;
    margin-bottom: 0.5rem;
  }

  .comparison-item p {
    color: #666;
    line-height: 1.6;
  }

  .requirements {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .requirements h3 {
    color: #333;
    margin-bottom: 1rem;
  }

  .requirements ul {
    color: #666;
    line-height: 1.8;
  }

  .download-link {
    display: inline-block;
    padding: 12px 32px;
    background: #2563eb;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.2s ease;
    border: 1px solid #2563eb;
  }

  .download-link:hover {
    background: white;
    color: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  }

  .download-link:active {
    transform: translateY(0);
  }

  @media (max-width: 768px) {
    .container {
      padding: 1rem;
    }

    .header h1 {
      font-size: 2rem;
    }

    .apps-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .comparison {
      grid-template-columns: 1fr;
    }
  }
</style>