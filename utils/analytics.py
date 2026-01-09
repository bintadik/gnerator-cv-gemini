import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def inject_ga4():
    """
    Injects GA4 tracking scripts into the Streamlit app.
    Tracks page views, specific button clicks (Generate), and success/error status messages.
    """
    measurement_id = os.getenv("GA_MEASUREMENT_ID")
    
    if not measurement_id:
        return

    # GA4 Global Site Tag and Event Tracking Script
    ga_script = f"""
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            
            // Explicitly set page location from parent window
            gtag('config', '{measurement_id}', {{
                'page_path': window.parent.location.pathname,
                'page_location': window.parent.location.href,
                'send_page_view': true
            }});

            console.log('✅ GA4 Initialized with ID: {measurement_id}');

            // Set to keep track of already tracked status messages to avoid duplicates
            const trackedStatuses = new Set();

            // Function to track button clicks
            function trackButtons() {{
                const buttons = window.parent.document.querySelectorAll('button');
                buttons.forEach(button => {{
                    if (!button.getAttribute('data-ga-tracked')) {{
                        button.addEventListener('click', function() {{
                            const buttonText = (this.innerText || this.textContent).trim();
                            
                            // Exclude GEMINI_API_KEY related buttons/actions
                            if (buttonText.includes('Gemini API Key') || 
                                buttonText.includes('GEMINI_API_KEY') || 
                                (this.closest('.stTextInput') && this.closest('.stTextInput').innerText.includes('Gemini API Key'))) {{
                                return;
                            }}
                            
                            // Categorize buttons
                            let eventName = 'button_click';
                            if (buttonText.includes('Generate Tailored CV')) {{
                                eventName = 'generate_cv_click';
                            }} else if (buttonText.includes('Generate Cover Letter')) {{
                                eventName = 'generate_cl_click';
                            }}
                            
                            console.log('📊 GA4 tracking event:', eventName, {{ 'button_name': buttonText }});
                            
                            gtag('event', eventName, {{
                                'button_name': buttonText,
                                'page_path': window.parent.location.pathname,
                                'page_location': window.parent.location.href
                            }});
                        }});
                        button.setAttribute('data-ga-tracked', 'true');
                    }}
                }});
            }}

            // Function to track status messages (Success/Error/Warning)
            function trackStatus() {{
                // Streamlit uses specific classes for different alert types
                const alerts = window.parent.document.querySelectorAll('.stAlert, [data-testid="stNotification"]');
                alerts.forEach(alert => {{
                    const alertText = (alert.innerText || alert.textContent).trim();
                    if (!alertText) return;

                    // Generate a unique key for this message instance
                    const messageKey = alertText + "_" + Math.floor(Date.now() / 5000); 

                    if (!trackedStatuses.has(messageKey)) {{
                        // Identify status type
                        let statusType = 'info';
                        if (alertText.includes('✅')) statusType = 'success';
                        if (alertText.includes('❌')) statusType = 'error';
                        if (alertText.includes('⚠️')) statusType = 'warning';

                        // Specific goal tracking
                        let eventName = 'app_status';
                        if (statusType === 'success' && alertText.includes('CV generated successfully')) {{
                            eventName = 'generate_cv_success';
                        }} else if (statusType === 'success' && alertText.includes('Cover letter generated successfully')) {{
                            eventName = 'generate_cl_success';
                        }}

                        console.log('📊 GA4 tracking status:', eventName, {{ 'type': statusType, 'msg': alertText.substring(0, 30) }});

                        gtag('event', eventName, {{
                            'status_type': statusType,
                            'status_message': alertText.substring(0, 100),
                            'page_path': window.parent.location.pathname,
                            'page_location': window.parent.location.href
                        }});

                        trackedStatuses.add(messageKey);
                        
                        // Clean up set occasionally
                        if (trackedStatuses.size > 100) {{
                            const firstItem = trackedStatuses.values().next().value;
                            trackedStatuses.delete(firstItem);
                        }}
                    }}
                }});
            }}

            // Observe changes in the DOM to track dynamically added buttons and status messages
            const observer = new MutationObserver((mutations) => {{
                trackButtons();
                trackStatus();
            }});

            observer.observe(window.parent.document.body, {{
                childList: true,
                subtree: true
            }});

            // Initial tracking
            trackButtons();
            trackStatus();
        </script>
    """
    
    # Inject the script into the app (using components for JS execution)
    st.components.v1.html(ga_script, height=0, width=0)
