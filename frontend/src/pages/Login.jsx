import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const navigate = useNavigate()

    async function handleSubmit(event){
        event.preventDefault()

        const formData = new URLSearchParams()

        formData.append("username", email)
        formData.append("password", password)

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/auth/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: formData
                }
            )

            if (!response.ok){
                throw new Error("Login Failed")
            }

            const data = await response.json()

            localStorage.setItem("access_token", data.access_token)
            console.log("About to navigate")
            navigate("/chat")

        } catch(error) {
            console.error(error)
        }
        
    }

    return (
        <div>
            <h1>Login</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="email">Email</label>

                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="password">Password</label>

                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />
                </div>

                <button type="submit">
                    Login
                </button>
            </form>

        </div>
    )
}

export default Login