import { useState } from 'react'

function UrlForm() {
    const [url, setUrl] = useState('')
    const [alias, setAlias] = useState('')
    const handleSubmit = (e) => {
        e.preventDefault()
        // TODO: call Flask API
        console.log('Shortening:', url)
    }

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
                    onChange={(e) => setAlias(e.target.value)}
                    placeholder="Enter custom URL name"
                    required
                />
            </label>
            <input type="submit" value="Submit" />
        </form>
    )
}

export default UrlForm
