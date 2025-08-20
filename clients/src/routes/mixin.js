const ORIGIN = "Webclient routes Mixin Post"

export const Post = async (action, payload={}, route='') => {
    if(! await Isonline())
        return { succeeded: false, failed: true, errcode: "Nointernet" }
    let result
    try{
		
        // result = await fetch(`https://sama.up.railway.app${route}`, {
        result = await fetch(route, {
				method: 'POST',
				mode: 'cors',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					action: action,
					payload: payload
				})
			})
            if (!result.ok) {
                return { succeeded: false, failed: true, errcode: "Anerroroccurred", value: result.status + ` for action ${action}, route ${route}, and payload ${payload}`, origin: ORIGIN}
            }
    }catch (error){
        return { succeeded: false, failed: true, value: error.message, errcode: "Anerroroccurred", origin: ORIGIN, error: error }
    }
    return await result.json()
}

export const Isonline = async (timeout = 3000) => {
	try {
		const controller = new AbortController();
		const signal = controller.signal;

		const timeoutId = setTimeout(() => controller.abort(), timeout);

		const response = await fetch('https://www.google.com/favicon.ico', {
			method: 'HEAD',
			mode: 'no-cors',
			signal
		});

		clearTimeout(timeoutId);

		// Note: mode: 'no-cors' will not throw on network errors
		return true;
	} catch (err) {
		return false;
	}
}
