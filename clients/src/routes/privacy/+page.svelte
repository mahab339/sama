<script>
    import { onMount, onDestroy } from 'svelte';
    import { App } from '@capacitor/app';
  
    let backButtonListener;
  
    onMount(() => {
      // Add back button listener when component mounts
      backButtonListener = App.addListener('backButton', handleBackButton);
    });
  
    onDestroy(() => {
      // Clean up the listener when component is destroyed
      if (backButtonListener) {
        backButtonListener.remove();
      }
    });
  
    function handleBackButton() {
      // Check if we're on the privacy page
      if (window.location.pathname === '/privacy') {
        // Navigate back to home page
        window.history.back();
        return false; // Prevent default back behavior
      }
      // For other pages, allow default back behavior
      return true;
    }
  </script>
  
  <!-- Your existing privacy page content here -->

  <div class="privacy-page">
      <div class="container px-0">
          <div class="row justify-content-center">
              <div class="col-12 col-lg-10">
                  <header class="privacy-header">
                      <h1>Privacy Policy</h1>
                      <div class="divider"></div>
                      
                  </header>
  
                  <div class="privacy-content">
                      <section class="privacy-section">
                          <p class="lead">At Sama Calculator, we prioritize your privacy and are committed to protecting your personal information. This Privacy Policy outlines how we collect, use, and safeguard your data when you use our application.</p>
                      </section>
  
                      <section class="privacy-section">
                          <h2>1. Information We Collect</h2>
                          <p><strong>1.1 Personal Information</strong><br>
                          We do not collect personally identifiable information unless explicitly provided by you through optional feedback forms or support requests.</p>
                          
                          <p><strong>1.2 Usage Data</strong><br>
                          We collect anonymous usage statistics to improve our application, including calculation frequency, feature usage, and crash reports. This data is aggregated and cannot be used to identify individual users.</p>
                      </section>
  
                      <section class="privacy-section">
                          <h2>2. How We Use Your Information</h2>
                          <p>We use the collected data to:</p>
                          <ul>
                              <li>Provide and maintain our service</li>
                              <li>Improve user experience and application performance</li>
                              <li>Monitor application usage and analyze trends</li>
                              <li>Respond to your inquiries and provide support</li>
                              <li>Comply with legal obligations</li>
                          </ul>
                      </section>
  
                      <section class="privacy-section">
                          <h2>3. Data Security</h2>
                          <p>We implement the appropriate, industry-standard technical and organizational measures to protect your data against unauthorized access, alteration, or destruction.</p>
                      </section>
  
                      <section class="privacy-section">
                          <h2>4. Third-Party Services</h2>
                          <p>Our application may contain links to third-party websites or services. We are not responsible for the privacy practices or content of these third-party sites. We encourage you to review their privacy policies before providing any personal information.</p>
                      </section>
  
                      <section class="privacy-section">
                          <h2>5. Changes to This Policy</h2>
                          <p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last Updated" date. You are advised to review this Privacy Policy periodically for any changes.</p>
                      </section>
  
                      <section class="privacy-section">
                          <h2>6. Contact Us</h2>
                          <p>If you have any questions about this Privacy Policy, please contact us at <a href="mailto:malmezayen@outlook.com" class="contact-link">malmezayen@outlook.com</a>.</p>
                      </section>
                      <div class="last-updated">
                        Last Updated: August 20, 2025
                    </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
<style>
    .privacy-page {
        min-height: 100vh;
        padding: 5rem 0;
        background: #f8fafc;
        color: #1e293b;
    }

    .privacy-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .privacy-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }

    .divider {
        height: 4px;
        width: 80px;
        background: linear-gradient(90deg, #00b4d8, #90e0ef);
        margin: 0 auto;
        border-radius: 2px;
    }

    .privacy-content {
        background: white;
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }

    .privacy-section {
        margin-bottom: 2.5rem;
    }

    .privacy-section:last-child {
        margin-bottom: 0;
    }

    .lead {
        font-size: 1.25rem;
        line-height: 1.7;
        color: #475569;
        margin-bottom: 2rem;
    }

    h2 {
        font-size: 1.75rem;
        font-weight: 600;
        color: #0f172a;
        margin: 2.5rem 0 1.5rem;
        position: relative;
        padding-bottom: 0.75rem;
    }

    h2:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: #e2e8f0;
        border-radius: 3px;
    }

    p {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #475569;
        margin-bottom: 1.5rem;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .privacy-content {
            padding: 13px;
        }

        .privacy-header h1 {
            font-size: 2rem;
        }

    }
    .last-updated {
        color: #64748b;
        font-size: x-small;
        margin-top: 3rem;
        text-align: right;
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
    }

    .privacy-section h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f172a;
        margin: 2.5rem 0 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }

    .privacy-section p {
        margin-bottom: 1.25rem;
        line-height: 1.8;
        color: #475569;
    }

    .privacy-section ul {
        margin: 1.25rem 0;
        padding-left: 1.5rem;
    }

    .privacy-section li {
        margin-bottom: 0.75rem;
        line-height: 1.7;
        color: #475569;
    }

    .privacy-section strong {
        color: #0f172a;
        font-weight: 600;
    }

    .contact-link {
        color: #00b4d8;
        text-decoration: none;
        transition: color 0.2s ease;
    }

    .contact-link:hover {
        color: #0096c7;
        text-decoration: underline;
    }

    @media (max-width: 768px) {
        .privacy-section h2 {
            font-size: 1.35rem;
        }
        
        .privacy-section p, 
        .privacy-section li {
            font-size: 1rem;
        }
    }
</style>