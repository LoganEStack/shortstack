import { useState } from 'react'

function Response({ response }) {
    console.log(response)
    if (response.length > 0) {
        if (response[0]) {
            return (
                <div className="card">
                    <p>Your shortened URL is:</p>
                    <p><a href={response[1]} target="_blank" style={{ "color": "#cea176" }}>{response[1]}</a></p>
                </div>
            )
        } else {
            return (
                <div className="card">
                    <p>Error:</p>
                    <p style={{ "color": "red" }}>{response[1]}</p>
                </div>
            )
        }
    }
}

export default Response
