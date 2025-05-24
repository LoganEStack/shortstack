import { useState } from 'react'


function UrlForm({ setResponse }) {
    const [url, setUrl] = useState('https://example.com/')
    const [alias, setAlias] = useState('')

    async function fetchJSON(url, options = {}) {
        // Validate alias if provided
        if (alias && (alias.length < 5 || alias.length > 16)) {
            setResponse([false, 'Alias must be between 5-16 characters long.']);
            return;
        }

        try {
            const res = await fetch(url, options);
            const data = await res.json();

            if (!res.ok) {
                return {
                    success: false,
                    status: res.status,
                    error: data?.error || res.statusText || 'Unknown error',
                };
            }
            return {
                success: true,
                status: res.status,
                data,
            };
        } catch (err) {
            return {
                success: false,
                status: null,
                error: 'Network error or server not responding',
            };
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const expiration_date = new Date();
        expiration_date.setDate(expiration_date.getDate() + 7);
        const expiration_date_ISO8601 = expiration_date.toISOString();

        const result = await fetchJSON('http://localhost:5000/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, expiration_date: expiration_date_ISO8601, alias: alias }),
        });
        setResponse(result)
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Enter your URL
                <input
                    id="url"
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com/"
                    required
                />
            </label>
            <label>
                Optionally, enter a custom URL name
                <input
                    id="alias"
                    type="text"
                    value={alias}
                    placeholder="Enter custom URL name"
                    title="Alias must contain 5-16 alphanumeric characters, dashes, or underscores"
                    minLength="5"
                    maxLength="16"
                    onChange={(e) => {
                        const value = e.target.value;
                        const regex = /^[a-zA-Z0-9_-]{0,16}$/; // allow up to 16 chars
                        if (regex.test(value)) {
                            setAlias(value);
                        }
                    }}
                />
            </label>
            <input type="submit" value="Submit" />
        </form>
    )
}

export default UrlForm