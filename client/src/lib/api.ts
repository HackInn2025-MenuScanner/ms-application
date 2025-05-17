export async function apiCall(method: "GET" | "POST", path: string, data: Record<string, any>) {
    return await fetch('/api/fastapi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
            apiMethod: method,
            apiPath: path,
            apiData: data
        })
    });
}