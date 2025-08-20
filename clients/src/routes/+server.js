// src/routes/api/hello/+server.ts
import { json } from '@sveltejs/kit';

export async function POST({ request }) {
    try {
        const { action, payload } = await request.json();
        
        if (action !== 'calculate') {
            return json({
                succeeded: false,
                failed: true,
                errcode: 'UNKNOWN_ACTION',
                message: 'Unknown action requested'
            });
        }

        const { Expression } = payload;
        if (!Expression) {
            return json({ 
                succeeded: false, 
                failed: true, 
                errcode: 'DATA_MISSING',
                message: 'Expression is required'
            });
        }

        const apiUrl = 'https://samaapi.up.railway.app/api/calculate/';
        

        try {
            const requestBody = { expression: Expression };
            

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            
            
            
            const responseText = await response.text();
            
            
            if (!response.ok) {
                let errorData = {};
                try {
                    errorData = responseText ? JSON.parse(responseText) : {};
                } catch (e) {
                    console.error('Failed to parse error response:', e);
                    errorData = { detail: 'Invalid JSON response', raw: responseText };
                }
                
                console.error('API Error:', {
                    status: response.status,
                    statusText: response.statusText,
                    url: apiUrl,
                    error: errorData
                });

                return json({
                    succeeded: false,
                    failed: true,
                    errcode: 'API_ERROR',
                    message: (errorData && 'detail' in errorData ? errorData.detail : '') || response.statusText || 'Failed to process request',
                    status: response.status,
                    details: errorData
                });
            }

            // Parse successful response
            let result;
            try {
                result = responseText ? JSON.parse(responseText) : {};
                
                
                return json({
                    succeeded: true,
                    failed: false,
                    result: result.result || result,
                    message: 'Success'
                });
            } catch (e) {
                console.error('Failed to parse success response:', e);
                throw new Error('Invalid JSON response from server');
            }

        } catch (/** @type {any} */ error) {
            console.error('Request failed:', error);
            return json({
                succeeded: false,
                failed: true,
                errcode: 'NETWORK_ERROR',
                message: 'Failed to connect to the server',
                details: error?.message || 'Unknown network error'
            });
        }

    } catch (/** @type {any} */ error) {
        console.error('Unexpected error:', error);
        return json({
            succeeded: false,
            failed: true,
            errcode: 'INTERNAL_ERROR',
            message: 'An unexpected error occurred',
            details: error?.message || 'Unknown error'
        }, { status: 500 });
    }
}

