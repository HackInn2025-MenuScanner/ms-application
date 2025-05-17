export async function POST({ request }) {
    const body = await request.json();
    const apiPath = body.apiPath;
    const apiData = body.apiData;
    const apiMethod = body.apiMethod;
    console.log(apiPath, apiData);

    const response = await fetch('http://backend:8000' + apiPath + (apiMethod === "GET" ? ("?" + new URLSearchParams(apiData).toString()) : ""), {
        method: apiMethod,
        headers: apiMethod === "GET" ? undefined : { 'Content-Type': 'application/json' },
        body: apiMethod === "GET" ? undefined : JSON.stringify(apiData),
    });

    const data = await response.json();

    return new Response(JSON.stringify(data), {
        status: response.status,
        headers: { 'Content-Type': 'application/json' }
    });
}