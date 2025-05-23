import { useState } from 'react'

function UrlForm({ setResponse }) {
    const [url, setUrl] = useState('https://example.com/')
    const [alias, setAlias] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate alias if provided
        if (alias && (alias.length < 5 || alias.length > 16)) {
            setResponse([false, 'Alias must be between 5-16 characters long.']);
            return;
        }

        try {
            const res = await fetch('http://localhost:5000/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url, alias: alias })
            });

            const data = await res.json();

            if (res.ok) {
                setResponse([true, data.short_url]);
            } else {
                setResponse([false, data.error]);
            }
        } catch (err) {
            setResponse([false, 'Network error or server not responding.']);
            console.error('Request failed:', err);
        }
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