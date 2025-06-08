import Spinner from './Spinner'

function Response({ response }) {
    if (!response || Object.keys(response).length === 0) return null;

    if (response.status === "pending") {
        return (
            <div className="card">
                <Spinner/>
                <i>
                    Short Stack uses a free version of Render for hosting and can take
                    up to 60 seconds to spin up on first use after periods of inactivity.
                </i>
            </div>
        )
    }

    if (response.success) {
        const date = new Date(response.data.expiration_date);
        const formatted = date.toLocaleString(undefined, {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });

        return (
            <div className="card">
                <p>Your shortened URL is:</p>
                <p>
                    <a href={response.data.short_url} target="_blank" style={{ color: "#cea176" }}>
                        {response.data.short_url}
                    </a>
                </p>
                <i>It will expire on {formatted}</i>
            </div>
        );
    } else {
        return (
            <div className="card">
                <p>Error:</p>
                <p style={{ color: "red" }}>{response.error}</p>
            </div>
        );
    }
}

export default Response
