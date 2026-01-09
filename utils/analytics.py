import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def inject_ga4():
    """
    Injects GA4 tracking scripts into the Streamlit app.
    Following simplified structure while maintaining button and status tracking.
    """
    measurement_id = os.getenv("GA_MEASUREMENT_ID")
    
    if not measurement_id:
        return

    ga_code = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        
        // Configuration with page view tracking
        gtag('config', '{measurement_id}', {{
            'page_path': window.parent.location.pathname,
            'page_location': window.parent.location.href
        }});

        console.log('✅ GA4 Tracked Initialized: {measurement_id}');

        // --- Custom Tracking Logic ---
        
        const trackedStatuses = new Set();

        function trackElements() {{
            // 1. Track Buttons
            const buttons = window.parent.document.querySelectorAll('button');
            buttons.forEach(button => {{
                if (!button.getAttribute('data-ga-tracked')) {{
                    button.addEventListener('click', function() {{
                        const text = (this.innerText || this.textContent).trim();
                        
                        // Security: Exclude API Key interactions
                        if (text.includes('Gemini API Key') || text.includes('GEMINI_API_KEY')) return;
                        
                        let event = 'button_click';
                        if (text.includes('Generate Tailored CV')) event = 'generate_cv_click';
                        if (text.includes('Generate Cover Letter')) event = 'generate_cl_click';
                        
                        gtag('event', event, {{
                            'button_name': text,
                            'page_path': window.parent.location.pathname
                        }});
                        console.log('📊 GA4 Event:', event);
                    }});
                    button.setAttribute('data-ga-tracked', 'true');
                }}
            }});

            // 2. Track Status Messages
            const alerts = window.parent.document.querySelectorAll('.stAlert, [data-testid="stNotification"]');
            alerts.forEach(alert => {{
                const msg = (alert.innerText || alert.textContent).trim();
                const key = msg + "_" + Math.floor(Date.now() / 10000); 

                if (msg && !trackedStatuses.has(key)) {{
                    let type = 'info';
                    if (msg.includes('✅')) type = 'success';
                    if (msg.includes('❌')) type = 'error';

                    let event = 'app_status';
                    if (type === 'success' && msg.includes('CV generated successfully')) event = 'generate_cv_success';
                    if (type === 'success' && msg.includes('Cover letter generated successfully')) event = 'generate_cl_success';

                    gtag('event', event, {{
                        'status_type': type,
                        'status_message': msg.substring(0, 100),
                        'page_path': window.parent.location.pathname
                    }});
                    console.log('📊 GA4 Status:', event);
                    trackedStatuses.add(key);
                }}
            }});
        }}

        // Observe DOM changes to catch dynamic elements
        new MutationObserver(() => trackElements()).observe(window.parent.document.body, {{
            childList: true,
            subtree: true
        }});

        // Run initial check
        trackElements();
    </script>
    """
    components.html(ga_code, height=0)
