import { useState } from 'react'

function Response({response}) {
    if (response) {
        return (
            <div className="card">
                {response}
            </div>
        )
    }
    return (<></>)
}

export default Response
