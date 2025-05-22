import UrlForm from '../components/UrlForm'
import Response from '../components/Response'


function Home() {
    return (
        <main>
            <header>
                <img className="logo" src="/logo.svg" alt="Logo" draggable="false" />
                <h1>Short Stack</h1>
                <h3>A URL shortener</h3>
            </header>
            <UrlForm />
            <Response response=""/>
        </main>
    )
}

export default Home
