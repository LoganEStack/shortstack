import { useState } from 'react'
import UrlForm from '../components/UrlForm'
import Response from '../components/Response'


function Home() {
    const [response, setResponse] = useState([])

    return (
        <main>
            <header>
                <img className="logo" src="/logo.svg" alt="Logo" draggable="false" />
                <h1>Short Stack</h1>
                <h3>A URL shortener</h3>
            </header>
            <UrlForm setResponse={setResponse} />
            <Response response={response}/>
            <div className="footer">© 2025 Logan Stack</div>
        </main>
    )
}

export default Home