import { useState } from 'react'

function Response({ response }) {
    if (Object.keys(response).length) {
        console.log(response)
        if (response.success) {
            return (
                <div className="card">
                    <p>Your shortened URL is:</p>
                    <p>
                        <a href={response.data.short_url} target="_blank" style={{ "color": "#cea176" }}>
                            {response.data.short_url}
                        </a>
                    </p>
                    <i>It will expire on {response.data.expiration_date}</i>
                </div>
            )
        } else {
            return (
                <div className="card">
                    <p>Error:</p>
                    <p style={{ "color": "red" }}>{response.error}</p>
                </div>
            )
        }
    }
}

export default Response
