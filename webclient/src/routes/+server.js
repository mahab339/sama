import { json } from '@sveltejs/kit'

/** @satisfies {import('./$types.js').Actions} */
export async function POST({ cookies, request, url }) {
    console.log('~~~~~~~~~~~~~~')
    try {
        const { action, payload } = await request.json()
        let result
        switch (action) {
            case 'calculate':
                result = await Calculate(payload, cookies, url)
                break
            default:
                result = { succeeded: false, failed: true, errcode: "Unknownaction" }
        }
        console.log(result)
        return json(result, {
            status: 200,
            headers: {
                'Content-Type': 'application/json'
            }
        })
    } catch (/** @type {any} */ error) {
        return json(
            { succeeded: false, failed: true, errcode: error.message },
            { status: 500 }
        )
    }
}

async function Calculate(payload, cookies, url) {
    const { Expression } = payload
    const clientid = cookies.get('sama-clientid')
    if (!Expression) {
        return { succeeded: false, failed: true, errcode: "Datamissing" }
    }

    try {
        /** @type {Record<string, string>} */
        const headers = {
            'Content-Type': 'application/json',
            'sama-clienttype': 'web'
        }
        console.log('Client id:', clientid)

        // Add clientid to headers if it exists
        if (clientid) {
            headers['sama-clientid'] = clientid
        }

        const response = await fetch('http://127.0.0.1:8000/api/calculate/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ expression: Expression })
        })

        if (!response.ok) {
            const error = await response.json().catch(() => ({}))
            return { 
                succeeded: false, 
                failed: true, 
                errcode: error.errcode || 'RequestFailed',
                message: error.message || 'Failed to process calculation'
            }
        }

        const result = await response.json()
        
        // Set the client_id cookie if it exists in the response
        if (result.client_id) {
            cookies.set('sama-clientid', result.client_id, {
                path: '/',
                httpOnly: true,
                sameSite: 'strict',
                maxAge: 60 * 60 * 24 * 30, // 30 days
                secure: process.env.NODE_ENV === 'production'
            })
        }
        
        return result
    } catch (/** @type {any} */ error) {
        return {
            succeeded: false,
            failed: true,
            errcode: 'NetworkError',
            message: error?.message || 'Unknown error occurred'
        }
    }
}
