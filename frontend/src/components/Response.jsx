import { useState } from 'react'

function Response({ response }) {
    if (Object.keys(response).length) {
        if (response.success) {
            return (
                <div className="card">
                    <p>Your shortened URL is:</p>
                    <p><a href={response[1]} target="_blank" style={{ "color": "#cea176" }}>{response.data.short_url}</a></p>
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
